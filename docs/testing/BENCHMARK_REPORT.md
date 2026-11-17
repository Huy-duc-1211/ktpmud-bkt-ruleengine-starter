# Benchmark M3 — kết quả sơ bộ

## Phạm vi và trạng thái

- Kết quả sơ bộ để review, chưa phải benchmark trên SHA freeze; chưa tự xác nhận A-10 hoàn tất.
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

Hai lượt thấp hơn ngưỡng đề p95 <100 ms trong môi trường đo. Timing thay đổi theo hệ thống và I/O; chưa có báo cáo trên SHA freeze. Mẫu thô hiện không được lưu trong repository, cần lưu lại cùng môi trường khi nghiệm thu. Kiểm lại schema/UUID/privacy qua 61 test audit tại commit code đã nêu; không suy rộng sang bảo đảm ghi đồng thời hay durability sau mất điện.

Trước freeze cần đối chiếu protocol, chạy lại trên SHA chọn nộp, lưu samples và ghi điều kiện I/O, môi trường, lỗi nếu có. Nếu bất kỳ lượt gọi lỗi thì run không hợp lệ; không công bố percentile của tập đã lọc.
