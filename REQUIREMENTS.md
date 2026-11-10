# Yêu cầu và phạm vi Track A

| Thuộc tính | Giá trị |
|---|---|
| Cuộc thi | KTPMUD Hack Marathon 2026, Track A — Dr May Day: Rule Engine Sprint |
| Mã nhóm | `173820_n27` |
| Người phụ trách | Huy Đức |
| Mốc bàn giao | M1-01, Checkpoint 1, ngày 08/11/2026 |
| Phiên bản | Revision 04 |
| Cập nhật | 11/11/2026 |
| Trạng thái | M1 Revision 04 đã tích hợp vào `track-a-development` ngày 10/11/2026; chưa có xác nhận nghiệm thu scope của TA hoặc bằng chứng kiểm thử runtime |
| Mốc nguồn starter | `bkt-2026-v1` → `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Mốc nguồn tích hợp | `track-a-development` tại `9bc4fc186415d7a13cd9d49692c50f3c945ddf7b` (merge commit PR #4, hoàn tất tích hợp M1 ngày 10/11/2026) |
| Baseline trước Revision 04 | `c855c6d4f2135a14ad94485734d4d2e604cb9cff` trên `docs/m1-requirements-huy`; snapshot Revision 03, không phải HEAD sau patch này |
| Làm rõ chính thức | [fossbk-spec — Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), ngày 08/11/2026; nguồn TA cho D01–D03 và null/missing |

Revision 04 được hoàn thiện trên nhánh `docs/m1-requirements-huy` và đã **merge qua [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1)** vào `track-a-development` ngày 10/11/2026. Cùng ngày, [PR #2 (ADR)](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3 (Rule Design/Test Plan)](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) và [PR #4 (QA Matrix)](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) cũng đã merge. GitHub ghi nhận Leader self-review dạng `COMMENTED` và tài khoản `nvldvc` `APPROVED` trên cả bốn PR; chưa có lượt review của thành viên còn lại tại thời điểm merge. Quyết định tích hợp thuộc Leader và có ghi nhận ngoại lệ review. Đây là **hoàn tất tích hợp hồ sơ thiết kế nội bộ**, không phải bằng chứng TA đã duyệt Checkpoint 1 hoặc A-01–A-11 đã được kiểm chứng.

**Thứ tự nguồn:** Decision Table V1 và làm rõ TA [TA] cao hơn quyết định nội bộ đã duyệt; quyết định nội bộ cao hơn đề xuất. TA không yêu cầu riêng Kleene logic hoặc Enum. Mười OPEN và phần D04–D13 không bị TA thay thế vẫn giữ hiệu lực theo quyết định của Leader; lượt approval trên PR là review tài liệu, không thay thế kiểm chứng triển khai M2 và việc xử lý các điểm kỹ thuật còn mở. D01–D03 đã được TA xác nhận cho các tình huống được trả lời, không còn là câu hỏi chờ TA.

**APPROVED BY LEAD — D13-E — 09/11/2026.** Leader phê duyệt D13-E — Evidence-first Boolean Coverage with Canonical Attribution trong TASK 02G và chấp nhận residual risk về nghĩa mã đại diện. Đây là APPROVED TEAM POLICY trong quyền TA §§5–6, không phải quy tắc TA mới. PR đã được review và tích hợp, nhưng điều đó không đồng nghĩa TA nghiệm thu giải pháp hay AC được xác minh. Chỉ phê duyệt D13; default audit path và unexpected internal exception giữ trạng thái riêng. [L; TA]


## 1. Giới thiệu


Phạm vi Hack Marathon là mô-đun Rule Engine Python phân loại dữ liệu giả lập theo bảng quyết định đã khóa. Starter có interface `classify(patient)` nhưng thân hàm đang phát sinh `NotImplementedError`. Mục tiêu của nhóm là chuyển đặc tả thành yêu cầu đầu vào/đầu ra có thể kiểm chứng, kết quả giải thích được và bằng chứng về tính đúng, audit an toàn cùng hiệu năng. [E §§4–7, 9; C dòng 11–36]

Sinh viên phát triển và bảo trì mô-đun. Các thành viên review yêu cầu, thiết kế và hành vi. Giảng viên/TA xem xét phạm vi và đánh giá bài làm. Dữ liệu giả lập phục vụ kiểm thử và trình diễn. Mô-đun bài thi chưa được xác minh hoặc phê duyệt cho sử dụng lâm sàng. Cảnh báo bắt buộc được giữ nguyên là `educational/synthetic — not for clinical use`. [E §§5–7, 12]

## 2. Phạm vi

| Trong phạm vi | Ngoài phạm vi |
|---|---|
| Phân loại bằng quy tắc và validation theo bảng quyết định cùng chính sách nhóm đã duyệt | Website, giao diện bệnh viện hoặc giao diện ngoài yêu cầu bài thi |
| Output ba trường, giải thích truy vết được và audit bốn trường | Dữ liệu bệnh nhân thật, hệ thống quản lý bệnh nhân hoặc cơ sở dữ liệu thật |
| Kiểm thử tự động, kiểm chứng từ bản checkout sạch, CI trên PR và benchmark | AI/ML hoặc LLM suy đoán kết quả phân loại |
| Yêu cầu, bằng chứng thiết kế/kiểm chứng, bảo mật, riêng tư và bàn giao | Tích hợp production, chẩn đoán hoặc khuyến nghị điều trị, quy tắc hoặc ngưỡng lâm sàng tự bổ sung |

Bản M1 đã tích hợp mô tả yêu cầu và phương pháp kiểm chứng dự kiến; đây vẫn là **đầu ra thiết kế**, chưa phải kết quả thực thi. Chi tiết test case thuộc Test Plan, còn lý do và đánh đổi thiết kế thuộc ADR. Mốc Checkpoint 1 theo đề là cuối ngày 08/11/2026; trường hợp chưa nộp có hướng bổ sung hồ sơ trên fork trước 9:30 ngày 11/11 theo [erratum #25](https://github.com/fossbk-spec/ktpmud-project/issues/25). [E §§4–7; G §§2, 5; P §3]

## 3. Đặc tả dữ liệu đầu vào

Danh sách cho phép vẫn đúng chín tên khóa. Missing là khóa vắng mặt; null là khóa hiện diện với giá trị None. Data Dictionary gốc [D] khóa tên/ý nghĩa trường; [TA §5] làm rõ unavailable được phép cho ba trường số và sáu boolean. TypedDict(total=False) chỉ mô tả kiểu tĩnh, không thực thi validation runtime. Không thêm UUID/path hoặc khóa định danh vào PatientInput.

| Tên trường chính xác | Kiểu theo nguồn chính thức | Mô tả | Chính sách null/missing hiện hành | Validation và hành vi | Nguồn |
|---|---|---|---|---|---|
| `tuoi` | float (năm); missing/null theo TA | Tuổi cho phép số lẻ như 0.5 | Null và missing đều là tuổi chưa có | Giữ int/float hữu hạn ≥0, loại bool; không ép chuỗi. None/missing không tự gây TypeError. Khi Tầng 2 TRUE nhưng tuổi unavailable: THEO_DOI / null. | D dòng 12; TA §§2,5; D04 |
| `huyet_ap_tam_thu` | int hoặc null; cho phép thiếu | HATT hiện tại, mmHg | Null và missing tương đương unavailable | Giữ int ≥0, loại bool/float/chuỗi; không đặt trần. HATT=0 vẫn hợp lệ theo policy nhóm. Nếu tuổi có và Tầng 2 TRUE nhưng HATT unavailable: PHAN_VE / rule Tầng 2 được chọn. | D dòng 13; TA §§3,5; D04 |
| `huyet_ap_tam_thu_nen` | int hoặc null; cho phép thiếu | HATT nền cho nhánh giảm tương đối ở tuổi ≥18 | Null và missing tương đương unavailable | Nếu có số phải int >0, loại bool/float/chuỗi; nền 0 vẫn invalid. Ở người lớn HATT <90 đủ chứng minh nhánh tuyệt đối; HATT ≥90 thiếu nền không chặn Tầng 2 đã xác nhận. | D dòng 14,35; TA §§4,5; D04 |
| `co_di_nguyen_nghi_ngo` | bool; missing/null được TA cho phép | Có dị nguyên nghi ngờ; xuất hiện cả nhánh phủ định và khẳng định | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN theo D13-E đã duyệt ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `di_nguyen_qua_duong_hit` | bool; missing/null được TA cho phép | Dị nguyên qua đường hít, ảnh hưởng nhánh hô hấp R03 | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN theo D13-E đã duyệt ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_ton_thuong_da_niem_mac` | bool; missing/null được TA cho phép | Tổn thương da/niêm mạc | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN theo D13-E đã duyệt ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_trieu_chung_ho_hap` | bool; missing/null được TA cho phép | Triệu chứng hô hấp | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN theo D13-E đã duyệt ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_trieu_chung_tuan_hoan` | bool; missing/null được TA cho phép | Triệu chứng tuần hoàn | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN theo D13-E đã duyệt ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_trieu_chung_tieu_hoa_nang` | bool; missing/null được TA cho phép | Triệu chứng tiêu hóa nặng | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN theo D13-E đã duyệt ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |

### 3.1. D04 — Validation nghiêm ngặt, được TA thay thế một phần

**TA-CONFIRMED:** tuổi null không còn bị coi là input invalid; boolean null không còn bị coi là sai kiểu chỉ vì null. Thiếu/null HATT hiện tại và nền là unavailable hợp lệ. Các quy tắc nội bộ cũ trái các điểm này đã được thay thế trong Revision 03. Không đồng nhất unavailable với invalid. [TA §§2–5]

**APPROVED BY LEAD — phần không bị thay thế:** non-null sai kiểu raise TypeError; sai miền số hoặc khóa ngoài allowlist raise ValueError. Giữ tuổi hữu hạn ≥0, HATT hiện tại int ≥0 và nền int >0 nếu có số; bool không thay số, không ép kiểu, không tự đặt giới hạn trên. Ví dụ “huyết áp ≤0” ở TA §6 là phạm vi nhóm được chọn policy, không phải lệnh sửa policy đã duyệt: HATT hiện tại 0 tiếp tục hợp lệ, nền 0 tiếp tục invalid.

Validate mọi trường có mặt trước suy luận. Một trường invalid không được bỏ qua vì rule khác đã TRUE. Không đổi invalid thành UNKNOWN hoặc trả THEO_DOI để che lỗi dữ liệu. Nếu audit thành công, phát sinh TypeError/ValueError đúng D04; lỗi kép ưu tiên lỗi audit an toàn theo §4.4. Không đưa raw input hoặc dữ liệu nhạy cảm vào message/chaining/log. [L; TA §6]

### 3.2. D13-E — Chuẩn hóa boolean đã được Leader phê duyệt

**APPROVED BY LEAD — D13-E — 09/11/2026.** Giữ Enum TRUE/FALSE/UNKNOWN, Kleene AND/OR/NOT và R02 T/U đã duyệt. Boolean True/False đúng kiểu → TRUE/FALSE; thiếu khóa hoặc explicit null → UNKNOWN. Non-null sai kiểu vẫn TypeError theo D04; không đổi invalid thành UNKNOWN hoặc tự ép kiểu. Quy định không exception chỉ vì missing/null là TA; representation, coverage, fallback và canonical attribution là lựa chọn nhóm đã duyệt. [TA §5; L]

| Dữ liệu boolean nhận được | Xử lý | Nguồn thẩm quyền |
|---|---|---|
| Có True đúng kiểu bool | TRUE | Thiết kế nội bộ đã duyệt |
| Có False đúng kiểu bool | FALSE | Thiết kế nội bộ đã duyệt |
| Thiếu khóa hoặc null/None | UNKNOWN; không tự exception | TA cho unavailable; normalization theo D13-E đã duyệt |
| Số, chuỗi hoặc non-null sai kiểu | TypeError, không UNKNOWN | D04 không bị thay thế |

Raw input khác trạng thái nội bộ; UNKNOWN không phải giá trị input mới hoặc output thứ tư. Không fill patient bằng giá trị giả. HATT unavailable có thể giữ trạng thái điều kiện UNKNOWN; lựa chọn output vẫn theo TA/D13-E ở §4.2. Không biến UNKNOWN thành False để kết luận mức.

## 4. Yêu cầu chức năng và quy tắc xử lý

### 4.1. Yêu cầu chức năng

| ID | Yêu cầu | Phân loại nguồn và căn cứ |
|---|---|---|
| FR-01 | Thực thi classify(patient), điều phối validation, rule evaluation, classification/explanation và audit kể cả direct call. Không đổi signature hoặc phụ thuộc ID fixture; UUID/context ngoài PatientInput. | FACT — C; E A-01–A-02. Thiết kế D05/D07 đã duyệt. |
| FR-02 | R01-PV khớp khi `co_di_nguyen_nghi_ngo = false` **VÀ** `co_ton_thuong_da_niem_mac = true` **VÀ** (`co_trieu_chung_ho_hap = true` **HOẶC** `co_trieu_chung_tuan_hoan = true`). | FACT — D dòng 41. D13 quy định cách đánh giá khóa boolean vắng mặt. |
| FR-03 | R02-PV khớp khi `co_di_nguyen_nghi_ngo = true` **VÀ** ít nhất hai trong bốn nhóm da/niêm mạc, hô hấp, tuần hoàn, tiêu hóa nặng là true. | FACT — D dòng 42. D13 quy định cách xác định trạng thái điều kiện đếm khi thiếu dữ liệu. |
| FR-04 | R03-PV khớp khi `co_di_nguyen_nghi_ngo = true` **VÀ** ((`di_nguyen_qua_duong_hit = false` **VÀ** `co_trieu_chung_ho_hap = true`) **HOẶC** `co_trieu_chung_tuan_hoan = true`). Dùng đúng trường dị nguyên nghi ngờ trong biểu thức. | FACT — D dòng 43. Giữ nguyên ngoặc và AND/OR khi áp dụng D13. |
| FR-05 | R-SOC cần phản vệ được chứng minh bởi rule definite hoặc AllPV theo D13-E, VÀ bằng chứng tụt HATT theo bảng. Tuổi missing/null → THEO_DOI/null. Tuổi có, thiếu current BP hoặc adult current ≥90 thiếu nền không chặn positive đã được chứng minh; không tự gán BP/nền. | D dòng 25–35; TA §§2–5; D13-E (L). |
| FR-06 | Sau validation mọi trường: tuổi unavailable override THEO_DOI/null. Khi tuổi có, chọn rule definite ưu tiên R01 > R02 > R03; không để possible đẩy definite. Nếu Def rỗng nhưng AllPV, giữ positive; PHAN_VE dùng mã canonical ưu tiên trong Poss và disclosure theo §4.2/§5. Positive + bằng chứng hypotension → SOC_PHAN_VE/R-SOC. Mixed hoặc không completion positive → THEO_DOI/null, phân biệt thiếu thông tin với không khớp. | D; TA; APPROVED TEAM POLICY D13-E. |
| FR-07 | Áp dụng §3: missing/null được TA cho phép không tự invalid; boolean unavailable → UNKNOWN theo D13-E đã duyệt. Non-null sai kiểu, sai miền và khóa lạ vẫn D04. Validate mọi trường kể cả unrelated invalid trước suy luận; không ép kiểu. | TA §§5–6; D04/D13-E; E A-04. |
| FR-08 | Trả đúng ba trường §5. ly_do nêu rule/kết quả và thiếu tuổi/current BP/nền khi tương ứng. PHAN_VE/CANONICAL phải công bố mã đại diện và chưa xác nhận rule riêng, không khẳng định unknown=False đã được quan sát. DIRECT gắn rule definite; Mixed nêu insufficient information, không kết luận an toàn. Không raw input/điều trị. | D dòng 49–55; TA §§1–4; D06 và D13-E. |
| FR-09 | Public classify() audit đúng Timestamp, User_UUID, Action_Type, Status. Lần phân loại hợp lệ hoàn tất gồm output do dữ liệu unavailable dùng SUCCESS; không ghi INVALID_INPUT chỉ vì missing/null được TA cho phép. Invalid thực sự theo D04 vẫn audit INVALID_INPUT khi writer thành công. Giữ fail-closed và ưu tiên lỗi audit khi lỗi kép. | E A-06; D05/D07/D08; TA §5. |

| Tuổi tính bằng năm | Điều kiện tụt HATT cho FR-05 |
|---|---|
| 0 ≤ tuổi < 1 | HATT < 70 mmHg |
| 1 ≤ tuổi < 11 | HATT < 70 + 2 × tuổi, đơn vị mmHg |
| 11 ≤ tuổi < 18 | HATT < 90 mmHg |
| Tuổi ≥ 18 | HATT < 90 mmHg **HOẶC** giảm > 30% so với HATT nền |

Các ngưỡng và dấu so sánh giữ nguyên. Với người lớn, giảm >30% tương đương HATT <0,7 × nền; giảm đúng 30% không thỏa. Thiếu nền không cần cho nhánh HATT <90 đã TRUE. Nếu nhánh tuyệt đối không thỏa và nền unavailable, nhánh tương đối không được tính là đã thỏa để xếp Tầng 1; đây không phải bằng chứng huyết áp bình thường. [D; TA §4]

### 4.2. D13-E — Evidence-first Boolean Coverage with Canonical Attribution

**APPROVED BY LEAD — D13-E — 09/11/2026.** Các định nghĩa/selection dưới đây là policy nhóm, không gán là TA đã định danh kết quả cho từng ca thiếu boolean.

Giữ nguyên biểu thức R01/R02/R03. AND: có FALSE → FALSE, mọi vế TRUE → TRUE, còn lại UNKNOWN. OR: có TRUE → TRUE, mọi vế FALSE → FALSE, còn lại UNKNOWN. NOT TRUE → FALSE, NOT FALSE → TRUE, NOT UNKNOWN → UNKNOWN. Không dùng truthiness của Enum hay ép UNKNOWN thành False. [L]

| Biểu thức minh họa | Trạng thái nội bộ |
|---|---|
| TRUE OR UNKNOWN | TRUE |
| FALSE OR UNKNOWN | UNKNOWN |
| FALSE AND UNKNOWN | FALSE |
| TRUE AND UNKNOWN | UNKNOWN |

R02: T là số hệ TRUE, U là số hệ UNKNOWN. T ≥2 → điều kiện đếm TRUE; T+U <2 → FALSE; còn lại UNKNOWN. Sau đó AND với co_di_nguyen_nghi_ngo như bảng gốc. Rule chắc chắn TRUE không bị mất hiệu lực vì rule khác UNKNOWN. Chọn trong các rule TRUE theo thứ tự TA; vẫn áp dụng tuổi missing/null → THEO_DOI và ưu tiên R-SOC khi có bằng chứng. [TA §§1–5; L]

Với p hợp lệ, C(p) là mọi completion True/False của boolean unavailable, giữ nguyên giá trị đã biết; có 1–64 completion. Chỉ đánh giá biểu thức R01/R02/R03 gốc. Không hoàn thiện numeric hoặc ghi dữ liệu giả vào input.
- Def: rule TRUE trong mọi completion (definite).
- Poss: rule TRUE trong ít nhất một completion (possible).
- AllPV: mọi completion khớp ít nhất một rule Tầng 2.
- AnyPV: có ít nhất một completion khớp Tầng 2.
Các tập/ký hiệu là nội bộ, không field public.

Thứ tự chuẩn tắc:
1. Validation mọi trường theo D04 trước selector. Tuổi missing/null → THEO_DOI/null, nêu thiếu tuổi theo TA.
2. Có Def: chọn rule definite ưu tiên R01 > R02 > R03; DIRECT attribution. Rule possible ưu tiên cao hơn không được thay rule definite.
3. Def rỗng nhưng AllPV: mức positive đã được coverage chứng minh. Nếu không đủ bằng chứng sốc, trả PHAN_VE và chọn rule ưu tiên cao nhất trong Poss làm mã CANONICAL.
4. Positive theo bước 2 hoặc 3 VÀ hypotension TRUE theo bảng → SOC_PHAN_VE/R-SOC. Hypotension đơn độc không đủ. HATT unavailable không là bằng chứng sốc; vẫn giữ PHAN_VE nếu tuổi có và positive đã chứng minh.
5. AnyPV nhưng không AllPV (Mixed): THEO_DOI/null với lý do chưa đủ thông tin, không khẳng định một giá trị unknown thực ra FALSE.
6. Không AnyPV: THEO_DOI/null theo không khớp. Cùng nhãn với Mixed nhưng lý do phải khác.

DIRECT/CANONICAL là provenance nội bộ để tạo ly_do, không thêm khóa output/audit. DIRECT nghĩa mã rule được xác nhận độc lập. CANONICAL chỉ dùng ở PHAN_VE, Def rỗng/AllPV: mã là đại diện của lớp khả năng, không là rule definite. ly_do MUST công bố nghĩa này, thông tin còn thiếu và không khẳng định rule đại diện đã đúng độc lập hoặc unknown đã quan sát là False. Priority giữa definite theo TA; dùng cùng thứ tự trong Poss ở nhánh canonical là convention nhóm.

Ví dụ S=co_di_nguyen_nghi_ngo unavailable, K=H=TRUE, I=TRUE, C=G=FALSE, tuổi 15/HATT 110: S=False khớp R01, S=True khớp R02; Kleene cả hai UNKNOWN nhưng AllPV. D13-E chọn PHAN_VE/R01-PV CANONICAL, giải thích đại diện R01/R02; không sửa helper R01 thành TRUE. BP thấp đủ ngưỡng → SOC_PHAN_VE/R-SOC; thiếu BP → giữ PHAN_VE canonical; thiếu tuổi → THEO_DOI/null.

Leader chấp nhận residual risk: người đọc chỉ rule_id có thể hiểu quá mức; strict interpretation của “rule đã kích hoạt” có thể khác convention nhóm. Disclosure/test bắt buộc giảm rủi ro nhưng không biến canonical thành definite hoặc TA approval. Không thêm clinical rule/ngưỡng; coverage chỉ suy luận lượng từ từ original rules. [TA §§5–6; L]

### 4.3. Quyết định và nguồn thẩm quyền hiện hành

| ID | Nội dung | Trạng thái / yêu cầu |
|---|---|---|
| D01 | Chọn một rule Tầng 2 theo R01 > R02 > R03; R-SOC ưu tiên khi sốc xác nhận | TA CONFIRMED — FR-06/FR-08 |
| D02 | Tuổi missing/null → THEO_DOI / null, giải thích thiếu tuổi | TA CONFIRMED — FR-05–FR-08 |
| D03 | Tuổi có, Tầng 2 TRUE: thiếu/null HATT hiện tại hoặc thiếu nền người lớn không chặn PHAN_VE; HATT <90 vẫn có thể xác nhận sốc | TA CONFIRMED — FR-05–FR-08 |
| D04 | Giữ strict validation cho invalid thực sự; loại bỏ policy cũ coi tuổi null/boolean null là invalid | Đã duyệt, được TA thay thế một phần — FR-07 |
| D05 | Public classify(patient) điều phối audit; helper rule tách I/O | APPROVED BY LEAD — FR-01/NFR-04 |
| D06 | Explanation tất định, thêm giải thích unavailable theo TA; không raw input/điều trị | APPROVED BY LEAD + TA — FR-08 |
| D07 | JSONL writer, ContextVar, explicit/single-call UUID ngoài input | APPROVED BY LEAD — FR-09/NFR-03 |
| D08 | CLASSIFY; SUCCESS/INVALID_INPUT; fail-closed/error precedence; allowed unavailable không tự là INVALID_INPUT | APPROVED BY LEAD, áp dụng theo TA — FR-09 |
| D09 | Thay/chỉnh stub M2; kiểm overlap, null/missing, context, failures, isolation, D13 | APPROVED BY LEAD, cập nhật expected theo TA — NFR-05 |
| D10 | perf_counter_ns, 100 warm-up, N≥1.000, nearest-rank, full-path I/O thật | APPROVED BY LEAD — NFR-01 |
| D13 | Giữ Enum/Kleene/T-U; missing/null → UNKNOWN; definite-first, AllPV positive, Mixed THEO_DOI/null; canonical ID/disclosure khi PHAN_VE/Def rỗng | APPROVED BY LEAD — D13-E — 09/11/2026; residual risk đã chấp nhận, chưa có runtime evidence |

D11 giữ clinical rules/ngưỡng; D12 giữ chín tên input, ba output, bốn audit fields và privacy. Mười OPEN đã duyệt không được mở lại. Default audit path vẫn PROPOSED — AWAITING PEER REVIEW; unexpected internal exceptions vẫn là residual review item. [TA; L]

### 4.4. Nghĩa vụ audit và hành vi lỗi đã phê duyệt

Audit JSONL giữ đúng bốn trường sau, không trường thứ năm. Allowed missing/null không tự là invalid: một lần phân loại hợp lệ hoàn tất dùng SUCCESS; INVALID_INPUT chỉ cho dữ liệu invalid thực sự theo D04. Status mô tả việc xử lý thao tác, không phản ánh mức độ phản vệ. [E §§7.2–7.3 A-06; L D07/D08]

| Trường audit | Giá trị/yêu cầu |
|---|---|
| Timestamp | ISO 8601 có timezone UTC |
| User_UUID | UUID hợp lệ, synthetic theo scope phiên người thao tác, không phải định danh bệnh nhân/danh tính thật |
| Action_Type | CLASSIFY |
| Status | SUCCESS hoặc INVALID_INPUT |

ContextVar là hướng triển khai đã được chọn ngoài PatientInput. Các call trong cùng phiên tường minh dùng chung UUID, reset khi kết thúc scope. Không có phiên tường minh thì mỗi call độc lập tạo UUID tạm mới, dùng để audit và reset trong finally kể cả exception; không tái sử dụng giữa hai call độc lập. Không thêm UUID vào chín input keys hoặc đổi chữ ký classify(patient). [L OPEN-01–OPEN-02]

| Tình huống | Hành vi bắt buộc theo policy nhóm |
|---|---|
| Valid, phân loại đủ kết luận, audit thành công | Hoàn tất audit SUCCESS rồi trả ba trường kết quả |
| Validation lỗi thực sự theo D04, audit thành công | Có record INVALID_INPUT, raise TypeError/ValueError đúng D04; không trả THEO_DOI |
| Validation thành công, audit lỗi | Raise lỗi audit vận hành an toàn, không trả thành công và không mặc định record đã lưu |
| Validation và audit cùng lỗi | Ưu tiên lỗi audit an toàn ra public boundary, không giả định record INVALID_INPUT tồn tại; message/chaining không lộ raw input |

Fail-closed có kiểm soát chỉ áp dụng module bài thi synthetic; không mặc nhiên áp dụng sản phẩm y tế thực tế. Path audit cấu hình ngoài input, trong vùng dữ liệu sinh của lần chạy, độc lập working directory; test dùng file/thư mục riêng, không commit runtime log. V1 ghi tuần tự, quyền sở hữu writer/file rõ; không cam kết thread/process-safe khi ghi chung file. [L OPEN-03–OPEN-06]

Writer M2 hoàn tất open append/write/close theo từng record trước khi public call báo thành công; lỗi write/flush/close phải được nhận biết theo fail-closed. Không retry vô hạn, không tạo trường/status mới hoặc mặc định fsync/durability sau mất điện. [L OPEN-09]

**Kiểm chứng tích hợp M2 — còn cần peer review:** direct `classify(patient)` khi chưa cấu hình audit path phải được đưa vào kế hoạch kiểm chứng. Cơ chế chọn path mặc định ổn định ngoài repository, không phụ thuộc working directory, là đề xuất chưa được Leader duyệt; cần kiểm tra override ngoài PatientInput cho test/demo, fail-closed khi không tạo/ghi được file và hướng dẫn nơi lưu/cấu hình trong README khi triển khai. Giữ nguyên signature và chín input keys. [TASK 02C.4 Patch A]

## 5. Đặc tả dữ liệu đầu ra

Mọi kết quả phân loại vẫn có đúng ba khóa dưới đây. Dữ liệu unavailable được TA cho phép không tự là lỗi; non-null invalid theo D04 phát sinh lỗi validation khi audit thành công, hoặc lỗi audit an toàn nếu writer thất bại. [D; TA; L]

| Trường | Kiểu | Giá trị và điều kiện |
|---|---|---|
| `muc_do` | Chuỗi | SOC_PHAN_VE, PHAN_VE, THEO_DOI. Tuổi missing/null → THEO_DOI. Tuổi có, positive definite hoặc AllPV + hypotension TRUE → SOC_PHAN_VE; positive chưa xác nhận sốc → PHAN_VE; Mixed/all-negative → THEO_DOI. |
| `rule_id` | Chuỗi hoặc null | R-SOC khi Tier1 được chứng minh. PHAN_VE/DIRECT: rule definite ưu tiên R01-PV > R02-PV > R03-PV. PHAN_VE/CANONICAL: chỉ khi Def rỗng/AllPV, dùng rule ưu tiên cao nhất trong Poss làm mã đại diện, không independently confirmed. THEO_DOI dùng null thực; D13-E không chọn PHAN_VE/null. |
| `ly_do` | Chuỗi | Truy vết DIRECT hoặc công bố rõ CANONICAL/uncertainty theo §4.2; Mixed nêu chưa đủ thông tin, all-negative nêu không khớp. Nêu thiếu tuổi/BP/nền phù hợp TA. Không raw input, clinical fact chưa biết, an toàn hoặc điều trị. |

Từ reason trong đề tương ứng ly_do. UNKNOWN chỉ là trạng thái nội bộ, không phải output mới. Không khẳng định “không có sốc” chỉ vì không có số đo; chỉ nêu chưa có bằng chứng xác nhận sốc. [D; TA §§1–4]

### 5.1. Ma trận kiểm chứng tài liệu theo TA — không phải kết quả chạy engine

| ID | Tình huống synthetic | Expected / yêu cầu | Giải thích và ánh xạ bàn giao |
|---|---|---|---|
| TA-EX-01 | R02/R03 TRUE, tuổi 15, HATT 110, không sốc | PHAN_VE / R02-PV | Ưu tiên chính thức; ly_do có thể nêu thêm R03; PEND-001 |
| TA-EX-02 | R01 TRUE, tuổi thiếu, HATT có | THEO_DOI / null | Nêu thiếu tuổi, không chọn được ngưỡng; PEND-002 |
| TA-EX-03 | R01 TRUE, tuổi null, HATT có | THEO_DOI / null | Không TypeError chỉ vì tuổi null; INV-001 |
| TA-EX-04 | R01 TRUE, tuổi 15, HATT hiện tại null | PHAN_VE / R01-PV | Nêu chưa xác nhận sốc vì thiếu số đo; PEND-003 |
| TA-EX-05 | Như trên, khóa HATT hiện tại thiếu | PHAN_VE / R01-PV | Missing tương đương null; PEND-004 |
| TA-EX-06 | Tuổi 25, HATT 110, nền null, R02 TRUE | PHAN_VE / R02-PV | Nêu chưa đánh giá được giảm >30%; PEND-005 |
| TA-EX-07 | Như trên, khóa HATT nền thiếu | PHAN_VE / R02-PV | Không suy/gán nền mặc định; PEND-006 |
| TA-EX-08 | Tuổi 25, HATT 89, nền thiếu, R01 TRUE | SOC_PHAN_VE / R-SOC | Nhánh tuyệt đối đủ bằng chứng; BP-025/026 |
| TA-EX-09 | Tuổi 25, HATT 140, nền 200, R01 TRUE | PHAN_VE / R01-PV | Giảm đúng 30%, không HATT tuyệt đối thấp; BP-022 |
| TA-EX-10 | Tuổi 15, HATT 110, S=FALSE, K=H=TRUE, C=FALSE, G=null | PHAN_VE / R01-PV; không exception/hạ mức | Fixture bổ sung; INV-037/043 chịu thay policy nhưng phải tính lại riêng |
| TA-EX-11 | Như TA-EX-10, G thiếu khóa | PHAN_VE / R01-PV; không exception/hạ mức | Không đổi UNKNOWN thành bằng chứng âm; MISS-007 |
| TA-EX-12 | Tuổi 15, HATT 110, S=TRUE, I=TRUE, K=TRUE, H=C=FALSE, G thiếu/null | THEO_DOI / null | Mixed: G=False không rule, G=True R02; fallback D13-E đã duyệt; MISS-012 |
| TA-EX-13 | Tuổi 15, HATT 110, S thiếu/null, I=TRUE, K=H=TRUE, C=G=FALSE | PHAN_VE / R01-PV | CANONICAL: AllPV/Def rỗng; ly_do bắt buộc nêu mã đại diện R01/R02, không xác nhận S=False; MISS-009/TA15-BOOL1-* |

TA-EX-01–11 đối chiếu TA; TA-EX-12–13 ghi expected theo D13-E đã được Leader duyệt, không gán TA đã chỉ định fallback/mã canonical. Đây là đối chiếu tài liệu, chưa chạy engine. Valid unavailable sau phân loại và audit hoàn tất dùng SUCCESS; không INVALID_INPUT chỉ vì missing/null. Không khóa nguyên văn template, nhưng nghĩa attribution/uncertainty là bắt buộc.

## 6. Yêu cầu phi chức năng

| ID | Yêu cầu | Bằng chứng kiểm chứng dự kiến | Nguồn |
|---|---|---|---|
| NFR-01 | Dùng time.perf_counter_ns(); 100 warm-up ngoài mẫu, N≥1.000 lượt đo; nearest-rank p50/p95, p95 <100 ms. Phép đo chính là full public classify() có open/write/close audit thực; logic thuần báo riêng. | Protocol tái lập, mẫu thực, Python/OS/CPU-hardware, số lượt, dữ liệu synthetic và cấu hình I/O; chưa có số liệu | E §7.3 A-10; G D10; L OPEN-09/10 |
| NFR-02 | Chỉ dùng dữ liệu synthetic. Không có PII, dữ liệu bệnh nhân thật, thông tin xác thực hoặc secret trong input, dữ liệu test, log và hồ sơ bàn giao. | Review bảo mật/riêng tư trên file được theo dõi và bằng chứng sinh ra | D dòng 22–23; E §§5, 7 |
| NFR-03 | Audit bốn trường/giá trị §4.4, UUID đúng scope, fail-closed/error precedence. Allowed missing/null không tự thành INVALID_INPUT. Message/chaining/log không lộ raw input. | Kiểm schema/UTC/UUID, SUCCESS cho unavailable hợp lệ, INVALID_INPUT cho invalid thực sự, writer failure/lỗi kép | E A-06; D07/D08; TA §5 |
| NFR-04 | Giữ classify(patient), ranh giới rule/I/O, Enum/Kleene/T-U không truthiness. D13-E phân biệt definite/possible, DIRECT/CANONICAL và TA bắt buộc/team policy đã duyệt. | Review interface, source hierarchy, coverage/selection/provenance | E §§7.1,9; D05/D13-E; L. |
| NFR-05 | Test normal/boundary/invalid/missing/null và overlap; thay/chỉnh stub M2. Giữ context/failure/isolation; thêm normalization, Def/Poss/AllPV/Mixed, canonical explanation, 1–64 completions, TA-EX-01–13 và sáu ca §8.2. | Test Plan và QA Matrix đã có ở mức thiết kế (nguồn §8.1). Bằng chứng cần thu: clean-checkout business tests và PR CI thật. Approval không chứng minh runtime. | E A-07/A-08; D09/D13-E; L. |
| NFR-06 | GitHub Actions chạy test trên Pull Request. | Cấu hình workflow và liên kết lượt chạy PR có bước test thực tế | E §7.3 A-09; W |
| NFR-07 | Explanation ngắn gắn rule/kết quả; DIRECT có definite evidence; CANONICAL công bố mã đại diện/uncertainty, không claim independently confirmed; Mixed không khẳng định an toàn. Missing numeric đúng TA; không raw input/điều trị. | Review template và negative assertions cho cả sáu ca §8.2, unavailable BP/age và canonical risk | D; TA; D06/D13-E. |
| NFR-08 | Có hướng dẫn cài/chạy/test tái lập, disclaimer chính xác trong README và hồ sơ tài liệu/bàn giao theo các mốc đề yêu cầu. | README và tài liệu yêu cầu, quyết định, kiểm thử, bảo mật/riêng tư, AI-use, đóng góp | E §§4–6, 7.3 A-11, 11 |

Protocol D10 đã được Leader chốt: sắp N mẫu tăng dần, lấy phần tử tại vị trí `ceil(p × N)` theo chỉ số bắt đầu từ 1; p50 dùng p=0,50 và p95 dùng p=0,95. Chuyển nanosecond sang millisecond bằng chia 1.000.000. Loại 100 warm-up khỏi mẫu; không mock writer trong phép đo full-path. p95 <100 ms là ngưỡng của đề, chưa có kết quả để kết luận đạt. [L OPEN-10; E A-10]

## 7. Tiêu chí nghiệm thu

Trạng thái dưới đây phản ánh bằng chứng có thể kiểm tra tại thời điểm tích hợp M1 ngày 10/11/2026: NOT IMPLEMENTED là chưa có chức năng/tài liệu cần thiết, PARTIALLY AVAILABLE là có khung nhưng thiếu bằng chứng nghiệp vụ. TA CONFIRMED là nguồn yêu cầu đã rõ, không đồng nghĩa VERIFIED. Không AC nào được nâng thành VERIFIED chỉ từ việc merge tài liệu; chưa có bằng chứng runtime test/CI nghiệp vụ/benchmark đạt. Các trạng thái cần cập nhật lại khi M2 có kết quả thực tế.

| AC | Yêu cầu | Điều kiện nghiệm thu | Bằng chứng cần có | Nguồn | Trạng thái hiện tại |
|---|---|---|---|---|---|
| A-01 | Phân loại đúng contract | classify() thực thi bảng và làm rõ TA, hết NotImplementedError | Rule–code/test mapping gồm priority, age override và BP unavailable | E A-01; D; TA | NOT IMPLEMENTED |
| A-02 | Không hard-code fixture ID | Kết quả dựa trên dữ liệu đặc tả | Review code và fixture synthetic độc lập | E A-02; C | NOT IMPLEMENTED |
| A-03 | Đủ mức phân loại | SOC_PHAN_VE/PHAN_VE/THEO_DOI theo bảng và TA | Tầng 1/2, overlap, missing/null và TA-EX | E A-03; D; TA | NOT IMPLEMENTED |
| A-04 | Policy dữ liệu công bố và thực thi | Giữ missing/null theo TA và strict D04 cho invalid thực sự. D13-E đã duyệt: UNKNOWN, definite-first/coverage, Mixed fallback và canonical disclosure. | Policy/source review; test null/missing, invalid và cả sáu ca approved §8.2 | E A-04; TA; D04/D13-E; L | NOT IMPLEMENTED — policy đã duyệt, chưa có implementation evidence |
| A-05 | Explanation truy vết | ly_do DIRECT/CANONICAL đúng §4.2/§5; canonical không giả rule đã xác nhận độc lập, không raw input/điều trị. | Output/negative explanation assertions cho TA và D13-E | E A-05; D; TA; D06/D13-E | NOT IMPLEMENTED |
| A-06 | Audit an toàn đúng schema | Bốn trường; CLASSIFY, SUCCESS/INVALID_INPUT theo nghĩa thao tác; không INVALID_INPUT chỉ vì allowed unavailable | Schema/UTC/UUID/status, failure paths, dữ liệu cấm | E A-06; D07/D08; TA §5 | NOT IMPLEMENTED |
| A-07 | Test nghiệp vụ đủ nhóm | Normal/boundary/invalid/missing/null; thay/chỉnh test stub | Bộ test được review và map TA-EX/FR | E A-07; T | PARTIALLY AVAILABLE — mới có test minh họa NotImplementedError; chưa có bộ test nghiệp vụ đạt |
| A-08 | Chạy đạt từ clean checkout | pytest -q đạt với test nghiệp vụ đã thay/chỉnh stub | Lệnh, môi trường, kết quả thực chạy | E A-08; R | PARTIALLY AVAILABLE — có lệnh, chưa có bằng chứng test nghiệp vụ clean checkout đạt |
| A-09 | CI trên PR | GitHub Actions thực sự chạy bộ test cho PR | PR run URL và bước test thực tế | E A-09; W | PARTIALLY AVAILABLE — có workflow, chưa có bằng chứng CI chạy đạt với bộ test nghiệp vụ |
| A-10 | Benchmark đúng protocol | N≥1.000 sau 100 warm-up; nearest-rank p50/p95; p95 <100 ms, công bố máy và I/O full-path | Phương pháp và số liệu thật | E A-10; D10 | NOT IMPLEMENTED — protocol đã duyệt, chưa có số liệu |
| A-11 | Disclaimer README | Có chính xác educational/synthetic — not for clinical use | Kiểm tra README | E A-11; R | NOT IMPLEMENTED |

Việc test stub có thể chạy đạt chỉ chứng minh stub; không chứng minh yêu cầu nghiệp vụ. Test Plan và QA Matrix hiện hành đã được tích hợp qua PR #3 và #4. Bộ pytest nghiệp vụ, kết quả chạy, bằng chứng audit/CI và cập nhật QA theo thực thi vẫn thuộc M2/M3. [P; L]

## 8. Ma trận truy vết yêu cầu

| ID yêu cầu | Rule hoặc AC liên quan | Kiểm chứng dự kiến ở mức yêu cầu |
|---|---|---|
| FR-01 | A-01, A-02 | Giữ interface và fixture independence; public orchestration vẫn audit, provider ngoài input |
| FR-02 | R01-PV; A-01/A-03/A-07 | Giữ NOT/AND/OR; kiểm rule độc lập vẫn TRUE khi boolean khác missing/null theo TA-EX-10/11 |
| FR-03 | R02-PV; A-01/A-03/A-07 | Đếm 2/4 và T/U; assert R02 riêng tránh bị R03 che; TA-EX-01,06,07,12 |
| FR-04 | R03-PV; A-01/A-03/A-07 | Giữ ngoặc/đường hít/tuần hoàn; rule TRUE không bị rule UNKNOWN làm mất hiệu lực |
| FR-05 | R-SOC; A-01/A-03/A-07 | Biên tuổi/BP, giảm đúng/trên 30%, không suy nền; TA-EX-02–09, nguồn TA-02–04 |
| FR-06 | Ưu tiên, coverage, fallback; A-01/A-03/A-07 | Rule definite thắng possible; AllPV/Def rỗng giữ positive; Mixed TD/null; canonical disclosure. TA age override/shock giữ nguyên; TA-EX-01–13, sáu ID §8.2 |
| FR-07 | A-04/A-07 | Missing/null không tự là invalid; D04 strict với non-null sai kiểu/miền/khóa lạ; tính lại INV/AUD cũ theo TA-EX |
| FR-08, NFR-07 | A-05 | Ba khóa và explanation DIRECT/CANONICAL, uncertainty, thiếu tuổi/BP/nền; không raw input hoặc claim unknown=False |
| FR-09, NFR-02/03 | A-06 | SUCCESS cho phân loại unavailable hợp lệ, INVALID_INPUT cho invalid thực sự; giữ UTC/UUID, scope/reset và fail-closed/lỗi kép |
| NFR-01 | A-10 | Protocol D10 và số liệu thực, không đổi do TA |
| NFR-04 | A-01/A-02 | Review minimal helpers, Enum và tách policy TA/team/proposal |
| NFR-05 | A-07, A-08 | Test nghiệp vụ thay/chỉnh stub, bảng logic, context/failure/isolation; pytest -q từ clean checkout, có bằng chứng thực chạy |
| NFR-06 | A-09 | Cấu hình và PR run có bước test thực tế |
| NFR-08 | A-11; E §§6,11 | Disclaimer và hồ sơ bàn giao đầy đủ |

TA-EX-01–13 ở §5.1 là ví dụ/ánh xạ yêu cầu để đối chiếu với Test Plan, test cases và QA Matrix hiện hành sau PR #3/#4; **không phải bằng chứng test đã chạy**. Phần thiết kế đã được tích hợp, còn triển khai và đối chiếu kết quả thực tế thuộc M2/M3.

### 8.1. Bàn giao test và nguồn hiện hành

Baseline lịch sử của TASK 02G/02E: [nhánh Hải tại commit 768f196e6a9ec3b1142c44399ce8288f7cc2e87e](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/tree/768f196e6a9ec3b1142c44399ce8288f7cc2e87e/docs/m1-hai), gồm 157 ca chính và 81 ca logic nội bộ riêng. Baseline này là nguồn của sáu oracle §8.2.

Nguồn thiết kế hiện hành: [PR #3 — đã merge](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) có [175 ca chính](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv) theo [Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_PLAN.md) và bộ [81 ca logic nội bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTERNAL_STATE_CASES.csv) riêng. [PR #4 — đã merge](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) có [QA Matrix tại commit của PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d7f7e34860c3878cdbc07b4486f785cf4ae1ca99/docs/m1-qa/QA_MATRIX_M1_CODEX_FINAL_CANDIDATE.xlsx) để truy vết A-01–A-11. Các mục thực thi trong workbook vẫn `NOT RUN`. PEND-001→PHAN_VE/R02-PV; PEND-002/007→THEO_DOI/null; PEND-003/004→PHAN_VE/R01-PV; PEND-005/006→PHAN_VE/R02-PV theo TA.

Tám INV nullable hợp lệ: INV-001, INV-017/021/025/029/033/037, INV-043. Với fixture hiện có, INV-043→SOC_PHAN_VE/R-SOC; bảy ca còn lại THEO_DOI/null. Audit SUCCESS nếu hoàn tất. AUD-002 hiện dùng chuỗi "true", là TypeError/INVALID_INPUT khi audit thành công. Nhóm invalid hiện có 36 ca =28 TypeError+8 ValueError; lỗi kép vẫn audit precedence.

Lịch sử: đối chiếu baseline 2c6685e55af47eea55ffeea63c250272a4e71fe3 từng có 35 invalid+9 nullable trong nhóm 44 cũ; AUD-002 sau đó đổi fixture nên con số hiện hành khác. Không áp output của fixture cũ lên bản mới. Mục này đồng bộ nguồn và trạng thái bàn giao.

### 8.2. Sáu expected D13-E đã được Leader phê duyệt — bàn giao TASK 02E

**APPROVED BY LEAD — D13-E — 09/11/2026.** Với đúng fixture tại nhánh Hải commit 768f196e6a9ec3b1142c44399ce8288f7cc2e87e, tuổi/HATT đủ như đang có, các expected sau được chốt ở mức policy. Test cases và QA Matrix đã được đồng bộ trong các PR #3/#4 đã merge; **chưa chạy engine hoặc xác nhận các expected bằng runtime**. Review trên GitHub được ghi nhận theo tài khoản, không thay thế kết quả kiểm thử thực tế.

| Test ID | muc_do | rule_id | Attribution / explanation bắt buộc |
|---|---|---|---|
| MISS-009 | PHAN_VE | R01-PV | CANONICAL: AllPV qua R01/R02, Def rỗng; nêu mã đại diện và thiếu attribution, không claim S=False/riêng R01 đã được xác nhận |
| TA15-BOOL1-NULL | PHAN_VE | R01-PV | CANONICAL như MISS-009; null tương đương missing; không chỉ generic reason |
| TA15-BOOL1-MISSING | PHAN_VE | R01-PV | CANONICAL như cặp null; không bắt UUID/reason nguyên văn bằng nhau |
| MISS-012 | THEO_DOI | null | Mixed do G unavailable; nêu chưa đủ thông tin, không nói G=False hoặc R02 chắc chắn FALSE |
| TA15-DEPENDENT_INHALATION-NULL | THEO_DOI | null | Mixed do I unavailable; không ép I hoặc kết luận an toàn |
| TA15-DEPENDENT_INHALATION-MISSING | THEO_DOI | null | Cùng fallback/uncertainty như cặp null |

SUCCESS chỉ khi thao tác phân loại hợp lệ và writer hoàn tất. Các dòng trên không tạo status audit mới. Thiết kế và expected hiện hành tiếp tục yêu cầu helper của MISS-009 giữ R01/R02 UNKNOWN, không đổi thành TRUE chỉ để khớp `rule_id` canonical; khi triển khai M2 phải có negative explanation assertions tương ứng. Ba cặp mức/mã từ baseline Hải được giữ nguyên, có approval của Leader, không phải TA định danh.

## 9. Cơ sở yêu cầu và trạng thái phê duyệt

Đã đọc toàn bộ [bình luận fossbk-spec](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) tại Issue #15, tạo/cập nhật lúc 14:01:50 UTC ngày 08/11/2026. Làm rõ áp dụng chung cho Track A; D01–D03 trong phạm vi đã trả lời không còn chờ TA. Không biến phê duyệt TA về hành vi thành phê duyệt toàn bộ kiến trúc nhóm.

| ID | Hành vi hiện hành | Trạng thái và nguồn |
|---|---|---|
| D01 | Khi nhiều rule Tầng 2 TRUE, PHAN_VE và chọn R01>R02>R03; sốc xác nhận thì SOC_PHAN_VE/R-SOC | TA CONFIRMED — [TA §1](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D02 | Tuổi missing/null: THEO_DOI/null; giải thích thiếu tuổi | TA CONFIRMED — [TA §§2,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D03 | Tuổi có, Tầng 2 TRUE: current BP missing/null vẫn PHAN_VE; người lớn HATT ≥90 thiếu/null nền vẫn PHAN_VE; HATT <90 có thể xác nhận sốc không cần nền | TA CONFIRMED — [TA §§3–5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |

TA-05 bắt buộc missing/null boolean không tự gây exception và không hạ kết luận khi một rule đã được dữ liệu còn lại chứng minh trọn vẹn. TA-06 cho phép policy nội bộ trong khoảng chưa quy định, phải công bố/test/giải trình và không đổi rule/ngưỡng/schema.

**D13-E hiện hành: APPROVED BY LEAD — D13-E — 09/11/2026.** Normalization, coverage, definite-first, Mixed fallback và canonical semantics §3.2/§4.2/§5/§8.2 đã được phê duyệt nội bộ; không còn chờ Leader cho D13. Leader chấp nhận residual risk về activated-rule semantics. Không cần chờ một câu trả lời TA mới để thực hiện policy được duyệt; không gán convention nhóm thành lời TA hoặc đóng bằng chứng triển khai.

Các quyết định ContextVar, UUID scope, JSONL, fail-closed, error precedence, isolation, Enum và benchmark vẫn giữ nguyên ngoài phần bị TA thay thế. Tên helper/exception audit và path cụ thể là chi tiết triển khai. Default path vẫn đề xuất chờ peer review; unexpected internal exception vẫn residual review item. Các tài liệu M1 hiện hành đã nằm cùng nhánh `track-a-development`, gồm `DECISIONS.md`; giữ liên kết pin commit cho nguồn lịch sử và sử dụng đường dẫn hiện hành khi điều hướng trong fork.

Tiêu đề R03 nói dị nguyên đã biết nhưng biểu thức dùng co_di_nguyen_nghi_ngo; tiếp tục giữ biểu thức và chín tên khóa như D. Không suy thêm khóa hoặc rule. [D; TA]

## 10. Rủi ro, phụ thuộc và tài liệu tham chiếu

| Rủi ro | Kiểm soát và review |
|---|---|
| Còn dùng policy cũ coi tuổi/boolean null là invalid | Đồng bộ dữ liệu/expected/AUD status theo TA; không chuyển máy móc 44 ca lỗi cũ sang exception |
| Quên tuổi unavailable override hoặc để thiếu BP chặn PHAN_VE | Review TA-EX-01–09 và ly_do, phân biệt thiếu bằng chứng sốc với loại bỏ Tầng 2 |
| Ép UNKNOWN thành False hoặc chọn rule_id không được chứng minh | Giữ D13-E, Def trước Poss; canonical chỉ ở AllPV/Def rỗng, disclosure MUST. Leader đã chấp nhận risk mã không definite; QA cần negative assertions, không gọi rule canonical là confirmed |
| Sai ngoặc/ngưỡng hoặc suy BP mặc định | Đối chiếu biểu thức gốc, boundary và >30% nghiêm ngặt; không tạo rule y khoa mới |
| Audit SUCCESS/INVALID_INPUT bị dùng nhầm | Allowed missing/null không tự là lỗi; giữ D04 cho invalid thực sự, bốn trường và error precedence |
| Direct call chưa cấu hình audit path | Tiếp tục review đề xuất ở ADR, không tự chọn/duyệt path trong task này |
| Unexpected internal exception trước audit thành công | Residual implementation risk / review item: không SUCCESS hoặc tự gán INVALID_INPUT; không thêm status/schema hoặc log payload; Hải/Việt Đức review cách xử lý |
| Nhầm review tài liệu với nghiệm thu | Giữ 11 AC chưa VERIFIED; Leader approval D13-E và GitHub PR approval không chứng minh TA đã nghiệm thu scope hoặc runtime/test/clean checkout/CI/benchmark đạt |
| Nguồn snapshot lịch sử còn policy cũ | Giữ snapshot là lịch sử; source TA và Revision 04/D13-E ưu tiên hơn. Bản M1-02/QA hiện hành đã được đồng bộ và merge trong PR #3/#4; không dùng snapshot cũ làm policy hiện hành |
| AI-use hoặc phối hợp thiếu bằng chứng | Ghi công cụ/phạm vi/kiểm chứng/quyết định và người chịu trách nhiệm thực tế; Huy review nguồn, Hải M1-02, Việt Đức M1-03 |

| Ký hiệu | Nguồn và phiên bản |
|---|---|
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung hiển thị v1.0.2 dù tên URL ghi v1.0.0, đối chiếu ngày 08/11/2026 qua HTML xuất bản của fossbk-spec/ktpmud-book. Áp dụng §§4–7, 9, 11–12. |
| D | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag starter chính thức `bkt-2026-v1`. |
| TA | [Trả lời chính thức fossbk-spec — Issue #15 comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), §§1–6, tạo/cập nhật 08/11/2026 14:01:50 UTC; áp dụng chung Track A. |
| Q2 | [Requirements Revision 02 — lịch sử trước đồng bộ TA](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/662c47be9eba076bf9ca551403cc3e961f421d42/REQUIREMENTS.md); không dùng policy cũ trái TA cho hiện trạng. |
| Q3 | [Requirements Revision 03 — lịch sử trước D13-E](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/c855c6d4f2135a14ad94485734d4d2e604cb9cff/REQUIREMENTS.md), snapshot từng giữ extension/fallback chờ Leader; Revision 04 thay phần đó bằng approval D13-E. |
| G | [Project Guide](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b/docs/PROJECT_GUIDE.md), mốc nguồn tích hợp, đặc biệt §§3–5. |
| P | [Team Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b/docs/TEAM_PLAN.md), mốc nguồn tích hợp, đặc biệt §3. |
| C | [Interface classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b/rule_engine/classifier.py), mốc nguồn tích hợp. |
| T | [Test mẫu starter](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b/tests/test_classifier.py), mốc nguồn tích hợp. |
| W | [Workflow GitHub Actions](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b/.github/workflows/test.yml), mốc nguồn tích hợp. |
| R | [README starter](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b/README.md), mốc nguồn tích hợp. |
| I | [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15), câu hỏi và trả lời của fossbk-spec ngày 08/11/2026, áp dụng chung cho Track A; không thay thế Decision Table V1. |
| L | Quyết định Leader trong quá trình M1, gồm TASK 02G ngày 09/11/2026 phê duyệt D13-E và chấp nhận residual risk canonical attribution. TASK 02F chỉ là tư vấn; D13 pending ở Revision 03 là lịch sử. Các PR #1–#4 đã merge ngày 10/11 theo quyết định tích hợp của Leader; chưa có bằng chứng thực thi code/test/CI/benchmark. Phần sử dụng AI, hậu kiểm của con người và đóng góp được ghi trung thực trong hồ sơ `AI_USE.md`/`CONTRIBUTIONS.md` khi hoàn thiện. |

Nguồn D + TA quyết định yêu cầu bắt buộc; G/P là snapshot phân công/lịch sử, không ghi đè TA. D13-E là approved team policy theo quyền TA §§5–6, không TA approval; default audit path/internal exception giữ trạng thái riêng. Không diễn giải approval D13 thành thay đổi tự động miền validation hoặc các OPEN đã chọn.

### 10.1. Lịch sử thay đổi

| Phiên bản | Nội dung | Tình trạng bằng chứng |
|---|---|---|
| Revision 02, 08/11/2026 — lịch sử tại 662c47be9eba076bf9ca551403cc3e961f421d42 | D01–D03 khi đó PENDING TA CONFIRMATION; tuổi/boolean null bị coi invalid theo policy cũ | Snapshot trước trả lời TA, không phải policy hiện hành |
| Revision 03, 08/11/2026 — TASK 02C.6 | Đồng bộ TA-01–06, thay thế một phần D04/D13, cập nhật FR/AC/truy vết và 12 ví dụ; extension null → UNKNOWN chờ Leader | **Trạng thái lịch sử tại 08/11:** Draft/chờ review; chưa có implementation/test/benchmark evidence |
| Revision 04, 09/11/2026 — TASK 02G | APPROVED BY LEAD — D13-E — 09/11/2026; chuẩn hóa missing/null, Def/Poss/AllPV, definite-first, canonical attribution và Mixed fallback; chốt sáu expected, đồng bộ nguồn/bàn giao TASK 02E | **Trạng thái lịch sử tại 09/11:** Draft/chờ peer review; chưa có implementation verification; default path/internal exception còn review | 
| Đồng bộ trạng thái sau merge, 10–11/11/2026 *(không đổi Revision 04 hoặc chính sách kỹ thuật)* | Xác nhận PR #1–#4 đã merge vào `track-a-development`; chỉnh tham chiếu SHA, trạng thái peer review và bàn giao M2 | Có Leader self-review và review APPROVED từ `nvldvc`; chưa có lượt review thành viên còn lại; chưa có TA scope acceptance hoặc bằng chứng runtime/test/CI/benchmark đạt |
