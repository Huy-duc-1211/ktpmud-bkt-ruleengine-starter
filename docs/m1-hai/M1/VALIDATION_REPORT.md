# Kết quả kiểm tra tài liệu M1

Ngày: 08/11/2026. Bộ file bàn giao trên nhánh `docs/m1-tests-hai`, không tạo PR hoặc merge.

Kết quả: **26/26 kiểm tra đạt**. CSV chính có 157 ca; bảng logic nội bộ có 81 ca. Các mã case gốc được giữ nguyên.

## Phạm vi kiểm tra

Tôi đã review nội dung M1. Phần kiểm tra tự động đối chiếu cấu trúc thư mục, dữ liệu CSV/JSON, liên kết và phạm vi thay đổi Git. CSV input/expected, registry và các snapshot nguồn được so SHA256 với bản đã review; các file này giữ nguyên. Lần sửa này cập nhật cách viết của tài liệu Markdown.

Lệnh đã chạy: `python .context-shears/validate_reviewed_publish.py`. Script và manifest lưu local trong `.context-shears`, không đưa vào bộ bàn giao. Chưa gọi `classify()`, chạy pytest nghiệp vụ, CI hoặc đo benchmark trong lần kiểm tra này.

| Kiểm tra | Kết quả |
|---|---|
| Đúng nhánh docs/m1-tests-hai | Đạt |
| HEAD local và remote target khớp trước commit | Đạt |
| Chỉ thay đổi bộ docs/m1-hai | Đạt |
| Không sửa runtime/tests/CI hoặc file chung | Đạt |
| Đúng 26 file đã review, không nhập file dư | Đạt |
| CSV, JSON và snapshot nguồn giữ đúng SHA256 bản review | Đạt |
| Cấu trúc root chỉ README +M1 +M2 | Đạt |
| CSV chính đủ 157 ID gốc, không trùng | Đạt |
| Không còn cột Legacy ID/tên case đã hủy | Đạt |
| CSV không thiếu/thừa ô | Đạt |
| 157 ca vẫn chưa chạy, không có pending TA | Đạt |
| Giữ 121 classification và 36 invalid | Đạt |
| Classification giữ nhãn/rule đúng contract | Đạt |
| Bảy ca D01–D03 giữ kết quả phản hồi thầy | Đạt |
| 22 ca T15 gộp đủ 11 cặp | Đạt |
| Cặp null/missing giữ expected như nhau | Đạt |
| Policy mã đại diện vẫn chờ Leader, không giả duyệt | Đạt |
| 81 bảng nội bộ giữ mã gốc và nội dung logic | Đạt |
| Fixture nonfinite đủ registry/refs an toàn | Đạt |
| Chỉ mục M1 khớp 157 ca | Đạt |
| Liên kết hiện hành trong M1/M2 hợp lệ | Đạt |
| Không nhập snapshot đã bỏ hoặc resurrect tên Việt cũ | Đạt |
| Ghi nhận review M1 và chỉ bàn giao lên nhánh | Đạt |
| Chỉ có file tài liệu/data được review | Đạt |
| Bộ file xuất bản đúng phạm vi bàn giao | Đạt |
| Biểu thức và ngưỡng trong thiết kế giữ nguyên | Đạt |

## Trạng thái nghiệm thu

Ba ca đề xuất mã đại diện vẫn ghi `PROPOSED FOR LEADER REVIEW`, chờ Huy duyệt. Việt Đức chưa có QA Matrix nên phần đối chiếu QA còn chờ. Các AC về runtime, CI và benchmark chưa được đánh dấu VERIFIED. Liên kết phản hồi Issue #15 trỏ đến nguồn GitHub chính thức.
