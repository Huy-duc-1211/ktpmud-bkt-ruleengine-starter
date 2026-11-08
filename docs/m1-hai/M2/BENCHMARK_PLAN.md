# D10 — Kế hoạch đo benchmark

Nguồn Q/A Revision 04 pin ở [sources](../M1/sources/README.md), Q NFR-01/§6; A §§5.7,8.10–8.11. T15 không thay protocol benchmark; phần nullable/selection theo [ISSUE15_SYNC](../M1/ISSUE15_SYNC.md) và D13-E đã duyệt. 100 warm-up/nearest-rank là lựa chọn Leader đã duyệt, không còn là đề xuất cần chọn. Ở M1, tôi chỉ đối chiếu protocol và công thức; chưa có số đo để kết luận A-10 đạt.

## Phép đo chính M3

1. Ghi Python/version, OS, CPU/hardware, nguồn điện/chế độ chạy nếu ảnh hưởng, commit source, N, dataset synthetic, cấu hình context và I/O/storage/path resolved ngoài repo.
2. Dùng các ca đủ dữ liệu để cô lập phép đo, không lẫn ca nullable/policy nhóm: ví dụ cycle RULE-001/002/011/014/021. Khai báo thứ tự/lịch lặp trước đo, không chọn lọc mẫu theo tốc độ. Test ID chỉ là metadata harness, không đưa vào PatientInput.
3. Cấu hình writer thật theo OPEN-09: mỗi record open append/write/close. Không mock writer, dùng /dev/null, bỏ audit, giữ stream cả lô hoặc hoãn ghi đến sau timed call. Nếu runtime có flush, phần đó phải nằm trong timing lifecycle. Không mặc định fsync/durability chưa được duyệt.
4. **100 warm-up full public call** có audit thật, loại cả 100 duration khỏi tập mẫu. Warm-up phải hoàn tất bình thường; sau warm-up xác định baseline count audit cho riêng run.
5. **N>=1.000** lần đo: t0=perf_counter_ns() ngay trước public classify(patient); t1 ngay sau hàm trả về khi audit đã hoàn tất; duration_ns=t1-t0. Bao gồm validation/rules/explanation/provider bên trong call và I/O audit thật. Metadata, parse CSV và thống kê ở ngoài timing. Nếu chọn no-session mode, tạo/reset UUID tạm bên trong call cũng được tính; phải ghi mode trong báo cáo.
6. Không âm thầm loại exception, retry, thay duration hoặc chỉ lấy mẫu thành công. Có lỗi thì ghi run chưa hợp lệ để nghiệm thu và điều tra; không công bố p95 đạt từ tập đã lọc.
7. Kiểm file audit riêng: delta N success records sau baseline warm-up; nếu file ban đầu trống và không có call phụ, tổng 100+N records. Schema/status/UUID và lifecycle đã được integration test trước khi coi phép đo hợp lệ. Không đưa raw input vào log benchmark/audit.
8. Sắp N duration tăng dần. Nearest-rank: vị trí **ceil(p*N)** tính từ 1, index Python là ceil(p*N)-1. p50 p=0.50, p95 p=0.95. Chia **1.000.000** từ ns sang ms. N=1.000 -> vị trí 500/950, index 499/949.
9. Báo p50/p95 thực và so **p95 <100 ms**; bằng 100 không đạt target. Lưu samples duration/environment/protocol để tính lại. Đây là dữ liệu timing synthetic, không patient payload. Chưa có kết quả thực đo trong M1.

Logic thuần là phép đo phụ tách nhãn, không thay full-path audit. Nếu cần tối ưu writer sau số liệu phải review đề xuất riêng, không tự đổi semantics đã duyệt để đạt latency.

## Test protocol trước khi benchmark runtime

| ID | Kiểm chứng | Expected / evidence |
|---|---|---|
| BENCH-001 | Review timing boundary và writer configuration | Bao toàn public path/open-write-close thật; không mock hoặc async deferred audit |
| BENCH-002 | Kiểm warm-up/mẫu bằng bộ đếm | 100 warm-up ngoài tập N>=1.000; không lọc/retry lỗi |
| BENCH-003 | Tính tay nearest-rank trên vector giả lập 1..20 ms | p50=10 ms, p95=19 ms; đây là kiểm công thức, không phải latency đo được |
| BENCH-004 | Kiểm chỉ số ở N=1.000 và chuyển ns/ms | index 499/949; 1.000.000 ns=1 ms; không lẫn percentile nội suy mặc định |
| BENCH-005 | Failure lúc writer đang ghi | Run không đủ điều kiện nghiệm thu; không drop duration lỗi rồi nhận đạt |
| BENCH-006 | So evidence môi trường, dataset, audit delta và samples | Có đủ metadata/số đo thật mới đánh giá A-10; pure-logic báo riêng |

Theo phân công trong ADR (A), Việt Đức chủ trì benchmark và QA Matrix; Hải review phạm vi timing của public call và context. Nguồn TASK 02E chưa cung cấp/xác minh QA Matrix; các ID BENCH cần Việt Đức đối chiếu A-10. Chưa có bằng chứng benchmark/runtime; protocol trong mục Phép đo chính M3 giữ nguyên.
