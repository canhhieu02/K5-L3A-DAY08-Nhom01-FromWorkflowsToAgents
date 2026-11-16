# Báo cáo cá nhân — 2A202603667_NguyenCanhHieu

## 1. Thông tin thành viên

- Họ tên: Nguyễn Cảnh Hiếu
- MSSV: 2A202603667
- Email: hieucoi098765@gmail.com
- GitHub: canhhieu02

## 2. Phần việc phụ trách

- Shape A (Deterministic Workflow).
- Host Integration, Idempotency & Durability (`issue_refund`, transaction safety).
- Chạy và kiểm tra Crash Safety suite (`reports/crash.json`).

## 3. Đóng góp cụ thể

- Setup ban đầu môi trường Python 3.12, chạy smoke test và duy trì cổng host xanh 100%.
- Triển khai `src/lab8/shapes/workflow.py` theo đúng quy trình tuần tự, bảo đảm quote đầy đủ và không lộ PII/secret.
- Thêm file test kiểm chứng crash & idempotency: `src/tests/test_workflow_custom.py`.
- Tích hợp và chạy suite crash safety đạt kết quả tuyệt đối 20/20.

## 4. Bằng chứng

- Commit chính: `627b34f` (implement shapes and complete documentation).
- Tên test đã thêm: `tests/test_workflow_custom.py::test_workflow_idempotency_custom`, `tests/test_workflow_custom.py::test_workflow_crash_safety_custom`.
- Run ID dẫn chứng: `R-workflow-C-001-s11`.
- File bằng chứng: `src/reports/crash.json` đạt `crash_safety: "20/20"`.

## 5. Công cụ AI đã dùng

- Trợ lý AI (Antigravity Assistant): Hỗ trợ đọc tài liệu hợp đồng (`docs/contracts.md`, `docs/business_rules.md`), rà soát cơ chế bắt `InjectedCrash` và trace flush.
- Tự kiểm tra kết quả bằng lệnh CLI độc lập: `python -m lab8.smoke`, `python -m pytest -q`, `python -m lab8.crash_test --count 20`.

## 6. Tự đánh giá

- Hoàn thành xuất sắc nhiệm vụ được giao, hiểu sâu sắc ranh giới giữa code tài chính và model, làm chủ cơ chế idempotency trong hệ thống phân tán.
