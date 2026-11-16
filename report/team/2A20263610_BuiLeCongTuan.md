# Báo cáo cá nhân — 2A20263610_BuiLeCongTuan

## 1. Thông tin thành viên

- Họ tên: Bùi Lê Công Tuấn
- MSSV: 2A20263610
- Email: blct15102004@gmail.com
- GitHub: blct15102004

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

- Commit code & test chính: `8cbffa3` ("feat(shapes): optimize Single & Orchestrator shapes, expand custom tests for scope and bounded ReAct").
- Các bài test đã thêm và xác thực thành công trong `src/tests/test_orchestrator_custom.py` (4/4 passed):
  1. `test_orchestrator_handoff_no_secret_leak_custom`: Kiểm tra gói handoff không mang CANARY_SECRET_ hoặc parent_secret, allowed_tools chỉ chứa read tools.
  2. `test_orchestrator_order_cap_difference_custom`: Kiểm tra trần đơn hàng T14 (đơn đã hoàn 30k ship, hỏng 150k -> chỉ hoàn thêm 120k phần chênh).
  3. `test_orchestrator_scope_escalated_no_pii_custom`: Kiểm tra trường hợp đơn không thuộc quyền sở hữu (T05) -> trả về `escalated` và tuyệt đối không rò rỉ SĐT, địa chỉ hay internal note vào trace.
  4. `test_single_react_bounded_steps_and_read_only_custom`: Kiểm tra Shape B (Single ReAct) chạy trong ngưỡng 8 bước và các hành động trong trace không được cấp write tools.
- Run ID dẫn chứng: `R-orchestrator-C-001-s11` và `R-single-C-001-s11` (trích xuất từ `src/reports/benchmark.json`).
- Kết quả kiểm thử thực tế: Cả 4 test trong `tests/test_orchestrator_custom.py` và 62 student tests cho cả 2 shape Single & Orchestrator đều xanh 100%.

## 5. Công cụ AI đã dùng

- Trợ lý AI (Antigravity Assistant): Hỗ trợ phân tích cấu trúc allowlist của handoff và kiểm tra cú pháp ReAct runner.
- Tự kiểm tra kết quả bằng pytest và phân tích trace logs JSON qua `python -m pytest -q` và `python -m lab8.benchmark`.

## 6. Tự đánh giá

- Nắm vững kiến trúc Multi-agent và sự khác biệt về chi phí, độ dao động (variance) so với workflow cố định; hoàn thành tốt các mục tiêu đề ra.

