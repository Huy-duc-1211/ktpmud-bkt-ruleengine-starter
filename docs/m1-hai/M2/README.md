# Kế hoạch cho giai đoạn sau — M2/M3

Thư mục này giữ kế hoạch M2/M3 từ bản của Hải và các bản sửa do Huy Đức phụ trách với AI hỗ trợ. Nhánh M2 đã triển khai cách chọn mã sau Issue #31, chạy các ca nghiệp vụ và bổ sung test audit. Xem cách chạy tại [README](../../../README.md).

- [INTERNAL_STATE_TEST_PLAN.md](INTERNAL_STATE_TEST_PLAN.md) và [INTERNAL_STATE_CASES.csv](INTERNAL_STATE_CASES.csv): chi tiết helper/Enum và 81 ca logic nội bộ.
- [INTEGRATION_TEST_PLAN.md](INTEGRATION_TEST_PLAN.md): public call, context UUID, audit, lỗi và isolation.
- [FIXTURE_CONTRACT.md](FIXTURE_CONTRACT.md), [fixtures/NONFINITE_INPUTS.json](fixtures/NONFINITE_INPUTS.json): cách dựng test data đặc biệt cho pytest M2.
- [BENCHMARK_PLAN.md](BENCHMARK_PLAN.md): protocol đo hiệu năng sẽ thực hiện ở M3 sau khi có runtime chạy được.

Mã case giữ dạng gốc. CSV chính 175 ca và quyết định logic nằm trong M1; không tạo bộ input/expected thứ hai ở đây.

## Các điểm cần review trên bản M2

- `INT-010`: bản hiện tại dùng thư mục người dùng và tạo một file audit riêng cho mỗi lần nạp chương trình. Đường dẫn này theo đề xuất tại ADR §5.4.1, còn chờ nhóm chốt.
- `INT-013`: lỗi bất ngờ từ logic phân loại trả `RuntimeError` với thông báo chung. Ca thử lỗi xác nhận chương trình không ghi `SUCCESS` hay `INVALID_INPUT` và không đưa lỗi gốc vào chuỗi lỗi công khai. Nhóm cần chốt hành vi này khi review.
- Hải và Việt Đức đối chiếu `ly_do` thực tế với INT-021, kiểm đường dẫn và lỗi audit. Kết quả pytest local cần bổ sung bằng chứng GitHub Actions sau khi nhánh M2 lên PR. Benchmark vẫn theo kế hoạch M3.
