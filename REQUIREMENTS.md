# Yêu cầu và phạm vi Track A

| Thuộc tính | Giá trị |
|---|---|
| Cuộc thi | KTPMUD Hack Marathon 2026, Track A — Dr May Day: Rule Engine Sprint |
| Mã nhóm | `173820_n27` |
| Người phụ trách | Huy Đức |
| Mốc bàn giao | M1-01, Checkpoint 1, ngày 08/11/2026 |
| Phiên bản | Revision 03 — Draft PR #1 / Awaiting Peer Review |
| Cập nhật | 08/11/2026 — TASK 02C.6, đồng bộ làm rõ TA chính thức |
| Trạng thái | Bản đưa lên nhánh Requirements để peer review; PR #1 chưa merge |
| Mốc nguồn starter | `bkt-2026-v1` → `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Mốc nguồn tích hợp | `track-a-development` tại `b65032f94ec3ce600df07d81b5df6b9b4bd203d1` |
| Baseline trước Revision 03 | `662c47be9eba076bf9ca551403cc3e961f421d42` trên `docs/m1-requirements-huy`; lịch sử Revision 02, không phải HEAD mới sau đồng bộ TA |
| Làm rõ chính thức | [fossbk-spec — Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), ngày 08/11/2026; nguồn TA cho D01–D03 và null/missing |

Revision 03 được đưa lên nhánh `docs/m1-requirements-huy` qua [Draft PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1) để review. Preflight ngày 08/11/2026 xác nhận PR Open/Draft, chưa merge, chưa có peer approval của Hải/Việt Đức. Xem HEAD thực tế trên PR; không ghi SHA tương lai của chính commit vào tài liệu. Publish tài liệu không nâng trạng thái bằng chứng A-01–A-11 hoặc xác nhận hoàn tất Checkpoint 1.

**Thứ tự nguồn:** Decision Table V1 và làm rõ TA [TA] cao hơn quyết định nội bộ đã duyệt; quyết định nội bộ cao hơn đề xuất. TA không yêu cầu riêng Kleene logic hoặc Enum. Mười OPEN và phần D04–D13 không bị TA thay thế vẫn giữ trạng thái đã duyệt, chờ peer technical review. D01–D03 đã được TA xác nhận cho các tình huống được trả lời, không còn là câu hỏi chờ TA.

**Đề xuất cần Leader xác nhận:** ánh xạ boolean missing/null sang UNKNOWN nội bộ theo D13, đặc biệt phần mở rộng cho explicit null, mang nhãn **PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION**. Quy định bắt buộc không raise chỉ vì boolean missing/null đã có hiệu lực từ TA; không phụ thuộc việc nhóm chọn representation nào. [TA §5; L]


## 1. Giới thiệu

Theo thông tin nhóm cung cấp trong yêu cầu Revision 01, Dr May Day có định hướng thử nghiệm và ứng dụng thực tế ở phạm vi phát triển rộng hơn. Thông tin này được ghi nhận với nguồn là nhóm, chưa có bằng chứng độc lập về triển khai production, kiểm định y tế hoặc khách hàng thực tế. [L]

Phạm vi Hack Marathon là mô-đun Rule Engine Python phân loại dữ liệu giả lập theo bảng quyết định đã khóa. Starter có interface `classify(patient)` nhưng thân hàm đang phát sinh `NotImplementedError`. Mục tiêu của nhóm là chuyển đặc tả thành yêu cầu đầu vào/đầu ra có thể kiểm chứng, kết quả giải thích được và bằng chứng về tính đúng, audit an toàn cùng hiệu năng. [E §§4–7, 9; C dòng 11–36]

Sinh viên phát triển và bảo trì mô-đun. Các thành viên review yêu cầu, thiết kế và hành vi. Giảng viên/TA xem xét phạm vi và đánh giá bài làm. Dữ liệu giả lập phục vụ kiểm thử và trình diễn. Mô-đun bài thi chưa được xác minh hoặc phê duyệt cho sử dụng lâm sàng. Cảnh báo bắt buộc được giữ nguyên là `educational/synthetic — not for clinical use`. [E §§5–7, 12]

## 2. Phạm vi

| Trong phạm vi | Ngoài phạm vi |
|---|---|
| Phân loại bằng quy tắc và validation theo bảng quyết định cùng chính sách nhóm đã duyệt | Website, giao diện bệnh viện hoặc giao diện ngoài yêu cầu bài thi |
| Output ba trường, giải thích truy vết được và audit bốn trường | Dữ liệu bệnh nhân thật, hệ thống quản lý bệnh nhân hoặc cơ sở dữ liệu thật |
| Kiểm thử tự động, kiểm chứng từ bản checkout sạch, CI trên PR và benchmark | AI/ML hoặc LLM suy đoán kết quả phân loại |
| Yêu cầu, bằng chứng thiết kế/kiểm chứng, bảo mật, riêng tư và bàn giao | Tích hợp production, chẩn đoán hoặc khuyến nghị điều trị, quy tắc hoặc ngưỡng lâm sàng tự bổ sung |

Bản nháp M1 mô tả yêu cầu và phương pháp kiểm chứng dự kiến. Chi tiết test case thuộc Test Plan, còn lý do và đánh đổi thiết kế thuộc ADR. Mốc Checkpoint 1 là cuối ngày 08/11/2026. [E §§4–7; G §§2, 5; P §3]

## 3. Hợp đồng dữ liệu đầu vào

Danh sách cho phép vẫn đúng chín tên khóa. Missing là khóa vắng mặt; null là khóa hiện diện với giá trị None. Data Dictionary gốc [D] khóa tên/ý nghĩa trường; [TA §5] làm rõ unavailable được phép cho ba trường số và sáu boolean. TypedDict(total=False) chỉ mô tả kiểu tĩnh, không thực thi validation runtime. Không thêm UUID/path hoặc khóa định danh vào PatientInput.

| Tên trường chính xác | Kiểu theo nguồn chính thức | Mô tả | Chính sách null/missing hiện hành | Validation và hành vi | Nguồn |
|---|---|---|---|---|---|
| `tuoi` | float (năm); missing/null theo TA | Tuổi cho phép số lẻ như 0.5 | Null và missing đều là tuổi chưa có | Giữ int/float hữu hạn ≥0, loại bool; không ép chuỗi. None/missing không tự gây TypeError. Khi Tầng 2 TRUE nhưng tuổi unavailable: THEO_DOI / null. | D dòng 12; TA §§2,5; D04 |
| `huyet_ap_tam_thu` | int hoặc null; cho phép thiếu | HATT hiện tại, mmHg | Null và missing tương đương unavailable | Giữ int ≥0, loại bool/float/chuỗi; không đặt trần. HATT=0 vẫn hợp lệ theo policy nhóm. Nếu tuổi có và Tầng 2 TRUE nhưng HATT unavailable: PHAN_VE / rule Tầng 2 được chọn. | D dòng 13; TA §§3,5; D04 |
| `huyet_ap_tam_thu_nen` | int hoặc null; cho phép thiếu | HATT nền cho nhánh giảm tương đối ở tuổi ≥18 | Null và missing tương đương unavailable | Nếu có số phải int >0, loại bool/float/chuỗi; nền 0 vẫn invalid. Ở người lớn HATT <90 đủ chứng minh nhánh tuyệt đối; HATT ≥90 thiếu nền không chặn Tầng 2 đã xác nhận. | D dòng 14,35; TA §§4,5; D04 |
| `co_di_nguyen_nghi_ngo` | bool; missing/null được TA cho phép | Có dị nguyên nghi ngờ; xuất hiện cả nhánh phủ định và khẳng định | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN là đề xuất D13 ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `di_nguyen_qua_duong_hit` | bool; missing/null được TA cho phép | Dị nguyên qua đường hít, ảnh hưởng nhánh hô hấp R03 | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN là đề xuất D13 ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_ton_thuong_da_niem_mac` | bool; missing/null được TA cho phép | Tổn thương da/niêm mạc | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN là đề xuất D13 ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_trieu_chung_ho_hap` | bool; missing/null được TA cho phép | Triệu chứng hô hấp | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN là đề xuất D13 ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_trieu_chung_tuan_hoan` | bool; missing/null được TA cho phép | Triệu chứng tuần hoàn | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN là đề xuất D13 ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |
| `co_trieu_chung_tieu_hoa_nang` | bool; missing/null được TA cho phép | Triệu chứng tiêu hóa nặng | Không raise chỉ vì missing/null | True/False có kiểu bool hợp lệ. Missing/null → UNKNOWN là đề xuất D13 ở §3.2; non-null sai kiểu vẫn TypeError. Không hạ mức khi dữ liệu khác đã chứng minh trọn một rule. | D dòng 15–20; TA §5; D04/D13 |

### 3.1. D04 — Validation nghiêm ngặt, được TA thay thế một phần

**TA-CONFIRMED:** tuổi null không còn bị coi là input invalid; boolean null không còn bị coi là sai kiểu chỉ vì null. Thiếu/null HATT hiện tại và nền là unavailable hợp lệ. Các quy tắc nội bộ cũ trái các điểm này đã được thay thế trong Revision 03. Không đồng nhất unavailable với invalid. [TA §§2–5]

**APPROVED BY LEAD — phần không bị thay thế:** non-null sai kiểu raise TypeError; sai miền số hoặc khóa ngoài allowlist raise ValueError. Giữ tuổi hữu hạn ≥0, HATT hiện tại int ≥0 và nền int >0 nếu có số; bool không thay số, không ép kiểu, không tự đặt giới hạn trên. Ví dụ “huyết áp ≤0” ở TA §6 là phạm vi nhóm được chọn policy, không phải lệnh sửa policy đã duyệt: HATT hiện tại 0 tiếp tục hợp lệ, nền 0 tiếp tục invalid.

Validate mọi trường có mặt trước suy luận. Một trường invalid không được bỏ qua vì rule khác đã TRUE. Không đổi invalid thành UNKNOWN hoặc trả THEO_DOI để che lỗi dữ liệu. Nếu audit thành công, phát sinh TypeError/ValueError đúng D04; lỗi kép ưu tiên lỗi audit an toàn theo §4.4. Không đưa raw input hoặc dữ liệu nhạy cảm vào message/chaining/log. [L; TA §6]

### 3.2. D13 — Logic nội bộ đã duyệt và đề xuất mở rộng unavailable

Enum TRUE/FALSE/UNKNOWN cùng AND/OR/NOT tường minh và cách đếm T/U của R02 là thiết kế nội bộ đã được Leader duyệt. TA chỉ bắt buộc không raise vì boolean missing/null, và không hạ kết luận từ một rule đã được dữ liệu hiện có chứng minh trọn vẹn; TA không chỉ định Enum hoặc Kleene là cách duy nhất. [TA §5; L]

**PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION:** hợp nhất boolean missing và explicit null thành UNKNOWN; phần missing → UNKNOWN đã có trong thiết kế cũ, còn mở rộng null và cách áp dụng cho các ca phụ thuộc unavailable cần Leader xác nhận. Đây không phải TA phê duyệt implementation detail.

| Dữ liệu boolean nhận được | Xử lý/định hướng | Trạng thái nguồn |
|---|---|---|
| Có True đúng kiểu bool | TRUE | Thiết kế nội bộ đã duyệt |
| Có False đúng kiểu bool | FALSE | Thiết kế nội bộ đã duyệt |
| Thiếu khóa hoặc có null/None | Không exception chỉ vì unavailable; đề xuất UNKNOWN | Ràng buộc không exception là TA; ánh xạ hợp nhất là đề xuất chờ Leader |
| Có số, chuỗi hoặc non-null sai kiểu | Validation TypeError, không chuyển UNKNOWN | D04 không bị thay thế |

Raw input và trạng thái đánh giá điều kiện là hai lớp khác nhau. UNKNOWN không là giá trị input mới hoặc nhãn output thứ tư. HATT unavailable có thể để điều kiện nội bộ chưa xác định; TA §§3–4 vẫn cho phép trả PHAN_VE khi Tầng 2 TRUE và tuổi có, dù chưa có bằng chứng sốc. Không cần biến mọi UNKNOWN thành FALSE để thực hiện quy định này.

## 4. Yêu cầu phân loại

### 4.1. Yêu cầu chức năng

| ID | Yêu cầu | Phân loại nguồn và căn cứ |
|---|---|---|
| FR-01 | Thực thi classify(patient), điều phối validation, rule evaluation, classification/explanation và audit kể cả direct call. Không đổi signature hoặc phụ thuộc ID fixture; UUID/context ngoài PatientInput. | FACT — C; E A-01–A-02. Thiết kế D05/D07 đã duyệt. |
| FR-02 | R01-PV khớp khi `co_di_nguyen_nghi_ngo = false` **VÀ** `co_ton_thuong_da_niem_mac = true` **VÀ** (`co_trieu_chung_ho_hap = true` **HOẶC** `co_trieu_chung_tuan_hoan = true`). | FACT — D dòng 41. D13 quy định cách đánh giá khóa boolean vắng mặt. |
| FR-03 | R02-PV khớp khi `co_di_nguyen_nghi_ngo = true` **VÀ** ít nhất hai trong bốn nhóm da/niêm mạc, hô hấp, tuần hoàn, tiêu hóa nặng là true. | FACT — D dòng 42. D13 quy định cách xác định trạng thái điều kiện đếm khi thiếu dữ liệu. |
| FR-04 | R03-PV khớp khi `co_di_nguyen_nghi_ngo = true` **VÀ** ((`di_nguyen_qua_duong_hit = false` **VÀ** `co_trieu_chung_ho_hap = true`) **HOẶC** `co_trieu_chung_tuan_hoan = true`). Dùng đúng trường dị nguyên nghi ngờ trong biểu thức. | FACT — D dòng 43. Giữ nguyên ngoặc và AND/OR khi áp dụng D13. |
| FR-05 | R-SOC cần ít nhất một rule Tầng 2 TRUE và bằng chứng tụt HATT theo bảng. Tuổi unavailable không chọn được ngưỡng: áp dụng THEO_DOI / null. HATT hiện tại unavailable, hoặc người lớn HATT ≥90 thiếu nền, không đủ xác nhận nhánh sốc nhưng không chặn PHAN_VE đã được Tầng 2 xác nhận khi tuổi có. Không gán BP mặc định. | D dòng 25–35; TA §§2–5. |
| FR-06 | Sau validation, tuổi missing/null → THEO_DOI / null. Khi tuổi có và sốc được chứng minh → SOC_PHAN_VE / R-SOC. Nếu Tầng 2 có rule TRUE mà chưa xác nhận sốc → PHAN_VE, chọn đúng một rule theo R01-PV > R02-PV > R03-PV. Tất cả rule FALSE → THEO_DOI / null. Các ca phụ thuộc boolean unavailable và chưa có rule TRUE theo D13 thuộc đề xuất policy §4.2, không phải D01–D03 chờ TA. | D; TA §§1–5; D13 với phạm vi đề xuất được ghi rõ. |
| FR-07 | Áp dụng §3: không exception chỉ vì missing/null ở các trường được TA cho phép. Non-null sai kiểu, sai miền, khóa lạ vẫn validation D04. Không bỏ qua invalid ở trường không cần cho rule. Phân biệt quy định TA với đề xuất boolean unavailable → UNKNOWN. | TA §§5–6; D04/D13; E A-04. |
| FR-08 | Trả đúng ba trường §5. ly_do gắn rule/kết quả, nêu thiếu tuổi hoặc chưa xác nhận sốc do thiếu HATT hiện tại/nền khi tương ứng. Có thể nêu rule khác cùng thỏa; không raw input, khẳng định an toàn hoặc khuyên điều trị. | D dòng 49–55; TA §§1–4; D06. |
| FR-09 | Public classify() audit đúng Timestamp, User_UUID, Action_Type, Status. Lần phân loại hợp lệ hoàn tất gồm output do dữ liệu unavailable dùng SUCCESS; không ghi INVALID_INPUT chỉ vì missing/null được TA cho phép. Invalid thực sự theo D04 vẫn audit INVALID_INPUT khi writer thành công. Giữ fail-closed và ưu tiên lỗi audit khi lỗi kép. | E A-06; D05/D07/D08; TA §5. |

| Tuổi tính bằng năm | Điều kiện tụt HATT cho FR-05 |
|---|---|
| 0 ≤ tuổi < 1 | HATT < 70 mmHg |
| 1 ≤ tuổi < 11 | HATT < 70 + 2 × tuổi, đơn vị mmHg |
| 11 ≤ tuổi < 18 | HATT < 90 mmHg |
| Tuổi ≥ 18 | HATT < 90 mmHg **HOẶC** giảm > 30% so với HATT nền |

Các ngưỡng và dấu so sánh giữ nguyên. Với người lớn, giảm >30% tương đương HATT <0,7 × nền; giảm đúng 30% không thỏa. Thiếu nền không cần cho nhánh HATT <90 đã TRUE. Nếu nhánh tuyệt đối không thỏa và nền unavailable, nhánh tương đối không được tính là đã thỏa để xếp Tầng 1; đây không phải bằng chứng huyết áp bình thường. [D; TA §4]

### 4.2. D13 — Đánh giá ba trạng thái và ranh giới policy

Giữ nguyên biểu thức R01/R02/R03. AND: có FALSE → FALSE, mọi vế TRUE → TRUE, còn lại UNKNOWN. OR: có TRUE → TRUE, mọi vế FALSE → FALSE, còn lại UNKNOWN. NOT TRUE → FALSE, NOT FALSE → TRUE, NOT UNKNOWN → UNKNOWN. Không dùng truthiness của Enum hay ép UNKNOWN thành False. [L]

| Biểu thức minh họa | Trạng thái nội bộ |
|---|---|
| TRUE OR UNKNOWN | TRUE |
| FALSE OR UNKNOWN | UNKNOWN |
| FALSE AND UNKNOWN | FALSE |
| TRUE AND UNKNOWN | UNKNOWN |

R02: T là số hệ TRUE, U là số hệ UNKNOWN. T ≥2 → điều kiện đếm TRUE; T+U <2 → FALSE; còn lại UNKNOWN. Sau đó AND với co_di_nguyen_nghi_ngo như bảng gốc. Rule chắc chắn TRUE không bị mất hiệu lực vì rule khác UNKNOWN. Chọn trong các rule TRUE theo thứ tự TA; vẫn áp dụng tuổi missing/null → THEO_DOI và ưu tiên R-SOC khi có bằng chứng. [TA §§1–5; L]

**PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION:** dùng UNKNOWN cho boolean missing/null và giữ hướng THEO_DOI / null khi kết quả phụ thuộc unavailable, chưa có rule chắc chắn TRUE và không có nhánh TA đã quy định riêng. Không tự công bố đây là expected duy nhất bắt buộc từ TA; Leader cần xác nhận mở rộng trước khi khóa các ca này.

**Rủi ro co_di_nguyen_nghi_ngo:** trường này xuất hiện dưới NOT ở R01 và trực tiếp ở R02/R03. Ví dụ tuổi/HATT đủ, da và hô hấp TRUE, đường hít TRUE, tuần hoàn/tiêu hóa FALSE nhưng S unavailable: theo Kleene R01 và R02 đều UNKNOWN; nếu S=False thì R01 khớp, nếu S=True thì R02 khớp. Suy mặc định S=False có thể chọn sai rule_id; fallback THEO_DOI có thể bỏ qua mức phản vệ chung của các khả năng. Đây là rủi ro policy cần Hải/Việt Đức phân tích để Leader xét đề xuất D13, không phải rule y khoa hoặc cách gán rule_id mới được phê duyệt. Không downgrade khi một rule độc lập đã chắc chắn TRUE. [TA §5]

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
| D13 | Enum/toán tử/T-U giữ nguyên; extension boolean null → UNKNOWN và áp dụng cho ca phụ thuộc unavailable | Thiết kế lõi đã duyệt; extension là PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION |

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

## 5. Hợp đồng dữ liệu đầu ra

Mọi kết quả phân loại vẫn có đúng ba khóa dưới đây. Dữ liệu unavailable được TA cho phép không tự là lỗi; non-null invalid theo D04 phát sinh lỗi validation khi audit thành công, hoặc lỗi audit an toàn nếu writer thất bại. [D; TA; L]

| Trường | Kiểu | Giá trị và điều kiện |
|---|---|---|
| `muc_do` | Chuỗi | Chỉ SOC_PHAN_VE, PHAN_VE, THEO_DOI. Tuổi thiếu/null → THEO_DOI. Tuổi có, Tầng 2 TRUE và sốc xác nhận → SOC_PHAN_VE; chưa xác nhận sốc do thiếu BP/nền vẫn PHAN_VE. |
| `rule_id` | Chuỗi hoặc null | R-SOC cho sốc; nếu PHAN_VE chọn một rule TRUE theo R01-PV > R02-PV > R03-PV. THEO_DOI dùng null thực, không chuỗi null. |
| `ly_do` | Chuỗi | Ngắn, truy vết rule/kết quả; nêu thiếu tuổi hoặc thiếu BP/nền khi tương ứng; không raw patient data, khẳng định an toàn hoặc khuyên điều trị. |

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
| TA-EX-12 | Tuổi 15, HATT 110, S=TRUE, I=TRUE, K=TRUE, H=C=FALSE, G thiếu/null | Không exception; expected cuối theo policy nhóm được công bố | Đề xuất UNKNOWN và fallback THEO_DOI/null khi R02 UNKNOWN, chờ Leader; MISS-012 và null tương ứng |

TA-EX-01–11 được đối chiếu quy định TA, không phải lời khẳng định đã thực thi test. TA-EX-12 kiểm việc ghi rõ policy đề xuất và trạng thái chờ Leader, chưa khóa expected như một quyết định đã duyệt. Khi không có lỗi invalid khác và audit thành công, các ca phân loại hợp lệ dùng SUCCESS, không INVALID_INPUT chỉ vì missing/null. Các lý do trong ma trận là yêu cầu diễn đạt, không khóa nguyên văn template.

## 6. Yêu cầu phi chức năng

| ID | Yêu cầu | Bằng chứng kiểm chứng dự kiến | Nguồn |
|---|---|---|---|
| NFR-01 | Dùng time.perf_counter_ns(); 100 warm-up ngoài mẫu, N≥1.000 lượt đo; nearest-rank p50/p95, p95 <100 ms. Phép đo chính là full public classify() có open/write/close audit thực; logic thuần báo riêng. | Protocol tái lập, mẫu thực, Python/OS/CPU-hardware, số lượt, dữ liệu synthetic và cấu hình I/O; chưa có số liệu | E §7.3 A-10; G D10; L OPEN-09/10 |
| NFR-02 | Chỉ dùng dữ liệu synthetic. Không có PII, dữ liệu bệnh nhân thật, thông tin xác thực hoặc secret trong input, dữ liệu test, log và hồ sơ bàn giao. | Review bảo mật/riêng tư trên file được theo dõi và bằng chứng sinh ra | D dòng 22–23; E §§5, 7 |
| NFR-03 | Audit bốn trường/giá trị §4.4, UUID đúng scope, fail-closed/error precedence. Allowed missing/null không tự thành INVALID_INPUT. Message/chaining/log không lộ raw input. | Kiểm schema/UTC/UUID, SUCCESS cho unavailable hợp lệ, INVALID_INPUT cho invalid thực sự, writer failure/lỗi kép | E A-06; D07/D08; TA §5 |
| NFR-04 | Giữ classify(patient) và ranh giới rule/I/O; Enum/toán tử tường minh theo D13 đã duyệt, không truthiness. Phân biệt TA bắt buộc với null → UNKNOWN đang đề xuất. | Review interface, source hierarchy và test-state coverage | E §§7.1,9; D05/D13; TA |
| NFR-05 | Test normal/boundary/invalid/missing/null, overlap với thứ tự TA; thay/chỉnh stub ở M2. tmp_path/fixtures reset context, độc lập thứ tự; direct/explicit session, writer failure/lỗi kép, Enum/T-U và TA-EX-01–12. | Test Plan/QA Matrix cập nhật theo TA; policy extension chờ Leader ghi riêng; pytest -q từ clean checkout với test nghiệp vụ thực | E A-07/A-08; D09; TA; L |
| NFR-06 | GitHub Actions chạy test trên Pull Request. | Cấu hình workflow và liên kết lượt chạy PR có bước test thực tế | E §7.3 A-09; W |
| NFR-07 | Giải thích ngắn gắn rule/kết quả, đúng mức chắc chắn: thiếu tuổi, thiếu số đo hiện tại hoặc chưa xét được giảm tương đối. Không raw input/điều trị hoặc kết luận an toàn. | Review output cho các ví dụ TA, không khóa template chưa duyệt | D; TA §§1–4; D06 |
| NFR-08 | Có hướng dẫn cài/chạy/test tái lập, disclaimer chính xác trong README và hồ sơ tài liệu/bàn giao theo các mốc đề yêu cầu. | README và tài liệu yêu cầu, quyết định, kiểm thử, bảo mật/riêng tư, AI-use, đóng góp | E §§4–6, 7.3 A-11, 11 |

Protocol D10 đã được Leader chốt: sắp N mẫu tăng dần, lấy phần tử tại vị trí `ceil(p × N)` theo chỉ số bắt đầu từ 1; p50 dùng p=0,50 và p95 dùng p=0,95. Chuyển nanosecond sang millisecond bằng chia 1.000.000. Loại 100 warm-up khỏi mẫu; không mock writer trong phép đo full-path. p95 <100 ms là ngưỡng của đề, chưa có kết quả để kết luận đạt. [L OPEN-10; E A-10]

## 7. Tiêu chí nghiệm thu

Trạng thái vẫn phản ánh bằng chứng tại baseline: NOT IMPLEMENTED là chưa có chức năng/tài liệu cần thiết, PARTIALLY AVAILABLE là có khung nhưng thiếu bằng chứng nghiệp vụ. TA CONFIRMED là nguồn yêu cầu đã rõ, không đồng nghĩa VERIFIED. Không AC nào được nâng thành VERIFIED trong Revision 03; không có kết quả chạy test/CI/benchmark mới từ việc sửa tài liệu.

| AC | Yêu cầu | Điều kiện nghiệm thu | Bằng chứng cần có | Nguồn | Trạng thái hiện tại |
|---|---|---|---|---|---|
| A-01 | Phân loại đúng contract | classify() thực thi bảng và làm rõ TA, hết NotImplementedError | Rule–code/test mapping gồm priority, age override và BP unavailable | E A-01; D; TA | NOT IMPLEMENTED |
| A-02 | Không hard-code fixture ID | Kết quả dựa trên dữ liệu đặc tả | Review code và fixture synthetic độc lập | E A-02; C | NOT IMPLEMENTED |
| A-03 | Đủ mức phân loại | SOC_PHAN_VE/PHAN_VE/THEO_DOI theo bảng và TA | Tầng 1/2, overlap, missing/null và TA-EX | E A-03; D; TA | NOT IMPLEMENTED |
| A-04 | Policy dữ liệu công bố và thực thi | Không lỗi chỉ vì missing/null được TA cho phép; tuổi null không TypeError; Boolean unavailable không tự invalid; giữ lỗi non-null sai kiểu/miền/khóa thừa. Extension D13 phải được Leader xác nhận trước khi coi đã duyệt | Policy/source review, tính lại invalid cũ, test null/missing và dữ liệu thực sự invalid | E A-04; TA §§2–6; D04/D13 | NOT IMPLEMENTED; TA đã làm rõ D01–D03; extension D13 AWAITING LEADER CONFIRMATION |
| A-05 | Explanation truy vết | ly_do gắn rule/kết quả, nêu tuổi/BP/nền unavailable phù hợp; không raw input/điều trị | Output và privacy assertions theo TA | E A-05; D; TA | NOT IMPLEMENTED |
| A-06 | Audit an toàn đúng schema | Bốn trường; CLASSIFY, SUCCESS/INVALID_INPUT theo nghĩa thao tác; không INVALID_INPUT chỉ vì allowed unavailable | Schema/UTC/UUID/status, failure paths, dữ liệu cấm | E A-06; D07/D08; TA §5 | NOT IMPLEMENTED |
| A-07 | Test nghiệp vụ đủ nhóm | Normal/boundary/invalid/missing/null; thay/chỉnh test stub | Bộ test được review và map TA-EX/FR | E A-07; T | PARTIALLY AVAILABLE — mới có test minh họa NotImplementedError; chưa có bộ test nghiệp vụ đạt |
| A-08 | Chạy đạt từ clean checkout | pytest -q đạt với test nghiệp vụ đã thay/chỉnh stub | Lệnh, môi trường, kết quả thực chạy | E A-08; R | PARTIALLY AVAILABLE — có lệnh, chưa có bằng chứng test nghiệp vụ clean checkout đạt |
| A-09 | CI trên PR | GitHub Actions thực sự chạy bộ test cho PR | PR run URL và bước test thực tế | E A-09; W | PARTIALLY AVAILABLE — có workflow, chưa cập nhật bằng chứng CI nghiệp vụ trong task tài liệu |
| A-10 | Benchmark đúng protocol | N≥1.000 sau 100 warm-up; nearest-rank p50/p95; p95 <100 ms, công bố máy và I/O full-path | Phương pháp và số liệu thật | E A-10; D10 | NOT IMPLEMENTED — protocol đã duyệt, chưa có số liệu |
| A-11 | Disclaimer README | Có chính xác educational/synthetic — not for clinical use | Kiểm tra README | E A-11; R | NOT IMPLEMENTED |

Việc test stub có thể chạy đạt chỉ chứng minh stub; không chứng minh yêu cầu nghiệp vụ. Hải lập/cập nhật Test Plan, Việt Đức cập nhật QA traceability và bằng chứng; task này không sửa các file đó. [P; L]

## 8. Truy vết yêu cầu

| ID yêu cầu | Rule hoặc AC liên quan | Kiểm chứng dự kiến ở mức yêu cầu |
|---|---|---|
| FR-01 | A-01, A-02 | Giữ interface và fixture independence; public orchestration vẫn audit, provider ngoài input |
| FR-02 | R01-PV; A-01/A-03/A-07 | Giữ NOT/AND/OR; kiểm rule độc lập vẫn TRUE khi boolean khác missing/null theo TA-EX-10/11 |
| FR-03 | R02-PV; A-01/A-03/A-07 | Đếm 2/4 và T/U; assert R02 riêng tránh bị R03 che; TA-EX-01,06,07,12 |
| FR-04 | R03-PV; A-01/A-03/A-07 | Giữ ngoặc/đường hít/tuần hoàn; rule TRUE không bị rule UNKNOWN làm mất hiệu lực |
| FR-05 | R-SOC; A-01/A-03/A-07 | Biên tuổi/BP, giảm đúng/trên 30%, không suy nền; TA-EX-02–09, nguồn TA-02–04 |
| FR-06 | Ưu tiên, fallback; A-01/A-03/A-07 | R-SOC trước, tuổi unavailable override, R01>R02>R03; fallback phụ thuộc unavailable ghi là đề xuất; TA-EX-01–12 |
| FR-07 | A-04/A-07 | Missing/null không tự là invalid; D04 strict với non-null sai kiểu/miền/khóa lạ; tính lại INV/AUD cũ theo TA-EX |
| FR-08, NFR-07 | A-05 | Ba khóa và ly_do phản ánh rule/thiếu tuổi/BP/nền; không raw input hoặc điều trị |
| FR-09, NFR-02/03 | A-06 | SUCCESS cho phân loại unavailable hợp lệ, INVALID_INPUT cho invalid thực sự; giữ UTC/UUID, scope/reset và fail-closed/lỗi kép |
| NFR-01 | A-10 | Protocol D10 và số liệu thực, không đổi do TA |
| NFR-04 | A-01/A-02 | Review minimal helpers, Enum và tách policy TA/team/proposal |
| NFR-05 | A-07, A-08 | Test nghiệp vụ thay/chỉnh stub, bảng logic, context/failure/isolation; pytest -q từ clean checkout, có bằng chứng thực chạy |
| NFR-06 | A-09 | Cấu hình và PR run có bước test thực tế |
| NFR-08 | A-11; E §§6,11 | Disclaimer và hồ sơ bàn giao đầy đủ |

TA-EX-01–12 ở §5.1 là ánh xạ bàn giao yêu cầu, không phải test ID đã được Hải sửa hoặc bằng chứng đã chạy. Theo P, Hải cập nhật M1-02, Việt Đức map M1-03, Huy kiểm nguồn và phê duyệt nội bộ.

### 8.1. Tác động cần Hải/Việt Đức tính lại — không phải kết quả chạy

Đối chiếu dữ liệu synthetic ở nhánh Hải tại [commit 2c6685e55af47eea55ffeea63c250272a4e71fe3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/tree/2c6685e55af47eea55ffeea63c250272a4e71fe3/docs/m1-hai). Chưa sửa Test Plan/QA workbook, chưa chạy engine.

| Test ID đang có | Kỳ vọng cần cập nhật theo TA | Audit khi hoàn tất và writer thành công |
|---|---|---|
| PEND-001 | PHAN_VE / R02-PV | SUCCESS |
| PEND-002, PEND-007 | THEO_DOI / null vì thiếu tuổi | SUCCESS |
| PEND-003, PEND-004 | PHAN_VE / R01-PV, nêu thiếu HATT hiện tại | SUCCESS |
| PEND-005, PEND-006 | PHAN_VE / R02-PV, nêu thiếu nền | SUCCESS |
| INV-001, INV-017/021/025/029/033/037, AUD-002 | Không exception chỉ vì null; với dữ liệu hiện có của các ca này: THEO_DOI / null | SUCCESS, không INVALID_INPUT |
| INV-043 | G=null không che R01 TRUE; tuổi 15, HATT 80 nên SOC_PHAN_VE / R-SOC | SUCCESS |
| 35 ca invalid còn lại trong 44 ca lỗi cũ | 27 TypeError, 8 ValueError khi audit thành công; không trả classification | INVALID_INPUT; nếu writer cũng lỗi thì áp dụng ưu tiên lỗi audit |

Chín ca từ nhóm invalid cũ nay hợp lệ gồm INV-001, sáu boolean-null INV-017/021/025/029/033/037, INV-043 và AUD-002. Không chuyển máy móc cả 44 ca sang exception. Hải phải tái tính từng input/expected và cập nhật nhãn; Việt Đức đối chiếu từng Test ID/bằng chứng. Các ca thực sự phụ thuộc boolean unavailable như MISS-009/MISS-012 và null tương ứng cần review theo extension D13, không tự gắn một kết quả duy nhất là TA bắt buộc.


## 9. Làm rõ TA, trạng thái quyết định và phần còn chờ Leader

Đã đọc toàn bộ [bình luận fossbk-spec](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) tại Issue #15, tạo/cập nhật lúc 14:01:50 UTC ngày 08/11/2026. Làm rõ áp dụng chung cho Track A; D01–D03 trong phạm vi đã trả lời không còn chờ TA. Không biến phê duyệt TA về hành vi thành phê duyệt toàn bộ kiến trúc nhóm.

| ID | Hành vi hiện hành | Trạng thái và nguồn |
|---|---|---|
| D01 | Khi nhiều rule Tầng 2 TRUE, PHAN_VE và chọn R01>R02>R03; sốc xác nhận thì SOC_PHAN_VE/R-SOC | TA CONFIRMED — [TA §1](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D02 | Tuổi missing/null: THEO_DOI/null; giải thích thiếu tuổi | TA CONFIRMED — [TA §§2,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D03 | Tuổi có, Tầng 2 TRUE: current BP missing/null vẫn PHAN_VE; người lớn HATT ≥90 thiếu/null nền vẫn PHAN_VE; HATT <90 có thể xác nhận sốc không cần nền | TA CONFIRMED — [TA §§3–5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |

TA-05 bắt buộc missing/null boolean không tự gây exception và không hạ kết luận khi một rule đã được dữ liệu còn lại chứng minh trọn vẹn. TA-06 cho phép policy nội bộ trong khoảng chưa quy định, phải công bố/test/giải trình và không đổi rule/ngưỡng/schema.

**Chờ Leader:** extension D13 boolean missing/null → UNKNOWN, đặc biệt explicit null, và áp dụng policy đã công bố cho trường hợp kết quả phụ thuộc unavailable: **PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION**. Khi xét cần phân tích rủi ro S xuất hiện cả true/false ở §4.2. Không hỏi lại hoặc trì hoãn các đầu ra TA đã chốt. Không tạo câu hỏi TA mới trong patch này.

Các quyết định ContextVar, UUID scope, JSONL, fail-closed, error precedence, isolation, Enum và benchmark vẫn giữ nguyên ngoài phần bị TA thay thế. Tên helper/exception audit và path cụ thể là chi tiết triển khai. Default path vẫn đề xuất chờ peer review; unexpected internal exception vẫn residual review item. Dùng liên kết GitHub theo commit cho tài liệu khác nhánh; chưa có DECISIONS.md trên nhánh PR #1 nên không thêm liên kết tương đối bị thiếu.

Tiêu đề R03 nói dị nguyên đã biết nhưng biểu thức dùng co_di_nguyen_nghi_ngo; tiếp tục giữ biểu thức và chín tên khóa như D. Không suy thêm khóa hoặc rule. [D; TA]

## 10. Rủi ro, phụ thuộc và tài liệu tham chiếu

| Rủi ro | Kiểm soát và review |
|---|---|
| Còn dùng policy cũ coi tuổi/boolean null là invalid | Đồng bộ dữ liệu/expected/AUD status theo TA; không chuyển máy móc 44 ca lỗi cũ sang exception |
| Quên tuổi unavailable override hoặc để thiếu BP chặn PHAN_VE | Review TA-EX-01–09 và ly_do, phân biệt thiếu bằng chứng sốc với loại bỏ Tầng 2 |
| Ép UNKNOWN thành False hoặc chọn rule_id không được chứng minh | Giữ Enum/toán tử; xem rủi ro S true/false và xác nhận extension D13 trước khi khóa các ca phụ thuộc unavailable |
| Sai ngoặc/ngưỡng hoặc suy BP mặc định | Đối chiếu biểu thức gốc, boundary và >30% nghiêm ngặt; không tạo rule y khoa mới |
| Audit SUCCESS/INVALID_INPUT bị dùng nhầm | Allowed missing/null không tự là lỗi; giữ D04 cho invalid thực sự, bốn trường và error precedence |
| Direct call chưa cấu hình audit path | Tiếp tục review đề xuất ở ADR, không tự chọn/duyệt path trong task này |
| Unexpected internal exception trước audit thành công | Residual implementation risk / review item: không SUCCESS hoặc tự gán INVALID_INPUT; không thêm status/schema hoặc log payload; Hải/Việt Đức review cách xử lý |
| Nhầm review tài liệu với nghiệm thu | Giữ 11 AC chưa VERIFIED; cần test nghiệp vụ/clean checkout/CI/benchmark thực tế |
| Nguồn snapshot G/P và M1-02/M1-03 còn policy cũ | Giữ snapshot là lịch sử; source TA và Revision 03 ưu tiên hơn. Chỉ bàn giao tác động, không tuyên bố đã sửa file Hải/QA |
| AI-use hoặc phối hợp thiếu bằng chứng | Ghi công cụ/phạm vi/kiểm chứng/quyết định và người chịu trách nhiệm thực tế; Huy review nguồn, Hải M1-02, Việt Đức M1-03 |

| Ký hiệu | Nguồn và phiên bản |
|---|---|
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung hiển thị v1.0.2 dù tên URL ghi v1.0.0, đối chiếu ngày 08/11/2026 qua HTML xuất bản của fossbk-spec/ktpmud-book. Áp dụng §§4–7, 9, 11–12. |
| D | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag starter chính thức `bkt-2026-v1`. |
| TA | [Trả lời chính thức fossbk-spec — Issue #15 comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), §§1–6, tạo/cập nhật 08/11/2026 14:01:50 UTC; áp dụng chung Track A. |
| Q2 | [Requirements Revision 02 — lịch sử trước đồng bộ TA](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/662c47be9eba076bf9ca551403cc3e961f421d42/REQUIREMENTS.md); không dùng policy cũ trái TA cho hiện trạng. |
| G | [Project Guide](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/PROJECT_GUIDE.md), mốc nguồn tích hợp, đặc biệt §§3–5. |
| P | [Team Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/TEAM_PLAN.md), mốc nguồn tích hợp, đặc biệt §3. |
| C | [Interface classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/rule_engine/classifier.py), mốc nguồn tích hợp. |
| T | [Test mẫu starter](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/tests/test_classifier.py), mốc nguồn tích hợp. |
| W | [Workflow GitHub Actions](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/.github/workflows/test.yml), mốc nguồn tích hợp. |
| R | [README starter](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/README.md), mốc nguồn tích hợp. |
| I | [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15), đã đọc toàn bộ hai comments trong preflight 08/11/2026: câu hỏi nhóm và trả lời fossbk-spec; không sửa/đăng comment trong task này. |
| L | Phê duyệt Leader trong hội thoại đến TASK 02C.5 cho D04–D13/10 OPEN và xuất bản Revision 02. TASK 02C.6 yêu cầu đồng bộ TA, cho phép chỉnh/commit/push đúng Requirements/ADR và cập nhật hai PR hiện có, không merge. Phần cũ trái TA đã bị thay thế; extension boolean null → UNKNOWN chưa được Leader phê duyệt. |

Nguồn D + TA quyết định các yêu cầu bắt buộc; G/P là snapshot phân công/lịch sử, không ghi đè làm rõ TA. Phê duyệt nội bộ chỉ giữ phần không xung đột; extension còn đề xuất phải được ghi/test và Leader xác nhận. Không diễn giải TA §6 thành thay đổi tự động miền validation đã duyệt.

### 10.1. Lịch sử thay đổi

| Phiên bản | Nội dung | Tình trạng bằng chứng |
|---|---|---|
| Revision 02, 08/11/2026 — lịch sử tại 662c47be9eba076bf9ca551403cc3e961f421d42 | D01–D03 khi đó PENDING TA CONFIRMATION; tuổi/boolean null bị coi invalid theo policy cũ | Snapshot trước trả lời TA, không phải policy hiện hành |
| Revision 03, 08/11/2026 — TASK 02C.6 | Đồng bộ TA-01–06, thay thế một phần D04/D13, cập nhật FR/AC/truy vết và 12 ví dụ; extension null → UNKNOWN chờ Leader | Draft PR / Awaiting Peer Review; chưa có implementation/test/benchmark evidence |
