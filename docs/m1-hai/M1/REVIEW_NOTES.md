# Ghi chú remediation TASK 02E — Leader-owned

> **Bối cảnh lịch sử:** Nội dung dưới ghi nhận TASK 02E/02Q tại thời điểm thực hiện; các chữ “hiện hành” hoặc “chờ review” trong báo cáo phản ánh mốc đó. Sau Issue #31, cách chọn mã đã được nhóm cập nhật: xem [RULE_DESIGN](RULE_DESIGN.md), [TEST_PLAN](TEST_PLAN.md) và [Requirements](../../../REQUIREMENTS.md). Không dùng báo cáo tĩnh cũ làm bằng chứng chạy hoặc kết quả kiểm cho selector mới.

Nguồn hiện hành: [Requirements Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md) (Q), [ADR Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md) (A), Decision Table (D) và [TA comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15). D13-E là **APPROVED BY LEAD — D13-E — 09/11/2026**, không phải canonical rule do TA định danh. Bản sửa TASK 02E do Leader Huy Đức sở hữu, AI hỗ trợ; chưa xác nhận Hải/Việt Đức peer review hoặc Leader nghiệm thu bản sửa.

## 1. Finding được tái hiện ở baseline và bản sửa

| Finding | Baseline 768f196 | Repair / tiêu chí static cần kiểm |
|---|---|---|
| F01 P1 | MISS-012, TA15-DEPENDENT_INHALATION-* Policy review trống; chỉ representative có proposal tag | Đủ sáu rows ghi approval D13-E/current source; giữ original Input/level/ID; tách policy approval khỏi runtime/peer acceptance |
| F02 P2 | ISSUE15_SYNC/HANDOFF/REVIEW_RESPONSE còn giao Leader sync Q/A cũ | Q/A Revision 04 là current source; Q2/A2/Q0 archived, không overwrite snapshots; không yêu cầu làm lại TASK 02G |
| F03 P2 | TA15-BOOL1-* thiếu representative uncertainty assertions | Cả ba canonical rows có required/forbidden explanation patterns; safe sample khớp, unsafe S=False/independent-R01 claim phải fail; actual ly_do chưa chạy |
| F04 P2 | Chỉ S single-U coverage; thiếu multi-U/max64/numeric crossover | 18 D13E-001–018 mới có mục tiêu; thêm property plan729, giữ ca cũ DefR03/PossR02 và tăng selection assertions; boundary17.99/18 có nhánh relative phân biệt |

Revision 04 đã giải quyết quyết định chính sách của F01; việc sửa labels/source/assertions trong file Hải vẫn cần và được thực hiện ở nhánh này. Không chỉ đổi chữ APPROVED để che các gap F03/F04. Đây là kết quả remediation cần Leader kiểm tra, không review chéo/final acceptance đã hoàn tất.

## 2. RULE-020 và các trạng thái

SHOCK_EVIDENCE baseline=TRUE có nghĩa bằng chứng HATT, không sai oracle theo contract helper cũ. Bản sửa dùng tên HYPOTENSION_EVIDENCE và TIER1_MATCH để loại nhập nhằng: RULE-020 có HATT evidence TRUE nhưng Tier2 FALSE/Tier1 FALSE, output THEO_DOI/null. Không đổi input, output hoặc ngưỡng. TIER1_MATCH là Kleene AND của coverage-state và HATT-state, có thể UNKNOWN, không status runtime mới.

## 3. D13-E approved, không còn current approval gate

Boolean missing/null UNKNOWN, Def trước Poss, AllPV positive, canonical disclosure khi PV/Def rỗng, Mixed TD/null. MISS-009 helpers vẫn UNKNOWN/UNKNOWN/FALSE; mã public R01 không làm helper thành TRUE. Source/current oracle theo Q §8.2/A §9.4. Canonical risk đã được Leader chấp nhận; TA chỉ cho quyền policy, không định danh canonical rule.

## 4. Phần giữ nguyên và còn chờ

D01–D03 TA-confirmed; strict D04, Enum/Kleene/count và D05–D10 không đổi. ContextVar/UUID, audit schema/error precedence/isolation/benchmark giữ nguyên. 36 invalid (28 TypeError/8 ValueError), INV nullable và AUD-002 chuỗi giữ expected. Không có runtime test/CI/benchmark hoặc QA acceptance mới.

Default path còn PROPOSED — AWAITING PEER REVIEW; unexpected internal exception residual. CON-004 nonmutation vẫn đề nghị kỹ thuật, không được approval D13 tự nâng thành AC bắt buộc.

## 5. Attribution và nghiệm thu

Baseline là đóng góp của Hải; remediation do Huy Đức sở hữu, AI hỗ trợ trên nhánh mới. Không gán Hải/Việt Đức đã review bản sửa. QA Matrix chưa được cung cấp/xác minh trong task; chờ Việt Đức map/review. Leader tự kiểm checklist HANDOFF và quyết định acceptance/tích hợp/PR/merge riêng.
