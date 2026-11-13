# QA M1-03

Thư mục này lưu QA Matrix và hồ sơ rà soát thiết kế của nhóm `173820_n27`. Việt Đức là tác giả QA gốc. Huy Đức tiếp quản việc sửa và kiểm chứng thiết kế với công cụ AI hỗ trợ.

| Tài liệu | Mục đích |
|---|---|
| [QA_MATRIX.xlsx](QA_MATRIX.xlsx) | Workbook chính để theo dõi tiêu chí nghiệm thu, ca thiết kế, checklist và bằng chứng QA. |
| [QA_REVIEW_REPORT.md](QA_REVIEW_REPORT.md) | Báo cáo audit thiết kế, gồm phạm vi kiểm tra tĩnh và các phát hiện. |
| [QA_WORKBOOK_VALIDATION.md](QA_WORKBOOK_VALIDATION.md) | Kiểm chứng workbook và nhật ký các ô đã sửa trong TASK 02N-C. |
| [QA_REVIEW_COMPARISON.md](QA_REVIEW_COMPARISON.md) | Đối chiếu các nhận định review với dữ liệu và bằng chứng có tại thời điểm rà soát. |
| [QA_LEADER_REVIEW_NOTES.md](QA_LEADER_REVIEW_NOTES.md) | Ghi chú bàn giao cho Leader, các điểm cần review và việc chuyển sang M2/M3. |

Bốn báo cáo ghi lại trạng thái tại TASK 02N-C, trước khi Leader cập nhật cách chọn mã sau [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002). Câu “chưa mở PR #4” phản ánh thời điểm viết; PR #4 đã merge ngày 10/11/2026. Xem workbook cùng phiên bản và [Test Cases](../m1-hai/M1/TEST_CASES.csv) cho thiết kế hiện hành; báo cáo tĩnh cũ không chứng minh selector mới đã chạy. [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4)

Các URL ghim commit cũ trong workbook là nguồn lịch sử để truy vết; expected và assertion sau Issue #31 được xem trong `TEST_CASES.csv` ở cùng commit với workbook. Workbook vẫn cần Hải/Việt Đức review và bằng chứng thực thi riêng.

Ô `GAP_REVIEW!L8` lưu tên báo cáo kiểm chứng theo thời điểm viết. Báo cáo hiện ở [QA_WORKBOOK_VALIDATION.md](QA_WORKBOOK_VALIDATION.md).

## Đọc trạng thái QA

Ca thiết kế mô tả dữ liệu và kết quả dự kiến. Các mục thực thi trong workbook đang là `NOT RUN`. Bằng chứng chạy nghiệp vụ, CI và benchmark cần lấy từ lần chạy tương ứng. Peer review của thành viên và nghiệm thu của TA cần xác nhận riêng.

A-11 trong Requirements ghi `VERIFIED` cho disclaimer trong README gốc. Phạm vi bằng chứng là A-11. [Requirements hiện hành](../../REQUIREMENTS.md#7-tiêu-chí-nghiệm-thu) · [README tại commit bằng chứng](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/README.md#L43)

Đối chiếu rule, ca thiết kế và kế hoạch kiểm thử qua [chỉ mục M1-02](../m1-hai/M1/README.md).
