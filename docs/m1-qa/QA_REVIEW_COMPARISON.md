# TASK 02N-C — Đối chiếu bản ChatGPT

Phase A đã được ghi độc lập trước khi đối chiếu lịch sử. Phần này đánh giá các kết luận thể hiện trong `GAP_REVIEW!A2:L16`, các cột đã vá và 15 finding của audit TASK 02J. Đã tìm tại Downloads, attachments và workspace. Tìm được `QA_MATRIX.xlsx` ban đầu với SHA `9e423bf96969568278ab5e0473d0cd5a99b051ce9c3be9ab4264642d64ddb015`, khớp bản đã review 02J. Không tìm được `QA_MATRIX (1)(1).xlsx`, `QA_MATRIX_M1_LEADER_REMEDIATED.xlsx`, changelog/validation hoặc hai báo cáo self-review/rereview nêu trong yêu cầu. Do đó chỉ xác nhận hai mốc có file, không quy lỗi vào một lần sửa ChatGPT cụ thể.

| Finding cũ | Kết luận | Ô và bằng chứng | Xử lý |
| --- | --- | --- | --- |
| F01 | Chấp nhận | D13-E approved đã ghi ở AC I/J và QA H41:H42/H55:H56. Sáu oracle đã tách. | Giữ peer review và NOT RUN riêng. |
| F02 | Chấp nhận | QA_CASES!G21 I=true trùng MISS-009, H21 U/U/F. QA_CASES!G57/H57 là MISS-012 riêng. | Thay I=false → true sửa fixture/helper đúng. Public vẫn cùng mức/mã canonical. |
| F03 | Chấp nhận | QA_CASES!E23/H23 và QA_CHECKLIST!G14 tách INV-001 nullable SUCCESS khỏi AUD-002. QA-023/CHK-059 kiểm đường invalid riêng. | AUD-002 chỉ là đối chứng trong success, không chạy chung JSON. |
| F04 | Có điều kiện | QA-003/009/010/011/016–019/023 phần lớn đã phân EXACT/VARIANT/CONTRAST. QA_CASES!E16 và E22/G22 còn mơ hồ. | NC-02 sửa liên kết còn thiếu. H22 có expected riêng theo fixture. |
| F05 | Có điều kiện | QA_CASES!E58:E65 đủ 18 ID và checklist có 81 nội bộ riêng. G65 mô tả 015/016 ngược thứ tự. CHK-056 chưa assert MISS-013/014 riêng. | NC-04 làm rõ null/missing, definite-first thật, RULE-020 và 64 khả năng. |
| F06 | Có điều kiện | AC_MATRIX!C6/E6, QA_CHECKLIST!E8/F8, E59/F59 đã có INT-021, negative và review người. QA_CASES!G30 không đưa actual ly_do vào thủ tục. | NC-03/04 tách canary lỗi và output hợp lệ. Giữ human semantics bên cạnh regex. |
| F07 | Có điều kiện | Table ranges và dropdown đã mở rộng đủ. Excel COM xác nhận ShowAutoFilter=false trên bốn Table của bản vào/copy trước chỉnh. | Bật AutoFilter bốn Table. Giữ Table, vùng và dropdown. |
| F08 | Bác bỏ nếu hiểu số đã được tính lại | AC_MATRIX!M2:N12 vẫn dùng wildcard đúng, nhưng 22 cache bằng 0. 21 giá trị khác đếm độc lập. M3 đúng 0. | Excel 16.0 CalculateFullRebuild rồi đối chiếu từng ô. Count là lượt gắn AC, không là quality/PASS. |
| F09 | Có điều kiện | Link cũ L3/L19 và pin nguồn đã sửa. AC_MATRIX!D9 vẫn 157, và bốn nguồn QA_CASES!I11/I14:I15/I23 ghi §8.2 không đúng phạm vi. | NC-05/06 sửa các trường cụ thể. Không đổi URL nào đang trỏ đúng. |
| F10 | Có điều kiện | QA_CASES!G19/H19/N19 dùng nonfinite registry đúng. QA_CHECKLIST!G7 nói lọc 36 trong INV-002–043, thực tế 35 INV + AUD-002. | NC-06 ghi rõ cách đếm. Chuỗi None là own variant, không thay fixture gốc. |
| F11 | Có điều kiện | QA_CASES!E27:E30 đã map INT-001/006/007/008/015/021. G27:G30 còn thiếu input và stage/nhánh để thực thi như H/N yêu cầu. | NC-03 hoàn chỉnh procedure. INT-010/013 giữ quyết định mở. |
| F12 | Chấp nhận | AC_MATRIX!C3:I3 và QA_CHECKLIST!D3:G3 tách CON-004 khỏi gate A-02. INT-014 ở CHK-043 hỗ trợ A-04. | Giữ code review và input synthetic độc lập trong M2. |
| F13 | Chấp nhận với điều kiện bàn giao | AC E, QA L31:L34 và CHK-060 đã mô tả evidence theo hoạt động, sign-off rõ. F/M/I evidence trống và đúng NOT RUN. | Không suy peer review đã thực hiện từ cột vai trò. |
| F14 | Chấp nhận | Checklist tổng quan và chi tiết ghi quan hệ, đặc biệt CHK-011/030, 015/035, 016/036. | Giữ ca có mục đích khác nhau. Có thể giảm trùng sau. |
| F15 | Chấp nhận | QA-033, CHK-029/045 và AC A-11 đã có chuỗi exact và gate README root trên SHA nghiệm thu. | M2 mới thu evidence. Không tự đóng A-11. |

## Các kết luận phải bác bỏ hoặc giới hạn

- **“21/21 inline JSON đủ chứng minh workbook.”** Bác bỏ phạm vi suy luận. Tái lập được 21/21 kết quả tĩnh với 18 liên kết trùng và 3 own variant. Trong 43 dòng còn lại có fixture group và procedure. Ví dụ QA-021 E22/G22 trỏ hai nhóm, QA-027 G28 chỉ inject append và QA-064 G65 đảo mô tả 015/016 dù cả cặp cho cùng kết quả. Kiểm inline không thể bắt các lỗi này. [CSV hiện hành](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv), [Integration Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md).
- **“Giữ/đóng đủ filter và formula evidence.”** Chỉ đúng với phạm vi Table, dropdown và định nghĩa công thức. Trước chỉnh, bốn Table thiếu AutoFilter, 22 cache bằng 0. Xem native COM và số liệu ở báo cáo Excel.
- **“Tất cả đúng nguồn Rev04 và inventory hiện hành.”** Bốn ô cite sai mục Requirements và D9 ghi 157. Các URL pin chính vẫn hợp lệ. [Requirements Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md), [CSV](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv).
- **“QA đã được nghiệm thu.”** Workbook chỉ có status thiết kế đã vá và chờ review. Không có căn cứ cho kết luận peer QA, M1 acceptance hay runtime PASS.

So với workbook 02J, 55 ID cũ còn đủ. Trong các dòng cũ, G12 đổi từ JSON sang mô tả RULE-011, G21 sửa một field I của MISS-009 và G34 làm rõ kiểm README. Không thấy input JSON cũ nào khác bị thay đổi. So các ca giữ nguyên input, không thấy mức/mã/lớp lỗi valid bị sửa trái nguồn. Các cột expected được mở rộng ở nhiều dòng. Hai trạng thái thành công/lỗi audit đã tách đúng và 18 D13E được bổ sung theo nhóm. Đây là kiểm hai đầu mốc, không chứng nhận mọi intermediate workbook.

So cấu trúc hai đầu mốc cho thấy Table được mở rộng, tên Table thay đổi, GAP_REVIEW được thêm và freeze QA_CHECKLIST chuyển từ A52 về A2. Bề rộng khai báo của các cột cũ giữ tại hai mốc. Không có căn cứ xác nhận từng kiểu ô/validation qua các bản trung gian chưa tìm thấy. Bản cuối của 02N-C được so trực tiếp với bản patched, xem [Excel validation](QA_WORKBOOK_VALIDATION.md).
