# Bàn giao M1-02 — Hải

## Nội dung bàn giao

Tôi phụ trách thiết kế logic và bộ test case M1. Tôi đã review M1 trước khi bàn giao lên nhánh `docs/m1-tests-hai`. Mốc trước đợt cập nhật này là `2c6685e55af47eea55ffeea63c250272a4e71fe3`.

- [RULE_DESIGN.md](RULE_DESIGN.md): validation, biểu thức rule, thứ tự chọn kết quả và cách xử lý dữ liệu thiếu.
- [TEST_PLAN.md](TEST_PLAN.md) và [TEST_CASES.csv](TEST_CASES.csv): kế hoạch test và 157 ca, gồm 135 ca gốc và 22 ca bổ sung từ Issue #15.
- [ISSUE15_SYNC.md](ISSUE15_SYNC.md): các thay đổi theo phản hồi chính thức của thầy.
- [REVIEW_NOTES.md](REVIEW_NOTES.md) và [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md): phần đã sửa theo review và các điểm cần nhóm xem tiếp.
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md): kết quả kiểm tra cấu trúc, dữ liệu và liên kết tài liệu.
- [sources/README.md](sources/README.md): nguồn tham chiếu và các bản lưu lịch sử.

## Những thay đổi chính

Bảy ca D01–D03 đã có expected theo phản hồi Issue #15. Tám ca null không còn được xem là input lỗi. Bộ CSV hiện còn 36 ca invalid, gồm 28 ca TypeError và 8 ca ValueError. Các mã test case gốc được giữ để thuận tiện đối chiếu review.

Phản hồi chính thức là [comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), do fossbk-spec đăng và cập nhật lúc 2026-11-08T14:01:50Z. Với những điểm mâu thuẫn, áp dụng phản hồi này thay cho cách diễn giải cũ trong Requirements/ADR Revision 02. Các bản nguồn cũ vẫn được giữ để tra lịch sử.

## Các điểm còn chờ review

1. **Huy:** xem đề xuất BOOL-COVERAGE và cách chọn mã đại diện ở MISS-009, TA15-BOOL1-NULL và TA15-BOOL1-MISSING. Ba ca này vẫn ghi `PROPOSED FOR LEADER REVIEW`.
2. **Huy:** đồng bộ Requirements/ADR với phản hồi Issue #15 ở nhánh nguồn. Các snapshot trong bộ tài liệu này là mốc tham chiếu lịch sử.
3. **Việt Đức:** đối chiếu các ID INT/BENCH với QA Matrix khi có. Hiện chưa có QA Matrix và chưa hoàn tất review chéo phần này.
4. Cơ chế default audit path và cách xử lý unexpected internal exception vẫn giữ trạng thái cần review trong ADR; Issue #15 không chốt hai điểm này.

D01–D03 đã được thầy trả lời, không còn chờ TA. Đề xuất mã đại diện của nhóm là phần riêng, vẫn cần Huy duyệt.

## Phần chưa triển khai

M1 bàn giao tài liệu và dữ liệu test. Chưa triển khai `classify()`, helper, fixture factory, audit hoặc context; chưa chạy 157 ca trên engine, CI hoặc benchmark có audit I/O thật. Kết quả kiểm tra tài liệu không thay cho kết quả chạy chương trình.

Kế hoạch chi tiết cho các việc này nằm trong [M2](../M2/README.md). Đợt bàn giao này chỉ commit/push lên nhánh, không tạo PR hoặc merge.
