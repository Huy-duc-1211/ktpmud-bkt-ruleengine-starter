# Bàn giao M2 và kế hoạch M3

Tôi chuyển bộ ca M1 sang pytest để kiểm tra `classify()` trên nhánh M2. Phần chọn mã theo Issue #31 lấy từ bản cập nhật của Huy Đức, có AI hỗ trợ. Tôi gửi kèm test audit để Việt Đức chạy và review. [Cách chạy](../../../README.md)

- Thiết kế helper, Enum và 81 ca logic nội bộ. [Kế hoạch test](INTERNAL_STATE_TEST_PLAN.md) · [CSV](INTERNAL_STATE_CASES.csv)
- Gọi trực tiếp `classify()`, kiểm UUID theo phiên, đường lỗi audit và file riêng cho từng test. [Kế hoạch test tích hợp](INTEGRATION_TEST_PLAN.md)
- Cách tạo fixture NaN và Infinity cho pytest. [Quy ước fixture](FIXTURE_CONTRACT.md) · [Dữ liệu fixture](fixtures/NONFINITE_INPUTS.json)
- Cách đo hiệu năng ở M3. [Kế hoạch benchmark](BENCHMARK_PLAN.md)

Pytest đọc input và expected của 175 ca từ CSV ở M1, dùng mã ca gốc.

## Các điểm cần review trên bản M2

- `INT-010` dùng thư mục người dùng và tạo file audit riêng cho mỗi lần nạp chương trình, theo đề xuất ở ADR §5.4.1. Nhóm còn cần chốt đường dẫn mặc định.
- `INT-013` thử ghi `INTERNAL_ERROR` khi logic phân loại gặp lỗi. Ghi xong thì báo `RuntimeError` với thông báo chung. Nếu ghi cũng lỗi thì báo `AuditError`. Nhờ Việt Đức review tên status và ca lỗi kép. Đây là phương án của nhóm đang chờ review, chưa có xác nhận của thầy.
- Tôi sẽ đối chiếu `ly_do` thực tế theo INT-021 cùng Việt Đức. Khi có PR M2, Việt Đức thu thêm kết quả GitHub Actions để đối chiếu với lần chạy local. Benchmark làm ở M3.
