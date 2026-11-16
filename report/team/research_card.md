# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R1 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Google Research 2026, *Towards a Science of Scaling Agent Systems*, Benchmark & Empirical scaling study |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Multi-agent topologies only provide efficiency gains when subtasks are parallelizable; on sequential chains, multi-agent overhead increases latency and cost by 39–70% without accuracy improvement |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Áp dụng trên chuỗi tác vụ có sự phụ thuộc tuần tự giữa các bước (step-dependent reasoning), setup agent điều phối tập trung hoặc tuần tự |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Đổi từ Workflow (Shape A) sang Orchestrator (Shape C), do tác vụ claims mang tính tuần tự phụ thuộc dữ liệu đơn hàng, Pass rate giữ nguyên 1.000 nhưng Cost per success sẽ tăng 60-70% (từ ~28.79 lên ~47.36 VND) và Mean steps tăng từ ~3.79 lên ~4.71 |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định: MockLLM backend, 14 claims public, 5 seeds (11, 22, 33, 44, 55), pricing.yaml, evaluator. Biến duy nhất thay đổi: Kiến trúc topology (Workflow A vs Orchestrator C) |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Đo lường: Pass rate, Pass^5, Seed variance, Cost per success (VND) và Mean steps được ghi nhận trong src/reports/benchmark.json |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
- Run id / file report: src/reports/benchmark.json (Run ID dẫn chứng: R-workflow-C-001-s11, R-orchestrator-C-001-s11)
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: Đúng. Trên 70 trials (14 claims x 5 seeds), cả Workflow và Orchestrator đều đạt Pass rate = 1.000, Pass^5 = 1.000, Variance = 0.000000. Tuy nhiên, Cost per success của Orchestrator tăng từ 28.79 VND lên 47.36 VND (+64.5%), Mean steps tăng từ 3.79 lên 4.71 (+24.3%). Điều này hoàn toàn khớp với Claim của Google Research 2026 về multi-agent overhead trên sequential tasks.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
