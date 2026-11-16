# Kế hoạch cho giai đoạn sau — M2/M3

Thư mục này giữ kế hoạch M2/M3 từ baseline Hải và các bản sửa do Huy Đức phụ trách với AI hỗ trợ. Cách chọn mã trong kế hoạch đã được cập nhật theo chính sách nhóm sau Issue #31; runtime, test nghiệp vụ và benchmark chưa được thực hiện. Khi đang review M1, quay lại [M1/README.md](../M1/README.md).

- [INTERNAL_STATE_TEST_PLAN.md](INTERNAL_STATE_TEST_PLAN.md) và [INTERNAL_STATE_CASES.csv](INTERNAL_STATE_CASES.csv): chi tiết helper/Enum và 81 ca logic nội bộ.
- [INTEGRATION_TEST_PLAN.md](INTEGRATION_TEST_PLAN.md): public call, context UUID, audit, lỗi và isolation.
- [FIXTURE_CONTRACT.md](FIXTURE_CONTRACT.md), [fixtures/NONFINITE_INPUTS.json](fixtures/NONFINITE_INPUTS.json): cách dựng test data đặc biệt cho pytest M2.
- [BENCHMARK_PLAN.md](BENCHMARK_PLAN.md): protocol đo hiệu năng sẽ thực hiện ở M3 sau khi có runtime chạy được.

Mã case giữ dạng gốc. CSV chính 175 ca và quyết định logic nằm trong M1; không tạo bộ input/expected thứ hai ở đây.
