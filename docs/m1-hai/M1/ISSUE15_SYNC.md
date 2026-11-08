# Áp dụng làm rõ Issue #15 — comment 6722429248

Nguồn hiện hành: [Requirements Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md) (Q), [ADR Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md) (A), Decision Table (D) và [TA comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15). D13-E là **APPROVED BY LEAD — D13-E — 09/11/2026**, không phải canonical rule do TA định danh. Bản sửa TASK 02E do Leader Huy Đức sở hữu, AI hỗ trợ; chưa xác nhận Hải/Việt Đức peer review hoặc Leader nghiệm thu bản sửa.

Lịch sử: Revision 02/03 và đề xuất BOOL-COVERAGE ở baseline từng chờ review; nay nguồn hiện hành Q/A Revision 04 đã chốt D13-E. Không giao lại việc đồng bộ Requirements/ADR đã hoàn thành; chỉ đối chiếu và sửa deliverable này.

## 1. Quy định chung đã được chốt

| Điểm | Cách xử lý bắt buộc / nguồn |
|---|---|
| D01, nhiều rule Tầng 2 | Không sốc: PHAN_VE, chọn một rule theo R01-PV > R02-PV > R03-PV. Có đủ bằng chứng Tầng 1: SOC_PHAN_VE/R-SOC. [T15 §1] |
| D02, tuổi không có dữ liệu | Thiếu khóa hoặc null tuổi: THEO_DOI/null; reason nói thiếu tuổi, kể cả biểu hiện đủ rule. Tuổi thiếu ưu tiên hơn nhánh thiếu HATT. [T15 §§2,5] |
| D03, HATT hiện tại không có | Tuổi có, đủ phản vệ nhưng HATT thiếu/null: PHAN_VE và mã Tầng 2 theo thứ tự; reason nên nói chưa đánh giá tiêu chí sốc vì thiếu số đo. [T15 §3] |
| D03, người lớn thiếu nền | b>=90, nền thiếu/null: không coi nhánh giảm tương đối đã thỏa; PHAN_VE nếu đủ Tầng 2. Không gán nền mặc định; reason nên nói thiếu nền. b<90 vẫn đủ nhánh tuyệt đối. [T15 §4] |
| Numeric null/missing | tuoi, HATT, HATT nền: cả hai đều không có dữ liệu, cùng muc_do/rule_id; không coi null tuổi là TypeError. [T15 §5] |
| Boolean null/missing | Không raise vì thiếu/null; không hạ mức khi dữ liệu hiện có đã đủ rule bất kể phần còn thiếu. Chính sách cho phần phụ thuộc dữ liệu thiếu do nhóm công bố và test. [T15 §5] |

Không ghi D01–D03 là PENDING TA CONFIRMATION nữa. Giữ tên PEND-001–007 để truy vết lịch sử, cột Pending trống và cột Resolved decision ghi D01/D02/D03. Kết quả vẫn DRAFT_NOT_EXECUTED vì chưa chạy runtime.

## 2. Các thay đổi chính trong test case

| ID | Expected mới |
|---|---|
| PEND-001 | PHAN_VE/R02-PV |
| PEND-002 | THEO_DOI/null, thiếu tuổi |
| PEND-003/004 | PHAN_VE/R01-PV, thiếu HATT hiện tại |
| PEND-005/006 | PHAN_VE/R02-PV, thiếu nền |
| PEND-007 | THEO_DOI/null, thiếu tuổi dù HATT cũng thiếu |
| INV-001 | Tuổi null là dữ liệu thiếu: THEO_DOI/null trong ca này, không TypeError |
| INV-017/021/025/029/033/037 | Boolean null không invalid; với biểu hiện còn lại của các ca này trả THEO_DOI/null |
| INV-043 | R01 và số đo đã đủ sốc: SOC_PHAN_VE/R-SOC dù tiêu hóa null, không hạ mức |
| AUD-002 | Giữ mục tiêu audit invalid bằng boolean chuỗi "true", không còn dùng null làm dữ liệu invalid |

CSV chung hiện có 175 ca: giữ 157 ca baseline (135 gốc +22 T15), thêm 18 D13E-001–018. ID/input 157 ca và level/ID/exception đúng được giữ nguyên. Mã Test ID đã khôi phục về mã gốc. Số invalid hiện còn **36 =28 TypeError+8 ValueError**; không cố giữ 44 invalid trái quy định mới. INV/PEND trong ID là lịch sử, không quyết định hành vi.

[các ca T15 trong TEST_CASES.csv](TEST_CASES.csv) chứa chung **22 ca bổ sung /11 cặp null-vs-missing** cho ba trường số, cả sáu boolean, không hạ sốc và ca thực sự phụ thuộc đường hít. Các cặp phải có cùng muc_do/rule_id; không assert hai phiên có cùng UUID hoặc reason nguyên văn giống nhau.

## 3. D13-E hiện hành và ranh giới HATT/Tier1

**APPROVED BY LEAD — D13-E — 09/11/2026.** Normalization missing/null→UNKNOWN và fallback/canonical đã được Huy phê duyệt. Không gán Enum/canonical convention thành lời TA mới.

C(p) là mọi True/False completion của boolean UNKNOWN, giữ known values; không fill patient hoặc numeric. Def là rule TRUE trong mọi completion; Poss là rule TRUE ở ít nhất một completion; AllPV là mọi completion khớp ít nhất một original rule; AnyPV là tồn tại completion positive. Có 1–64 completion.

1. Validation mọi trường theo D04 trước selector; tuổi missing/null → THEO_DOI/null theo TA.
2. Có Def: chọn priority R01 > R02 > R03 trong Def, attribution DIRECT; possible rule không được đẩy definite.
3. Def rỗng/AllPV: giữ positive. PHAN_VE chọn canonical priority trong Poss, MUST disclosure mã đại diện và chưa xác nhận rule độc lập, không nói UNKNOWN=False đã được quan sát.
4. Positive definite/coverage + HYPOTENSION TRUE → SOC_PHAN_VE/R-SOC. HATT thấp đơn độc không đủ; thiếu BP hoặc adult thiếu nền không hạ positive đã chứng minh khi tuổi có.
5. Mixed → THEO_DOI/null kèm insufficient-information reason; không AnyPV → THEO_DOI/null theo không khớp. Không gọi Mixed là chắc chắn không phản vệ hoặc an toàn.

DIRECT/CANONICAL là provenance private, không public key hoặc status mới. Canonical dùng priority trong Poss là convention nhóm đã duyệt, không TA priority giữa rules đã đồng thời TRUE. Giữ Enum/Kleene/T-U; không suy mức bằng all-UNKNOWN=False. Leader đã chấp nhận residual risk consumer hiểu representative như rule definite; disclosure và negative tests vẫn bắt buộc.

Các tên sau chỉ là assertion nội bộ/harness, không thêm PatientInput/output/audit:
- HYPOTENSION: Enum TRUE/FALSE/UNKNOWN cho điều kiện số đo theo tuổi.
- HYPOTENSION_EVIDENCE: TRUE khi HYPOTENSION TRUE, còn lại FALSE nghĩa chưa có bằng chứng; không khẳng định BP bình thường.
- TIER2_COVERAGE: TRUE nếu AllPV; FALSE nếu không AnyPV; UNKNOWN nếu Mixed.
- TIER1_MATCH: Kleene AND(TIER2_COVERAGE,HYPOTENSION); chỉ TRUE đủ điều kiện R-SOC khi tuổi có. UNKNOWN không là bằng chứng sốc.
Tên SHOCK_EVIDENCE cũ diễn đạt bằng chứng HATT được thay bằng HYPOTENSION_EVIDENCE để tránh nhầm complete Tier1. Với RULE-020: HYPOTENSION=TRUE, HYPOTENSION_EVIDENCE=TRUE, TIER2_COVERAGE=FALSE, TIER1_MATCH=FALSE; output vẫn THEO_DOI/null. Không sửa giá trị HATT evidence thành FALSE để hợp output.

## 4. Sáu approved oracles và disclosure

| Test ID | muc_do | rule_id | Attribution / explanation |
|---|---|---|---|
| MISS-009 | PHAN_VE | R01-PV | CANONICAL; AllPV qua R01/R02, Def rỗng; không claim S=False hoặc R01 đã confirmed |
| TA15-BOOL1-NULL | PHAN_VE | R01-PV | CANONICAL như MISS-009, có meaningful positive/negative explanation assertions |
| TA15-BOOL1-MISSING | PHAN_VE | R01-PV | Cùng level/ID như null; không bắt cùng UUID/reason nguyên văn |
| MISS-012 | THEO_DOI | null | MIXED do G unavailable; chưa đủ thông tin, không gọi R02 FALSE như fact |
| TA15-DEPENDENT_INHALATION-NULL | THEO_DOI | null | MIXED do I unavailable; không mặc định I hoặc khẳng định an toàn |
| TA15-DEPENDENT_INHALATION-MISSING | THEO_DOI | null | Cùng Mixed semantics như null |

Mỗi row giữ Input/level/ID gốc, cột Policy review ghi approval và Nguồn dẫn Q/A Revision 04. Internal MISS-009 vẫn R01=UNKNOWN,R02=UNKNOWN,R03=FALSE. Expected.explanation_assertions là metadata harness; không trả thêm key vào ClassificationResult. Xem TEST_PLAN §3 và M2/INTERNAL_STATE_TEST_PLAN.

Lịch sử: FALSE representative từng là đề xuất của Hải; D13-E hiện chọn canonical từ Poss sau definite-first, không giả UNKNOWN=False là observed input. Bounded 64 không chứng minh latency; còn full-path audit benchmark.

## 5. Phần không thay đổi và phạm vi lượt sửa

Không đổi ngưỡng tuổi/HATT, dấu < và >30%, chín tên khóa input, ba output, bốn audit fields hoặc protocol benchmark. Miền số không phải null và khóa lạ giữ policy nhóm trước; T15 §6 cho nhóm công bố policy ở chỗ chưa quy định, không tự dùng ví dụ của thầy để thay mọi miền số.

ContextVar/UUID, audit error precedence, privacy và benchmark đã duyệt vẫn áp dụng. Null/missing được xử lý hợp lệ thì audit SUCCESS, không INVALID_INPUT chỉ vì thiếu dữ liệu. Có invalid khác hoặc audit failure vẫn theo đường lỗi đã duyệt. Default path proposal/internal exception residual không được phản hồi này giải quyết thay.

Phạm vi là tài liệu/data M1 và các kế hoạch giai đoạn sau đã tách ở M2; chưa viết classify()/loader/audit runtime. Baseline do Hải bàn giao trên docs/m1-tests-hai; remediation do Leader sở hữu trên review/m1-02-leader-remediation, AI hỗ trợ. Chưa xác nhận peer review/QA hoặc final acceptance; không tạo PR/merge trong TASK 02E.
