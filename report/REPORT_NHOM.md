# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** Nhóm K3 - Quy định & Dịch vụ Đại học  
**Thành viên:** Trần Anh Văn (2A202601513) và các thành viên nhóm K3  
**Ngày:** 03/08/2026  

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

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

### Chiến lược của từng thành viên

**Thành viên 1 — Trần Anh Văn**
- **Loại chiến lược:** `RecursiveChunker` (`chunk_size=300`, phân cách `["\n\n", "\n", ". ", " ", ""]`)
- **Mô tả & lý do chọn cho chủ đề này:** Văn bản pháp lý và quy chế đào tạo có cấu trúc phân tầng rõ ràng theo Tiêu đề (#), Điều (##), và các khoản mục (-). Tách đệ quy giúp ưu tiên ngắt ở ranh giới giữa các Điều (`\n\n`), giữ nguyên vẹn ngữ cảnh của từng điều khoản quy định.
- **Code snippet:**
```python
chunker = RecursiveChunker(
    separators=["\n\n", "\n", ". ", " ", ""],
    chunk_size=300
)
```

**Thành viên 2 — Thành viên Nhóm K3 (Thử nghiệm SentenceChunker)**
- **Loại chiến lược:** `SentenceChunker` (`max_sentences_per_chunk=3`)
- **Mô tả & lý do chọn:** Chia nhỏ văn bản theo đơn vị câu giúp mỗi chunk là một tập hợp các ý độc lập, tránh được việc tạo ra chunk quá dài gây loãng vector embedding.

**Thành viên 3 — Thành viên Nhóm K3 (Thử nghiệm FixedSizeChunker)**
- **Loại chiến lược:** `FixedSizeChunker` (`chunk_size=250`, `overlap=40`)
- **Mô tả & lý do chọn:** Chiến lược đường cơ sở cố định với độ chồng chéo 40 ký tự giúp tránh mất mát ngữ cảnh tại điểm nối giữa hai chunk kề nhau.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Trần Anh Văn | `RecursiveChunker` | 9.5 / 10 | Giữ trọn vẹn ngữ cảnh của từng Điều/Mục quy định; điểm tương đồng cao. | Độ dài các chunk không đồng đều tùy theo độ dài từng điều khoản. |
| Thành viên 2 | `SentenceChunker` | 8.0 / 10 | Các chunk đồng đều về số câu, thích hợp cho các câu hỏi tra cứu ngắn. | Đôi khi cắt rời bảng điểm/tiêu chí đánh giá gồm nhiều mục nhỏ. |
| Thành viên 3 | `FixedSizeChunker` | 7.5 / 10 | Đơn giản, tốc độ xử lý nhanh và kích thước chunk cố định. | Có thể cắt ngang giữa câu hoặc điều khoản làm giảm ngữ nghĩa. |

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

### Tổng hợp chất lượng truy xuất của nhóm

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | GPA cảnh báo học tập sinh viên năm 2 | `RecursiveChunker` + Filter (`audience: student`) | Có (Top-1) | Lọc theo `audience: student` loại bỏ các quy chế của giảng viên/nhân viên. |
| 2 | Mức học bổng khuyến khích học tập | `RecursiveChunker` + Filter (`department: student-affairs`) | Có (Top-1) | Truy xuất chính xác Điều 3 của Quy chế HBKKHT. |
| 3 | Rút học phần muộn (tuần 2 - tuần 8) | `RecursiveChunker` + Filter (`department: academic-affairs`) | Có (Top-1) | Trả về trọn vẹn Điều 3 về quy trình và điểm ghi nhận W. |
| 4 | Miễn 100% học phí (NĐ 81/2021) | `RecursiveChunker` + Filter (`department: financial-affairs`) | Có (Top-1) | Trả về danh sách 4 nhóm đối tượng ưu tiên chính sách. |
| 5 | Tiêu chí đánh giá rèn luyện (TT 16) | `RecursiveChunker` + Filter (`audience: student`) | Có (Top-1) | Trả về bảng 5 tiêu chí chấm điểm rèn luyện thang 100. |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Metadata filtering có vai trò cực kỳ quan trọng. Đặc biệt ở **Câu 1 và Câu 5** (dùng `metadata_filter={"audience": "student"}`) và **Câu 4** (dùng `metadata_filter={"department": "financial-affairs"}`), việc lọc trước bằng metadata giúp loại bỏ hoàn toàn các tài liệu không đúng đơn vị hoặc không đúng đối tượng mục tiêu, giúp kết quả tìm kiếm tương đồng vector đạt điểm số chính xác 100% ở vị trí Top-1.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
1. **Chia nhỏ theo cấu trúc văn bản pháp lý (`RecursiveChunker`):** Đối với các quy định/thông tư đại học, việc ngắt đệ quy theo dấu `\n\n` (giữa các Điều) vượt trội hơn hẳn so với ngắt theo độ dài cố định vì giữ nguyên vẹn tính toàn vẹn thông tin của một điều khoản.
2. **Sức mạnh của Metadata Pre-Filtering:** Kết hợp vector search với bộ lọc metadata (`audience`, `department`) giải quyết triệt để sự nhầm lẫn giữa các quy định trùng từ khóa nhưng khác đối tượng áp dụng.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một tập dữ liệu quy định đại học, nếu dùng `FixedSizeChunker` thì các điều khoản bị ngắt nửa chừng dẫn đến RAG Agent trả lời thiếu ý. Khi chuyển sang `RecursiveChunker` kết hợp metadata filter, chất lượng câu trả lời của RAG Agent được nâng lên mức hoàn chỉnh và có khả năng trích dẫn điều khoản chính xác.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ bổ sung thêm trường metadata `section_title` (tên của từng Điều/Mục) vào từng chunk trong quá trình nạp (`ingest.py`) để RAG Agent có thể trích dẫn chính xác "Theo Điều X của Quy chế Y..." trong câu trả lời tự động.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
