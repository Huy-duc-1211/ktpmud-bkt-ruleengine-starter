# Tra kết quả theo mã ca

## Chạy bằng cách bấm đúp

1. Mở thư mục dự án rồi bấm đúp [run_case.cmd](run_case.cmd).
2. Nhập `TEST_CASES.csv` rồi nhấn Enter. Nếu dùng file CSV khác, nhập đường dẫn đầy đủ. Có thể dán cả dòng `cd D:\1.TNHH\project\ktpm_hackathon\TEST_CASES.csv`.
3. Nhập mã ca trong cột `Test ID` của CSV, ví dụ `MISS-009`. Chương trình lấy dữ liệu trong cột `Input`, gọi `classify()` và in kết quả.
4. Nhập mã khác để tra tiếp trong cùng file. Gõ `END` rồi nhấn Enter để kết thúc. Cửa sổ chờ bạn nhấn thêm một phím trước khi đóng.

[Mở TEST_CASES.csv](TEST_CASES.csv)

## Đọc kết quả

Với `MISS-009`, bạn sẽ thấy `muc_do` là `PHAN_VE`, `rule_id` là `R01-PV` và `ly_do` giải thích vì sao R01 là mã đại diện. Để đối chiếu, tìm cùng mã ca trong CSV rồi đọc cột `Expected`. Phần `ly_do_contract` mô tả yêu cầu đối với câu giải thích.

- Nếu đường dẫn sai hoặc file không tồn tại, chương trình in `null` rồi dừng.
- Nếu gõ nhầm mã ca hoặc bấm Enter khi chưa nhập mã, bạn có thể nhập lại.
- Với ca đầu vào bị từ chối, chương trình in loại lỗi và thông báo. Bạn vẫn có thể tra mã khác.

## Chạy một ca từ PowerShell

Mở PowerShell ở thư mục gốc của dự án rồi chạy lệnh sau. Đổi `MISS-009` thành mã muốn xem.

```powershell
.\.venv\Scripts\python.exe -X utf8 .\run_case.py MISS-009
```

Để chỉ rõ file CSV, thêm `--csv "D:\đường-dẫn\ca-test.csv"` vào cuối lệnh. Nếu chưa có `.venv`, xem [cách cài đặt trong README](README.md#cài-đặt-và-kiểm-thử).
