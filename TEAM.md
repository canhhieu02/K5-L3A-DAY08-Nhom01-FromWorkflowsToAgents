# Team

## Thông tin nhóm

- Tên nhóm: Nhom01
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-Nhom01-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: `https://github.com/canhhieu02/K5-L3A-DAY08-Nhom01-FromWorkflowsToAgents.git`, nhánh `main`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Cảnh Hiếu | 2A202603667 | hieucoi098765@gmail.com | canhhieu02 | Workflow, Integration & Durability |
|   2 | Bùi Lê Công Tuấn | 2A20263610 | blct15102004@gmail.com | blct15102004 | Single Agent, Orchestrator & Benchmark/ADR |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Cảnh Hiếu | Workflow, Durability & Integration | 1af7fb2 | tests/test_workflow_custom.py |
| Bùi Lê Công Tuấn | Single Agent, Orchestrator & Benchmark | 8cbffa3 | tests/test_orchestrator_custom.py |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

## 2A202603667_NguyenCanhHieu

### Phần việc phụ trách

- Shape A (Workflow), Durability & Idempotency, Crash Safety suite, Tích hợp hệ thống.

### Đóng góp cụ thể

- Thiết lập môi trường, xác thực smoke test và cổng host.
- Cài đặt Shape A (`workflow.py`).
- Xử lý tham số `crash_at`, kiểm tra cơ chế chống double refund.

### Bằng chứng

- Commit ban đầu, test cổng host và crash test `20/20`.

## 2A20263610_BuiLeCongTuan

### Phần việc phụ trách

- Shape B (Single Agent), Shape C (Orchestrator), Handoff sanitizer, Benchmark & ADR.

### Đóng góp cụ thể

- Cài đặt Shape B (`single.py`) với vòng ReAct tối đa 8 bước.
- Cài đặt Shape C (`orchestrator.py`) với handoff allowlist.
- Chạy benchmark 4 shapes và viết báo cáo quyết định kiến trúc.

### Bằng chứng

- Commit cài đặt shape B và C, file `reports/benchmark.json`.
