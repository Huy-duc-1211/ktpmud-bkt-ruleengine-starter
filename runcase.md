# Tra kết quả theo mã ca

## Chạy bằng cách bấm đúp

1. Mở thư mục dự án rồi bấm đúp [run_case.cmd](run_case.cmd).
2. Nhập `TEST_CASES.csv` rồi nhấn Enter. Nếu dùng file CSV khác, nhập đường dẫn đầy đủ. Có thể dán cả dòng `cd D:\1.TNHH\project\ktpm_hackathon\TEST_CASES.csv`.
3. Nhập mã ca trong cột `Test ID` của CSV, ví dụ `MISS-009`. Chương trình lấy dữ liệu trong cột `Input`, gọi `classify()` và in kết quả.
4. Nhập mã khác để tra tiếp trong cùng file. Gõ `END` rồi nhấn Enter để kết thúc. Cửa sổ chờ bạn nhấn thêm một phím trước khi đóng.

Để lưu các kết quả đã tra, nhập `/CSV` ở ô mã ca, rồi nhập tên file mới như `ket_qua.csv` hoặc đường dẫn đầy đủ. Sau khi xuất, bạn có thể tra tiếp. Tên file tương đối được tính từ thư mục đang chạy lệnh.

Nếu xuất CSV thất bại, bạn có thể nhập `/CSV` và thử lại với tên file khác. Phiên trả mã thoát `1` khi kết thúc, kể cả khi lần xuất sau thành công.

[Mở TEST_CASES.csv](TEST_CASES.csv)

## Đọc kết quả

Với `MISS-009`, bạn sẽ thấy `muc_do` là `PHAN_VE`, `rule_id` là `R01-PV` và `ly_do` giải thích vì sao R01 là mã đại diện. Để đối chiếu, tìm cùng mã ca trong CSV rồi đọc cột `Expected`. Phần `ly_do_contract` mô tả yêu cầu đối với câu giải thích.

- Nếu không tìm thấy file CSV, chương trình báo đường dẫn bị lỗi trên `stderr` và trả mã thoát `1`. Điều này áp dụng cả khi nhập đường dẫn tương tác lẫn khi dùng `--csv`.
- Nếu gõ nhầm mã ca hoặc bấm Enter khi chưa nhập mã, bạn có thể nhập lại.
- Với ca đầu vào bị từ chối, chương trình in loại lỗi và thông báo. Bạn vẫn có thể tra mã khác. Khi kết thúc, phiên trả mã thoát `1` nếu có ít nhất một ca phân loại báo lỗi, kể cả khi ca sau chạy thành công.

## Chạy một ca từ CMD hoặc PowerShell

Trong CMD, dùng `cd /d` để chuyển tới thư mục dự án rồi gọi `run_case.cmd`.

```bat
cd /d "D:\1.TNHH\project\ktpm_hackathon"
run_case.cmd MISS-009
```

Lệnh tương đương trong PowerShell khi đang ở thư mục dự án.

```powershell
.\.venv\Scripts\python.exe -X utf8 .\run_case.py MISS-009
```

Để chỉ rõ file CSV, thêm `--csv "D:\đường-dẫn\ca-test.csv"` vào cuối lệnh. Nếu chưa có `.venv`, xem [cách cài đặt trong README](README.md#cài-đặt-và-kiểm-thử).

## Xuất kết quả ra CSV

Thêm `--export-csv` để lưu kết quả. Ví dụ trong CMD.

```bat
run_case.cmd MISS-009 --export-csv "ket qua.csv"
```

Trong PowerShell, dùng lệnh sau.

```powershell
.\.venv\Scripts\python.exe -X utf8 .\run_case.py MISS-009 --export-csv ket_qua.csv
```

Nếu bỏ `MISS-009`, chương trình vào chế độ tương tác và lưu các kết quả đã tra khi kết thúc. Có thể dùng `--csv` để chọn file ca test và `--export-csv` để chọn file kết quả trong cùng lệnh.

File kết quả có các cột `test_id`, `muc_do`, `rule_id`, `ly_do`, `exception_class` và `message`. Mỗi lần chạy một ca tạo một dòng. Ca bị từ chối có loại lỗi và thông báo. Mã không tìm thấy trong file ca test sẽ không tạo dòng.

Chương trình tự thêm đuôi `.csv` nếu thiếu và giữ nguyên file đã có. File dùng UTF-8 có BOM để giữ dấu tiếng Việt. Trên Windows, dấu phân cách là dấu phẩy hoặc chấm phẩy theo thiết lập vùng. Nếu mở file trên máy có thiết lập khác và Excel dồn dữ liệu vào cột A, dùng **Data → From Text/CSV** rồi chọn dấu phân cách trong mục **Delimiter**.
