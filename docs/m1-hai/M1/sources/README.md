# Nguồn hiện hành Revision 04 và snapshots lịch sử

TASK 02E — Huy Đức sở hữu remediation, AI hỗ trợ. Ngày 09/11/2026. Không sửa/ghi đè các snapshot cũ.

## 1. Thứ tự thẩm quyền và nguồn hiện hành

Decision Table + TA > approved team policy Q/A Revision 04 > đề xuất chưa duyệt > source snapshots lịch sử > ghi chú.

| Ký hiệu hiện hành | Nguồn pin | Phạm vi |
|---|---|---|
| Q | [REQUIREMENTS.md Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md), a574ce20fbf307ad90f0d60064da394652462aea, PR #1 | §3 validation/normalization, §4.2 D13-E, §5 output attribution, §8.2 six approved expected |
| A | [DECISIONS.md Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md), 7af011f3f95e21ac829a163ee4be36200c1e7d88, PR #2 | §5.8 D13-E, §9.4 six expected; giữ default path/internal exception unresolved |
| D | [Official Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag bkt-2026-v1, blob95c2bbd43be8e80c8c7ecb938761a273d062c17e | Chín input, ba output, formulas và ngưỡng duy nhất |
| T15 | [fossbk-spec comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), created/updated 2026-11-08T14:01:50Z | D01–D03, null/missing và quyền chọn policy khoảng trống |
| E | [Đề chính thức Track A](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html) | AC A-01–A-11, audit/privacy/CI/benchmark |

Q/A trong CSV và M2 plans nay trỏ bảng hiện hành này; không dùng alias Q/A cho Revision 02. Quyền/phê duyệt D13-E do Leader, không phải TA đã chỉ định canonical ID. Nhãn **APPROVED BY LEAD — D13-E — 09/11/2026** đã được ghi ở cả Q/A; không cần giao Leader làm lại việc xuất bản Revision 04.

## 2. Snapshots lịch sử bất biến

| Ký hiệu lịch sử | File lưu | Mốc / giới hạn |
|---|---|---|
| Q2 | [revision-02/REQUIREMENTS.md](revision-02/REQUIREMENTS.md) | 662c47be9eba076bf9ca551403cc3e961f421d42; nguồn trước TA/D13-E approval, không current oracle |
| A2 | [revision-02/DECISIONS.md](revision-02/DECISIONS.md) | d6ba079df62a9494160ca4224f87439d5b9e7ae6; giữ lịch sử, không mở lại decisions |
| Q0 | [REQUIREMENTS.md](REQUIREMENTS.md) | 673aaef3c320475196366103289c7c174e2d3b54, Revision 01 |
| G0 | [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) | Snapshot cùng mốc Q0, có trạng thái cũ; không sửa trong task |
| P0 | [docs/TEAM_PLAN.md](docs/TEAM_PLAN.md) | Snapshot phân công, không ghi đè policy hiện hành |
| D0 | [docs/decision-table.md](docs/decision-table.md) | Official table copy tại tag, không sửa |
| I0 | [ISSUE_15_COMMENTS.md](ISSUE_15_COMMENTS.md) | Snapshot câu hỏi trước phản hồi; không được dùng để nói TA hiện chưa trả lời |

History Q3/A3 trước approval: Requirements c855c6d4f2135a14ad94485734d4d2e604cb9cff và ADR 7a62d90dcd774c3b3e1ffbfa07d60aee695f1b41, xem lịch sử Q/A live pin hiện hành. Không tạo copy thay thế hoặc ghi đè snapshots.

## 3. Provenance remediation

Baseline của Hải 768f196e6a9ec3b1142c44399ce8288f7cc2e87e trên docs/m1-tests-hai; giữ tác giả/lịch sử và original branch. Bản sửa trên review/m1-02-leader-remediation, owner Huy Đức/AI hỗ trợ. TASK 02D review độc lập chỉ là evidence/rationale, TASK 02F là recommendation; approval D13-E nằm ở Q/A Revision 04 sau TASK 02G.

Current source không imply peer review, M1 acceptance hoặc runtime/CI/benchmark đã đạt. QA Matrix chưa được cung cấp/xác minh ở task; Việt Đức cần map/review riêng. Default audit path vẫn PROPOSED — AWAITING PEER REVIEW, unexpected internal exception residual; CON-004 nonmutation còn đề nghị kỹ thuật riêng. Không đổi các mục này nhờ approval D13.
