# Slide LSTM (Slidev)

```bash
npm install          # lần đầu
npm run dev          # trình chiếu: http://localhost:3030 (presenter mode: /presenter, có lời thoại)
npm run notes        # xuất lời thoại trong slides.md ra ../thuyet-trinh.md
npm run export       # xuất PDF (cần: npx playwright install chromium)
```

- `slides.md`: nội dung 29 slide; lời thoại nằm trong comment `<!-- -->` cuối mỗi slide
- `components/`: LstmCell (sơ đồ ô LSTM), LstmSimulator (slide 15), GradientDecay (slide 5, 20), CompareChart (slide 23), GateHeatmap (slide 16)
- `data/compare.json`: kết quả thật từ `../experiment/compare_rnn_lstm.py` (chạy lại: `python ../experiment/compare_rnn_lstm.py`, ~5 phút CPU)

**Điều khiển bằng chuột** (`global-bottom.vue`): chuột trái = bước/slide tiếp theo, chuột phải = quay lại. Bấm vào thanh trượt, nút, checkbox trong các demo (slide 5, 15, 20, 23) sẽ không chuyển slide. Bàn phím (→ ←, Space) vẫn dùng bình thường.
