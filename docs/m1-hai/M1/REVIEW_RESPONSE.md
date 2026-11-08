# Phản hồi review R01–R11, cập nhật sau Issue #15

Tôi đã cập nhật các finding P1/P2 và đối chiếu lại với [T15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248). Phản hồi này thay đổi cách xử lý null/missing và D01–D03, nên số ca invalid và trạng thái pending cũng được cập nhật. Bảng dưới ghi phần đã sửa để nhóm review; chưa đánh dấu các tiêu chí runtime là VERIFIED.

| Finding | Trạng thái sửa hiện tại và bằng chứng |
|---|---|
| R01 — lớp lỗi validation | Thay PENDING_ADR bằng lớp lỗi cụ thể. Sau T15, tám ca null không còn invalid; còn 28 TypeError và 8 ValueError. AUD-002 dùng chuỗi boolean để kiểm input sai kiểu. Chi tiết ở CSV và ISSUE15_SYNC |
| R02 — thiết kế rule | Đồng bộ context, audit, Enum và benchmark theo Q/A đã duyệt; cập nhật D01–D03 và null/missing theo T15 |
| R03 — ghi chú review và kế hoạch test | Bỏ trạng thái chờ TA của D01–D03, làm rõ thứ tự ưu tiên nguồn và các đề xuất còn chờ review. Default audit path và internal exception giữ trạng thái theo ADR |
| R04 — R03 có thể che lỗi R02 | Bổ sung assertion riêng cho count và Enum R02 ở các ca RULE/PAIR/MISS. Kiểm thêm tương quan S/NOT S; cách chọn mã đại diện vẫn là đề xuất riêng |
| R05 — integration và audit | Có kế hoạch kiểm direct call, phiên UUID, reset context, audit failure, lỗi kép, isolation và privacy. Input null/missing hợp lệ phải ghi SUCCESS |
| R06 — trạng thái nội bộ D13 | Có 81 ca toán tử, count và dị nguyên; kiểm null boolean thành UNKNOWN, SHOCK_EVIDENCE và bước chọn kết quả theo T15, thay vì chỉ nhìn output cuối |
| R07 — provenance | Giữ mốc commit Q/A và các bản nguồn cũ; dẫn link phản hồi chính thức kèm ID/timestamp. T15 được ưu tiên ở phần mâu thuẫn; Requirements/ADR cần đồng bộ ở nhánh nguồn |
| R08 — CON-004 | Sửa định dạng assertion: before=deepcopy(patient), so sánh với patient sau lời gọi. Yêu cầu không sửa input vẫn là đề nghị kỹ thuật cần review |
| R09 — benchmark | Kế hoạch dùng perf_counter_ns, 100 warm-up, N>=1.000, nearest-rank và đo toàn bộ public call có audit I/O thật. Chưa thực đo |
| R10 — NaN/Infinity | Ba fixture dùng fixture_ref, registry và hằng math theo allowlist; expected là ValueError cho tuổi không hữu hạn. Không dùng eval hoặc runner ngoài repo |
| R11 — bàn giao | Cập nhật nội dung bàn giao, nguồn, kết quả kiểm tra và các điểm còn chờ review. Phần runtime, benchmark và đối chiếu QA chưa thực hiện |

## Các điểm còn chờ nhóm review

- D01–D03 đã được T15 làm rõ. Bảy ca PEND đã có expected; tiền tố PEND chỉ giữ để tra lịch sử.
- UNKNOWN và cách trả kết quả khi dữ liệu thiếu quyết định kết luận là policy nhóm. Đề xuất BOOL-COVERAGE và mã đại diện ở MISS-009/cặp TA15-BOOL1 còn chờ Huy review.
