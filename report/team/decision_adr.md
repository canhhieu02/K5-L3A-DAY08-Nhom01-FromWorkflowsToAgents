# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 627b34f
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.0 / 1.0 / 1.000-1.000 / 0.000000
- Cost per success (mô phỏng, VND): 28.79
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0

## Vì sao shape này

Qua thực nghiệm benchmark trên 14 claims public × 5 seeds (70 trials tổng cộng), Shape Workflow đạt kết quả hoàn hảo tuyệt đối: Pass rate = 1.0 (70/70 trials pass), Pass^5 = 1.0 (100% claims pass cả 5 seed), độ dao động phương sai variance = 0.000000, và chi phí mô phỏng rẻ nhất toàn diện (28.79 VND/success). Logic bồi thường hoàn phí và xử lý hàng hỏng của LogiX-VN hoàn toàn dựa trên dữ liệu có cấu trúc từ database (bảng orders và policies). Bằng cách để code kiểm tra điều kiện và tính tiền tất định qua `compute_compensation`, Workflow loại bỏ hoàn toàn nguy cơ ảo giác (hallucination) và prompt injection từ phía khách hàng. Ngược lại, Swarm tham chiếu có chi phí đắt hơn tới 72% (49.57 VND) và xuất hiện dao động (variance = 0.000816, pass rate = 0.986) do tại seed 55 bị đánh lừa bởi text ticket ở ca T02. Theo nguyên lý cốt lõi của môn học: "Chọn kiến trúc ít tự chủ nhất mà vẫn hoàn thành được công việc", Workflow là giải pháp tối ưu nhất về cả độ chính xác, an toàn và kinh tế.

## Có đáng đổi lấy multi-agent không

Không đáng đổi. Việc chuyển sang các kiến trúc Multi-agent (Orchestrator hoặc Swarm) làm tăng vọt chi phí thực thi (từ 28.79 VND lên 47.36 - 49.57 VND, tức tăng 64.5% - 72.2%) và tăng số bước xử lý (mean steps tăng từ 3.79 lên 4.71, p95 lên 5 bước) mà không hề mang lại bất kỳ sự gia tăng nào về độ chính xác hay chất lượng bồi hoàn (Pass rate vẫn là 1.0 đối với Orchestrator và thậm chí sụt giảm xuống 0.986 đối với Swarm). Quyết định này chỉ đảo ngược khi hệ thống gặp các điều kiện sau:
1. Nhiệm vụ mang tính chất bán cấu trúc hoặc phi cấu trúc cao, yêu cầu tổng hợp dữ liệu từ nhiều nguồn API/dịch vụ ngoài phân tán chưa có schema cố định.
2. Cần điều tra song song độc lập với ranh giới phân quyền bảo mật riêng biệt giữa các tổ chức (Cross-organization Handoff).
3. Đòi hỏi cơ chế phản biện/tranh luận (Debate/Consensus) giữa các mô hình AI độc lập để giải quyết các khiếu nại tranh chấp pháp lý phức tạp và mơ hồ mà luật cứng chưa bao phủ.

## Trace và bằng chứng

Trace của nhóm ghi nhận đầy đủ chuỗi sự kiện vận hành gồm: `claim` (thông tin claim cơ bản), `order_view` (dữ liệu đơn hàng sau khi đối chiếu quyền sở hữu), `quote` (chi tiết tính toán bồi thường), `decision` (trạng thái quyết định cuối cùng) và `crash` (điểm ngắt nếu có crash injection). Nhóm cố ý **KHÔNG ghi nhận** các trường: `parent_secret`, mã bí mật canary `CANARY_SECRET_*`, raw headers, số điện thoại, địa chỉ nhà, tên mặt hàng và ghi chú nội bộ. Việc này nhằm tuân thủ tuyệt đối Trace Contract v1 và bảo vệ dữ liệu định danh cá nhân (PII). Nếu trace được lưu trữ ở hệ thống bên ngoài vùng scanner của giảng viên quét tới, đội ngũ bảo mật có thể chứng minh hệ thống không rò rỉ secret thông qua 3 bằng chứng:
1. Kiểm toán mã nguồn (Static Code Analysis): Chứng minh các adapter dữ liệu (`get_claim_view`, `lookup_order`, `make_handoff`) chỉ trích xuất các trường nằm trong Allowlist (`ORDER_FIELDS`, `FACT_KEYS`).
2. Fuzzing & Canary Testing: Đưa các token canary giả định vào context cha và xác thực bộ lọc regex tự động loại bỏ mọi chuỗi nhạy cảm trước khi emit event.
3. Kiểm soát quyền truy cập hạ tầng (Access Control & Encryption): Toàn bộ file trace lưu trữ trên đĩa được mã hóa AES-256 và chỉ có dịch vụ audit được cấp quyền giải mã.

## Giới hạn

Thực nghiệm được thực hiện trên MockLLM với các seed cố định nhằm đảm bảo tính công bằng và tái lập giữa các nhóm, do đó không phản ánh toàn diện các hành vi ngẫu nhiên, độ trễ mạng thực tế (latency được ghi nhận là `unavailable`) hay chi phí API thương mại thực tế của LLM sản xuất (GPT-4o, Gemini 1.5 Pro). Toàn bộ số liệu trong file báo cáo được trích xuất nguyên bản từ `src/reports/benchmark.json` và `src/reports/crash.json`, nhóm cam kết không chỉnh sửa thủ công số liệu.
