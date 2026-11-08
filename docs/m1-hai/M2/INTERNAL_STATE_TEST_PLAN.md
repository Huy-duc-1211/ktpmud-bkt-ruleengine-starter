# D13-E — Internal math và public selection, kế hoạch M2

Nguồn hiện hành: [Requirements Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md) (Q), [ADR Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md) (A), Decision Table (D) và [TA comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15). D13-E là **APPROVED BY LEAD — D13-E — 09/11/2026**, không phải canonical rule do TA định danh. Bản sửa TASK 02E do Leader Huy Đức sở hữu, AI hỗ trợ; chưa xác nhận Hải/Việt Đức peer review hoặc Leader nghiệm thu bản sửa.

## 1. Phân tầng assertion

Pure helper dùng Enum identity trước priority, không Python truthiness. Public assert ba trường output và audit thực. Internal states/selection/explanation_assertions trong CSV là harness metadata, không input/output/audit mới. Tên helper khi code là chi tiết M2; không public debug API hoặc log raw input.

## 2. Bảng logic 81 hàng giữ nguyên

[INTERNAL_STATE_CASES.csv](INTERNAL_STATE_CASES.csv) không đổi byte: 9 AND+9 OR+3 NOT+15 cặp T/U khả thi+45 AND(count,S). Count T>=2 TRUE, T+U<2 FALSE, còn lại UNKNOWN rồi AND S. Independent static recomputation phải kiểm từng hàng, không chỉ parse; chưa gọi helper nhóm.

RULE-009–013/sáu PAIR assert count/R02 riêng, RULE-014/016/017 R02 FALSE khi R03 TRUE; MISS-010/011/012 T/U; MISS-013/014 R03 definite và R02 chỉ possible. Public SOC/R03 không chứng minh R02 đúng, nên giữ cả helper và public assertion.

## 3. HATT evidence khác complete Tier1

Các tên sau chỉ là assertion nội bộ/harness, không thêm PatientInput/output/audit:
- HYPOTENSION: Enum TRUE/FALSE/UNKNOWN cho điều kiện số đo theo tuổi.
- HYPOTENSION_EVIDENCE: TRUE khi HYPOTENSION TRUE, còn lại FALSE nghĩa chưa có bằng chứng; không khẳng định BP bình thường.
- TIER2_COVERAGE: TRUE nếu AllPV; FALSE nếu không AnyPV; UNKNOWN nếu Mixed.
- TIER1_MATCH: Kleene AND(TIER2_COVERAGE,HYPOTENSION); chỉ TRUE đủ điều kiện R-SOC khi tuổi có. UNKNOWN không là bằng chứng sốc.
Tên SHOCK_EVIDENCE cũ diễn đạt bằng chứng HATT được thay bằng HYPOTENSION_EVIDENCE để tránh nhầm complete Tier1. Với RULE-020: HYPOTENSION=TRUE, HYPOTENSION_EVIDENCE=TRUE, TIER2_COVERAGE=FALSE, TIER1_MATCH=FALSE; output vẫn THEO_DOI/null. Không sửa giá trị HATT evidence thành FALSE để hợp output.

Raw null/missing hợp lệ; non-null sai kiểu vẫn TypeError. Ba numeric unavailable theo TA, không gán số đo. PEND-002/007 age override; PEND-003/004 giữ PV thiếu BP; PEND-005/006 giữ PV adult thiếu nền; b<90 đủ absolute khi positive được chứng minh. Rule thấp BP đơn độc RULE-020 phải ở THEO_DOI/null.

## 4. Coverage, attribution và explanation

C(p) là mọi True/False completion của boolean UNKNOWN, giữ known values; không fill patient hoặc numeric. Def là rule TRUE trong mọi completion; Poss là rule TRUE ở ít nhất một completion; AllPV là mọi completion khớp ít nhất một original rule; AnyPV là tồn tại completion positive. Có 1–64 completion.

1. Validation mọi trường theo D04 trước selector; tuổi missing/null → THEO_DOI/null theo TA.
2. Có Def: chọn priority R01 > R02 > R03 trong Def, attribution DIRECT; possible rule không được đẩy definite.
3. Def rỗng/AllPV: giữ positive. PHAN_VE chọn canonical priority trong Poss, MUST disclosure mã đại diện và chưa xác nhận rule độc lập, không nói UNKNOWN=False đã được quan sát.
4. Positive definite/coverage + HYPOTENSION TRUE → SOC_PHAN_VE/R-SOC. HATT thấp đơn độc không đủ; thiếu BP hoặc adult thiếu nền không hạ positive đã chứng minh khi tuổi có.
5. Mixed → THEO_DOI/null kèm insufficient-information reason; không AnyPV → THEO_DOI/null theo không khớp. Không gọi Mixed là chắc chắn không phản vệ hoặc an toàn.

DIRECT/CANONICAL là provenance private, không public key hoặc status mới. Canonical dùng priority trong Poss là convention nhóm đã duyệt, không TA priority giữa rules đã đồng thời TRUE. Giữ Enum/Kleene/T-U; không suy mức bằng all-UNKNOWN=False. Leader đã chấp nhận residual risk consumer hiểu representative như rule definite; disclosure và negative tests vẫn bắt buộc.

Sáu approved cases ở [ISSUE15_SYNC §4](../M1/ISSUE15_SYNC.md) phải giữ helper UNKNOWN ở MISS-009 nhưng canonical R01 ở public. 175 ca chính gồm 18 equivalence groups. Cặp null/missing so level/ID, không UUID hoặc reason nguyên văn.

[D13E-001–018](../M1/TEST_CASES.csv) thêm multi-U/crossovers/max64/near18; các ca MISS-013/014/TA15-BOOL3 và PEND-001 cũ đã có fixture phù hợp nên tăng selection asserts. Explanation patterns trong Expected là điều kiện cho controlled template families; required_all/forbidden_any được dùng cho ly_do, không so như public fields. Kiểm câu unsafe mẫu bị reject không chứng minh mọi câu tự nhiên đúng; cần peer review actual templates.

## 5. Property checks cần triển khai M2

- Mỗi 729 T/F/U patterns: lấy consistent worlds từ original D, không dùng expected của CSV/implementation làm oracle. u=0 có1 world, u=6 có64.
- Khi Def có, selected rule trong Def và priority, không possible cao hơn thắng.
- AllPV/Def rỗng bảo toàn positive; canonical chỉ PV, disclosure và không claim independent evidence.
- Mixed không promote; all-negative TD; age override, BP/nền unavailable theo TA.
- Null/missing normalization, permutation world/key-order và selection idempotence giữ level/ID.
- TIER1_MATCH phối hợp coverage và HATT, không suy từ HYPOTENSION_EVIDENCE đơn lẻ.
- Các property tests còn NOT EXECUTED trên runtime; static analysis trong remediation chỉ là evidence thiết kế. Thu helper/test name, môi trường, kết quả thật và reviewer trước khi đánh dấu AC VERIFIED.
