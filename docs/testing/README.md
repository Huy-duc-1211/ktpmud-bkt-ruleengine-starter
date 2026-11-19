# Kiểm thử và benchmark

Tôi chuyển các ca thiết kế sang pytest để kiểm tra `classify()`. Phần chọn mã theo Issue #31 lấy từ bản cập nhật của Huy Đức, có AI hỗ trợ. Tôi gửi kèm test audit để Việt Đức chạy và review. [Cách chạy](../../README.md)

- Thiết kế helper, Enum và 81 ca logic nội bộ. [Kế hoạch test](INTERNAL_STATE_TEST_PLAN.md) · [CSV](../../tests/fixtures/INTERNAL_STATE_CASES.csv)
- Gọi trực tiếp `classify()`, kiểm UUID theo phiên, đường lỗi audit và file riêng cho từng test. [Kế hoạch test tích hợp](INTEGRATION_TEST_PLAN.md)
- Cách tạo fixture NaN và Infinity cho pytest. [Quy ước fixture](FIXTURE_CONTRACT.md) · [Dữ liệu fixture](../../tests/fixtures/NONFINITE_INPUTS.json)
- Cách đo hiệu năng ở M3. [Kế hoạch benchmark](BENCHMARK_PLAN.md)
- Phép đo trên ứng viên Freeze `4be2751`: [báo cáo benchmark](BENCHMARK_REPORT.md) và [1.000 mẫu thời gian](benchmark_4be_timings.json). Đây chưa phải xác nhận trên SHA/tag cuối.

Pytest đọc input và expected của 175 ca từ [CSV ở thư mục gốc](../../TEST_CASES.csv), dùng mã ca gốc.

PR #7 đã merge bộ test M2. [CI ứng viên `4be2751`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44134696873) thành công trên Linux; ba test Windows được skip. Workbook QA giữ trạng thái thiết kế riêng. Cần đối chiếu lại các bằng chứng trên SHA/tag Freeze.

## Các điểm cần review

- `INT-010` dùng thư mục người dùng và tạo file audit riêng cho mỗi lần nạp chương trình. Leader đã chọn hướng này ở ADR §5.4.1, còn cần peer review.
- `INT-013` thử ghi `INTERNAL_ERROR` khi validator hoặc rule bất ngờ gặp lỗi. Ghi xong thì báo `RuntimeError` với thông báo chung. Nếu audit cũng thất bại thì báo `AuditError`. Test dùng dữ liệu synthetic để kiểm lỗi kép và các đầu ra có thể lộ dữ liệu. Thầy chưa xác nhận riêng status mới.
- `INT-021` kiểm cả output `ly_do` thật và câu đối chứng. Kết quả CI và benchmark được dẫn riêng ở trên; review ngữ nghĩa của Leader không thay thế việc xác nhận review cá nhân của Hải/Việt Đức.
- Writer kiểm byte cuối trước khi ghi. Test dùng file thật để kiểm trường hợp thiếu newline và ghi dở. Lần ghi tiếp theo phải giữ nội dung cũ, tạo bản ghi mới trên dòng riêng và đọc lại được. Công cụ truy vấn báo số dòng lỗi đã bỏ qua.
