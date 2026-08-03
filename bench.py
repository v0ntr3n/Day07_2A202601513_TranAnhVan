"""
bench.py — Script đánh giá Benchmark cho Lab 7 (CHECKPOINT 5).

Mỗi thành viên chọn CHIẾN LƯỢC CHUNKER RIÊNG ở bước 1 (dòng duy nhất khác với đồng đội).
Mọi thành viên dùng chung: cùng corpus, cùng 5 query, cùng embedder.
"""
from __future__ import annotations

import os
from pathlib import Path

from ingest import build_knowledge_base
from src.agent import KnowledgeBaseAgent
from src.chunking import (
    FixedSizeChunker,
    HeadingSectionChunker,
    RecursiveChunker,
    SentenceChunker,
)
from src.embeddings import (
    EMBEDDING_PROVIDER_ENV,
    LOCAL_EMBEDDING_MODEL,
    LocalEmbedder,
    _mock_embed,
)

# ---------------------------------------------------------
# 1. BƯỚC 1: Chọn Chunker riêng của bạn (Chiến lược cá nhân)
# ---------------------------------------------------------
# Bạn có thể thử:
# - HeadingSectionChunker(max_chunk_size=400) [Khuyên dùng cho văn bản quy chế K3]
# - RecursiveChunker(chunk_size=400)
# - SentenceChunker(max_sentences_per_chunk=3)
# - FixedSizeChunker(chunk_size=300, overlap=50)

MY_CHUNKER = HeadingSectionChunker(max_chunk_size=400)
STRATEGY_NAME = MY_CHUNKER.__class__.__name__
STRATEGY_PARAMS = {"max_chunk_size": getattr(MY_CHUNKER, "max_chunk_size", 400)}

DATA_DIR = "data/k3_university"


def select_embedder():
    provider = os.getenv(EMBEDDING_PROVIDER_ENV, "local").strip().lower()
    if provider == "local":
        try:
            embedder = LocalEmbedder(model_name=LOCAL_EMBEDDING_MODEL)
            print(f"[EMBEDDER] Đã tải LocalEmbedder: {LOCAL_EMBEDDING_MODEL}")
            return embedder
        except Exception as e:
            print(f"[EMBEDDER] LocalEmbedder chưa sẵn sàng ({e}), chuyển sang _mock_embed.")
            return _mock_embed
    return _mock_embed


# ---------------------------------------------------------
# 2. BƯỚC 2: Bộ 5 câu hỏi Benchmark đã chốt của nhóm K3
# ---------------------------------------------------------
BENCHMARK_QUERIES = [
    {
        "id": 1,
        "type": "Số liệu (Number) - Có Filter K3",
        "query": "Điểm trung bình chung học kỳ GPA bao nhiêu thì sinh viên năm thứ hai bị cảnh báo học tập?",
        "gold_answer": "Sinh viên năm thứ hai bị cảnh báo học tập nếu GPA học kỳ đạt dưới 1.40.",
        "expected_doc": "quy-dinh-canh-bao-hoc-tap",
        "filter": {"audience": "student"},
    },
    {
        "id": 2,
        "type": "Liệt kê (Enumeration)",
        "query": "Các tiêu chí và thang điểm đánh giá kết quả rèn luyện sinh viên theo Thông tư 16/2015/TT-BGDĐT?",
        "gold_answer": "Thang 100 điểm với 5 tiêu chí: Ý thức học tập (20đ), Chấp hành nội quy (25đ), Ngoại khóa (20đ), Ý thức công dân (25đ), Cán bộ lớp/đoàn thể (10đ).",
        "expected_doc": "thong-tu-16-2015-tt-bgddt",
        "filter": None,
    },
    {
        "id": 3,
        "type": "Quy trình (Process)",
        "query": "Quy trình rút học phần muộn sau tuần 2 đến trước tuần 8 được thực hiện ra sao và ghi nhận điểm gì?",
        "gold_answer": "Nộp đơn có xác nhận Cố vấn học tập và Trưởng khoa. Điểm ghi nhận là W, không tính GPA/CPA và không hoàn học phí.",
        "expected_doc": "quy-trinh-dang-ky-rut-hoc-phan",
        "filter": None,
    },
    {
        "id": 4,
        "type": "Ngoại lệ / Chính sách (Exception)",
        "query": "Những sinh viên thuộc đối tượng nào được miễn 100% học phí theo Nghị định 81/2021/NĐ-CP?",
        "gold_answer": "Sinh viên dân tộc thiểu số rất ít người vùng ĐBKK, mồ côi cả cha lẫn mẹ, khuyết tật nặng, con người có công với cách mạng.",
        "expected_doc": "nghi-dinh-81-2021-nd-cp",
        "filter": None,
    },
    {
        "id": 5,
        "type": "Điều kiện (Condition)",
        "query": "Điều kiện tiêu chuẩn và các mức học bổng khuyến khích học tập dành cho sinh viên?",
        "gold_answer": "Mức Khá (100% học phí, GPA>=2.5, ĐRL>=70), Mức Giỏi (120%, GPA>=3.2, ĐRL>=80), Mức Xuất sắc (150%, GPA>=3.6, ĐRL>=90). Đăng ký tối thiểu 15 tín chỉ và không bị kỷ luật.",
        "expected_doc": "quy-che-hoc-bong-khuyen-khich",
        "filter": None,
    },
]



def simple_llm(prompt: str) -> str:
    """Mô phỏng trả lời câu hỏi dựa trên context."""
    first_lines = [line for line in prompt.splitlines() if line.strip() and not line.startswith("Answer")]
    context_snippet = " ".join(first_lines[:3])[:200]
    return f"[RAG Answer] Trích xuất từ ngữ cảnh: {context_snippet}..."


def main() -> int:
    print("=" * 70)
    print("      LAB 07 — BENCHMARK EVALUATION (CHECKPOINT 5)")
    print("=" * 70)
    print(f"Chiến lược Chunker: {STRATEGY_NAME}")
    print(f"Tham số Chunker  : {STRATEGY_PARAMS}")
    print(f"Thư mục Corpus   : {DATA_DIR}")

    embedder = select_embedder()

    # Nạp dữ liệu vào Vector Store
    store = build_knowledge_base(DATA_DIR, embedding_fn=embedder, chunker=MY_CHUNKER)
    total_chunks = store.get_collection_size()
    print(f" Tổng số chunks đã nạp vào Vector Store: {total_chunks}")
    print("=" * 70)

    agent = KnowledgeBaseAgent(store=store, llm_fn=simple_llm)

    for q in BENCHMARK_QUERIES:
        print(f"\nQuery #{q['id']} [{q['type']}]:")
        print(f"  Câu hỏi      : {q['query']}")
        print(f"  Metadata Filter: {q['filter']}")
        print(f"  Gold Answer  : {q['gold_answer']}")
        print(f"  Doc kỳ vọng  : {q['expected_doc']}")

        # Nếu query có metadata_filter -> search_with_filter; ngược lại -> search() chuẩn
        if q.get("filter"):
            results = store.search_with_filter(
                query=q["query"], top_k=3, metadata_filter=q["filter"]
            )
        else:
            results = store.search(query=q["query"], top_k=3)


        print(f"   Kết quả Top-3 retrieved ({len(results)} chunks):")
        for idx, res in enumerate(results, 1):
            doc_id = res["metadata"].get("doc_id", res["id"])
            score = res.get("score", 0.0)
            preview = res["content"][:120].replace("\n", " ")
            print(f"    [{idx}] score={score:.4f} | doc_id={doc_id} | {preview}...")

        # Câu trả lời của Agent
        agent_resp = agent.answer(q["query"], top_k=3)
        print(f"  🤖 Agent Answer: {agent_resp}")
        print("-" * 70)

    print("\n HOÀN THÀNH RUN BENCHMARK CHECKPOINT 5!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
