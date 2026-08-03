# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Trần Anh Văn  
**Mã sinh viên:** 2A202601513  
**Nhóm:** Nhóm K3 - Quy định & Dịch vụ Đại học  
**Ngày:** 03/08/2026  

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao (gần 1.0) nghĩa là hai góc của vector biểu diễn văn bản trùng khớp với nhau về hướng trong không gian vector đa chiều, thể hiện hai câu văn/đoạn văn có mức độ tương đồng ngữ nghĩa cao bất kể độ dài ngắn của chúng.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Sinh viên đăng ký học phần trên hệ thống quản lý đào tạo trực tuyến."
- Câu B: "Sinh viên thực hiện đăng ký môn học qua cổng thông tin học vụ của nhà trường."
- Tại sao tương đồng: Cả hai câu cùng diễn đạt cùng một hành động học vụ (đăng ký môn học/học phần trực tuyến) với từ vựng đồng nghĩa.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Sinh viên bị cảnh báo kết quả học tập nếu GPA dưới 1.40."
- Câu B: "Thư viện mở cửa phục vụ sinh viên mượn trả sách từ 7h30 sáng đến 21h00 tối."
- Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn độc lập (cảnh báo học tập vs dịch vụ thư viện), không có sự liên quan về ngữ nghĩa.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Độ tương tự cosine chỉ quan tâm đến hướng (góc) của vector mà không bị ảnh hưởng bởi độ dài (mô-đun) của vector. Điều này giúp so sánh chính xác mức độ tương đồng ngữ nghĩa giữa các văn bản có độ dài khác nhau, tránh việc hai văn bản cùng chủ đề nhưng độ dài chênh lệch bị khoảng cách Euclid tính thành xa nhau.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*  
> $\text{Số lượng chunk} = \left\lceil \frac{10000 - 50}{500 - 50} \right\rceil = \left\lceil \frac{9950}{450} \right\rceil = \lceil 22.11 \rceil = 23$  
> *Đáp án:* 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Nếu overlap = 100: $\text{Số lượng chunk} = \left\lceil \frac{10000 - 100}{500 - 100} \right\rceil = \left\lceil \frac{9900}{400} \right\rceil = \lceil 24.75 \rceil = 25$ chunks.  
> Tăng độ chồng chéo giúp giữ lại ngữ cảnh liên tục ở ranh giới giữa các chunk, giảm nguy cơ mất mát thông tin quan trọng hoặc cắt đứt các câu văn bị chia đôi ở ranh giới cắt.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Sử dụng biểu thức chính quy `re.split(r'(?<=[.!?])\s+|(?<=\.)\n', text)` để nhận diện chính xác ranh giới kết thúc câu. Sau đó lọc các câu trống và gom các câu thành từng nhóm tối đa `max_sentences_per_chunk` câu, nối lại bằng dấu cách và loại bỏ khoảng trắng dư thừa.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Áp dụng thuật toán chia đệ quy ưu tiên từ các dấu phân cách lớn đến nhỏ (`["\n\n", "\n", ". ", " ", ""]`). Khi đoạn văn hiện tại vượt quá `chunk_size`, hàm tiến hành tách theo dấu phân cách ưu tiên cao nhất, gom các mảnh nhỏ lại cho đến khi đạt hạn mức `chunk_size`. Nếu một mảnh nhỏ vẫn vượt quá `chunk_size`, tiếp tục gọi đệ quy `_split` với danh sách dấu phân cách còn lại.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Lưu trữ văn bản dưới dạng danh sách `list[dict]` gồm `id`, `content`, `metadata` và `embedding` được tạo từ `self._embedding_fn`. Khi thực hiện `search`, nhúng vector cho câu truy vấn (query) rồi tính tích vô hướng (dot product) hoặc cosine similarity với toàn bộ embedding đã lưu, sắp xếp giảm dần theo điểm số `score` và trả về `top_k` kết quả đầu tiên.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> `search_with_filter` tiến hành lọc tiền xử lý (pre-filtering) trên tập record trong bộ nhớ sao cho tất cả các cặp khóa-giá trị trong `metadata_filter` đều trùng khớp với metadata của chunk, sau đó mới tính tương đồng vector. `delete_document` thực hiện duyệt tập record và loại bỏ tất cả các chunk có `doc_id` hoặc `metadata['doc_id']` khớp với `doc_id` cần xóa, trả về `True` nếu có ít nhất 1 chunk bị loại bỏ.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Gọi `EmbeddingStore.search` để lấy `top_k` chunk văn bản liên quan nhất. Nối nội dung các chunk này thành đoạn văn ngữ cảnh `context_str` qua phân cách `\n---\n`, sau đó tạo prompt theo mẫu: "Answer the question based ONLY on the following context..." và chuyển cho `llm_fn` xử lý.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
============================= 42 passed in 0.13s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Điểm trung bình chung học tập GPA được tính theo thang điểm 4. | Điểm GPA và CPA tích lũy được quy đổi từ thang điểm chữ sang thang điểm 4.0. | cao | 0.803 | Đúng |
| 2 | Sinh viên có thể nộp đơn xin hủy hoặc rút bớt học phần đã đăng ký. | Thực hiện thủ tục rút học phần muộn và ghi nhận điểm W trên hệ thống. | cao | 0.457 | Đúng |
| 3 | Sinh viên vi phạm kỷ luật bị xử lý theo hình thức khiển trách hoặc cảnh cáo. | Thư viện mở cửa phục vụ mượn trả sách từ 7h30 đến 21h00 hàng ngày. | thấp | 0.032 | Đúng |
| 4 | Miễn giảm 100% học phí đối với sinh viên thuộc hộ nghèo và đối tượng chính sách. | Quy định giờ đóng cửa Ký túc xá vào lúc 23 giờ đêm. | thấp | 0.165 | Đúng |
| 5 | Đăng ký ở ký túc xá cho sinh viên năm thứ nhất. | Đăng ký học phần tín chỉ cho học kỳ đầu khóa. | trung bình | 0.683 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp 5 có từ chung "Đăng ký" và "sinh viên" đạt điểm tương đồng khá cao (0.683) do mô hình nhúng phát hiện cấu trúc hành động tương đồng ("Đăng ký... cho sinh viên..."). Điều này phản ánh mô hình `sentence-transformers` biểu diễn ngữ nghĩa đồng thời dựa trên cả cú pháp câu và ngữ cảnh chủ đề.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân với `HeadingSectionChunker` (`max_chunk_size=400`) và `LocalEmbedder` (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`).

> **Kiểm chứng ở mức CHUNK LEVEL:** Kiểm tra xem chuỗi bằng chứng đáp án có nằm chính xác trong chunk truy xuất được hay không (thay vì chỉ kiểm tra tên file `doc_id`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có bằng chứng đáp án trong Top-3? | Vị trí Chunk chứa đáp án | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------------------------|--------------------------|------------------------|
| 1 | GPA bao nhiêu sinh viên năm 2 bị cảnh báo học tập? | `## Điều 2. Các điều kiện bị cảnh báo học tập: GPA học kỳ dưới 1.40...` | 0.838 | Có | **Top-1** | GPA dưới 1.40 đối với SV năm 2 (doc: quy-dinh-canh-bao-hoc-tap). |
| 2 | Các tiêu chí và thang điểm đánh giá rèn luyện (TT 16)? | `# Thông tư 16/2015/TT-BGDĐT - Quy định đánh giá kết quả rèn luyện...` | 0.933 | Có | **Top-3** (Score 0.711 - `## Điều 2. Thang 100 điểm`) | Đánh giá theo thang 100 điểm với 5 tiêu chí (doc: thong-tu-16-2015-tt-bgddt). |
| 3 | Quy trình rút học phần muộn (tuần 2 - tuần 8)? | `## Điều 3. Quy trình Rút học phần muộn: Nộp đơn có xác nhận CVHT, điểm W...` | 0.722 | Có | **Top-1** | Nộp đơn từ tuần 2-8, điểm W, không hoàn tiền (doc: quy-trinh-dang-ky-rut-hoc-phan). |
| 4 | Đối tượng được miễn 100% học phí (NĐ 81/2021)? | `# Nghị định 81/2021/NĐ-CP - Quy định về học phí và chính sách miễn giảm...` | 0.786 | Có | **Top-2** (Score 0.771 - `## Điều 2. Đối tượng miễn 100%`) | Miễn 100% cho SV mồ côi, khuyết tật, dân tộc thiểu số ĐBKK (doc: nghi-dinh-81-2021-nd-cp). |
| 5 | Điều kiện tiêu chuẩn và các mức học bổng khuyến khích? | `# Quy chế Xét cấp Học bổng Khuyến khích Học tập...` | 0.805 | Không (Nằm Top-4) | **Top-4** (Score 0.698 - `## Điều 3. Mức HBKhá/Giỏi/XS`) | Trích xuất từ ngữ cảnh tổng quan nguyên tắc học bổng (doc: quy-che-hoc-bong-khuyen-khich). |

**Bao nhiêu câu hỏi trả về chunk chứa đáp án trực tiếp trong top-3?** 4 / 5

**Bài học đắt giá nhất rút ra từ kiểm thử Chunk-level & Failure Analysis:**
> Đánh giá bằng `doc_id` cho cảm giác giả tạo rằng 5/5 câu đều thành công vì đúng file xuất hiện ở Top-1. Tuy nhiên khi kiểm tra chuỗi bằng chứng đáp án ở mức **Chunk-level**, câu 5 bị trượt khỏi Top-3 do chunk tiêu đề `# Quy chế` có điểm Cosine cao hơn chunk nội dung `## Điều 3`. Bài học rút ra là: Cosine Similarity đo độ tương đồng chủ đề chung chứ không đo mật độ thông tin chi tiết; cần kế thừa tiêu đề cấp cha vào từng chunk con để tránh mất mát từ khóa tổng quan.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 9 / 10 |
| **Tổng phần cá nhân** | **59 / 60** |
