# Benchmark M3 — kết quả và đối chiếu trước Freeze

## Phạm vi và trạng thái

- Kết quả sơ bộ để review, chưa phải benchmark trên SHA freeze; chưa tự xác nhận A-10 hoàn tất.
- **Lượt đối chiếu 19/11/2026:** chạy script nguyên bản trên mã nguồn commit `4be2751f76e540a563de9f09f24935753f80a2e7` từ checkout Git sạch. Mẫu ở [benchmark_4be_timings.json](benchmark_4be_timings.json). Chạy lại trên cùng mã nguồn sau lượt rà QA; mẫu bổ sung ở [benchmark_4be_recheck.json](benchmark_4be_recheck.json). Nếu SHA code cuối thay đổi, đo lại trước khi chốt A-10.
- Code classifier/audit và fixture: commit `274b3bf1e0ddfabfaf6f30084cf1ea04762ad55a` của PR #7. Script benchmark ở PR này được chạy trong checkout đó trước khi commit script; bản script cùng nội dung được đưa vào PR để tái lập. Không khẳng định script đã tồn tại trong commit 274b3bf.
- Thời điểm: 17/11/2026. Python 3.12.14; Linux 6.18.57 x86-64 glibc 2.41; CPU môi trường báo AMD EPYC 9V74 80-Core Processor. Loại ổ vật lý và chế độ nguồn chưa xác minh.

## Phương pháp

- Chạy `python benchmarks/benchmark_classify.py --output /duong-dan-tuyet-doi-ngoai-repo/benchmark.json` từ repo. File output là dữ liệu timing synthetic, không chứa patient payload; file lưu mẫu không được commit mặc định.
- Chu kỳ cố định RULE-001/002/011/014/021 trong CSV. Cả năm fixture gốc có tuổi 15 và huyết áp nền null; phép đo thay huyết áp nền bằng 110 synthetic cho đủ 9 trường. Kiểm trước đo cho thấy mức/mã không đổi so với fixture gốc.
- 100 warm-up full public call, loại khỏi thống kê; 1.000 lượt đo bằng perf_counter_ns ngay trước và sau `classify()`. Input được chuẩn bị trước; không mock audit, không lọc mẫu lỗi hay retry.
- UUID tạm mỗi call; audit file tạm ngoài repo, mỗi record open/append/write/flush/close; không fsync. Audit baseline 100 record, sau đo 1.100; schema, UUID phiên bản 4, action và status SUCCESS được kiểm tra.
- Nearest-rank: p50 vị trí 500 (index 499), p95 vị trí 950 (index 949); chia 1.000.000 để đổi ns thành ms.

## Kết quả

| Lượt | p50 (ms) | p95 (ms) | Ghi chú |
|---|---:|---:|---|
| Khảo sát sơ bộ | 0.067722 | 0.116214 | Chạy trước khi đóng gói script; mẫu thô lưu tạm trong môi trường kiểm tra. |
| Chạy kiểm tra script | 0.070977 | 0.175715 | 1.000 mẫu, không có exception; file timing lưu tạm ngoài repo. |
| Đối chiếu 19/11, checkout `4be2751` | **0.107712** | **0.301703** | 100 warm-up, 1.000 mẫu; 1.100 audit record; dữ liệu timing đã lưu. |
| Rà QA lần hai 19/11, cùng mã nguồn `4be2751` | **0.110113** | **0.349306** | 100 warm-up, 1.000 mẫu; 1.100 audit record; raw data lưu riêng, không thay mẫu lượt đầu. |

Hai lượt cũ thấp hơn ngưỡng đề p95 <100 ms trong môi trường đo. Timing thay đổi theo hệ thống và I/O; chưa có báo cáo trên SHA freeze. Mẫu thô của hai lượt cũ không được lưu trong repository; lượt 19/11 đã lưu mẫu riêng bên trên. Kiểm lại schema/UUID/privacy qua 61 test audit tại commit code cũ đã nêu; không suy rộng sang bảo đảm ghi đồng thời hay durability sau mất điện.

Lượt 19/11 dùng Python 3.12.14, Linux 6.18.57 x86-64 glibc 2.41; CPU môi trường báo Intel Xeon Platinum 8573C. Script đo full public `classify()` với audit JSONL thật qua open/append/write/flush/close mỗi lần, UUID tạm mỗi call, không `fsync`. Thư mục tạm mặc định `/tmp` thuộc `tmpfs` (lưu trong bộ nhớ), **không đại diện hiệu năng ghi ổ đĩa vật lý**. Input là vòng lặp cố định RULE-001/002/011/014/021, được chuẩn bị trước timing; HATT nền synthetic 110 để đủ 9 trường. Script kiểm 100 record warm-up và 1.000 record đo với đúng bốn trường, UUID v4, `CLASSIFY/SUCCESS`; không có exception. Nearest-rank lấy phần tử 500 và 950 trong 1.000 duration sau warm-up. Kết quả **p95 0.301703 ms < 100 ms** trong môi trường khai báo. Kết quả chưa phải lời xác nhận trên tag Freeze và không suy ra hiệu năng ở máy khác.

Lượt rà QA lần hai chạy Python 3.12.14 trên Linux 6.18.57 x86-64, CPU môi trường báo Intel Xeon Platinum 8573C, RAM `/proc/meminfo` 10.206.468 kB (khoảng 9,7 GiB), `/tmp` là tmpfs. Từ [mẫu lần hai](benchmark_4be_recheck.json), nearest-rank p50/p95 tính lại đúng 0.110113/0.349306 ms; writer thực ghi 100 + 1.000 bản ghi. Mô phỏng writer lỗi ở lần gọi 105 khi đo cho thấy script dừng, không xuất percentile của lượt lỗi. Không có kết quả ghi trên ổ vật lý.

Trước Freeze cần xác nhận SHA cuối có cùng code đo, ghi nhận link CI và tag thật; nếu code thay đổi thì đo lại. Nếu bất kỳ lượt gọi lỗi thì run không hợp lệ; không công bố percentile của tập đã lọc.
