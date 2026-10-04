---
theme: default
title: LSTM — Long Short-Term Memory
info: Thuyết trình LSTM, 45 phút, 4 người
colorSchema: light
highlighter: shiki
lineNumbers: false
mdc: true
transition: slide-left
fonts:
  sans: Be Vietnam Pro
  mono: JetBrains Mono
layout: cover
class: text-center
clicks: 2
---

# LSTM
## Long Short-Term Memory

<div class="mt-10 text-xl hook">
<span>"Tôi lớn lên ở </span><span class="key" :class="{ fade: $clicks >= 2 }">Pháp</span><span>, </span>
<span v-click="1" class="mid">… học tiểu học, chuyển nhà ba lần, chơi bóng đá, mê truyện tranh, làm quen bạn mới …</span>
<span>, nên tôi nói thành thạo tiếng </span><span class="blank">___</span>"
</div>

<div class="abs-b mb-8 w-full text-sm opacity-70">Nhóm [số] · [Tên môn học] · [Tên 4 thành viên]</div>

<style>
.hook .key { color: #2563eb; font-weight: 800; transition: opacity 2.5s; }
.hook .key.fade { opacity: .12; }
.hook .mid { opacity: .6; font-style: italic; }
.hook .blank { color: #dc2626; font-weight: 800; }
</style>

<!--
**[Người 1 · ~1 phút]**

Xin chào thầy và các bạn. Hôm nay nhóm mình trình bày về LSTM, viết tắt của Long Short-Term Memory.

Trước khi vào bài, mời các bạn đọc câu này: "Tôi lớn lên ở Pháp, nên tôi nói thành thạo tiếng ___". Ai cũng điền được ngay: tiếng Pháp.

[click] Nhưng nếu câu dài ra thế này, ở giữa chen vào ba chục từ không liên quan, thì để điền được chỗ trống, mô hình phải **nhớ chữ "Pháp" qua khoảng 30 bước**.

[click] Với RNN thông thường, đến cuối câu thì chữ "Pháp" gần như đã mờ hết. Bài hôm nay trả lời ba câu hỏi: vì sao RNN quên, LSTM sửa chuyện đó bằng cách nào, và vì sao về mặt toán học cách sửa đó hiệu quả.
-->

---
layout: center
---

# LSTM đứng ở đâu trong gia phả mạng nơ-ron?

<svg viewBox="0 0 760 330" class="w-full" style="max-height: 360px">
  <defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#64748b"/></marker></defs>
  <g v-click="1">
    <rect x="300" y="10" width="160" height="56" rx="10" fill="#e2e8f0" stroke="#475569" stroke-width="2"/>
    <text x="380" y="36" text-anchor="middle" style="font-size:20px;font-weight:700">MLP</text>
    <text x="380" y="56" text-anchor="middle" style="font-size:12px">đầu vào cố định</text>
  </g>
  <g v-click="2">
    <line x1="340" y1="66" x2="180" y2="128" stroke="#64748b" stroke-width="2" marker-end="url(#a2)"/>
    <rect x="50" y="130" width="260" height="60" rx="10" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="180" y="156" text-anchor="middle" style="font-size:20px;font-weight:700">CNN</text>
    <text x="180" y="177" text-anchor="middle" style="font-size:12px">chia sẻ trọng số theo KHÔNG GIAN</text>
  </g>
  <g v-click="3">
    <line x1="420" y1="66" x2="580" y2="128" stroke="#64748b" stroke-width="2" marker-end="url(#a2)"/>
    <rect x="450" y="130" width="260" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="580" y="156" text-anchor="middle" style="font-size:20px;font-weight:700">RNN</text>
    <text x="580" y="177" text-anchor="middle" style="font-size:12px">chia sẻ trọng số theo THỜI GIAN</text>
  </g>
  <g v-click="4">
    <line x1="580" y1="190" x2="580" y2="238" stroke="#64748b" stroke-width="2" marker-end="url(#a2)"/>
    <rect x="470" y="240" width="220" height="70" rx="12" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/>
    <text x="580" y="268" text-anchor="middle" fill="#1d4ed8" style="font-size:22px;font-weight:800">LSTM</text>
    <text x="580" y="290" text-anchor="middle" style="font-size:12px">vẫn là RNN, chỉ thay "ô" bên trong</text>
    <text x="580" y="304" text-anchor="middle" style="font-size:12px">bằng ô có cổng + bộ nhớ dài hạn</text>
    <text x="300" y="275" text-anchor="middle" fill="#475569" style="font-size:13px">LSTM ⊂ RNN: cùng cách unroll theo thời gian,</text>
    <text x="300" y="293" text-anchor="middle" fill="#475569" style="font-size:13px">cùng huấn luyện bằng BPTT</text>
  </g>
</svg>

<!--
**[Người 1 · ~1.5 phút]**

Trước khi vào LSTM, mình đặt nó vào bức tranh chung các mô hình mà lớp mình đã học.

[click] Gốc là **MLP**: đầu vào là một vector có kích thước cố định, mỗi trọng số dùng đúng một lần. MLP không biết gì về cấu trúc của dữ liệu.

[click] Nhánh thứ nhất là **CNN**, các bạn đã làm ở assignment trước. CNN thêm vào ý tưởng **chia sẻ trọng số theo không gian**: cùng một kernel trượt qua mọi vị trí của ảnh.

[click] Nhánh thứ hai là **RNN**. RNN cũng chia sẻ trọng số, nhưng **theo thời gian**: cùng một ô được dùng lại ở mọi bước của chuỗi.

[click] Và đây là nhân vật chính. Điểm quan trọng nhất của slide này: **LSTM không phải một họ mô hình mới, nó vẫn là RNN**. Vẫn unroll theo thời gian, vẫn huấn luyện bằng backpropagation through time. Thứ duy nhất thay đổi là cái ô bên trong: thay vì một phép tanh đơn giản, LSTM dùng một ô có các cổng và một bộ nhớ dài hạn riêng.
-->

---

# So sánh nhanh MLP · CNN · RNN · LSTM

| | MLP | CNN | RNN | <span class="text-blue-600">LSTM</span> |
|---|---|---|---|---|
| **Dữ liệu phù hợp** | vector cố định | ảnh, dữ liệu dạng lưới | chuỗi | chuỗi |
| **Chia sẻ trọng số** | không | theo không gian (kernel) | theo thời gian | theo thời gian |
| **Bộ nhớ** | không | không | $h_t$ | $h_t$ **và** $c_t$ |
| **Phụ thuộc xa nhất** | — | bằng trường tiếp nhận | khoảng 10 bước | hơn 1000 bước (bài báo 1997) |
| **Số tham số (một lớp, d = 100, h = 128)** | — | — | ≈ 29K | ≈ 117K (gấp 4) |
| **Ứng dụng điển hình** | dữ liệu bảng | phân loại ảnh | chuỗi ngắn | dịch máy, giọng nói, chuỗi thời gian |

<div v-click class="mt-6 text-center text-lg">
LSTM giữ nguyên ưu điểm của RNN, và sửa đúng một điểm yếu: <b class="text-red-600">trí nhớ ngắn</b>.
</div>

<!--
**[Người 1 · ~1 phút]**

Bảng này tóm tắt lại sự khác nhau giữa bốn mô hình. Mình chỉ lưu ý ba dòng.

Dòng **bộ nhớ**: MLP và CNN không có bộ nhớ, mỗi đầu vào được xử lý độc lập. RNN có một hidden state $h_t$. LSTM có **hai** trạng thái: $h_t$ và cell state $c_t$. Cái $c_t$ này là chìa khóa của cả bài.

Dòng **phụ thuộc xa**: trên thực tế RNN thường chỉ nhớ được khoảng 10 bước. Bài báo gốc năm 1997 cho thấy LSTM học được những phụ thuộc cách nhau hơn 1000 bước.

Dòng **số tham số**: LSTM có khoảng gấp 4 lần RNN. Lát nữa người thứ ba sẽ giải thích tại sao lại đúng là 4.

[click] Tóm lại: LSTM giữ nguyên mọi ưu điểm của RNN, và chỉ sửa một điểm yếu là trí nhớ ngắn.
-->

---

# Ôn lại RNN

<div class="text-center text-2xl my-4">

$h_t = \tanh(W_h\, h_{t-1} + W_x\, x_t + b)$

</div>

<svg viewBox="0 0 760 200" class="w-full" style="max-height: 230px">
  <defs><marker id="a4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker></defs>
  <g v-click="1">
    <rect x="60" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="115" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="115" y1="170" x2="115" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="115" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">1</tspan></text>
    <line x1="115" y1="60" x2="115" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="135" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">1</tspan></text>
    <line x1="170" y1="90" x2="238" y2="90" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="188" y="82" fill="#ea580c" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">h</tspan></text>
  </g>
  <g v-click="2">
    <rect x="240" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="295" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="295" y1="170" x2="295" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="295" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">2</tspan></text>
    <line x1="295" y1="60" x2="295" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="315" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">2</tspan></text>
    <line x1="350" y1="90" x2="418" y2="90" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="368" y="82" fill="#ea580c" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">h</tspan></text>
  </g>
  <g v-click="3">
    <rect x="420" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="475" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="475" y1="170" x2="475" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="475" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">3</tspan></text>
    <line x1="475" y1="60" x2="475" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="495" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">3</tspan></text>
    <line x1="530" y1="90" x2="598" y2="90" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="548" y="82" fill="#ea580c" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">h</tspan> …</text>
  </g>
  <g v-click="4">
    <rect x="600" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="655" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="655" y1="170" x2="655" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="655" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">T</tspan></text>
    <line x1="655" y1="60" x2="655" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="675" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">T</tspan></text>
  </g>
</svg>

<div v-click="5" class="text-center">

Cùng một $W_h$ được dùng lại ở <b>mọi</b> bước → huấn luyện bằng <b>BPTT</b> (backprop through time)

</div>

<!--
**[Người 1 · ~1.5 phút]**

Ôn lại nhanh RNN mà các bạn đã làm. Ở mỗi bước, hidden state mới $h_t$ được tính từ hidden state cũ $h_{t-1}$ và đầu vào $x_t$, rồi cho qua tanh.

[click] [click] [click] [click] Khi unroll theo thời gian, ta được một chuỗi các ô nối tiếp nhau. Lưu ý mũi tên màu cam: **cùng một ma trận $W_h$** được dùng lại ở mọi bước.

[click] Để huấn luyện, ta dùng backpropagation through time, tức là lan truyền ngược qua toàn bộ chuỗi đã unroll. Vì $W_h$ xuất hiện ở mọi bước, gradient từ bước cuối muốn về được bước đầu thì phải đi qua $W_h$ rất nhiều lần. Đây chính là nguồn gốc của vấn đề ở slide tiếp theo.
-->

---

# Vấn đề: gradient biến mất / bùng nổ

<div class="text-center text-xl">

$$\frac{\partial h_T}{\partial h_k} \;=\; \prod_{t=k+1}^{T} \operatorname{diag}\big(\tanh'(\cdot)\big)\, W_h \qquad\text{với}\quad \tanh' \le 1$$

</div>

<div class="grid grid-cols-2 gap-4 text-center text-sm mb-2">
<div class="text-orange-600">‖W<sub>h</sub>‖ · tanh′ &lt; 1 ⇒ tích → 0: <b>gradient biến mất</b></div>
<div class="text-red-600">‖W<sub>h</sub>‖ · tanh′ &gt; 1 ⇒ tích → ∞: <b>gradient bùng nổ</b></div>
</div>

<GradientDecay />

<!--
**[Người 1 · ~2 phút]**

Đây là phần toán quan trọng nhất của phần mở đầu. Muốn biết lỗi ở bước cuối $T$ ảnh hưởng thế nào tới bước $k$, ta lấy đạo hàm $\partial h_T / \partial h_k$. Theo quy tắc chuỗi, đạo hàm này là một **tích** gồm $T-k$ thừa số. Mỗi thừa số là đạo hàm của tanh nhân với $W_h$.

Đạo hàm của tanh luôn nhỏ hơn hoặc bằng 1. Vì vậy, gọi $\gamma$ là độ lớn của mỗi thừa số:
- nếu $\gamma < 1$, tích tiến về 0 theo hàm mũ: gradient biến mất;
- nếu $\gamma > 1$, tích tiến ra vô cùng: gradient bùng nổ.

**(Demo)** Mình kéo thử thanh trượt. Với $\gamma = 0.9$, một con số nghe rất "vô hại", và $T = 50$ bước, ta được $0.9^{50} \approx 0.005$. Nghĩa là tín hiệu học từ bước 50 về bước đầu chỉ còn **0.5%**. Kéo $T$ lên 100 thì còn khoảng $3 \cdot 10^{-5}$, tức là gần như bằng không. Kéo $\gamma$ lên 1.1 thì đồ thị vọt lên trên: gradient bùng nổ.

Muốn đúng bằng 1 thì phải "đặt trên lưỡi dao", điều gần như không thể giữ được trong lúc huấn luyện. Đó là lý do RNN không học được chữ "Pháp" ở slide đầu.
-->

---

# Lịch sử: người phát hiện ra vấn đề

<div class="grid grid-cols-2 gap-6 mt-2">
<div v-click="1" class="card">

### 1991 · Sepp Hochreiter
Sinh viên **TU München**, luận văn tốt nghiệp (diploma thesis), thầy hướng dẫn **Jürgen Schmidhuber**

→ Người **đầu tiên phân tích bằng toán** hiện tượng gradient biến mất ở RNN, đúng như công thức ở slide trước

<span class="text-sm opacity-70">(Bengio, Simard, Frasconi công bố độc lập năm 1994)</span>

</div>
<div v-click="2" class="card">

### Ý tưởng
Gradient chết vì bị **nhân lặp lại với hệ số khác 1**

→ Tạo một đơn vị **tự nối với chính nó bằng trọng số = 1**, hàm kích hoạt **tuyến tính**

$$c_t = 1 \cdot c_{t-1} + (\text{thông tin mới}) \;\Rightarrow\; \frac{\partial c_t}{\partial c_{t-1}} = 1$$

→ **Constant Error Carousel (CEC)**: "băng chuyền lỗi không đổi"

</div>
</div>

<div v-click="3" class="card mt-4">

**Vấn đề mới:** mọi input đều ghi vào bộ nhớ đó → thêm **cổng (gate)** để kiểm soát khi nào được *ghi*, khi nào được *đọc*.
**1997:** Hochreiter & Schmidhuber, *"Long Short-Term Memory"*, tạp chí **Neural Computation** (đã có technical report năm 1995).

</div>

<style>
.card { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: .6rem 1rem; font-size: .85rem; }
.card h3 { margin-top: 0 !important; color: #1d4ed8; }
</style>

<!--
**[Người 1 · ~2.5 phút]**

Vậy ai là người đã nhìn ra vấn đề này và sửa nó?

[click] Năm 1991, Sepp Hochreiter, lúc đó còn là **sinh viên** ở Đại học Kỹ thuật München, làm luận văn tốt nghiệp với thầy hướng dẫn là Jürgen Schmidhuber. Trong luận văn đó, ông là người đầu tiên **phân tích bằng toán** vì sao RNN không học được phụ thuộc xa, tức là đúng cái tích các đạo hàm mà chúng ta vừa xem. Ba năm sau, Bengio và cộng sự cũng công bố độc lập cùng kết quả. Nghĩa là hai người đọc một luận văn sinh viên trước, rồi mới đến một bài báo của Bengio.

[click] Ý tưởng sửa của ông rất đơn giản, gần như hiển nhiên khi nhìn vào công thức. Gradient chết vì bị nhân lặp lại với một số khác 1. Vậy thì tạo ra một đơn vị **tự nối với chính nó bằng trọng số đúng bằng 1**, không có hàm kích hoạt phi tuyến. Khi đó đạo hàm của $c_t$ theo $c_{t-1}$ đúng bằng 1, nên lỗi chảy qua bao nhiêu bước cũng không đổi. Ông đặt tên là **Constant Error Carousel**, tạm dịch là "băng chuyền lỗi không đổi".

[click] Nhưng như vậy lại sinh ra vấn đề mới: mọi đầu vào đều được cộng thẳng vào bộ nhớ, thông tin rác cũng ghi vào, và bộ nhớ bị ghi đè lung tung. Giải pháp là thêm các **cổng** để kiểm soát khi nào được ghi vào, khi nào được đọc ra. Kết quả là bài báo "Long Short-Term Memory" năm 1997 trên tạp chí Neural Computation. Đến nay đây là một trong những bài báo được trích dẫn nhiều nhất của học sâu.
-->

---

# Hành trình của LSTM

<div class="timeline">
  <div v-click class="ev"><b>1997</b><span>Bản gốc: chỉ có <b>input gate</b> và <b>output gate</b>, <span class="text-red-600">chưa có forget gate</span></span></div>
  <div v-click class="ev"><b>1999–2000</b><span>Gers, Schmidhuber, Cummins thêm <b class="text-red-600">forget gate</b> (<i>"Learning to Forget"</i>); thêm peephole</span></div>
  <div v-click class="ev"><b>2005</b><span>Graves & Schmidhuber: huấn luyện bằng BPTT đầy đủ, <b>Bidirectional LSTM</b></span></div>
  <div v-click class="ev"><b>2009</b><span>LSTM thắng các cuộc thi nhận dạng chữ viết tay</span></div>
  <div v-click class="ev"><b>2014</b><span><b>seq2seq</b> (Sutskever et al.) cho dịch máy · <b>GRU</b> (Cho et al.)</span></div>
  <div v-click class="ev"><b>2015–2016</b><span>Google Voice, Google Translate chuyển sang LSTM</span></div>
  <div v-click class="ev"><b>2017</b><span><b>Transformer</b> ra đời và dần thay thế LSTM trong NLP</span></div>
</div>

<div v-click class="mt-4 text-center text-sm">
Tên gọi: bộ nhớ <b>ngắn hạn</b> (activation) nhưng giữ được <b>lâu</b> → <i>Long Short-Term Memory</i>
</div>

<style>
.timeline { border-left: 3px solid #2563eb; margin-left: 1rem; padding-left: 1rem; }
.ev { display: grid; grid-template-columns: 7rem 1fr; gap: .5rem; padding: .25rem 0; font-size: .9rem; position: relative; }
.ev::before { content: ''; position: absolute; left: -1.45rem; top: .6rem; width: .7rem; height: .7rem; border-radius: 50%; background: #2563eb; }
.ev b:first-child { color: #1d4ed8; }
</style>

<!--
**[Người 1 · ~1 phút]**

Điểm qua nhanh hành trình của LSTM.

[click] Bản gốc năm 1997 chỉ có hai cổng: input gate và output gate. **Chưa có forget gate**, nghĩa là bộ nhớ chỉ được cộng thêm, không bao giờ bị xóa.

[click] Khoảng năm 1999–2000, Felix Gers cùng Schmidhuber thêm **forget gate**, cho phép mạng chủ động xóa trí nhớ. Cái LSTM mà chúng ta dùng ngày nay, kể cả trong PyTorch, là bản có forget gate này.

[click] Năm 2005, Alex Graves huấn luyện LSTM bằng BPTT đầy đủ và giới thiệu Bidirectional LSTM. [click] Năm 2009, LSTM thắng các cuộc thi nhận dạng chữ viết tay. [click] Năm 2014 có seq2seq cho dịch máy, cùng năm đó GRU ra đời. [click] Khoảng 2015–2016, nhận dạng giọng nói của Google và Google Translate chuyển sang LSTM. [click] Đến 2017, Transformer xuất hiện và dần thay thế LSTM trong xử lý ngôn ngữ.

[click] Còn cái tên "Long Short-Term Memory": short-term memory là bộ nhớ ngắn hạn, tức là activation của mạng, và chữ "long" nghĩa là bộ nhớ ngắn hạn đó được giữ lâu.
-->

---
layout: center
class: text-center
---

# Vậy bên trong một ô LSTM có gì?

<div class="text-xl opacity-80 mt-4">Băng chuyền của Hochreiter + 3 cổng (kể cả forget gate được thêm vào sau)</div>

<!--
**[Người 1 · ~0.5 phút]**

Tóm lại, chúng ta đã thấy RNN quên vì gradient bị nhân lặp lại, và Hochreiter sửa bằng một băng chuyền có trọng số bằng 1 cộng với các cổng. Bây giờ mời bạn [tên người 2] mở ô LSTM ra, xem từng cổng hoạt động thế nào.
-->

---

# Ý tưởng: hai đường bộ nhớ

<div class="grid grid-cols-2 gap-6 items-center">
<div class="text-center">

**RNN: một đường**

<svg viewBox="0 0 260 180" style="width: 85%; margin: auto">
  <defs><marker id="a9" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker></defs>
  <rect x="70" y="40" width="120" height="90" rx="14" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
  <text x="130" y="92" text-anchor="middle" style="font-size:20px">tanh</text>
  <line x1="5" y1="85" x2="68" y2="85" stroke="#475569" stroke-width="2.5" marker-end="url(#a9)"/>
  <line x1="190" y1="85" x2="255" y2="85" stroke="#475569" stroke-width="2.5" marker-end="url(#a9)"/>
  <line x1="130" y1="178" x2="130" y2="132" stroke="#475569" stroke-width="2.5" marker-end="url(#a9)"/>
  <text x="8" y="75" style="font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">t-1</tspan></text><text x="215" y="75" style="font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">t</tspan></text><text x="140" y="172" style="font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">t</tspan></text>
</svg>

</div>
<div class="text-center">

**LSTM: thêm đường <span class="text-blue-600">cell state</span>**

<LstmCell active="state" />

</div>
</div>

<div class="grid grid-cols-2 gap-4 mt-2 text-sm">
<div v-click class="p-2 rounded bg-blue-50">

<b class="text-blue-600">$c_t$, cell state</b>: băng chuyền chạy thẳng, chỉ có phép × và + → <b>bộ nhớ dài hạn</b> (chính là CEC)

</div>
<div v-click class="p-2 rounded bg-slate-100">

<b>$h_t$, hidden state</b>: đầu ra ở mỗi bước → <b>bộ nhớ ngắn hạn</b>, phần "được đọc ra"

</div>
</div>

<!--
**[Người 2 · ~1 phút]**

Cảm ơn [tên người 1]. Chúng ta bắt đầu bằng hình ảnh tổng thể.

Bên trái là RNN: chỉ có **một đường** thông tin $h$ đi qua tanh ở mỗi bước. Mọi thứ cần nhớ đều phải nhét vào $h$ và bị bóp qua tanh liên tục.

Bên phải là LSTM. Để ý đường màu xanh chạy thẳng phía trên: đó là **cell state $c_t$**.

[click] Cell state giống như một **băng chuyền**: nó chạy thẳng qua ô, trên đường chỉ có một phép nhân và một phép cộng, không có ma trận trọng số hay hàm tanh nào chặn lại. Đây chính là Constant Error Carousel của Hochreiter, đóng vai trò bộ nhớ dài hạn.

[click] Còn $h_t$ vẫn là đầu ra ở mỗi bước, giống như RNN, đóng vai trò bộ nhớ ngắn hạn, phần được "đọc ra" từ bộ nhớ dài hạn.

Ba cổng mà mình sắp trình bày chính là ba cái van điều khiển băng chuyền này.
-->

---

# Cổng 1 · Forget gate: giữ lại bao nhiêu trí nhớ cũ?

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="f" />
<div>

$$f_t = \sigma\big(W_f\,[h_{t-1}, x_t] + b_f\big)$$

<v-clicks>

- $f_t \in (0, 1)$, từng phần tử một
- $f_t = 0$ → **quên sạch** $c_{t-1}$
- $f_t = 1$ → **giữ nguyên** $c_{t-1}$
- Vì sao dùng **sigmoid**? Đầu ra nằm trong (0,1), đóng vai trò cái **van**
- <span class="text-red-600">Không có trong bản 1997!</span> Bản gốc coi như $f \equiv 1$

</v-clicks>
</div>
</div>

<!--
**[Người 2 · ~1.5 phút]**

Cổng đầu tiên là **forget gate**, màu đỏ.

Nó nhận vào hai thứ: hidden state cũ $h_{t-1}$ và đầu vào hiện tại $x_t$, ghép lại thành một vector. Sau đó nhân với ma trận $W_f$, cộng bias, rồi cho qua sigmoid.

[click] Kết quả $f_t$ là một vector có giá trị trong khoảng 0 đến 1, cùng kích thước với cell state.

[click] Nếu một phần tử của $f_t$ bằng 0, phần tử tương ứng trong $c_{t-1}$ bị nhân với 0, tức là **quên sạch**. [click] Nếu bằng 1 thì **giữ nguyên**.

[click] Vì sao lại dùng sigmoid mà không dùng ReLU hay tanh? Vì sigmoid cho đầu ra trong khoảng (0, 1), đúng ý nghĩa của một cái van: 0 là đóng, 1 là mở hoàn toàn.

[click] Một chi tiết thú vị: như bạn [tên người 1] đã nói, cổng này **không có** trong bản gốc năm 1997. Bản gốc coi như $f$ luôn bằng 1, nên trí nhớ chỉ tăng chứ không bao giờ bị xóa. Ví dụ với câu "Tôi lớn lên ở Pháp", khi chuyển sang một câu chuyện khác, mạng cần biết quên chữ "Pháp" đi. Forget gate cho phép làm việc đó.
-->

---

# Cổng 2 · Input gate + candidate: ghi gì, ghi bao nhiêu?

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="i,c" />
<div>

$$i_t = \sigma\big(W_i\,[h_{t-1}, x_t] + b_i\big)$$

$$\tilde c_t = \tanh\big(W_c\,[h_{t-1}, x_t] + b_c\big)$$

<v-clicks>

- $\tilde c_t \in (-1, 1)$: **nội dung** muốn ghi
- $i_t \in (0, 1)$: **mức độ** cho phép ghi
- Phần được ghi thật sự: $i_t \odot \tilde c_t$

</v-clicks>
</div>
</div>

<!--
**[Người 2 · ~1.5 phút]**

Cổng thứ hai, màu xanh lá, gồm hai phần đi cùng nhau.

Phần thứ nhất là **candidate** $\tilde c_t$, tính bằng tanh. [click] Đây là **nội dung** mới mà mạng muốn ghi vào bộ nhớ. Dùng tanh nên giá trị nằm trong khoảng −1 đến 1, có thể tăng hoặc giảm giá trị trong bộ nhớ.

[click] Phần thứ hai là **input gate** $i_t$, lại là sigmoid. Nó quyết định **mức độ** được phép ghi: 0 là không ghi gì, 1 là ghi toàn bộ.

[click] Phần thực sự được ghi vào là tích từng phần tử $i_t \odot \tilde c_t$.

Tại sao phải tách làm hai? Đây chính là lý do Hochreiter thêm cổng: không phải mọi đầu vào đều đáng nhớ. Với câu ví dụ, khi gặp chữ "Pháp" thì $i$ mở ra để ghi, còn khi gặp các từ như "học tiểu học", "chơi bóng đá" thì $i$ đóng lại để bảo vệ bộ nhớ.
-->

---

# Cập nhật cell state: phép CỘNG

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="state,f,i,c" />
<div>

$$\boxed{\,c_t = \textcolor{#dc2626}{f_t} \odot c_{t-1} + \textcolor{#16a34a}{i_t \odot \tilde c_t}\,}$$

<v-clicks>

- <span class="text-red-600">Giữ lại một phần trí nhớ cũ</span> **+** <span class="text-green-600">thêm thông tin mới</span>
- So sánh với RNN: $h_t = \tanh(W_h h_{t-1} + \dots)$, trí nhớ cũ bị **nhân ma trận và bóp qua tanh**
- LSTM: trí nhớ cũ chỉ bị **nhân với một số trong (0,1)** rồi **cộng**
- Nhớ phép cộng này: đây là chìa khóa của phần toán!

</v-clicks>
</div>
</div>

<!--
**[Người 2 · ~1 phút]**

Bây giờ ghép hai cổng lại để cập nhật cell state. Công thức trong khung là công thức quan trọng nhất của LSTM.

[click] Đọc bằng lời: cell state mới bằng phần trí nhớ cũ được giữ lại, **cộng** với phần thông tin mới được ghi vào.

[click] So sánh với RNN: ở RNN, trí nhớ cũ $h_{t-1}$ bị nhân với ma trận $W_h$ rồi bóp qua tanh ở **mỗi bước**.

[click] Còn ở LSTM, trí nhớ cũ $c_{t-1}$ chỉ bị nhân từng phần tử với một số trong khoảng 0 đến 1, rồi **cộng** thêm. Không có ma trận, không có tanh.

[click] Các bạn hãy nhớ phép cộng này. Lát nữa bạn [tên người 3] sẽ cho thấy chính nó giúp gradient không bị biến mất.
-->

---

# Cổng 3 · Output gate: đọc ra bao nhiêu?

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="o" />
<div>

$$o_t = \sigma\big(W_o\,[h_{t-1}, x_t] + b_o\big)$$

$$h_t = o_t \odot \tanh(c_t)$$

<v-clicks>

- $\tanh(c_t)$: đưa bộ nhớ về khoảng (−1, 1)
- $o_t$: chọn **phần nào** của bộ nhớ được đưa ra ngoài ở bước này
- Bộ nhớ có thể **giữ** một thông tin rất lâu mà **không để lộ** ra $h_t$

</v-clicks>
</div>
</div>

<!--
**[Người 2 · ~1 phút]**

Cổng cuối cùng là **output gate**, màu tím.

Cell state là bộ nhớ "bên trong". Đầu ra $h_t$ được lấy từ cell state theo hai bước. [click] Đầu tiên cho $c_t$ qua tanh để đưa giá trị về khoảng −1 đến 1. [click] Sau đó nhân với output gate $o_t$ để chọn phần nào được đọc ra ở bước này.

[click] Ý nghĩa: mạng có thể **giữ** chữ "Pháp" trong bộ nhớ suốt 30 bước mà không để nó ảnh hưởng tới các đầu ra ở giữa. Chỉ khi đến chữ "tiếng", lúc cần dự đoán ngôn ngữ, output gate mới mở ra để đọc thông tin đó.
-->

---
clicks: 4
---

# Tổng hợp: 6 phương trình của LSTM

<div class="grid grid-cols-[1.2fr_1fr] gap-6 items-center">
<LstmCell :active="['all', 'f', 'i,c', 'state,f,i,c', 'o'][$clicks] || 'all'" />
<div class="eqs">

<div :class="{ hl: $clicks === 1 }">

$f_t = \sigma(W_f[h_{t-1}, x_t] + b_f)$

</div>
<div :class="{ hl: $clicks === 2 }">

$i_t = \sigma(W_i[h_{t-1}, x_t] + b_i)$

$\tilde c_t = \tanh(W_c[h_{t-1}, x_t] + b_c)$

</div>
<div :class="{ hl: $clicks === 3 }">

$c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$

</div>
<div :class="{ hl: $clicks === 4 }">

$o_t = \sigma(W_o[h_{t-1}, x_t] + b_o)$

$h_t = o_t \odot \tanh(c_t)$

</div>
</div>
</div>

<style>
.eqs > div { padding: .1rem .6rem; border-radius: 8px; transition: background .3s; }
.eqs .hl { background: #fef9c3; }
</style>

<!--
**[Người 2 · ~1 phút]**

Đây là toàn bộ LSTM trên một slide: sáu phương trình. Mình bấm lần lượt để nối từng phương trình với vị trí của nó trên sơ đồ.

[click] Forget gate. [click] Input gate và candidate. [click] Cập nhật cell state. [click] Output gate và đầu ra $h_t$.

Để ý rằng bốn phương trình $f$, $i$, $\tilde c$, $o$ có **cùng một dạng**: nhân ma trận với $[h_{t-1}, x_t]$, cộng bias, rồi cho qua sigmoid hoặc tanh. Điểm này rất quan trọng khi tính số tham số và khi xem cách PyTorch lưu trọng số. Bạn [tên người 3] sẽ quay lại điểm này.
-->

---

# Thử tay: LSTM tính toán thế nào?

<LstmSimulator />

<!--
**[Người 2 · ~3 phút] — slide demo, nên để chủ động thời gian**

Bây giờ chúng ta chạy thử một LSTM thật, nhưng rất nhỏ: hidden size bằng 1, nên mọi giá trị đều là số và có thể tính tay. Các trọng số được cố định như các phương trình bên dưới.

**Demo 1, kéo thanh trượt:**
- Kéo $x_t$ lên 2: input gate $i$ mở gần bằng 1, candidate gần bằng 1, nên cell state $c$ nhảy lên gần 1. Mạng vừa **ghi nhớ** một thông tin.
- Kéo $x_t$ về −2: forget gate $f$ đóng gần bằng 0, nên $c$ bị **xóa**.

**Demo 2, bấm Reset rồi bấm Step liên tục.** Chuỗi đầu vào là [2, 0, 0, 0, −2, 0].
- Bước 1, x = 2: $c$ lên khoảng 0.99, mạng ghi nhớ.
- Bước 2 đến 4, x = 0: $i$ nhỏ nên không ghi gì mới, nhưng $f$ khoảng 0.97 nên $c$ chỉ giảm rất chậm: 0.98, 0.96... Bộ nhớ được **giữ**. Các bạn để ý bảng bên phải.
- Bước 5, x = −2: $f$ gần bằng 0, $c$ tụt về gần 0. Mạng **quên**.

**Demo 3, bật "Chỉnh trực tiếp các cổng":** đặt $f = 1$, $i = 0$ thì $c$ giữ nguyên tuyệt đối. Đây chính là băng chuyền của Hochreiter năm 1997.

Trong mạng thật, các trọng số này được **học** từ dữ liệu, chứ không phải do chúng ta đặt.
-->

---

# Ví dụ: các cổng "hành xử" thế nào trong một câu?

<div class="mt-4">
<GateHeatmap />
</div>

<v-clicks>

- Tại **"Pháp"**: <span class="text-green-600">i ≈ 1</span>, ghi thông tin "Pháp" vào $c_t$
- Ở các từ giữa: <span class="text-red-600">f ≈ 1</span>, giữ nguyên bộ nhớ; <span class="text-green-600">i ≈ 0</span>, không ghi đè
- Tại **"tiếng"**: <span class="text-purple-600">o ≈ 1</span>, đọc thông tin ra để dự đoán "Pháp"

</v-clicks>

<!--
**[Người 2 · ~1 phút]**

Quay lại câu ví dụ ở đầu bài. Bảng này cho thấy, **về mặt ý tưởng**, ba cổng sẽ hoạt động thế nào trên từng từ. Lưu ý đây là số minh họa, không phải số đo từ một mô hình thật.

[click] Tại chữ "Pháp", input gate mở để ghi thông tin vào bộ nhớ.

[click] Ở các từ ở giữa, forget gate gần bằng 1 để giữ bộ nhớ, input gate gần bằng 0 để không ghi đè.

[click] Đến chữ "tiếng", output gate mở ra để đọc thông tin "Pháp" và dự đoán từ tiếp theo.

Vậy là đã rõ cách LSTM hoạt động. Câu hỏi còn lại: phép cộng ở cell state có ý nghĩa gì về mặt toán? Mời bạn [tên người 3].
-->

---

# Kích thước ma trận & số tham số

<div class="grid grid-cols-2 gap-6">
<div>

Với đầu vào $x_t \in \mathbb{R}^d$ và hidden $h_t \in \mathbb{R}^h$:

$$[h_{t-1}, x_t] \in \mathbb{R}^{h+d}, \qquad W_f, W_i, W_c, W_o \in \mathbb{R}^{h \times (h+d)}$$

Gộp **4 ma trận** thành 1:

$$W \in \mathbb{R}^{4h \times (h+d)} \;\Rightarrow\; \begin{bmatrix} i \\ f \\ \tilde c \\ o \end{bmatrix}$$

<div class="text-sm opacity-80">PyTorch lưu đúng như vậy: <code>weight_ih_l0</code> (4h × d), <code>weight_hh_l0</code> (4h × h), thứ tự các cổng là <b>i, f, g, o</b></div>

</div>
<div>

$$\#\text{params} = 4 \cdot \big[h(h+d) + h\big]$$

<div class="mt-6 text-lg">

❓ Với $d = 100$, $h = 128$?

</div>

<div v-click class="mt-2">

$4 \cdot [128 \cdot 228 + 128] = \mathbf{117{,}248}$

RNN: $128 \cdot 228 + 128 = 29{,}312$, nên **LSTM gấp 4 lần**

<div class="text-sm opacity-80 mt-2">

PyTorch dùng 2 vector bias (<code>b_ih</code>, <code>b_hh</code>) nên con số là $4 \cdot [h(h+d) + 2h] = 117{,}760$

</div>

</div>
</div>
</div>

<!--
**[Người 3 · ~1.5 phút]**

Cảm ơn [tên người 2]. Phần của mình đi vào toán, bắt đầu bằng một câu hỏi rất thực tế: một lớp LSTM có bao nhiêu tham số?

Gọi kích thước đầu vào là $d$, kích thước hidden là $h$. Vector ghép $[h_{t-1}, x_t]$ có kích thước $h + d$. Mỗi cổng cần một ma trận $h \times (h+d)$ và một bias $h$.

Như bạn [tên người 2] đã nói, bốn phương trình $f$, $i$, $\tilde c$, $o$ có cùng dạng, nên ta có thể **gộp 4 ma trận thành một** ma trận $4h \times (h+d)$, tính một phép nhân rồi tách kết quả thành 4 phần. PyTorch cũng làm đúng như vậy: các bạn mở `weight_ih_l0` sẽ thấy nó có $4h$ hàng, theo thứ tự i, f, g, o, trong đó g là candidate.

Vậy số tham số là $4 \cdot [h(h+d) + h]$. Mời các bạn tính nhẩm với d = 100, h = 128.

[click] Kết quả là 117,248, đúng gấp 4 lần RNN. Lưu ý nhỏ: PyTorch dùng hai vector bias riêng cho phần input và phần hidden, nên nếu các bạn đếm trong code sẽ ra 117,760. Đây là điểm hay gây nhầm lẫn khi làm bài.
-->

---

# Tính tay forward: 2 bước thời gian

<div class="text-sm mb-2">

Dùng LSTM vô hướng ở slide demo: &nbsp; $f = \sigma(0.5h + 3x + 3)$ · $i = \sigma(0.5h + 4x - 3)$ · $\tilde c = \tanh(0.5h + 2x)$ · $o = \sigma(0.5h + x + 1)$ · khởi tạo $h_0 = c_0 = 0$

</div>

<div class="calc">

| Đại lượng | t = 1 &nbsp;($x_1 = 2$, $h_0 = 0$) | t = 2 &nbsp;($x_2 = 0$, $h_1 = 0.7225$) |
|---|---|---|
| $f_t$ | <span v-click="1">$\sigma(9) = 0.9999$</span> | <span v-click="4">$\sigma(3.361) = 0.9665$</span> |
| $i_t$ | <span v-click="1">$\sigma(5) = 0.9933$</span> | <span v-click="4">$\sigma(-2.639) = 0.0667$</span> |
| $\tilde c_t$ | <span v-click="1">$\tanh(4) = 0.9993$</span> | <span v-click="4">$\tanh(0.361) = 0.3463$</span> |
| $c_t = f_t c_{t-1} + i_t \tilde c_t$ | <span v-click="2">$0 + 0.9933 \cdot 0.9993 = \mathbf{0.9926}$</span> | <span v-click="5">$0.9665 \cdot 0.9926 + 0.0667 \cdot 0.3463 = \mathbf{0.9825}$</span> |
| $o_t$ | <span v-click="3">$\sigma(3) = 0.9526$</span> | <span v-click="6">$\sigma(1.361) = 0.7960$</span> |
| $h_t = o_t \tanh(c_t)$ | <span v-click="3">$0.9526 \cdot \tanh(0.9926) = \mathbf{0.7225}$</span> | <span v-click="6">$0.7960 \cdot \tanh(0.9825) = \mathbf{0.6003}$</span> |

</div>

<style>
.calc table { font-size: .8rem; }
.calc td, .calc th { padding: .25rem .6rem !important; }
</style>

<div v-click="7" class="mt-3 p-2 rounded bg-blue-50 text-center">

Ở bước 2, input gần như không ghi gì (i ≈ 0.07) nhưng $c_t$ vẫn ≈ 0.98: trí nhớ được <b>giữ</b> nhờ $f_t$ ≈ 0.97

</div>

<!--
**[Người 3 · ~2 phút]**

Để chắc chắn mọi người hiểu forward, mình tính tay hai bước với đúng LSTM nhỏ ở slide demo. Ban đầu $h_0 = c_0 = 0$.

**Bước 1, x = 2.** [click] Forget gate bằng sigmoid của $0.5 \cdot 0 + 3 \cdot 2 + 3 = 9$, ra khoảng 0.9999. Input gate bằng sigmoid của 5, ra 0.9933. Candidate bằng tanh của 4, ra 0.9993.
[click] Cell state: $c_0 = 0$ nên chỉ còn phần ghi mới, $0.9933 \times 0.9993 = 0.9926$.
[click] Output gate bằng sigmoid của 3, ra 0.9526. Vậy $h_1 = 0.9526 \times \tanh(0.9926) = 0.7225$.

**Bước 2, x = 0.** Bây giờ $h_1 = 0.7225$, nên $0.5 h = 0.361$.
[click] f bằng sigmoid của 3.361, ra 0.9665. i bằng sigmoid của −2.639, ra 0.0667, rất nhỏ. Candidate là 0.3463.
[click] Cell state: $0.9665 \times 0.9926 + 0.0667 \times 0.3463 = 0.9825$.
[click] o là 0.796, và $h_2 = 0.6003$.

[click] Điểm cần thấy: ở bước 2 gần như không có gì mới được ghi, nhưng cell state vẫn giữ ở mức 0.98. Trí nhớ được giữ lại nhờ forget gate gần bằng 1.
-->

---
clicks: 3
---

# Backward: gradient đi qua cell state thế nào?

<div v-click="1" class="text-sm">

**Công thức đầy đủ** ($c_{t-1}$ ảnh hưởng tới $c_t$ qua 2 con đường):

$$
\frac{\partial c_t}{\partial c_{t-1}} =
\underbrace{\textcolor{#2563eb}{\operatorname{diag}(f_t)}}_{\text{trực tiếp}}
+
\underbrace{\textcolor{#94a3b8}{\Big[\operatorname{diag}(c_{t-1}\!\odot\!\sigma'_f)\,W_{fh} + \operatorname{diag}(\tilde c_t\!\odot\!\sigma'_i)\,W_{ih} + \operatorname{diag}(i_t\!\odot\!\tanh'_{\tilde c})\,W_{ch}\Big]\operatorname{diag}\big(o_{t-1}\!\odot\!\tanh'(c_{t-1})\big)}}_{\text{gián tiếp, đi qua } h_{t-1}\text{: có } W \text{ và đạo hàm, giống RNN}}
$$

</div>

<div v-click="2" class="grid grid-cols-2 gap-4 mt-2">
<div class="p-3 rounded bg-orange-50 text-center">

**RNN**

$$\frac{\partial h_T}{\partial h_k} = \prod \operatorname{diag}(\tanh')\,W_h$$

ma trận $W_h$ nhân lặp lại → biến mất / bùng nổ

</div>
<div class="p-3 rounded bg-blue-50 text-center">

**LSTM, đường trực tiếp**

$$\frac{\partial c_T}{\partial c_k} \approx \prod_{t=k+1}^{T} \operatorname{diag}(f_t)$$

không có $W$, không có $\tanh'$; mạng **tự học** giữ $f \approx 1$

</div>
</div>

<div v-click="3" class="mt-3 text-center text-sm">
📜 Bản gốc 1997 <b>chủ động cắt bỏ</b> các số hạng gián tiếp khi tính gradient, chỉ giữ đường trực tiếp.
</div>

<!--
**[Người 3 · ~3 phút] — slide toán quan trọng nhất**

Đây là câu hỏi cốt lõi: khi lan truyền ngược, gradient đi từ $c_t$ về $c_{t-1}$ như thế nào?

[click] Nhìn lại công thức $c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$. Biến $c_{t-1}$ ảnh hưởng tới $c_t$ qua **hai con đường**.

- **Đường trực tiếp**, màu xanh: $c_{t-1}$ được nhân thẳng với $f_t$. Đạo hàm theo đường này chỉ là $\operatorname{diag}(f_t)$.
- **Đường gián tiếp**, màu xám: $c_{t-1}$ tạo ra $h_{t-1}$, và $h_{t-1}$ lại là đầu vào của cả bốn cổng ở bước $t$. Đạo hàm theo đường này cho ra ba số hạng trong ngoặc vuông. Các bạn không cần nhớ chúng. Chỉ cần thấy mỗi số hạng đều có **ma trận $W$** và **đạo hàm của sigmoid hoặc tanh**, tức là có cấu trúc giống hệt RNN.

[click] Bây giờ đặt RNN và đường trực tiếp của LSTM cạnh nhau. Bên trái, RNN: một tích của các ma trận $W_h$ và $\tanh'$, nên biến mất hoặc bùng nổ. Bên phải, LSTM: chỉ là tích các $f_t$. **Không có ma trận trọng số, không có đạo hàm tanh.** Quan trọng hơn, $f_t$ là thứ mạng **tự học** được: khi cần nhớ, mạng học cách giữ $f$ gần bằng 1, và gradient đi qua gần như nguyên vẹn.

Các số hạng gián tiếp vẫn có thể biến mất. Nhưng gradient là tổng của các con đường, nên **chỉ cần còn đường trực tiếp là gradient vẫn về được**.

[click] Một chi tiết lịch sử: trong bài báo năm 1997, Hochreiter còn **chủ động cắt bỏ** các số hạng gián tiếp khi huấn luyện, chỉ giữ đường trực tiếp. Phải đến năm 2005, Graves mới huấn luyện bằng gradient đầy đủ.
-->

---

# So sánh trực quan: $\gamma^T$ (RNN) vs $\prod f_t$ (LSTM)

<div class="mt-6">
<GradientDecay lstm />
</div>

<div class="mt-4 text-center text-sm opacity-80">Thử: γ = 0.9, f = 0.99, T = 100 → RNN ≈ 3·10⁻⁵, LSTM ≈ 0.37</div>

<!--
**[Người 3 · ~1 phút]**

Đây là thanh trượt của bạn [tên người 1] ở slide 5, nhưng thêm đường màu xanh của LSTM.

**(Demo)** Đặt γ = 0.9 cho RNN, f = 0.99 cho LSTM, T = 100. RNN còn khoảng $3 \cdot 10^{-5}$, LSTM còn khoảng 0.37. Chênh nhau hơn **mười nghìn lần**.

Kéo f lên 1.0: đường xanh nằm ngang, gradient không suy giảm chút nào. Đây chính là Constant Error Carousel của bản 1997.

Khác biệt nằm ở chỗ γ của RNN phụ thuộc vào $W_h$ và tanh', rất khó giữ gần 1. Còn $f$ là một cổng mà mạng có thể học để đặt gần 1 khi cần nhớ.
-->

---

# Nối lại kiến thức CNN: "đường cao tốc" cho gradient

<div class="grid grid-cols-2 gap-6 mt-4">
<div class="p-4 rounded bg-amber-50">

### ResNet (2015)

$$x_{l+1} = x_l + F(x_l)$$

$$\frac{\partial x_{l+1}}{\partial x_l} = I + \frac{\partial F}{\partial x_l}$$

Skip connection theo **chiều sâu** (các lớp)

</div>
<div class="p-4 rounded bg-blue-50">

### LSTM (1997)

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$$

$$\frac{\partial c_t}{\partial c_{t-1}} \approx \operatorname{diag}(f_t)$$

"Skip connection" theo **thời gian** (các bước)

</div>
</div>

<div v-click class="mt-4 text-center">
Cùng một ý tưởng: <b>phép cộng</b> tạo đường đi để gradient không bị nhân nhỏ dần.<br>
<span class="text-sm opacity-80">Highway Network (Srivastava, Greff, Schmidhuber 2015), tiền thân của ResNet, chính là cổng kiểu LSTM đặt theo chiều sâu.</span>
</div>

<!--
**[Người 3 · ~1.5 phút]**

Slide này nối lại kiến thức CNN mà các bạn đã học.

Bên trái là ResNet. Khối residual tính $x_{l+1} = x_l + F(x_l)$. Đạo hàm là ma trận đơn vị $I$ cộng thêm một phần. Nhờ số hạng $I$, gradient luôn có một đường đi thẳng qua các lớp. Đó là lý do ResNet huấn luyện được mạng hơn 100 lớp.

Bên phải là LSTM: $c_t = f_t \odot c_{t-1} + \dots$. Đạo hàm theo đường trực tiếp là $\operatorname{diag}(f_t)$. Khi $f = 1$ thì chính là ma trận đơn vị.

[click] Hai mô hình dùng **cùng một ý tưởng**: dùng phép cộng để tạo "đường cao tốc" cho gradient. ResNet làm theo chiều sâu của mạng, LSTM làm theo chiều thời gian. LSTM ra đời trước ResNet gần 20 năm. Thêm nữa, Highway Network, tiền thân trực tiếp của ResNet, do chính nhóm của Schmidhuber đề xuất, và nó dùng đúng cơ chế cổng của LSTM.
-->

---

# Hệ quả thực tế từ toán

<div class="grid grid-cols-2 gap-6 mt-2">
<div>

### 1 · Khởi tạo forget bias = 1

Ban đầu $f_t = \sigma(b_f) \approx 0.73$ thay vì $0.5$ → mạng **"nhớ mặc định"**, gần với tinh thần bản 1997

```python
for name, p in lstm.named_parameters():
    if 'bias_ih' in name:
        h = p.size(0) // 4
        p.data[h:2*h].fill_(1.0)  # thứ tự i, f, g, o
```

</div>
<div v-click>

### 2 · Vẫn cần gradient clipping

Đường trực tiếp chống được **biến mất**, nhưng các số hạng **gián tiếp** (có $W$) vẫn có thể **bùng nổ**

```python
loss.backward()
torch.nn.utils.clip_grad_norm_(
    model.parameters(), max_norm=1.0)
optimizer.step()
```

</div>
</div>

<!--
**[Người 3 · ~1 phút]**

Từ phần toán vừa rồi, ta rút ra hai mẹo thực tế khi code.

Mẹo thứ nhất: **khởi tạo bias của forget gate bằng 1**. Nếu bias bằng 0 thì lúc đầu $f = \sigma(0) = 0.5$, nghĩa là mỗi bước mất một nửa trí nhớ, và gradient giảm theo $0.5^T$. Đặt bias bằng 1 thì $f$ khoảng 0.73, mạng có xu hướng nhớ ngay từ đầu. Trong PyTorch, các bias được xếp theo thứ tự i, f, g, o, nên phần forget nằm ở đoạn thứ hai, từ $h$ đến $2h$.

[click] Mẹo thứ hai: **vẫn phải dùng gradient clipping**. Đường trực tiếp chỉ giúp gradient không **biến mất**. Các số hạng gián tiếp ở slide 19 vẫn chứa ma trận $W$, nên gradient vẫn có thể **bùng nổ**. Clipping là một dòng code nhưng giúp tránh việc loss đột nhiên thành NaN.
-->

---

# Thí nghiệm: RNN vs LSTM trên cùng dữ liệu

<div class="text-sm mb-2"><b>Adding Problem</b>: chuỗi dài T, mỗi bước gồm (số ngẫu nhiên, cờ 0/1); đúng 2 vị trí được đánh dấu → dự đoán <b>tổng 2 số đó</b>. Cùng cấu hình: hidden 64, Adam lr 1e-3, batch 64, 5000 bước, clip 1.0</div>

<CompareChart />

<!--
**[Người 3 · ~2 phút]**

Cuối cùng là bằng chứng thực nghiệm. Nhóm mình tự huấn luyện RNN và LSTM bằng PyTorch trên **cùng một bộ dữ liệu**, với cùng cấu hình.

Bài toán là Adding Problem, một bài kinh điển có từ bài báo năm 1997. Đầu vào là một chuỗi dài T; mỗi bước có một số ngẫu nhiên và một cờ đánh dấu. Có đúng hai vị trí được đánh dấu, và mô hình phải trả về tổng của hai số đó. Một vị trí luôn nằm ở nửa đầu chuỗi, nên mô hình phải nhớ qua khoảng T/2 bước. Nếu đoán bừa, luôn trả về 1, thì MSE khoảng 0.167, là đường nét đứt.

**(Bấm T = 10)** Với chuỗi ngắn, **cả hai đều học được**: loss của cả hai giảm xuống dưới đường đoán bừa. Test MSE của RNN là khoảng 0.0013, của LSTM là 0.0001. LSTM tốt hơn, nhưng RNN cũng làm được.

**(Bấm T = 100)** Với chuỗi dài, **RNN đứng yên ở đường đoán bừa** suốt 5000 bước: test MSE là 0.163, gần như đúng bằng 0.167 của việc đoán bừa, nghĩa là nó không học được gì. LSTM ban đầu cũng dò dẫm khoảng 2700 bước, rồi đột ngột "bắt được" quy luật, loss giảm mạnh và kết thúc ở test MSE 0.0044, tốt hơn RNN gần **40 lần**.

Bảng bên phải cho thấy cái giá phải trả: LSTM có 17,473 tham số so với 4,417 của RNN, tức gần gấp 4, và thời gian huấn luyện cũng lâu hơn.

Đây chính là điều mà công thức ở slide 19 dự đoán. Sang phần cuối, bạn [tên người 4] sẽ nói về cách LSTM được dùng trong thực tế.
-->

---

# Biến thể: GRU (2014)

<div class="grid grid-cols-2 gap-6">
<div class="p-3 rounded bg-blue-50">

### LSTM: 3 cổng + cell state

$f_t,\ i_t,\ o_t = \sigma(\cdot)$, $\ \tilde c_t = \tanh(\cdot)$

$c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$

$h_t = o_t \odot \tanh(c_t)$

**4 khối** trọng số

</div>
<div class="p-3 rounded bg-emerald-50">

### GRU: 2 cổng, không có cell state riêng

$z_t = \sigma(W_z[h_{t-1}, x_t])$ (update)
$r_t = \sigma(W_r[h_{t-1}, x_t])$ (reset)

$\tilde h_t = \tanh(W[r_t \odot h_{t-1}, x_t])$

$h_t = \textcolor{#dc2626}{(1 - z_t)} \odot h_{t-1} + \textcolor{#16a34a}{z_t} \odot \tilde h_t$

**3 khối** trọng số → nhẹ hơn khoảng 25%

</div>
</div>

<div v-click class="mt-4 text-center">

GRU <b>gộp</b> forget và input gate thành một cổng $z_t$: "quên bao nhiêu thì ghi bấy nhiêu". Hiệu quả thường tương đương LSTM. → <code>nn.GRU</code>

</div>

<!--
**[Người 4 · ~1.5 phút]**

Cảm ơn [tên người 3]. Phần cuối nói về LSTM trong thực tế, bắt đầu từ biến thể nổi tiếng nhất: **GRU**, do Cho và cộng sự đề xuất năm 2014.

Bên trái là LSTM: ba cổng, một cell state, bốn khối trọng số.

Bên phải là GRU, chỉ có **hai cổng**: update gate $z$ và reset gate $r$, và **không có cell state riêng**, chỉ có $h$.

Phương trình quan trọng nhất là dòng cuối: $h_t = (1 - z_t) h_{t-1} + z_t \tilde h_t$. So với LSTM, $1 - z$ đóng vai trò forget gate, còn $z$ đóng vai trò input gate.

[click] Nghĩa là GRU **gộp** forget và input gate thành một: quên bao nhiêu thì ghi bấy nhiêu. Vẫn là phép cộng, nên vẫn có đường cao tốc cho gradient. GRU có ít hơn khoảng 25% tham số và trên nhiều bài toán cho kết quả tương đương LSTM. Trong PyTorch, chỉ cần đổi `nn.LSTM` thành `nn.GRU`.
-->

---

# Stacked & Bidirectional LSTM

<div class="grid grid-cols-2 gap-6">
<div>

### Stacked: xếp chồng nhiều lớp
Output $h_t$ của lớp 1 là input của lớp 2 → học đặc trưng ở mức trừu tượng cao hơn

### Bidirectional: chạy 2 chiều
$$h_t = [\,\overrightarrow{h}_t\,;\,\overleftarrow{h}_t\,]$$
Mỗi bước "nhìn" được cả quá khứ **và tương lai**

<div v-click class="text-red-600 text-sm mt-2">⚠️ Không dùng bidirectional cho bài toán <b>dự báo tương lai</b>, vì như vậy là nhìn trộm đáp án!</div>

</div>
<div>

```python
lstm = nn.LSTM(input_size=d, hidden_size=h,
               num_layers=2,          # stacked
               bidirectional=True,    # 2 chiều
               batch_first=True, dropout=0.2)

output, (h_n, c_n) = lstm(x)   # x: (B, T, d)
# output: (B, T, 2h)           mọi bước, lớp cuối
# h_n:    (2*2, B, h)          bước cuối, mọi lớp × chiều
```

</div>
</div>

<!--
**[Người 4 · ~1.5 phút]**

Hai cách mở rộng hay dùng nhất.

**Stacked LSTM**: xếp nhiều lớp LSTM chồng lên nhau. Chuỗi output $h$ của lớp dưới là chuỗi input của lớp trên. Giống CNN có nhiều lớp, lớp sau học được đặc trưng trừu tượng hơn.

**Bidirectional LSTM**: chạy một LSTM từ trái sang phải và một LSTM từ phải sang trái, rồi ghép hai hidden state lại. Như vậy mỗi bước được nhìn cả quá khứ lẫn tương lai. Cách này rất hữu ích cho phân loại văn bản hay gán nhãn từ loại.

[click] Lưu ý: **không** dùng bidirectional cho bài toán dự báo tương lai, ví dụ dự báo giá cổ phiếu, vì mô hình sẽ nhìn thấy dữ liệu tương lai, tức là nhìn trộm đáp án.

Bên phải là code PyTorch. Chỉ cần hai tham số `num_layers` và `bidirectional`. Chú ý **shape của output**: `output` có chiều cuối là 2h vì ghép hai chiều; `h_n` có số phần tử ở chiều đầu bằng số lớp nhân số chiều. Đây là chỗ các bạn hay bị lỗi shape nhất.
-->

---

# Ứng dụng & giới hạn

<div class="grid grid-cols-2 gap-6">
<div>

### Ứng dụng
- **many-to-one**: phân loại cảm xúc, phân loại chuỗi
- **many-to-many**: gán nhãn từ loại, nhận dạng giọng nói
- **seq2seq**: dịch máy (encoder–decoder)
- **Chuỗi thời gian**: dự báo nhu cầu, cảm biến, tài chính
- **Sinh dữ liệu**: văn bản, nhạc, chữ viết tay

</div>
<div>

### Giới hạn
- Tính **tuần tự**: bước t phải chờ bước t−1, nên **không song song hóa** theo thời gian được
- Chuỗi rất dài (hàng nghìn token) vẫn khó
- Nhiều tham số hơn RNN gấp 4 lần

<div v-click class="mt-4 p-3 rounded bg-slate-100">

→ **Attention** (2014) → **Transformer** (2017): bỏ hẳn hồi quy, mọi bước "nhìn" nhau trực tiếp

<span class="text-sm">MLP → CNN / RNN → LSTM → GRU → Transformer</span>

</div>
</div>
</div>

<!--
**[Người 4 · ~1.5 phút]**

LSTM được dùng ở đâu? Các bạn có thể chia theo kiểu đầu vào và đầu ra. **Many-to-one**: cả chuỗi cho ra một nhãn, ví dụ phân loại cảm xúc. **Many-to-many**: mỗi bước một nhãn, ví dụ nhận dạng giọng nói. **Seq2seq**: một LSTM encoder đọc câu nguồn, một LSTM decoder sinh câu đích; đây là kiến trúc Google Translate dùng năm 2016. Ngoài ra còn rất nhiều ứng dụng với chuỗi thời gian.

Nhưng LSTM cũng có giới hạn. Lớn nhất là nó tính **tuần tự**: muốn tính bước t thì phải xong bước t−1, nên không tận dụng được GPU song song theo thời gian. Với chuỗi rất dài, nó vẫn gặp khó khăn.

[click] Đó là lý do Attention và sau đó là Transformer ra đời năm 2017: bỏ hẳn cơ chế hồi quy, cho mọi bước nhìn nhau trực tiếp. Đây là chủ đề cho một buổi khác. Gia phả của chúng ta giờ đã đầy đủ: từ MLP, qua CNN và RNN, đến LSTM, GRU, rồi Transformer.
-->

---

# Hướng dẫn Assignment 7: khung LSTM với PyTorch

<div class="grid grid-cols-[1.4fr_1fr] gap-4">
<div>

```python {1-9|5|7-9|11-16|14}{maxHeight:'340px'}
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size,
                            batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    def forward(self, x):            # x: (batch, seq_len, input_size)
        output, (h_n, c_n) = self.lstm(x)
        return self.fc(h_n[-1])      # many-to-one: hidden cuối

# vòng train
for x, y in train_loader:
    loss = criterion(model(x), y)
    optimizer.zero_grad(); loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
```

</div>
<div class="text-sm">

**Pipeline:** dữ liệu → chuẩn hóa / tokenize → chia chuỗi, padding → (Embedding) → **LSTM** → Linear → loss

**3 lỗi hay gặp**
1. Quên `batch_first=True` → shape là (seq, batch, feat), sai thứ tự chiều
2. Lấy `output[:, -1]` khi có **padding** → lấy nhầm bước pad; dùng `h_n[-1]` hoặc `pack_padded_sequence`
3. Loss thành **NaN** → quên clip gradient, hoặc lr quá lớn

<div class="opacity-70 mt-2">Gợi ý: hidden 64–256, 1–2 lớp, dropout 0.2–0.5, Adam lr 1e-3, có baseline RNN để so sánh</div>

</div>
</div>

<!--
**[Người 4 · ~2.5 phút]**

Slide này là khung chung để các bạn chuẩn bị cho Assignment 7. Thầy chưa giao đề cụ thể nên mình chỉ đưa ra bộ khung dùng được cho hầu hết bài toán.

[click] Mô hình chỉ cần hai thành phần: một lớp `nn.LSTM` và một lớp `Linear` ở cuối.

[click] Chú ý `batch_first=True`. Mặc định PyTorch nhận đầu vào theo thứ tự (seq_len, batch, feature). Hầu hết mọi người chuẩn bị dữ liệu theo (batch, seq_len, feature), nên cần bật tham số này.

[click] Trong forward, `nn.LSTM` trả về hai thứ: `output` chứa hidden ở **mọi bước**, và cặp `(h_n, c_n)` chứa trạng thái ở **bước cuối**. Với bài phân loại many-to-one, ta lấy `h_n[-1]`, tức là hidden cuối của lớp trên cùng, rồi đưa vào Linear.

[click] Vòng train giống hệt CNN mà các bạn đã làm: forward, tính loss, zero_grad, backward, step. [click] Chỉ thêm đúng một dòng: **clip gradient**, như bạn [tên người 3] đã giải thích.

Bên phải là ba lỗi hay gặp nhất: sai thứ tự chiều do quên batch_first, lấy nhầm bước padding, và loss thành NaN. Lời khuyên cuối: luôn train thêm một baseline RNN để so sánh, giống thí nghiệm ở slide 23. Đó là cách tốt nhất để thấy LSTM thực sự giúp được bao nhiêu.
-->

---

# Tổng kết

<div class="grid grid-cols-3 gap-4 mt-2 text-center">
<div class="p-2 rounded bg-blue-50">

<span class="text-3xl">🧠</span><br><b>Cell state $c_t$</b><br><span class="text-sm">băng chuyền bộ nhớ dài hạn</span>

</div>
<div class="p-2 rounded bg-green-50">

<span class="text-3xl">🚪</span><br><b>3 cổng f, i, o</b><br><span class="text-sm">quên · ghi · đọc, đều là sigmoid</span>

</div>
<div class="p-2 rounded bg-amber-50">

<span class="text-3xl">➕</span><br><b>Phép cộng</b><br><span class="text-sm">$\partial c_t / \partial c_{t-1} \approx \operatorname{diag}(f_t)$ → gradient không biến mất</span>

</div>
</div>

### Mini-quiz

<div class="grid grid-cols-3 gap-4 text-sm">
<div>

1\. Nếu $f_t = 0$ ở mọi bước thì chuyện gì xảy ra?

<div v-click class="text-blue-600 mt-1">→ Mất toàn bộ trí nhớ dài hạn, mỗi bước bắt đầu lại từ đầu</div>
</div>
<div>

2\. Bản LSTM năm 1997 thiếu cổng nào?

<div v-click class="text-blue-600 mt-1">→ Forget gate (Gers và cộng sự thêm năm 1999–2000)</div>
</div>
<div>

3\. LSTM 1 lớp, $d = 50$, $h = 100$ có bao nhiêu tham số (công thức 1 bias)?

<div v-click class="text-blue-600 mt-1">→ 4 · (100 · 150 + 100) = 60,400</div>
</div>
</div>

<!--
**[Người 4 · ~2 phút]**

Tóm lại bài hôm nay bằng ba ý.

Một: LSTM thêm vào RNN một **cell state**, là băng chuyền bộ nhớ dài hạn.
Hai: **ba cổng** forget, input, output, đều dùng sigmoid, quyết định quên bao nhiêu, ghi bao nhiêu, đọc ra bao nhiêu.
Ba: nhờ **phép cộng** trên cell state, gradient có đường đi trực tiếp chỉ qua $f_t$, nên không bị biến mất như RNN.

Bây giờ là ba câu hỏi nhanh để kiểm tra. Mời các bạn trả lời.

Câu 1: nếu forget gate luôn bằng 0 thì sao? [click] Mất toàn bộ trí nhớ dài hạn; cell state chỉ còn thông tin của bước hiện tại.

Câu 2: bản LSTM năm 1997 thiếu cổng nào? [click] Forget gate.

Câu 3: tính số tham số. [click] $4 \cdot (100 \cdot 150 + 100) = 60{,}400$.
-->

---
layout: center
class: text-center
---

# Cảm ơn thầy và các bạn đã lắng nghe!

## Q&A

<div class="mt-8 text-sm opacity-70">
Tài liệu: Hochreiter & Schmidhuber (1997) · Gers et al. (2000) · Graves & Schmidhuber (2005) · Bengio et al. (1994) · colah.github.io/posts/2015-08-Understanding-LSTMs
</div>

<!--
**[Cả nhóm · ~2 phút]**

Phần trình bày của nhóm mình đến đây là kết thúc. Cảm ơn thầy và các bạn đã lắng nghe. Nhóm mình xin nhận câu hỏi.

*(Gợi ý chuẩn bị trước một số câu hỏi có thể gặp:)*
- *Vì sao không dùng ReLU cho các cổng?* Vì cổng cần giá trị trong (0,1) để đóng vai trò van; ReLU không bị chặn trên.
- *LSTM có hoàn toàn hết vanishing gradient không?* Không. Nó chỉ tạo một đường mà mạng **có thể học** để giữ gradient; nếu f nhỏ thì gradient vẫn suy giảm.
- *Khi nào dùng GRU, khi nào dùng LSTM?* GRU nhẹ hơn, hợp với dữ liệu ít; LSTM linh hoạt hơn một chút. Thực tế nên thử cả hai.
-->
