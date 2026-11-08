# Nguồn hiện hành và snapshot lịch sử

Tôi dùng các mốc commit dưới đây để đối chiếu bộ tài liệu M1. Đây là các bản nguồn được lưu ở đợt soạn Revision 02, không phải cam kết về HEAD hiện tại của PR #1/#2. Các liên kết commit giúp truy lại đúng phiên bản đã dùng.

## Làm rõ chính thức mới — T15 ưu tiên phần mâu thuẫn

T15: [comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), tác giả fossbk-spec, OWNER, created/updated 2026-11-08T14:01:50Z; [phản hồi gốc](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248). Comment áp dụng chung Track A, không đổi ngưỡng/rule nguồn.

D01–D03 đã được trả lời. Numeric null/missing tương đương; boolean null/missing không gây lỗi hoặc hạ mức đã đủ kết luận. Các phát biểu mâu thuẫn trong Q/A pin bên dưới (còn pending TA, null tuổi/bool invalid, thiếu HATT chưa chốt output) nay là lịch sử, không được dùng làm oracle hiện hành. [ISSUE15_SYNC.md](../ISSUE15_SYNC.md) phân biệt quy định bắt buộc và policy nhóm.

Phần Q/A không mâu thuẫn tiếp tục áp dụng. Các snapshot giữ nguyên nội dung tại mốc pin. Nếu nhánh nguồn có cập nhật, cần đối chiếu phần thay đổi trước khi sửa policy hoặc expected. Policy nhóm/mã đại diện BOOL-COVERAGE còn cần review, không phải T15 chỉ định mã cho mọi input thiếu S.

## Nguồn Revision 02 trước làm rõ — chỉ áp dụng phần không mâu thuẫn

| Ký hiệu | File snapshot | Nguồn pin / phạm vi |
|---|---|---|
| Q | [revision-02/REQUIREMENTS.md](revision-02/REQUIREMENTS.md) | [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), commit [662c47be9eba076bf9ca551403cc3e961f421d42](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/662c47be9eba076bf9ca551403cc3e961f421d42/REQUIREMENTS.md), Requirements Revision 02 |
| A | [revision-02/DECISIONS.md](revision-02/DECISIONS.md) | [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), commit [d6ba079df62a9494160ca4224f87439d5b9e7ae6](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d6ba079df62a9494160ca4224f87439d5b9e7ae6/DECISIONS.md), ADR Revision 02 |
| D | [docs/decision-table.md](docs/decision-table.md) | [Decision Table V1, tag bkt-2026-v1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), blob 95c2bbd43be8e80c8c7ecb938761a273d062c17e, clinical contract không đổi |
| E | Đề thi xuất bản | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html); dùng ràng buộc đã được Q/A truy vết, không tự thêm rule |

Q/A ghi nhận **Leader đã duyệt** các policy D04–D10/D13 và OPEN-01–OPEN-10, còn peer technical review; không gán là TA approval hoặc runtime evidence. Default audit path mechanism còn PROPOSED và unexpected internal exception còn residual review item. Nhãn pending D01–D03 trong Q/A là lịch sử trước T15; hiện đã được nguồn T15 làm rõ.

## Snapshot lịch sử — giữ nguyên, không dùng để mở lại approved policy

| Ký hiệu lịch sử | File | Mốc |
|---|---|---|
| Q0 | [REQUIREMENTS.md](REQUIREMENTS.md) | Revision 01 tại 673aaef3c320475196366103289c7c174e2d3b54 |
| G0 | [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) | Snapshot cùng mốc 673aaef3c320475196366103289c7c174e2d3b54; phần trạng thái cũ không thay Q/A Revision 02 |
| P0 | [docs/TEAM_PLAN.md](docs/TEAM_PLAN.md) | Snapshot phân vai cùng mốc; dùng ownership để bàn giao, policy mới theo Q/A |
| I0 | [ISSUE_15_COMMENTS.md](ISSUE_15_COMMENTS.md) | Bình luận đã đọc ngày 08/11/2026, nguồn [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15); không tuyên bố snapshot là trạng thái live hoặc TA trả lời |

Không sửa nội dung các snapshot cũ. Các phát biểu “chưa chọn” trong snapshot Revision 01 là lịch sử. Tham chiếu Q/A trong bộ test trỏ Revision 02 cho phần policy không mâu thuẫn; T15 có ưu tiên ở các phần đã làm rõ. Nếu upstream thay đổi sau mốc pin, review delta riêng trước khi đổi policy/expected.

Việt Đức chưa có QA Matrix. Phần đối chiếu INT/BENCH với matrix còn chờ và sẽ bổ sung nguồn khi có kết quả review.
