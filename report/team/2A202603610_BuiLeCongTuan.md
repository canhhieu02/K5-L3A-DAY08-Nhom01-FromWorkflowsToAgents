# Báo cáo cá nhân — 2A202603610_BuiLeCongTuan

## 1. Thông tin thành viên

- Họ tên: Bùi Lê Công Tuấn
- MSSV: 2A202603610
- Email: tuan.blc@vinuni.edu.vn
- GitHub: builecongtuan

## 2. Phần việc phụ trách

- Shape B (Single Agent ReAct).
- Shape C (Orchestrator + Read-only Investigators).
- Handoff Sanitization, Benchmark thực nghiệm và phân tích Decision Record (ADR).

## 3. Đóng góp cụ thể

- Triển khai Shape B (`single.py`) với vòng lặp ReAct giới hạn 8 bước, host là bên duy nhất ghi ledger.
- Triển khai Shape C (`orchestrator.py`) với cơ chế handoff allowlist nghiêm ngặt, không rò rỉ context cha hay secret.
- Thêm file test kiểm chứng cô lập handoff và trần đơn hàng: `src/tests/test_orchestrator_custom.py`.
- Chạy benchmark 4 shapes × 5 seeds trên bộ public, tổng hợp số liệu cho `decision_adr.md` và `research_card.md`.

## 4. Bằng chứng

- Commit chính: `1af7fb2` (triển khai shapes, tests và báo cáo) và commit báo cáo cá nhân.
- Tên test đã thêm: `tests/test_orchestrator_custom.py::test_orchestrator_handoff_no_secret_leak_custom`, `tests/test_orchestrator_custom.py::test_orchestrator_order_cap_difference_custom`.
- Run ID dẫn chứng: `R-orchestrator-C-001-s11`.
- File bằng chứng: `src/reports/benchmark.json` chứa kết quả so sánh đầy đủ 4 shapes.

## 5. Công cụ AI đã dùng

- Trợ lý AI (Antigravity Assistant): Hỗ trợ phân tích cấu trúc allowlist của handoff và kiểm tra cú pháp ReAct runner.
- Tự kiểm tra kết quả bằng pytest và phân tích trace logs JSON qua `python -m pytest -q` và `python -m lab8.benchmark`.

## 6. Tự đánh giá

- Nắm vững kiến trúc Multi-agent và sự khác biệt về chi phí, độ dao động (variance) so với workflow cố định; hoàn thành tốt các mục tiêu đề ra.
