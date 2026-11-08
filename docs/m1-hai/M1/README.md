# M1-02 — Thiết kế logic và test case

## Nội dung review M1

Tôi tập hợp phần cần review ở M1 theo thứ tự dưới đây:

1. [Phản hồi Issue #15 và delta logic](ISSUE15_SYNC.md).
2. [Thiết kế rule](RULE_DESIGN.md).
3. [Kế hoạch test M1](TEST_PLAN.md).
4. [CSV chung 157 ca](TEST_CASES.csv): giữ mã gốc, input/expected không đổi.
5. [Nhận xét cần review](REVIEW_NOTES.md) và [phản hồi R01–R11](REVIEW_RESPONSE.md).
6. [Bàn giao M1](HANDOFF.md) và [kết quả kiểm tra tài liệu](VALIDATION_REPORT.md).
7. [Nguồn và lịch sử](sources/README.md).

Các file kế hoạch chi tiết test nội bộ, integration, fixture và benchmark đã chuyển sang M2. Đây là chuẩn bị cho giai đoạn sau, không phải yêu cầu triển khai hoặc thực đo ở M1.

## Trạng thái nguồn và policy

Enum UNKNOWN và cách trả kết quả khi thiếu dữ liệu là policy nhóm; T15 cho phép nhóm công bố cách xử lý ở phần chưa quy định. **Mã đại diện BOOL-COVERAGE ở MISS-009/cặp TA15-BOOL1 là đề xuất chờ Huy Đức review**; phần bảo toàn mức và bảy kết quả D01–D03 không bị gán là còn chờ TA. Cơ chế default audit path và unexpected internal exception vẫn còn điểm cần review theo ADR (A).
