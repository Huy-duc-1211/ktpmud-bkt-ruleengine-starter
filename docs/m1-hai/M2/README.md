# Kế hoạch cho giai đoạn sau — M2/M3

Tôi để các kế hoạch triển khai sau M1 trong thư mục này. Runtime, test và benchmark ở đây chưa thực hiện. Khi đang review M1, quay lại [M1/README.md](../M1/README.md).

- [INTERNAL_STATE_TEST_PLAN.md](INTERNAL_STATE_TEST_PLAN.md) và [INTERNAL_STATE_CASES.csv](INTERNAL_STATE_CASES.csv): chi tiết helper/Enum và 81 ca logic nội bộ.
- [INTEGRATION_TEST_PLAN.md](INTEGRATION_TEST_PLAN.md): public call, context UUID, audit, lỗi và isolation.
- [FIXTURE_CONTRACT.md](FIXTURE_CONTRACT.md), [fixtures/NONFINITE_INPUTS.json](fixtures/NONFINITE_INPUTS.json): cách dựng test data đặc biệt cho pytest M2.
- [BENCHMARK_PLAN.md](BENCHMARK_PLAN.md): protocol đo hiệu năng sẽ thực hiện ở M3 sau khi có runtime chạy được.

Mã case giữ dạng gốc. CSV chính 157 ca và quyết định logic nằm trong M1; không tạo bộ input/expected thứ hai ở đây.
