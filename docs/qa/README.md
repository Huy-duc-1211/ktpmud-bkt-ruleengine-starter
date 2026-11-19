# QA M1-03

Thư mục này lưu QA Matrix và hồ sơ rà soát thiết kế của nhóm `173820_n27`. Việt Đức là tác giả QA gốc. Huy Đức tiếp quản việc sửa và kiểm chứng thiết kế với công cụ AI hỗ trợ.

| Tài liệu | Mục đích |
|---|---|
| [QA_MATRIX.xlsx](QA_MATRIX.xlsx) | Workbook chính để theo dõi tiêu chí nghiệm thu, ca thiết kế, checklist và bằng chứng QA. |
| [EXECUTION_REVIEW.md](EXECUTION_REVIEW.md) | Bằng chứng thực thi và giới hạn của các trạng thái `PASS` trên ứng viên Freeze. |
| [QA_REVIEW_REPORT.md](QA_REVIEW_REPORT.md) | Báo cáo audit thiết kế, gồm phạm vi kiểm tra tĩnh và các phát hiện. |
| [QA_WORKBOOK_VALIDATION.md](QA_WORKBOOK_VALIDATION.md) | Kiểm chứng workbook và nhật ký các ô đã sửa trong TASK 02N-C. |
| [QA_REVIEW_COMPARISON.md](QA_REVIEW_COMPARISON.md) | Đối chiếu các nhận định review với dữ liệu và bằng chứng có tại thời điểm rà soát. |
| [QA_LEADER_REVIEW_NOTES.md](QA_LEADER_REVIEW_NOTES.md) | Ghi chú bàn giao cho Leader, các điểm cần review và việc chuyển sang M2/M3. |

Bốn báo cáo ghi lại trạng thái tại TASK 02N-C, trước khi Leader cập nhật cách chọn mã sau [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002). Câu “chưa mở PR #4” phản ánh thời điểm viết; PR #4 đã merge ngày 10/11/2026. Xem workbook cùng phiên bản và [Test Cases](../../TEST_CASES.csv) cho thiết kế hiện hành; báo cáo tĩnh cũ không chứng minh selector mới đã chạy. [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4)

Các URL ghim commit cũ trong cột nguồn của workbook là lịch sử để truy vết; expected và assertion sau Issue #31 được xem trong `TEST_CASES.csv` ở cùng commit với workbook. Cột bằng chứng thực thi và [báo cáo đối chiếu](EXECUTION_REVIEW.md) ghi riêng kết quả trên ứng viên; review cá nhân của Hải/Việt Đức vẫn cần xác nhận riêng.

Nguồn lịch sử của các ô nguồn rút gọn: [Requirements cũ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md), [Test Plan cũ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_PLAN.md), [Test Cases cũ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv) và [Integration Test Plan cũ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md).

Ô `GAP_REVIEW!L8` lưu tên báo cáo kiểm chứng theo thời điểm viết. Báo cáo hiện ở [QA_WORKBOOK_VALIDATION.md](QA_WORKBOOK_VALIDATION.md).

## Đọc trạng thái QA

Ca thiết kế mô tả dữ liệu và kết quả dự kiến. Sau khi đối chiếu test, CI, input QA trực tiếp và benchmark ngày 19/11, workbook ghi **11 AC `PASS` trên ứng viên, 63/64 ca QA `PASS`, 55/60 checklist `PASS`**. Các ô còn lại là `BLOCKED` do thủ tục yêu cầu SHA/tag cuối hoặc record peer review. `PASS` ở đây có phạm vi ứng viên `4be2751`, không tự là nghiệm thu TA. Xem [phương pháp và từng nhóm bằng chứng](EXECUTION_REVIEW.md), [CI PR #10](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44479428343) và [benchmark ứng viên](../testing/BENCHMARK_REPORT.md).

A-11 trong Requirements ghi `VERIFIED` cho disclaimer trong README gốc. Bản ứng viên cũng có nguyên văn chuỗi; QA-033/CHK-029/045 chờ permalink README ở SHA cuối theo thủ tục của chính các dòng này. [Requirements hiện hành](../../REQUIREMENTS.md#7-tiêu-chí-nghiệm-thu) · [README tại commit bằng chứng](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/README.md#L43)

Đối chiếu rule, ca thiết kế và kế hoạch kiểm thử qua [chỉ mục M1-02](../design/README.md).

**Cập nhật quyết định M2:** Leader chọn thử ghi `INTERNAL_ERROR` cho lỗi bất ngờ ở validator hoặc rule; phân biệt lỗi input sai thực sự, giữ bốn trường và ưu tiên lỗi audit khi ghi thất bại. Xem [Integration Test Plan](../testing/INTEGRATION_TEST_PLAN.md#2-các-tình-huống-cần-kiểm-thử). Các ô workbook mô tả lỗi rule chưa bao phủ riêng lỗi validator; PR #7 đã bổ sung test audit/validator để đối chiếu riêng. Leader đã chọn hướng xử lý đuôi JSONL theo phương án Hải; code và test đã tích hợp, còn cần review độc lập và đối chiếu SHA/tag Freeze.
