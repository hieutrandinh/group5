"""So sánh RNN và LSTM trên cùng một bộ dữ liệu: bài toán Adding Problem.

Mỗi mẫu là chuỗi dài T, mỗi bước có 2 giá trị: (số ngẫu nhiên trong [0,1], cờ đánh dấu 0/1).
Đúng 2 vị trí được đánh dấu; mục tiêu là tổng 2 số tại 2 vị trí đó.
Một vị trí nằm ở nửa đầu chuỗi, nên mô hình phải nhớ thông tin qua ~T/2 bước.
Đoán bừa (luôn trả 1.0) cho MSE ≈ 1/6 ≈ 0.167.

Chạy:  python experiment/compare_rnn_lstm.py
Kết quả ghi ra slides/data/compare.json để slide 23 vẽ biểu đồ.
"""
import json
import time
from pathlib import Path

import torch
import torch.nn as nn

HIDDEN = 64
BATCH = 64
STEPS = 5000
LR = 1e-3
LOG_EVERY = 25
SEQ_LENS = [10, 100]
OUT = Path(__file__).resolve().parent.parent / "slides" / "data" / "compare.json"


def make_batch(batch, T, gen):
    values = torch.rand(batch, T, generator=gen)
    marks = torch.zeros(batch, T)
    first = torch.randint(0, T // 2, (batch,), generator=gen)
    second = torch.randint(T // 2, T, (batch,), generator=gen)
    idx = torch.arange(batch)
    marks[idx, first] = 1.0
    marks[idx, second] = 1.0
    x = torch.stack([values, marks], dim=-1)          # (batch, T, 2)
    y = (values * marks).sum(dim=1, keepdim=True)      # (batch, 1)
    return x, y


class SeqModel(nn.Module):
    def __init__(self, cell):
        super().__init__()
        rnn_cls = nn.LSTM if cell == "lstm" else nn.RNN
        self.rnn = rnn_cls(input_size=2, hidden_size=HIDDEN, batch_first=True)
        self.fc = nn.Linear(HIDDEN, 1)

    def forward(self, x):
        output, _ = self.rnn(x)
        return self.fc(output[:, -1])                  # many-to-one: lấy bước cuối


def train(cell, T, seed=0):
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed)
    model = SeqModel(cell)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.MSELoss()
    curve, window = [], []
    start = time.time()
    for step in range(1, STEPS + 1):
        x, y = make_batch(BATCH, T, gen)
        loss = loss_fn(model(x), y)
        opt.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        window.append(loss.item())
        if step % LOG_EVERY == 0:
            curve.append([step, sum(window) / len(window)])
            window = []
    elapsed = time.time() - start

    model.eval()
    test_gen = torch.Generator().manual_seed(12345)
    with torch.no_grad():
        x, y = make_batch(2000, T, test_gen)
        test_mse = loss_fn(model(x), y).item()
    params = sum(p.numel() for p in model.parameters())
    print(f"{cell:4s} T={T:3d}  test MSE={test_mse:.4f}  params={params}  time={elapsed:.0f}s")
    return {"curve": curve, "test_mse": test_mse, "params": params, "seconds": round(elapsed, 1)}


def main():
    results = {
        "config": {"hidden": HIDDEN, "batch": BATCH, "steps": STEPS, "lr": LR,
                   "optimizer": "Adam", "clip": 1.0, "baseline_mse": 1 / 6},
        "runs": {},
    }
    for T in SEQ_LENS:
        results["runs"][str(T)] = {cell: train(cell, T) for cell in ("rnn", "lstm")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
