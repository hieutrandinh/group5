# Lời thoại thuyết trình LSTM (45 phút, 4 người)

> File được sinh tự động từ speaker notes trong `slides/slides.md` (lệnh `npm run notes` trong thư mục `slides`). Muốn sửa lời thoại thì sửa trong `slides.md` rồi chạy lại lệnh, để slide và file này luôn khớp nhau.
>
> Ký hiệu: **[click]** = bấm sang bước animation tiếp theo · **(Demo)** = thao tác trên slide tương tác · `[tên người X]` = thay bằng tên thật.

---

## Phần 1 — Vì sao cần LSTM? + lịch sử ra đời (Người 1)

### Slide 1 · LSTM — Long Short-Term Memory  
*Người 1 · ~1 phút*

Xin chào thầy và các bạn. Hôm nay nhóm mình trình bày về LSTM, viết tắt của Long Short-Term Memory.

Trước khi vào bài, mời các bạn đọc câu này: "Tôi lớn lên ở Pháp, nên tôi nói thành thạo tiếng ___". Ai cũng điền được ngay: tiếng Pháp.

[click] Nhưng nếu câu dài ra thế này, ở giữa chen vào ba chục từ không liên quan, thì để điền được chỗ trống, mô hình phải **nhớ chữ "Pháp" qua khoảng 30 bước**.

[click] Với RNN thông thường, đến cuối câu thì chữ "Pháp" gần như đã mờ hết. Bài hôm nay trả lời ba câu hỏi: vì sao RNN quên, LSTM sửa chuyện đó bằng cách nào, và vì sao về mặt toán học cách sửa đó hiệu quả.

### Slide 2 · LSTM đứng ở đâu trong gia phả mạng nơ-ron?  
*Người 1 · ~1.5 phút*

Trước khi vào LSTM, mình đặt nó vào bức tranh chung các mô hình mà lớp mình đã học.

[click] Gốc là **MLP**: đầu vào là một vector có kích thước cố định, mỗi trọng số dùng đúng một lần. MLP không biết gì về cấu trúc của dữ liệu.

[click] Nhánh thứ nhất là **CNN**, các bạn đã làm ở assignment trước. CNN thêm vào ý tưởng **chia sẻ trọng số theo không gian**: cùng một kernel trượt qua mọi vị trí của ảnh.

[click] Nhánh thứ hai là **RNN**. RNN cũng chia sẻ trọng số, nhưng **theo thời gian**: cùng một ô được dùng lại ở mọi bước của chuỗi.

[click] Và đây là nhân vật chính. Điểm quan trọng nhất của slide này: **LSTM không phải một họ mô hình mới, nó vẫn là RNN**. Vẫn unroll theo thời gian, vẫn huấn luyện bằng backpropagation through time. Thứ duy nhất thay đổi là cái ô bên trong: thay vì một phép tanh đơn giản, LSTM dùng một ô có các cổng và một bộ nhớ dài hạn riêng.

### Slide 3 · So sánh nhanh MLP · CNN · RNN · LSTM  
*Người 1 · ~1 phút*

Bảng này tóm tắt lại sự khác nhau giữa bốn mô hình. Mình chỉ lưu ý ba dòng.

Dòng **bộ nhớ**: MLP và CNN không có bộ nhớ, mỗi đầu vào được xử lý độc lập. RNN có một hidden state $h_t$. LSTM có **hai** trạng thái: $h_t$ và cell state $c_t$. Cái $c_t$ này là chìa khóa của cả bài.

Dòng **phụ thuộc xa**: trên thực tế RNN thường chỉ nhớ được khoảng 10 bước. Bài báo gốc năm 1997 cho thấy LSTM học được những phụ thuộc cách nhau hơn 1000 bước.

Dòng **số tham số**: LSTM có khoảng gấp 4 lần RNN. Lát nữa người thứ ba sẽ giải thích tại sao lại đúng là 4.

[click] Tóm lại: LSTM giữ nguyên mọi ưu điểm của RNN, và chỉ sửa một điểm yếu là trí nhớ ngắn.

### Slide 4 · Ôn lại RNN  
*Người 1 · ~1.5 phút*

Ôn lại nhanh RNN mà các bạn đã làm. Ở mỗi bước, hidden state mới $h_t$ được tính từ hidden state cũ $h_{t-1}$ và đầu vào $x_t$, rồi cho qua tanh.

[click] [click] [click] [click] Khi unroll theo thời gian, ta được một chuỗi các ô nối tiếp nhau. Lưu ý mũi tên màu cam: **cùng một ma trận $W_h$** được dùng lại ở mọi bước.

[click] Để huấn luyện, ta dùng backpropagation through time, tức là lan truyền ngược qua toàn bộ chuỗi đã unroll. Vì $W_h$ xuất hiện ở mọi bước, gradient từ bước cuối muốn về được bước đầu thì phải đi qua $W_h$ rất nhiều lần. Đây chính là nguồn gốc của vấn đề ở slide tiếp theo.

### Slide 5 · Vấn đề: gradient biến mất / bùng nổ  
*Người 1 · ~2 phút*

Đây là phần toán quan trọng nhất của phần mở đầu. Muốn biết lỗi ở bước cuối $T$ ảnh hưởng thế nào tới bước $k$, ta lấy đạo hàm $\partial h_T / \partial h_k$. Theo quy tắc chuỗi, đạo hàm này là một **tích** gồm $T-k$ thừa số. Mỗi thừa số là đạo hàm của tanh nhân với $W_h$.

Đạo hàm của tanh luôn nhỏ hơn hoặc bằng 1. Vì vậy, gọi $\gamma$ là độ lớn của mỗi thừa số:
- nếu $\gamma < 1$, tích tiến về 0 theo hàm mũ: gradient biến mất;
- nếu $\gamma > 1$, tích tiến ra vô cùng: gradient bùng nổ.

**(Demo)** Mình kéo thử thanh trượt. Với $\gamma = 0.9$, một con số nghe rất "vô hại", và $T = 50$ bước, ta được $0.9^{50} \approx 0.005$. Nghĩa là tín hiệu học từ bước 50 về bước đầu chỉ còn **0.5%**. Kéo $T$ lên 100 thì còn khoảng $3 \cdot 10^{-5}$, tức là gần như bằng không. Kéo $\gamma$ lên 1.1 thì đồ thị vọt lên trên: gradient bùng nổ.

Muốn đúng bằng 1 thì phải "đặt trên lưỡi dao", điều gần như không thể giữ được trong lúc huấn luyện. Đó là lý do RNN không học được chữ "Pháp" ở slide đầu.

### Slide 6 · Lịch sử: người phát hiện ra vấn đề  
*Người 1 · ~2.5 phút*

Vậy ai là người đã nhìn ra vấn đề này và sửa nó?

[click] Năm 1991, Sepp Hochreiter, lúc đó còn là **sinh viên** ở Đại học Kỹ thuật München, làm luận văn tốt nghiệp với thầy hướng dẫn là Jürgen Schmidhuber. Trong luận văn đó, ông là người đầu tiên **phân tích bằng toán** vì sao RNN không học được phụ thuộc xa, tức là đúng cái tích các đạo hàm mà chúng ta vừa xem. Ba năm sau, Bengio và cộng sự cũng công bố độc lập cùng kết quả. Nghĩa là hai người đọc một luận văn sinh viên trước, rồi mới đến một bài báo của Bengio.

[click] Ý tưởng sửa của ông rất đơn giản, gần như hiển nhiên khi nhìn vào công thức. Gradient chết vì bị nhân lặp lại với một số khác 1. Vậy thì tạo ra một đơn vị **tự nối với chính nó bằng trọng số đúng bằng 1**, không có hàm kích hoạt phi tuyến. Khi đó đạo hàm của $c_t$ theo $c_{t-1}$ đúng bằng 1, nên lỗi chảy qua bao nhiêu bước cũng không đổi. Ông đặt tên là **Constant Error Carousel**, tạm dịch là "băng chuyền lỗi không đổi".

[click] Nhưng như vậy lại sinh ra vấn đề mới: mọi đầu vào đều được cộng thẳng vào bộ nhớ, thông tin rác cũng ghi vào, và bộ nhớ bị ghi đè lung tung. Giải pháp là thêm các **cổng** để kiểm soát khi nào được ghi vào, khi nào được đọc ra. Kết quả là bài báo "Long Short-Term Memory" năm 1997 trên tạp chí Neural Computation. Đến nay đây là một trong những bài báo được trích dẫn nhiều nhất của học sâu.

### Slide 7 · Hành trình của LSTM  
*Người 1 · ~1 phút*

Điểm qua nhanh hành trình của LSTM.

[click] Bản gốc năm 1997 chỉ có hai cổng: input gate và output gate. **Chưa có forget gate**, nghĩa là bộ nhớ chỉ được cộng thêm, không bao giờ bị xóa.

[click] Khoảng năm 1999–2000, Felix Gers cùng Schmidhuber thêm **forget gate**, cho phép mạng chủ động xóa trí nhớ. Cái LSTM mà chúng ta dùng ngày nay, kể cả trong PyTorch, là bản có forget gate này.

[click] Năm 2005, Alex Graves huấn luyện LSTM bằng BPTT đầy đủ và giới thiệu Bidirectional LSTM. [click] Năm 2009, LSTM thắng các cuộc thi nhận dạng chữ viết tay. [click] Năm 2014 có seq2seq cho dịch máy, cùng năm đó GRU ra đời. [click] Khoảng 2015–2016, nhận dạng giọng nói của Google và Google Translate chuyển sang LSTM. [click] Đến 2017, Transformer xuất hiện và dần thay thế LSTM trong xử lý ngôn ngữ.

[click] Còn cái tên "Long Short-Term Memory": short-term memory là bộ nhớ ngắn hạn, tức là activation của mạng, và chữ "long" nghĩa là bộ nhớ ngắn hạn đó được giữ lâu.

### Slide 8 · Vậy bên trong một ô LSTM có gì?  
*Người 1 · ~0.5 phút*

Tóm lại, chúng ta đã thấy RNN quên vì gradient bị nhân lặp lại, và Hochreiter sửa bằng một băng chuyền có trọng số bằng 1 cộng với các cổng. Bây giờ mời bạn [tên người 2] mở ô LSTM ra, xem từng cổng hoạt động thế nào.

---

## Phần 2 — Bên trong một ô LSTM (Người 2)

### Slide 9 · Ý tưởng: hai đường bộ nhớ  
*Người 2 · ~1 phút*

Cảm ơn [tên người 1]. Chúng ta bắt đầu bằng hình ảnh tổng thể.

Bên trái là RNN: chỉ có **một đường** thông tin $h$ đi qua tanh ở mỗi bước. Mọi thứ cần nhớ đều phải nhét vào $h$ và bị bóp qua tanh liên tục.

Bên phải là LSTM. Để ý đường màu xanh chạy thẳng phía trên: đó là **cell state $c_t$**.

[click] Cell state giống như một **băng chuyền**: nó chạy thẳng qua ô, trên đường chỉ có một phép nhân và một phép cộng, không có ma trận trọng số hay hàm tanh nào chặn lại. Đây chính là Constant Error Carousel của Hochreiter, đóng vai trò bộ nhớ dài hạn.

[click] Còn $h_t$ vẫn là đầu ra ở mỗi bước, giống như RNN, đóng vai trò bộ nhớ ngắn hạn, phần được "đọc ra" từ bộ nhớ dài hạn.

Ba cổng mà mình sắp trình bày chính là ba cái van điều khiển băng chuyền này.

### Slide 10 · Cổng 1 · Forget gate: giữ lại bao nhiêu trí nhớ cũ?  
*Người 2 · ~1.5 phút*

Cổng đầu tiên là **forget gate**, màu đỏ.

Nó nhận vào hai thứ: hidden state cũ $h_{t-1}$ và đầu vào hiện tại $x_t$, ghép lại thành một vector. Sau đó nhân với ma trận $W_f$, cộng bias, rồi cho qua sigmoid.

[click] Kết quả $f_t$ là một vector có giá trị trong khoảng 0 đến 1, cùng kích thước với cell state.

[click] Nếu một phần tử của $f_t$ bằng 0, phần tử tương ứng trong $c_{t-1}$ bị nhân với 0, tức là **quên sạch**. [click] Nếu bằng 1 thì **giữ nguyên**.

[click] Vì sao lại dùng sigmoid mà không dùng ReLU hay tanh? Vì sigmoid cho đầu ra trong khoảng (0, 1), đúng ý nghĩa của một cái van: 0 là đóng, 1 là mở hoàn toàn.

[click] Một chi tiết thú vị: như bạn [tên người 1] đã nói, cổng này **không có** trong bản gốc năm 1997. Bản gốc coi như $f$ luôn bằng 1, nên trí nhớ chỉ tăng chứ không bao giờ bị xóa. Ví dụ với câu "Tôi lớn lên ở Pháp", khi chuyển sang một câu chuyện khác, mạng cần biết quên chữ "Pháp" đi. Forget gate cho phép làm việc đó.

### Slide 11 · Cổng 2 · Input gate + candidate: ghi gì, ghi bao nhiêu?  
*Người 2 · ~1.5 phút*

Cổng thứ hai, màu xanh lá, gồm hai phần đi cùng nhau.

Phần thứ nhất là **candidate** $\tilde c_t$, tính bằng tanh. [click] Đây là **nội dung** mới mà mạng muốn ghi vào bộ nhớ. Dùng tanh nên giá trị nằm trong khoảng −1 đến 1, có thể tăng hoặc giảm giá trị trong bộ nhớ.

[click] Phần thứ hai là **input gate** $i_t$, lại là sigmoid. Nó quyết định **mức độ** được phép ghi: 0 là không ghi gì, 1 là ghi toàn bộ.

[click] Phần thực sự được ghi vào là tích từng phần tử $i_t \odot \tilde c_t$.

Tại sao phải tách làm hai? Đây chính là lý do Hochreiter thêm cổng: không phải mọi đầu vào đều đáng nhớ. Với câu ví dụ, khi gặp chữ "Pháp" thì $i$ mở ra để ghi, còn khi gặp các từ như "học tiểu học", "chơi bóng đá" thì $i$ đóng lại để bảo vệ bộ nhớ.

### Slide 12 · Cập nhật cell state: phép CỘNG  
*Người 2 · ~1 phút*

Bây giờ ghép hai cổng lại để cập nhật cell state. Công thức trong khung là công thức quan trọng nhất của LSTM.

[click] Đọc bằng lời: cell state mới bằng phần trí nhớ cũ được giữ lại, **cộng** với phần thông tin mới được ghi vào.

[click] So sánh với RNN: ở RNN, trí nhớ cũ $h_{t-1}$ bị nhân với ma trận $W_h$ rồi bóp qua tanh ở **mỗi bước**.

[click] Còn ở LSTM, trí nhớ cũ $c_{t-1}$ chỉ bị nhân từng phần tử với một số trong khoảng 0 đến 1, rồi **cộng** thêm. Không có ma trận, không có tanh.

[click] Các bạn hãy nhớ phép cộng này. Lát nữa bạn [tên người 3] sẽ cho thấy chính nó giúp gradient không bị biến mất.

### Slide 13 · Cổng 3 · Output gate: đọc ra bao nhiêu?  
*Người 2 · ~1 phút*

Cổng cuối cùng là **output gate**, màu tím.

Cell state là bộ nhớ "bên trong". Đầu ra $h_t$ được lấy từ cell state theo hai bước. [click] Đầu tiên cho $c_t$ qua tanh để đưa giá trị về khoảng −1 đến 1. [click] Sau đó nhân với output gate $o_t$ để chọn phần nào được đọc ra ở bước này.

[click] Ý nghĩa: mạng có thể **giữ** chữ "Pháp" trong bộ nhớ suốt 30 bước mà không để nó ảnh hưởng tới các đầu ra ở giữa. Chỉ khi đến chữ "tiếng", lúc cần dự đoán ngôn ngữ, output gate mới mở ra để đọc thông tin đó.

### Slide 14 · Tổng hợp: 6 phương trình của LSTM  
*Người 2 · ~1 phút*

Đây là toàn bộ LSTM trên một slide: sáu phương trình. Mình bấm lần lượt để nối từng phương trình với vị trí của nó trên sơ đồ.

[click] Forget gate. [click] Input gate và candidate. [click] Cập nhật cell state. [click] Output gate và đầu ra $h_t$.

Để ý rằng bốn phương trình $f$, $i$, $\tilde c$, $o$ có **cùng một dạng**: nhân ma trận với $[h_{t-1}, x_t]$, cộng bias, rồi cho qua sigmoid hoặc tanh. Điểm này rất quan trọng khi tính số tham số và khi xem cách PyTorch lưu trọng số. Bạn [tên người 3] sẽ quay lại điểm này.

### Slide 15 · Thử tay: LSTM tính toán thế nào?  
*Người 2 · ~3 phút*

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

### Slide 16 · Ví dụ: các cổng "hành xử" thế nào trong một câu?  
*Người 2 · ~1 phút*

Quay lại câu ví dụ ở đầu bài. Bảng này cho thấy, **về mặt ý tưởng**, ba cổng sẽ hoạt động thế nào trên từng từ. Lưu ý đây là số minh họa, không phải số đo từ một mô hình thật.

[click] Tại chữ "Pháp", input gate mở để ghi thông tin vào bộ nhớ.

[click] Ở các từ ở giữa, forget gate gần bằng 1 để giữ bộ nhớ, input gate gần bằng 0 để không ghi đè.

[click] Đến chữ "tiếng", output gate mở ra để đọc thông tin "Pháp" và dự đoán từ tiếp theo.

Vậy là đã rõ cách LSTM hoạt động. Câu hỏi còn lại: phép cộng ở cell state có ý nghĩa gì về mặt toán? Mời bạn [tên người 3].

---

## Phần 3 — Toán của LSTM + so sánh với RNN (Người 3)

### Slide 17 · Kích thước ma trận & số tham số  
*Người 3 · ~1.5 phút*

Cảm ơn [tên người 2]. Phần của mình đi vào toán, bắt đầu bằng một câu hỏi rất thực tế: một lớp LSTM có bao nhiêu tham số?

Gọi kích thước đầu vào là $d$, kích thước hidden là $h$. Vector ghép $[h_{t-1}, x_t]$ có kích thước $h + d$. Mỗi cổng cần một ma trận $h \times (h+d)$ và một bias $h$.

Như bạn [tên người 2] đã nói, bốn phương trình $f$, $i$, $\tilde c$, $o$ có cùng dạng, nên ta có thể **gộp 4 ma trận thành một** ma trận $4h \times (h+d)$, tính một phép nhân rồi tách kết quả thành 4 phần. PyTorch cũng làm đúng như vậy: các bạn mở `weight_ih_l0` sẽ thấy nó có $4h$ hàng, theo thứ tự i, f, g, o, trong đó g là candidate.

Vậy số tham số là $4 \cdot [h(h+d) + h]$. Mời các bạn tính nhẩm với d = 100, h = 128.

[click] Kết quả là 117,248, đúng gấp 4 lần RNN. Lưu ý nhỏ: PyTorch dùng hai vector bias riêng cho phần input và phần hidden, nên nếu các bạn đếm trong code sẽ ra 117,760. Đây là điểm hay gây nhầm lẫn khi làm bài.

### Slide 18 · Tính tay forward: 2 bước thời gian  
*Người 3 · ~2 phút*

Để chắc chắn mọi người hiểu forward, mình tính tay hai bước với đúng LSTM nhỏ ở slide demo. Ban đầu $h_0 = c_0 = 0$.

**Bước 1, x = 2.** [click] Forget gate bằng sigmoid của $0.5 \cdot 0 + 3 \cdot 2 + 3 = 9$, ra khoảng 0.9999. Input gate bằng sigmoid của 5, ra 0.9933. Candidate bằng tanh của 4, ra 0.9993.
[click] Cell state: $c_0 = 0$ nên chỉ còn phần ghi mới, $0.9933 \times 0.9993 = 0.9926$.
[click] Output gate bằng sigmoid của 3, ra 0.9526. Vậy $h_1 = 0.9526 \times \tanh(0.9926) = 0.7225$.

**Bước 2, x = 0.** Bây giờ $h_1 = 0.7225$, nên $0.5 h = 0.361$.
[click] f bằng sigmoid của 3.361, ra 0.9665. i bằng sigmoid của −2.639, ra 0.0667, rất nhỏ. Candidate là 0.3463.
[click] Cell state: $0.9665 \times 0.9926 + 0.0667 \times 0.3463 = 0.9825$.
[click] o là 0.796, và $h_2 = 0.6003$.

[click] Điểm cần thấy: ở bước 2 gần như không có gì mới được ghi, nhưng cell state vẫn giữ ở mức 0.98. Trí nhớ được giữ lại nhờ forget gate gần bằng 1.

### Slide 19 · Backward: gradient đi qua cell state thế nào?  
*Người 3 · ~3 phút*

Đây là câu hỏi cốt lõi: khi lan truyền ngược, gradient đi từ $c_t$ về $c_{t-1}$ như thế nào?

[click] Nhìn lại công thức $c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$. Biến $c_{t-1}$ ảnh hưởng tới $c_t$ qua **hai con đường**.

- **Đường trực tiếp**, màu xanh: $c_{t-1}$ được nhân thẳng với $f_t$. Đạo hàm theo đường này chỉ là $\operatorname{diag}(f_t)$.
- **Đường gián tiếp**, màu xám: $c_{t-1}$ tạo ra $h_{t-1}$, và $h_{t-1}$ lại là đầu vào của cả bốn cổng ở bước $t$. Đạo hàm theo đường này cho ra ba số hạng trong ngoặc vuông. Các bạn không cần nhớ chúng. Chỉ cần thấy mỗi số hạng đều có **ma trận $W$** và **đạo hàm của sigmoid hoặc tanh**, tức là có cấu trúc giống hệt RNN.

[click] Bây giờ đặt RNN và đường trực tiếp của LSTM cạnh nhau. Bên trái, RNN: một tích của các ma trận $W_h$ và $\tanh'$, nên biến mất hoặc bùng nổ. Bên phải, LSTM: chỉ là tích các $f_t$. **Không có ma trận trọng số, không có đạo hàm tanh.** Quan trọng hơn, $f_t$ là thứ mạng **tự học** được: khi cần nhớ, mạng học cách giữ $f$ gần bằng 1, và gradient đi qua gần như nguyên vẹn.

Các số hạng gián tiếp vẫn có thể biến mất. Nhưng gradient là tổng của các con đường, nên **chỉ cần còn đường trực tiếp là gradient vẫn về được**.

[click] Một chi tiết lịch sử: trong bài báo năm 1997, Hochreiter còn **chủ động cắt bỏ** các số hạng gián tiếp khi huấn luyện, chỉ giữ đường trực tiếp. Phải đến năm 2005, Graves mới huấn luyện bằng gradient đầy đủ.

### Slide 20 · So sánh trực quan: $\gamma^T$ (RNN) vs $\prod f_t$ (LSTM)  
*Người 3 · ~1 phút*

Đây là thanh trượt của bạn [tên người 1] ở slide 5, nhưng thêm đường màu xanh của LSTM.

**(Demo)** Đặt γ = 0.9 cho RNN, f = 0.99 cho LSTM, T = 100. RNN còn khoảng $3 \cdot 10^{-5}$, LSTM còn khoảng 0.37. Chênh nhau hơn **mười nghìn lần**.

Kéo f lên 1.0: đường xanh nằm ngang, gradient không suy giảm chút nào. Đây chính là Constant Error Carousel của bản 1997.

Khác biệt nằm ở chỗ γ của RNN phụ thuộc vào $W_h$ và tanh', rất khó giữ gần 1. Còn $f$ là một cổng mà mạng có thể học để đặt gần 1 khi cần nhớ.

### Slide 21 · Nối lại kiến thức CNN: "đường cao tốc" cho gradient  
*Người 3 · ~1.5 phút*

Slide này nối lại kiến thức CNN mà các bạn đã học.

Bên trái là ResNet. Khối residual tính $x_{l+1} = x_l + F(x_l)$. Đạo hàm là ma trận đơn vị $I$ cộng thêm một phần. Nhờ số hạng $I$, gradient luôn có một đường đi thẳng qua các lớp. Đó là lý do ResNet huấn luyện được mạng hơn 100 lớp.

Bên phải là LSTM: $c_t = f_t \odot c_{t-1} + \dots$. Đạo hàm theo đường trực tiếp là $\operatorname{diag}(f_t)$. Khi $f = 1$ thì chính là ma trận đơn vị.

[click] Hai mô hình dùng **cùng một ý tưởng**: dùng phép cộng để tạo "đường cao tốc" cho gradient. ResNet làm theo chiều sâu của mạng, LSTM làm theo chiều thời gian. LSTM ra đời trước ResNet gần 20 năm. Thêm nữa, Highway Network, tiền thân trực tiếp của ResNet, do chính nhóm của Schmidhuber đề xuất, và nó dùng đúng cơ chế cổng của LSTM.

### Slide 22 · Hệ quả thực tế từ toán  
*Người 3 · ~1 phút*

Từ phần toán vừa rồi, ta rút ra hai mẹo thực tế khi code.

Mẹo thứ nhất: **khởi tạo bias của forget gate bằng 1**. Nếu bias bằng 0 thì lúc đầu $f = \sigma(0) = 0.5$, nghĩa là mỗi bước mất một nửa trí nhớ, và gradient giảm theo $0.5^T$. Đặt bias bằng 1 thì $f$ khoảng 0.73, mạng có xu hướng nhớ ngay từ đầu. Trong PyTorch, các bias được xếp theo thứ tự i, f, g, o, nên phần forget nằm ở đoạn thứ hai, từ $h$ đến $2h$.

[click] Mẹo thứ hai: **vẫn phải dùng gradient clipping**. Đường trực tiếp chỉ giúp gradient không **biến mất**. Các số hạng gián tiếp ở slide 19 vẫn chứa ma trận $W$, nên gradient vẫn có thể **bùng nổ**. Clipping là một dòng code nhưng giúp tránh việc loss đột nhiên thành NaN.

### Slide 23 · Thí nghiệm: RNN vs LSTM trên cùng dữ liệu  
*Người 3 · ~2 phút*

Cuối cùng là bằng chứng thực nghiệm. Nhóm mình tự huấn luyện RNN và LSTM bằng PyTorch trên **cùng một bộ dữ liệu**, với cùng cấu hình.

Bài toán là Adding Problem, một bài kinh điển có từ bài báo năm 1997. Đầu vào là một chuỗi dài T; mỗi bước có một số ngẫu nhiên và một cờ đánh dấu. Có đúng hai vị trí được đánh dấu, và mô hình phải trả về tổng của hai số đó. Một vị trí luôn nằm ở nửa đầu chuỗi, nên mô hình phải nhớ qua khoảng T/2 bước. Nếu đoán bừa, luôn trả về 1, thì MSE khoảng 0.167, là đường nét đứt.

**(Bấm T = 10)** Với chuỗi ngắn, **cả hai đều học được**: loss của cả hai giảm xuống dưới đường đoán bừa. Test MSE của RNN là khoảng 0.0013, của LSTM là 0.0001. LSTM tốt hơn, nhưng RNN cũng làm được.

**(Bấm T = 100)** Với chuỗi dài, **RNN đứng yên ở đường đoán bừa** suốt 5000 bước: test MSE là 0.163, gần như đúng bằng 0.167 của việc đoán bừa, nghĩa là nó không học được gì. LSTM ban đầu cũng dò dẫm khoảng 2700 bước, rồi đột ngột "bắt được" quy luật, loss giảm mạnh và kết thúc ở test MSE 0.0044, tốt hơn RNN gần **40 lần**.

Bảng bên phải cho thấy cái giá phải trả: LSTM có 17,473 tham số so với 4,417 của RNN, tức gần gấp 4, và thời gian huấn luyện cũng lâu hơn.

Đây chính là điều mà công thức ở slide 19 dự đoán. Sang phần cuối, bạn [tên người 4] sẽ nói về cách LSTM được dùng trong thực tế.

---

## Phần 4 — LSTM trong thực tế + Assignment 7 (Người 4)

### Slide 24 · Biến thể: GRU (2014)  
*Người 4 · ~1.5 phút*

Cảm ơn [tên người 3]. Phần cuối nói về LSTM trong thực tế, bắt đầu từ biến thể nổi tiếng nhất: **GRU**, do Cho và cộng sự đề xuất năm 2014.

Bên trái là LSTM: ba cổng, một cell state, bốn khối trọng số.

Bên phải là GRU, chỉ có **hai cổng**: update gate $z$ và reset gate $r$, và **không có cell state riêng**, chỉ có $h$.

Phương trình quan trọng nhất là dòng cuối: $h_t = (1 - z_t) h_{t-1} + z_t \tilde h_t$. So với LSTM, $1 - z$ đóng vai trò forget gate, còn $z$ đóng vai trò input gate.

[click] Nghĩa là GRU **gộp** forget và input gate thành một: quên bao nhiêu thì ghi bấy nhiêu. Vẫn là phép cộng, nên vẫn có đường cao tốc cho gradient. GRU có ít hơn khoảng 25% tham số và trên nhiều bài toán cho kết quả tương đương LSTM. Trong PyTorch, chỉ cần đổi `nn.LSTM` thành `nn.GRU`.

### Slide 25 · Stacked & Bidirectional LSTM  
*Người 4 · ~1.5 phút*

Hai cách mở rộng hay dùng nhất.

**Stacked LSTM**: xếp nhiều lớp LSTM chồng lên nhau. Chuỗi output $h$ của lớp dưới là chuỗi input của lớp trên. Giống CNN có nhiều lớp, lớp sau học được đặc trưng trừu tượng hơn.

**Bidirectional LSTM**: chạy một LSTM từ trái sang phải và một LSTM từ phải sang trái, rồi ghép hai hidden state lại. Như vậy mỗi bước được nhìn cả quá khứ lẫn tương lai. Cách này rất hữu ích cho phân loại văn bản hay gán nhãn từ loại.

[click] Lưu ý: **không** dùng bidirectional cho bài toán dự báo tương lai, ví dụ dự báo giá cổ phiếu, vì mô hình sẽ nhìn thấy dữ liệu tương lai, tức là nhìn trộm đáp án.

Bên phải là code PyTorch. Chỉ cần hai tham số `num_layers` và `bidirectional`. Chú ý **shape của output**: `output` có chiều cuối là 2h vì ghép hai chiều; `h_n` có số phần tử ở chiều đầu bằng số lớp nhân số chiều. Đây là chỗ các bạn hay bị lỗi shape nhất.

### Slide 26 · Ứng dụng & giới hạn  
*Người 4 · ~1.5 phút*

LSTM được dùng ở đâu? Các bạn có thể chia theo kiểu đầu vào và đầu ra. **Many-to-one**: cả chuỗi cho ra một nhãn, ví dụ phân loại cảm xúc. **Many-to-many**: mỗi bước một nhãn, ví dụ nhận dạng giọng nói. **Seq2seq**: một LSTM encoder đọc câu nguồn, một LSTM decoder sinh câu đích; đây là kiến trúc Google Translate dùng năm 2016. Ngoài ra còn rất nhiều ứng dụng với chuỗi thời gian.

Nhưng LSTM cũng có giới hạn. Lớn nhất là nó tính **tuần tự**: muốn tính bước t thì phải xong bước t−1, nên không tận dụng được GPU song song theo thời gian. Với chuỗi rất dài, nó vẫn gặp khó khăn.

[click] Đó là lý do Attention và sau đó là Transformer ra đời năm 2017: bỏ hẳn cơ chế hồi quy, cho mọi bước nhìn nhau trực tiếp. Đây là chủ đề cho một buổi khác. Gia phả của chúng ta giờ đã đầy đủ: từ MLP, qua CNN và RNN, đến LSTM, GRU, rồi Transformer.

### Slide 27 · Hướng dẫn Assignment 7: khung LSTM với PyTorch  
*Người 4 · ~2.5 phút*

Slide này là khung chung để các bạn chuẩn bị cho Assignment 7. Thầy chưa giao đề cụ thể nên mình chỉ đưa ra bộ khung dùng được cho hầu hết bài toán.

[click] Mô hình chỉ cần hai thành phần: một lớp `nn.LSTM` và một lớp `Linear` ở cuối.

[click] Chú ý `batch_first=True`. Mặc định PyTorch nhận đầu vào theo thứ tự (seq_len, batch, feature). Hầu hết mọi người chuẩn bị dữ liệu theo (batch, seq_len, feature), nên cần bật tham số này.

[click] Trong forward, `nn.LSTM` trả về hai thứ: `output` chứa hidden ở **mọi bước**, và cặp `(h_n, c_n)` chứa trạng thái ở **bước cuối**. Với bài phân loại many-to-one, ta lấy `h_n[-1]`, tức là hidden cuối của lớp trên cùng, rồi đưa vào Linear.

[click] Vòng train giống hệt CNN mà các bạn đã làm: forward, tính loss, zero_grad, backward, step. [click] Chỉ thêm đúng một dòng: **clip gradient**, như bạn [tên người 3] đã giải thích.

Bên phải là ba lỗi hay gặp nhất: sai thứ tự chiều do quên batch_first, lấy nhầm bước padding, và loss thành NaN. Lời khuyên cuối: luôn train thêm một baseline RNN để so sánh, giống thí nghiệm ở slide 23. Đó là cách tốt nhất để thấy LSTM thực sự giúp được bao nhiêu.

### Slide 28 · Tổng kết  
*Người 4 · ~2 phút*

Tóm lại bài hôm nay bằng ba ý.

Một: LSTM thêm vào RNN một **cell state**, là băng chuyền bộ nhớ dài hạn.
Hai: **ba cổng** forget, input, output, đều dùng sigmoid, quyết định quên bao nhiêu, ghi bao nhiêu, đọc ra bao nhiêu.
Ba: nhờ **phép cộng** trên cell state, gradient có đường đi trực tiếp chỉ qua $f_t$, nên không bị biến mất như RNN.

Bây giờ là ba câu hỏi nhanh để kiểm tra. Mời các bạn trả lời.

Câu 1: nếu forget gate luôn bằng 0 thì sao? [click] Mất toàn bộ trí nhớ dài hạn; cell state chỉ còn thông tin của bước hiện tại.

Câu 2: bản LSTM năm 1997 thiếu cổng nào? [click] Forget gate.

Câu 3: tính số tham số. [click] $4 \cdot (100 \cdot 150 + 100) = 60{,}400$.

---

## Q&A (Cả nhóm)

### Slide 29 · Cảm ơn thầy và các bạn đã lắng nghe!  
*Cả nhóm · ~2 phút*

Phần trình bày của nhóm mình đến đây là kết thúc. Cảm ơn thầy và các bạn đã lắng nghe. Nhóm mình xin nhận câu hỏi.

*(Gợi ý chuẩn bị trước một số câu hỏi có thể gặp:)*
- *Vì sao không dùng ReLU cho các cổng?* Vì cổng cần giá trị trong (0,1) để đóng vai trò van; ReLU không bị chặn trên.
- *LSTM có hoàn toàn hết vanishing gradient không?* Không. Nó chỉ tạo một đường mà mạng **có thể học** để giữ gradient; nếu f nhỏ thì gradient vẫn suy giảm.
- *Khi nào dùng GRU, khi nào dùng LSTM?* GRU nhẹ hơn, hợp với dữ liệu ít; LSTM linh hoạt hơn một chút. Thực tế nên thử cả hai.

---

**Tổng thời lượng dự kiến:** ~45 phút
