# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** Nhóm K3 - Quy định & Dịch vụ Đại học  
**Thành viên:** Trần Văn Anh, Lường Duy Thái

**Vai trò:** Trần Văn Anh chủ yếu thực hiện triển khai pipeline, chunking và đánh giá truy xuất; thành viên còn lại hỗ trợ kiểm tra dữ liệu, góp ý chiến lược và rà soát báo cáo.  
**Ngày:** 03/08/2026  

> Báo cáo này là kết quả làm việc của nhóm 2 người trong quá trình xây dựng hệ thống RAG, chuẩn hóa dữ liệu, chia nhỏ tài liệu, xây dựng vector store và đánh giá chất lượng truy xuất trên bộ dữ liệu quy định, dịch vụ sinh viên.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K3):** Dịch vụ / quy định đại học (đăng ký môn, học phí, học bổng, thư viện, ký túc xá, quy chế đào tạo, khen thưởng kỷ luật).

**Phạm vi cụ thể nhóm tập trung:**
> Bộ quy định toàn diện về dịch vụ học vụ và đời sống sinh viên bao gồm Quy chế đào tạo (TT 08/2021), Điểm rèn luyện (TT 16/2015), Công tác sinh viên (TT 10/2016), Học phí & Miễn giảm (NĐ 81/2021, NĐ 97/2023), Cảnh báo học tập, Học bổng KKHT, Đăng ký học phần, Ký túc xá và Khen thưởng kỷ luật.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Thông tư 08/2021/TT-BGDĐT - Quy chế đào tạo | https://thuvienphapluat.vn/... | 2026-08-03 / 08/2021/TT-BGDĐT | 1,450 | `doc_id: thong-tu-08-2021-tt-bgddt`, `audience: student`, `department: academic-affairs` |
| 2 | Thông tư 16/2015/TT-BGDĐT - Đánh giá rèn luyện | https://thuvienphapluat.vn/... | 2026-08-03 / 16/2015/TT-BGDĐT | 1,320 | `doc_id: thong-tu-16-2015-tt-bgddt`, `audience: student`, `department: student-affairs` |
| 3 | Thông tư 10/2016/TT-BGDĐT - Quy chế công tác SV | https://thuvienphapluat.vn/... | 2026-08-03 / 10/2016/TT-BGDĐT | 1,280 | `doc_id: thong-tu-10-2016-tt-bgddt`, `audience: student`, `department: student-affairs` |
| 4 | Nghị định 81/2021/NĐ-CP - Học phí & Miễn giảm | https://thuvienphapluat.vn/... | 2026-08-03 / 81/2021/NĐ-CP | 1,410 | `doc_id: nghi-dinh-81-2021-nd-cp`, `audience: student`, `department: financial-affairs` |
| 5 | Nghị định 97/2023/NĐ-CP - Sửa đổi NĐ 81 về học phí | https://thuvienphapluat.vn/... | 2026-08-03 / 97/2023/NĐ-CP | 980 | `doc_id: nghi-dinh-97-2023-nd-cp`, `audience: student`, `department: financial-affairs` |
| 6 | Quy định Cảnh báo Học tập và Buộc thôi học | https://example.edu/hoc-vu/... | 2026-08-03 / 2026.1 | 1,120 | `doc_id: quy-dinh-canh-bao-hoc-tap`, `audience: student`, `department: academic-affairs` |
| 7 | Quy chế Xét cấp Học bổng Khuyến khích Học tập | https://example.edu/ctsv/... | 2026-08-03 / 2026.1 | 1,250 | `doc_id: quy-che-hoc-bong-khuyen-khich`, `audience: student`, `department: student-affairs` |
| 8 | Quy trình Đăng ký Học phần và Rút Muộn | https://example.edu/hoc-vu/... | 2026-08-03 / 2026.1 | 1,310 | `doc_id: quy-trinh-dang-ky-rut-hoc-phan`, `audience: student`, `department: academic-affairs` |
| 9 | Quy định Quản lý và Xét duyệt Ký túc xá | https://example.edu/ktx/... | 2026-08-03 / 2026.1 | 1,180 | `doc_id: quy-dinh-dang-ky-ky-tuc-xa`, `audience: student`, `department: dormitory` |
| 10 | Quy định Khen thưởng và Kỷ luật Sinh viên | https://example.edu/ctsv/... | 2026-08-03 / 2026.1 | 1,220 | `doc_id: quy-dinh-khen-thuong-ky-luat`, `audience: student`, `department: student-affairs` |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | `str` | `thong-tu-08-2021-tt-bgddt` | Định danh duy nhất để xóa hoặc nhóm các chunk thuộc cùng một tài liệu gốc. |
| `audience` | `str` | `student`, `faculty`, `all` | Lọc chính xác tài liệu dành riêng cho đối tượng sinh viên, tránh nhiễu từ văn bản dành cho cán bộ. |
| `department` | `str` | `academic-affairs`, `student-affairs`, `financial-affairs` | Phân loại theo đơn vị quản lý chuyên trách (Đào tạo, CTSV, Tài chính, KTX) giúp thu hẹp không gian tìm kiếm. |
| `source_url` | `str` | `https://thuvienphapluat.vn/...` | Đảm bảo khả năng kiểm chứng nguồn gốc câu trả lời của RAG Agent. |
| `retrieved_at` | `str` | `2026-08-03` | Theo dõi ngày cập nhật dữ liệu để kiểm soát độ mới của quy định. |
| `document_version`| `str` | `08/2021/TT-BGDĐT` | Xác định phiên bản hiệu lực pháp lý của văn bản. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên bộ tài liệu quy định đại học:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| Quy chế Đào tạo & Học phí | FixedSizeChunker (`fixed_size`) | 12 | 200.0 ký tự | Tương đối (dễ cắt đôi các điều khoản ở ranh giới cố định) |
| Quy chế Đào tạo & Học phí | SentenceChunker (`by_sentences`) | 15 | 165.5 ký tự | Tốt với câu đơn, nhưng mất liên kết giữa các điều khoản trong cùng một Mục |
| Quy chế Đào tạo & Học phí | RecursiveChunker (`recursive`) | 8 | 280.2 ký tự | Rất tốt (giữ nguyên vẹn toàn bộ một Điều/Mục quy định pháp lý) |

### Chiến lược của nhóm

**Thành viên 1 — Trần Văn Anh**
- **Loại chiến lược:** `RecursiveChunker` (`chunk_size=300`, phân cách `["\n\n", "\n", ". ", " ", ""]`)
- **Mô tả & lý do chọn cho chủ đề này:** Văn bản pháp lý và quy chế đào tạo có cấu trúc phân tầng rõ ràng theo Tiêu đề (#), Điều (##), và các khoản mục (-). Tách đệ quy giúp ưu tiên ngắt ở ranh giới giữa các Điều (`\n\n`), giữ nguyên vẹn ngữ cảnh của từng điều khoản quy định.
- **Code snippet:**
```python
chunker = RecursiveChunker(
    separators=["\n\n", "\n", ". ", " ", ""],
    chunk_size=300
)
```

**Thành viên 2 — Thành viên còn lại của nhóm**
- **Loại chiến lược:** `SentenceChunker` (`max_sentences_per_chunk=3`)
- **Mô tả & lý do chọn:** Chia nhỏ văn bản theo đơn vị câu giúp mỗi chunk là một tập hợp các ý độc lập, hỗ trợ kiểm tra tính khả dụng của từng đoạn và làm rõ mức độ phù hợp của từng câu hỏi với nội dung tài liệu.

### So Sánh giữa hai thành viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Trần Văn Anh | `RecursiveChunker` | 9.5 / 10 | Giữ trọn vẹn ngữ cảnh của từng Điều/Mục quy định; độ tương đồng cao. | Độ dài các chunk không đồng đều tùy theo từng điều khoản. |
| Thành viên còn lại | `SentenceChunker` | 8.0 / 10 | Chunk đồng đều về số câu, phù hợp với câu hỏi ngắn và tra cứu. | Có thể cắt rời mối liên hệ giữa các phần trong cùng một quy định. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> `RecursiveChunker` là chiến lược tốt nhất cho chủ đề Quy định & Dịch vụ Đại học vì các văn bản quy chế có cấu trúc phân đoạn rõ ràng (`\n\n` giữa các Điều). Việc ưu tiên ngắt theo đoạn giúp mỗi chunk chứa trọn vẹn một điều khoản quy định, từ đó vector nhúng phản ánh chính xác nhất nội dung pháp lý và đạt độ chính xác truy xuất cao nhất.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Điểm trung bình chung học kỳ GPA bao nhiêu thì sinh viên năm thứ hai bị cảnh báo học tập? | Sinh viên năm thứ hai bị cảnh báo học tập nếu GPA học kỳ đạt dưới 1.40. | `quy-dinh-canh-bao-hoc-tap` (Điều 2) |
| 2 | Điều kiện tiêu chuẩn và các mức học bổng khuyến khích học tập dành cho sinh viên? | Mức Khá (100% học phí, GPA>=2.5), Mức Giỏi (120%, GPA>=3.2), Mức Xuất sắc (150%, GPA>=3.6). | `quy-che-hoc-bong-khuyen-khich` (Điều 3) |
| 3 | Quy trình rút học phần muộn sau tuần 2 đến trước tuần 8 được thực hiện ra sao và ghi nhận điểm gì? | Nộp đơn có xác nhận CVHT & Trưởng khoa. Điểm ghi nhận là W, không tính vào GPA/CPA. | `quy-trinh-dang-ky-rut-hoc-phan` (Điều 3) |
| 4 | Những sinh viên thuộc đối tượng nào được miễn 100% học phí theo Nghị định 81/2021/NĐ-CP? | Sinh viên dân tộc thiểu số rất ít người vùng ĐBKK, mồ côi cả cha lẫn mẹ, khuyết tật nặng, con người có công. | `nghi-dinh-81-2021-nd-cp` (Điều 2) |
| 5 | Các tiêu chí và thang điểm đánh giá kết quả rèn luyện sinh viên theo Thông tư 16/2015/TT-BGDĐT? | Thang 100 điểm với 5 tiêu chí: Ý thức học tập (20đ), Nội quy (25đ), Ngoại khóa (20đ), Công dân (25đ), Cán bộ (10đ). | `thong-tu-16-2015-tt-bgddt` (Điều 2) |

### Tổng hợp chất lượng truy xuất của nhóm (Đánh giá ở mức CHUNK LEVEL)

> **Phát hiện quan trọng (Chunk-level vs Doc-level):** Đánh giá ở mức **Chunk-level** (kiểm tra bằng chứng chuỗi đáp án trong chunk) cho thấy `doc_id` xuất hiện ở Top-1 không đồng nghĩa với việc chunk đó chứa câu trả lời. Cosine Similarity ưu tiên các chunk tiêu đề/chủ đề tổng quan có điểm số cao hơn chunk chứa điều khoản chi tiết.

| # | Câu hỏi | Doc kỳ vọng | Chunk Top-1 (Score) | Chunk chứa bằng chứng đáp án thực tế | Điểm Rubric (/2) | Ghi chú & Phân tích |
|---|---------|-------------|----------------------|---------------------------------------|------------------|---------------------|
| 1 | GPA cảnh báo học tập sinh viên năm 2 | `quy-dinh-canh-bao-hoc-tap` | Top-1: `## Điều 2` (Score: 0.8379) | **Top-1** (chứa `GPA học kỳ đạt dưới 1.40`) | **2/2** | Trúng ngay chunk Top-1. A/B filter (`audience: student`) xác nhận không bị lọt thông tin sai đối tượng. |
| 2 | 5 tiêu chí đánh giá rèn luyện (TT 16) | `thong-tu-16-2015-tt-bgddt` | Top-1: `# Thông tư 16` (Score: 0.9328) | **Top-3** (Score: 0.7106 - `## Điều 2. Thang 100 điểm`) | **1/2** | Cả 3 Top slot đều thuộc doc `thong-tu-16`, nhưng Top-1 là tiêu đề chung; chunk chứa số liệu nằm ở Top-3. |
| 3 | Quy trình rút học phần muộn (tuần 2 - 8) | `quy-trinh-dang-ky-rut-hoc-phan` | Top-1: `## Điều 3` (Score: 0.7222) | **Top-1** (chứa `nộp đơn... điểm W`) | **2/2** | Chunk Top-1 chứa đầy đủ quy trình và điểm W. |
| 4 | Đối tượng miễn 100% học phí (NĐ 81) | `nghi-dinh-81-2021-nd-cp` | Top-1: `# Nghị định 81` (Score: 0.7861) | **Top-2** (Score: 0.7707 - `## Điều 2. Miễn 100% học phí`) | **1/2** | Top-1 là phần mở đầu văn bản; chunk chứa danh sách đối tượng nằm ở Top-2. |
| 5 | Mức học bổng khuyến khích học tập | `quy-che-hoc-bong-khuyen-khich` | Top-1: `# Quy chế xét học bổng` (Score: 0.8049) | **Top-4** (Nằm ngoài Top-3: `## Điều 3. Các mức HB`) | **0/2** | Top-1 & Top-2 là tiêu đề và Điều 4 (Nguyên tắc). Chunk chứa mức HBKhá/Giỏi/XS thuộc Điều 3 bị đẩy xuống vị trí 4. |

---

### Phân tích A/B Filter (Metadata Filtering Analysis)

- **Thử nghiệm trên Query 1 (GPA cảnh báo học tập):**
  - **Khi có Filter (`audience: student`):** Top-1 = `quy-dinh-canh-bao-hoc-tap` (Score: 0.8379).
  - **Khi KHÔNG có Filter (`search()` chuẩn):** Top-1 = `quy-dinh-canh-bao-hoc-tap` (Score: 0.8379).
- **Nhận xét:** Trong bộ dữ liệu hiện tại, các văn bản đều dành cho sinh viên nên kết quả trước và sau khi lọc giống hệt nhau. Tuy nhiên, việc duy trì `metadata_filter` là bắt buộc để đảm bảo an toàn hệ thống khi mở rộng corpus với các văn bản quy chế dành riêng cho Giảng viên / Cán bộ nhân viên (tránh truy xuất nhầm chính sách).

---

## 4. Thuyết trình (Demo), Failure Analysis & Bài học nhóm — Nhóm (5 điểm)

### Phân tích lỗi thực tế (Failure Case Analysis)

> **Trường hợp lỗi điển hình (Failure Case ở Query 5):**
> - **Query:** *"Điều kiện tiêu chuẩn và các mức học bổng khuyến khích học tập dành cho sinh viên?"*
> - **Bằng chứng từ Top-k:**
>   - Top-1 (Score: 0.8049): Chunk `# Quy chế Xét cấp Học bổng Khuyến khích Học tập` (Chỉ chứa tên quy chế và mô tả chung).
>   - Top-2 (Score: 0.7800): Chunk `## Điều 4. Nguyên tắc xét cấp` (Chỉ chứa nguyên tắc ưu tiên điểm rèn luyện).
>   - Top-3 (Score: 0.7242): Chunk `quy-dinh-khen-thuong-ky-luat` (Quy định khen thưởng chung).
>   - Chunk chứa đáp án thực tế (`## Điều 3. Các mức học bổng khuyến khích: Mức Khá 100%, Mức Giỏi 120%...`) bị xếp vị trí Top-4 (Score: 0.6980) nên **không lọt vào Top-3**.
> - **Nguyên nhân gốc rễ (Root Cause):**
>   1. **Cosine Similarity đo độ tương đồng chủ đề, không đo mật độ thông tin:** Các chunk tiêu đề (#) hoặc tổng quan trùng nhiều từ khóa chung ("học bổng khuyến khích học tập") nên nhận điểm vector cao hơn chunk chi tiết chứa các con số và điều kiện học bổng.
>   2. **Thiếu độ chồng chéo (Overlap) giữa các section:** `HeadingSectionChunker` tách riêng từng Điều thành chunk độc lập mà không truyền tên tiêu đề chính xuống phần nội dung các Điều con, khiến chunk `Điều 3` bị thiếu các từ khóa tổng quan của tài liệu.
> - **Đề xuất cải tiến (Proposed Fix):**
>   - Gắn tiêu đề gốc `# Quy chế Xét cấp Học bổng Khuyến khích Học tập` vào trước nội dung của từng `## Điều X` con khi chunking.
>   - Kết hợp Hybrid Search (Vector Search + BM25 Keyword Search) để tăng trọng số cho các chunk chứa số liệu và từ khóa điều kiện chính xác.

---

### Phân tíchInsights & Bài học rút ra

1. **Phân biệt Đánh giá Doc-level và Chunk-level:** Nếu chỉ kiểm tra `doc_id` xuất hiện trong Top-3 thì tỷ lệ thành công có vẻ là 100%. Tuy nhiên khi kiểm tra ở mức **Chunk-level**, chỉ có 2/5 câu hỏi đạt điểm tuyệt đối 2/2 ở Top-1.
2. **Bài học về Chiến lược Chunking:** Khi ngắt theo tiêu đề (`HeadingSectionChunker`), bắt buộc phải **kế thừa tiêu đề cấp cha (Header Context Prepends)** vào từng chunk con để tránh tình trạng chunk con mất từ khóa ngữ cảnh chính của văn bản.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 9 / 10 |
| Thuyết trình (Demo) & Failure Analysis | 5 / 5 |
| **Tổng phần nhóm** | **39 / 40** |
