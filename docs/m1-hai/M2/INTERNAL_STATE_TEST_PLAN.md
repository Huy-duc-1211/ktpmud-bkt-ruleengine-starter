# D13-E — Internal math và public selection, kế hoạch M2

Nguồn hiện hành: [Requirements](../../../REQUIREMENTS.md), [ADR](../../../DECISIONS.md), [Decision Table](../../decision-table.md), [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002). Leader duyệt D13-E ngày 09/11/2026 và cập nhật cách chọn mã sau Issue #31. Hải là tác giả baseline M1-02; Huy Đức phụ trách các bản sửa với AI hỗ trợ. Peer review và kết quả thực thi cần bằng chứng riêng.

## 1. Phân tầng assertion

Pure helper dùng Enum identity trước priority, không Python truthiness. Public assert ba trường output và audit thực. Internal states/selection/explanation_assertions trong CSV là harness metadata, không input/output/audit mới. Tên helper khi code là chi tiết M2; không public debug API hoặc log raw input.

## 2. Bảng logic 81 hàng giữ nguyên

[INTERNAL_STATE_CASES.csv](INTERNAL_STATE_CASES.csv) không đổi byte: 9 AND+9 OR+3 NOT+15 cặp T/U khả thi+45 AND(count,S). Count T>=2 TRUE, T+U<2 FALSE, còn lại UNKNOWN rồi AND S. Independent static recomputation phải kiểm từng hàng, không chỉ parse; chưa gọi helper nhóm.

RULE-009–013/sáu PAIR assert count/R02 riêng, RULE-014/016/017 R02 FALSE khi R03 TRUE; MISS-010/011/012 T/U. Với MISS-013/014, R03 definite và R02 possible: R02-PV là mã đại diện theo priority trong Poss, nhưng helper R02 vẫn UNKNOWN. Giữ cả helper và public assertion.

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

1. Validation mọi trường theo D04; tuổi missing/null → THEO_DOI/null theo TA, nêu thiếu tuổi và chuyển sang audit.
2. Có tuổi: xác định Def, Poss, AllPV và AnyPV từ các completion. AllPV chứng minh phản vệ kể cả khi Def rỗng.
3. AllPV và HYPOTENSION TRUE → SOC_PHAN_VE/R-SOC. HATT thấp đơn độc không đủ điều kiện sốc phản vệ.
4. AllPV nhưng chưa xác nhận sốc → PHAN_VE; chọn rule ưu tiên cao nhất trong Poss theo R01 > R02 > R03. Rule được chọn thuộc Def là DIRECT; nếu chưa chắc chắn là CANONICAL, kể cả khi rule ưu tiên thấp hơn đã chắc chắn. Nêu mã đại diện, dữ liệu thiếu và chưa xác nhận rule riêng.
5. Mixed → THEO_DOI/null và lý do thiếu thông tin; không AnyPV → THEO_DOI/null với lý do không khớp. Không gọi Mixed là an toàn.

DIRECT/CANONICAL là nhãn nội bộ, không thêm public key hoặc audit status. Issue #31 xác nhận trực tiếp MISS-009 và nêu quy tắc chọn mã; áp dụng cho overlap definite/possible là cách nhóm áp dụng quy tắc. Giữ Enum/Kleene/T-U, không gán UNKNOWN=False. Kiểm ngữ nghĩa và disclosure để tránh hiểu mã đại diện là rule đã chắc chắn.

Sáu approved cases ở [ISSUE15_SYNC §4](../M1/ISSUE15_SYNC.md) phải giữ helper UNKNOWN ở MISS-009 nhưng canonical R01 ở public. 175 ca chính gồm 18 equivalence groups. Cặp null/missing so level/ID, không UUID hoặc reason nguyên văn.

[D13E-001–018](../M1/TEST_CASES.csv) thêm multi-U/crossovers/max64/near18; các ca MISS-013/014/TA15-BOOL3 và PEND-001 cũ đã có fixture phù hợp nên tăng selection asserts. Explanation patterns trong Expected là điều kiện cho controlled template families; required_all/forbidden_any được dùng cho ly_do, không so như public fields. Kiểm câu unsafe mẫu bị reject không chứng minh mọi câu tự nhiên đúng; cần peer review actual templates.

## 5. Property checks cần triển khai M2

- Mỗi 729 T/F/U patterns: lấy consistent worlds từ original D, không dùng expected của CSV/implementation làm oracle. u=0 có1 world, u=6 có64.
- Khi AllPV và chưa xác nhận sốc, selected rule là rule ưu tiên cao nhất trong Poss. Nếu selected thuộc Def là DIRECT; nếu không là CANONICAL, kể cả khi Def không rỗng.
- AllPV/Def rỗng vẫn bảo toàn positive; canonical chỉ PV, disclosure và không claim independent evidence. Kiểm đối chứng D13E-014 và MISS-013/014, TA15-BOOL3 null/missing.
- Mixed không promote; all-negative TD; age override, BP/nền unavailable theo TA.
- Null/missing normalization, permutation world/key-order và selection idempotence giữ level/ID.
- TIER1_MATCH phối hợp coverage và HATT, không suy từ HYPOTENSION_EVIDENCE đơn lẻ.
- Các property tests còn NOT EXECUTED trên runtime; static analysis trong remediation chỉ là evidence thiết kế. Thu helper/test name, môi trường, kết quả thật và reviewer trước khi đánh dấu AC VERIFIED.
