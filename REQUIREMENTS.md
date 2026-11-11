# Yêu cầu và phạm vi Track A

| Thuộc tính | Giá trị |
|---|---|
| Cuộc thi | KTPMUD Hack Marathon 2026, Track A — Dr May Day: Rule Engine Sprint |
| Mã nhóm | `173820_n27` |
| Người phụ trách | Huy Đức |
| Mốc bàn giao | M1-01, Checkpoint 1, ngày 08/11/2026 |
| Phiên bản | Revision 04 — cập nhật cách trình bày và nguồn Issue #31 |
| Mốc đối chiếu | `track-a-development` tại [`912ad084`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/commit/912ad0847409002de195a91483dcf8fba4c073d9), đối chiếu ngày 12/11/2026 |
| Trạng thái | M1 Revision 04 đã tích hợp vào `track-a-development` ngày 10/11/2026; chưa có xác nhận nghiệm thu scope của TA hoặc bằng chứng kiểm thử runtime |
| Mốc nguồn starter | `bkt-2026-v1` → `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Mốc nguồn tích hợp | `track-a-development` tại `9bc4fc186415d7a13cd9d49692c50f3c945ddf7b` (merge commit PR #4, hoàn tất tích hợp M1 ngày 10/11/2026) |
| Baseline trước Revision 04 | `c855c6d4f2135a14ad94485734d4d2e604cb9cff` trên `docs/m1-requirements-huy`; snapshot Revision 03, không phải HEAD sau patch này |
| Làm rõ chính thức | [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) làm rõ D01–D03 và dữ liệu thiếu/null; [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002) làm rõ lựa chọn mã đại diện trong tình huống thiếu khóa boolean. |

Revision 04 được hoàn thiện trên nhánh `docs/m1-requirements-huy` và đã **merge qua [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1)** vào `track-a-development` ngày 10/11/2026. Cùng ngày, [PR #2 (ADR)](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3 (Rule Design/Test Plan)](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) và [PR #4 (QA Matrix)](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) cũng đã merge. GitHub ghi nhận Leader self-review dạng `COMMENTED` và tài khoản `nvldvc` `APPROVED` trên cả bốn PR; chưa có lượt review của thành viên còn lại tại thời điểm merge. Quyết định tích hợp thuộc Leader và có ghi nhận ngoại lệ review. Đây là **hoàn tất tích hợp hồ sơ thiết kế nội bộ**, không phải bằng chứng TA đã nghiệm thu Checkpoint 1 hoặc toàn bộ A-01–A-11 đã được kiểm chứng. A-11 có bằng chứng disclaimer riêng tại §7.

**Thứ tự nguồn:** Đề, Decision Table V1 và các làm rõ chính thức của GV/TA được ưu tiên khi xác định yêu cầu bắt buộc; tiếp theo là quyết định nội bộ đã duyệt và các đề xuất. D01–D03 đã được TA làm rõ trong phạm vi Issue #15. Issue #31 xác nhận cách chọn mã đại diện cho trường hợp thiếu khóa boolean được nêu. Các chi tiết kỹ thuật D04–D13 do nhóm lựa chọn vẫn được phân biệt với yêu cầu chính thức. [D; TA; TA31; L]

Tích hợp tài liệu và phê duyệt nội bộ không thay thế bằng chứng thực thi hoặc xác nhận nghiệm thu phạm vi của TA. D13-E được Leader duyệt trong M1; một số nội dung về mã đại diện đã có làm rõ sau đó trong Issue #31. Chi tiết quyết định, trạng thái và các điểm còn cần review nằm ở §4.2–4.4 và §9.

## Hướng dẫn đọc tài liệu

- §1–2: mục tiêu và phạm vi; §3: dữ liệu đầu vào và kiểm tra tính hợp lệ.
- §4: quy tắc, cách xử lý dữ liệu thiếu và audit; §5: kết quả đầu ra và ví dụ.
- §6–10: yêu cầu chất lượng, tiêu chí nghiệm thu, truy vết, nguồn và rủi ro.

Một lần xử lý dự kiến đi qua: **kiểm tra đầu vào → xét quy tắc → chọn kết quả và giải thích → ghi audit**. Trong tài liệu, “rule” là một quy tắc trong bảng quyết định. Các ký hiệu kỹ thuật ở §4.2 dùng để mô tả và kiểm thử cách xử lý dữ liệu chưa biết.

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

Đầu vào `patient` dùng đúng chín tên khóa trong bảng. Không thêm tên, thông tin định danh, UUID hoặc đường dẫn vào input. `TypedDict(total=False)` trong starter chỉ mô tả kiểu tĩnh; chương trình vẫn cần tự kiểm tra dữ liệu khi chạy. [D; TA; C]

**Hai cách không có dữ liệu:**

- **Missing:** khóa không xuất hiện, chẳng hạn `{}` không có khóa `tuoi`.
- **Null:** khóa có xuất hiện nhưng không có giá trị, chẳng hạn `{"tuoi": null}`; trong Python, giá trị tương ứng là `None`.

Với ba trường số và sáu trường boolean được TA cho phép thiếu/null, cả hai cách đều biểu thị thông tin không có sẵn; riêng các trường số có kết quả tương ứng theo TA, còn chính sách boolean của nhóm ở §3.2 và §4.2. Thiếu thông tin khác với dữ liệu sai kiểu hoặc sai miền.

**Validation** là bước kiểm tra dữ liệu trước khi phân loại. Ví dụ, `"tuoi": 15` hợp lệ, `"tuoi": null` là thiếu tuổi được phép, `"tuoi": "15"` sai kiểu và `"tuoi": -5` sai miền. [TA §§2–6; D04]

| Trường | Ý nghĩa và kiểu | Kiểm tra và xử lý chính | Nguồn |
|---|---|---|---|
| `tuoi` | Tuổi theo năm. Data Dictionary gốc ghi `float`; cho phép số lẻ, ví dụ `0.5`. | Chính sách nhóm chấp nhận `int` hoặc `float` hữu hạn, không âm; không nhận `bool` hay ép chuỗi. Thiếu/null là chưa có tuổi; sau validation chọn `THEO_DOI / null`, nêu thiếu tuổi. | D; TA §§2,5; D04 |
| `huyet_ap_tam_thu` | Huyết áp tâm thu (HATT) hiện tại, mmHg. | Nếu có số: `int ≥ 0`, không nhận `bool`, `float` hay chuỗi; nhóm không đặt trần. Giá trị `0` hợp lệ theo policy dữ liệu của nhóm. Thiếu/null là chưa có số đo; nếu có tuổi và phản vệ đã được chứng minh, không tự hạ kết luận xuống `THEO_DOI`. | D; TA §§3,5; D04 |
| `huyet_ap_tam_thu_nen` | HATT nền, dùng xét giảm tương đối ở tuổi từ 18. | Nếu có số: `int > 0`, không nhận `bool`, `float` hay chuỗi; `0` invalid. Thiếu/null là chưa có nền. Ở người lớn, HATT hiện tại `<90` đủ xét nhánh tuyệt đối; nếu HATT `≥90` mà thiếu nền, vẫn giữ phản vệ đã được chứng minh và nêu chưa đánh giá được nhánh giảm tương đối. | D; TA §§4–5; D04 |
| `co_di_nguyen_nghi_ngo` | Có dị nguyên nghi ngờ hay không; xuất hiện ở cả điều kiện đúng và phủ định của các rule. | Boolean theo quy tắc chung bên dưới. | D; TA §5; D04/D13-E |
| `di_nguyen_qua_duong_hit` | Dị nguyên qua đường hít hay không; ảnh hưởng nhánh hô hấp của R03. | Boolean theo quy tắc chung bên dưới. | D; TA §5; D04/D13-E |
| `co_ton_thuong_da_niem_mac` | Có tổn thương da/niêm mạc hay không. | Boolean theo quy tắc chung bên dưới. | D; TA §5; D04/D13-E |
| `co_trieu_chung_ho_hap` | Có triệu chứng hô hấp hay không. | Boolean theo quy tắc chung bên dưới. | D; TA §5; D04/D13-E |
| `co_trieu_chung_tuan_hoan` | Có triệu chứng tuần hoàn hay không. | Boolean theo quy tắc chung bên dưới. | D; TA §5; D04/D13-E |
| `co_trieu_chung_tieu_hoa_nang` | Có triệu chứng tiêu hóa nặng hay không. | Boolean theo quy tắc chung bên dưới. | D; TA §5; D04/D13-E |

**Quy tắc chung cho sáu trường boolean:** chỉ `True` hoặc `False` đúng kiểu là dữ liệu có giá trị. Thiếu khóa hoặc `null` không tự gây lỗi; nhóm biểu diễn là `UNKNOWN` — chưa biết. Giá trị non-null sai kiểu gây `TypeError`, không ép kiểu. Không hạ mức khi các trường còn lại đã chứng minh trọn vẹn một rule. [TA §5; D04; D13-E]

### 3.1. D04 — Kiểm tra dữ liệu đầu vào

D04 là chính sách kiểm tra nghiêm ngặt do Leader duyệt; phần chính sách cũ coi tuổi hoặc boolean `null` là invalid đã được thay thế theo làm rõ của TA. Thiếu/null được phép không tự là invalid. [TA §§2–6; L]

| Trường hợp | Hành vi theo chính sách nhóm |
|---|---|
| Giá trị non-null sai kiểu, ví dụ tuổi là chuỗi `"15"` hoặc boolean là chuỗi `"true"` | `TypeError`; không ép sang kiểu khác. |
| Giá trị số đúng kiểu nhưng sai miền, ví dụ tuổi âm hoặc HATT nền bằng 0 | `ValueError`. |
| Có khóa ngoài chín khóa được phép | `ValueError`. |
| Trường được phép thiếu hoặc `null` | Xử lý là dữ liệu không có sẵn; không tự phát sinh lỗi chỉ vì thiếu/null. |

Tuổi phải là số hữu hạn `≥0`; HATT hiện tại là số nguyên `≥0`; HATT nền là số nguyên `>0` nếu được cung cấp. `bool` không thay số, nhóm không tự đặt giới hạn trên và không chuyển dữ liệu sai thành `UNKNOWN` hay `THEO_DOI` để che lỗi. Ví dụ huyết áp `≤0` tại TA §6 là khu vực cho nhóm chọn chính sách; nhóm giữ HATT hiện tại `0` hợp lệ và HATT nền `0` không hợp lệ. [TA §6; L]

Phải kiểm tra **mọi trường có mặt trước khi suy luận**, kể cả trường không liên quan tới rule đã đủ điều kiện. Nếu audit thành công, lỗi validation được báo bằng `TypeError`/`ValueError`; nếu validation và audit cùng lỗi, áp dụng thứ tự ưu tiên lỗi tại §4.4. Không đưa dữ liệu đầu vào thô hoặc dữ liệu nhạy cảm vào thông báo lỗi, chuỗi lỗi hoặc log. [D04; D08]

### 3.2. D13-E — Biểu diễn thông tin boolean chưa biết

Nhóm dùng ba trạng thái nội bộ `TRUE`, `FALSE`, `UNKNOWN` để đánh giá boolean. `True`/`False` đúng kiểu tương ứng với `TRUE`/`FALSE`; missing hoặc `null` được chuẩn hóa thành `UNKNOWN`. Giá trị non-null sai kiểu vẫn là lỗi D04. `UNKNOWN` nghĩa là chưa có thông tin, không tự coi là `False`, không phải một giá trị input mới hoặc mức phân loại thứ tư. [TA §5; L]

TA cho phép missing/null theo phạm vi đã làm rõ. Cách biểu diễn `Enum`, logic ba trạng thái và phương pháp coverage là thiết kế nhóm đã duyệt; Issue #31 làm rõ thêm việc chọn mã đại diện trong tình huống được nêu. Không bổ sung giá trị giả vào `patient`. Tình trạng chưa có HATT cũng có thể làm điều kiện huyết áp chưa xác định; cách chọn kết quả được quy định ở §4.2. [TA; TA31; L]

## 4. Yêu cầu chức năng và quy tắc xử lý

### 4.1. Yêu cầu chức năng

FR (*Functional Requirement*) là yêu cầu về việc chương trình phải thực hiện. Ba rule R01–R03 bên dưới là điều kiện gốc; §4.2 giải thích cách đánh giá khi dữ liệu boolean chưa có.

| ID | Yêu cầu | Phân loại nguồn và căn cứ |
|---|---|---|
| FR-01 | Triển khai `classify(patient)` theo contract và giữ nguyên chữ ký. Hàm này điều phối kiểm tra đầu vào, đánh giá rule, chọn kết quả, giải thích và ghi audit, kể cả khi gọi trực tiếp. Kết quả không phụ thuộc mã ca kiểm thử; UUID/context nằm ngoài `PatientInput`. | FACT — C; E A-01–A-02. Thiết kế D05/D07 đã duyệt. |
| FR-02 | R01-PV: `co_di_nguyen_nghi_ngo = false` **VÀ** `co_ton_thuong_da_niem_mac = true` **VÀ** (`co_trieu_chung_ho_hap = true` **HOẶC** `co_trieu_chung_tuan_hoan = true`). | FACT — D dòng 41. D13 quy định cách đánh giá khóa boolean vắng mặt. |
| FR-03 | R02-PV: `co_di_nguyen_nghi_ngo = true` **VÀ** ít nhất 2 trong 4 nhóm da/niêm mạc, hô hấp, tuần hoàn, tiêu hóa nặng là `true`. | FACT — D dòng 42. D13 quy định cách xác định trạng thái điều kiện đếm khi thiếu dữ liệu. |
| FR-04 | R03-PV: `co_di_nguyen_nghi_ngo = true` **VÀ** ((`di_nguyen_qua_duong_hit = false` **VÀ** `co_trieu_chung_ho_hap = true`) **HOẶC** `co_trieu_chung_tuan_hoan = true`). Giữ đúng trường dị nguyên nghi ngờ và dấu ngoặc. | FACT — D dòng 43. Giữ nguyên ngoặc và AND/OR khi áp dụng D13. |
| FR-05 | R-SOC cần phản vệ được chứng minh bằng rule chắc chắn hoặc AllPV theo D13-E **và** bằng chứng tụt HATT theo bảng. AllPV nghĩa là mọi khả năng của boolean chưa biết đều có ít nhất một rule Tầng 2 thỏa (§4.2.2). Thiếu/null tuổi → `THEO_DOI / null`. Có tuổi, thiếu HATT hiện tại hoặc người lớn HATT ≥90 thiếu nền không làm mất kết luận phản vệ đã được chứng minh; không tự gán HATT hoặc nền. | D dòng 25–35; TA §§2–5; D13-E (L). |
| FR-06 | Sau kiểm tra mọi trường, tuổi thiếu/null → `THEO_DOI / null`. Nếu có tuổi, chọn rule chắc chắn trước theo R01 > R02 > R03; không để rule chỉ có thể đúng thay rule chắc chắn. Nếu không có rule chắc chắn nhưng AllPV, giữ kết luận phản vệ; với `PHAN_VE`, chọn mã đại diện ưu tiên trong Poss — tập các rule có thể thỏa — và giải thích theo §4.2/§5. Đủ bằng chứng phản vệ và tụt HATT → `SOC_PHAN_VE / R-SOC`. Mixed hoặc không có khả năng khớp → `THEO_DOI / null`, với lý do phù hợp. | D; TA; APPROVED TEAM POLICY D13-E. |
| FR-07 | Thực hiện validation §3: missing/null được cho phép không tự là invalid; boolean không có sẵn → `UNKNOWN` theo D13-E. Giá trị non-null sai kiểu, sai miền hoặc khóa lạ xử lý theo D04. Kiểm tra cả trường invalid không liên quan đến rule trước khi suy luận; không ép kiểu. | TA §§5–6; D04/D13-E; E A-04. |
| FR-08 | Trả ba trường theo §5. `ly_do` nêu kết quả/rule và thiếu tuổi, HATT hiện tại hoặc nền khi phù hợp. Mã đại diện phải được công bố là đại diện, chưa xác nhận rule riêng; không khẳng định thông tin chưa biết đã được quan sát là `False`. DIRECT là cách gắn mã rule chắc chắn (§4.2.4); Mixed nêu chưa đủ thông tin. Không kết luận an toàn, đưa dữ liệu thô hoặc lời khuyên điều trị. | D dòng 49–55; TA §§1–4; D06 và D13-E. |
| FR-09 | Hàm `classify()` ghi audit đúng bốn trường `Timestamp`, `User_UUID`, `Action_Type`, `Status`. Phân loại hợp lệ hoàn tất ghi `SUCCESS`, kể cả khi thiếu/null được phép; không dùng `INVALID_INPUT` chỉ vì thiếu/null. Dữ liệu invalid theo D04 ghi `INVALID_INPUT` nếu writer thành công. Giữ fail-closed và thứ tự ưu tiên lỗi audit khi có lỗi kép (§4.4). | E A-06; D05/D07/D08; TA §5. |

| Tuổi tính bằng năm | Điều kiện tụt HATT cho FR-05 |
|---|---|
| 0 ≤ tuổi < 1 | HATT < 70 mmHg |
| 1 ≤ tuổi < 11 | HATT < 70 + 2 × tuổi, đơn vị mmHg |
| 11 ≤ tuổi < 18 | HATT < 90 mmHg |
| Tuổi ≥ 18 | HATT < 90 mmHg **HOẶC** giảm > 30% so với HATT nền |

Các ngưỡng và dấu so sánh giữ nguyên. Với người lớn, giảm >30% tương đương HATT <0,7 × nền; giảm đúng 30% không thỏa. Thiếu nền không cần cho nhánh HATT <90 đã TRUE. Nếu nhánh tuyệt đối không thỏa và nền unavailable, nhánh tương đối không được tính là đã thỏa để xếp Tầng 1; đây không phải bằng chứng huyết áp bình thường. [D; TA §4]

### 4.2. Xử lý khi thiếu dữ liệu đúng/sai (D13-E)

D13-E là chính sách đã được Leader duyệt để xử lý thông tin boolean chưa biết, giữ nguyên các biểu thức R01/R02/R03 của Decision Table. Cách biểu diễn và tổ chức tính toán là lựa chọn của nhóm; thầy đã làm rõ thêm việc chọn mã đại diện cho tình huống thiếu khóa ở [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002). [D; TA; TA31; L]

**Đọc nhanh:** sau khi kiểm tra dữ liệu và tuổi, nhóm ưu tiên rule chắc chắn đúng. Nếu không có rule chắc chắn, xét các khả năng của dữ liệu boolean chưa biết: mọi khả năng đều dẫn tới phản vệ thì giữ kết luận phản vệ và chọn mã đại diện; nếu chỉ một số khả năng dẫn tới phản vệ thì trả `THEO_DOI` và nêu thiếu thông tin. Đã đủ bằng chứng phản vệ **và** thỏa điều kiện tụt HATT theo tuổi thì trả `SOC_PHAN_VE / R-SOC`. Các điều kiện và thứ tự chi tiết ở dưới.

#### 4.2.1. Đánh giá điều kiện với `UNKNOWN`

Nhóm dùng logic ba trạng thái (Kleene) với `TRUE`, `FALSE`, `UNKNOWN`:

- **AND / VÀ:** có ít nhất một vế `FALSE` → `FALSE`; mọi vế `TRUE` → `TRUE`; còn lại → `UNKNOWN`.
- **OR / HOẶC:** có ít nhất một vế `TRUE` → `TRUE`; mọi vế `FALSE` → `FALSE`; còn lại → `UNKNOWN`.
- **NOT / PHỦ ĐỊNH:** `NOT TRUE → FALSE`, `NOT FALSE → TRUE`, `NOT UNKNOWN → UNKNOWN`.

| Ví dụ | Kết quả nội bộ |
|---|---|
| `TRUE OR UNKNOWN` | `TRUE` |
| `FALSE OR UNKNOWN` | `UNKNOWN` |
| `FALSE AND UNKNOWN` | `FALSE` |
| `TRUE AND UNKNOWN` | `UNKNOWN` |

Với điều kiện đếm của R02, **T** là số hệ cơ quan `TRUE`, **U** là số hệ `UNKNOWN`: `T ≥ 2` → điều kiện đếm `TRUE`; `T + U < 2` → `FALSE`; trường hợp còn lại → `UNKNOWN`. Sau đó kết hợp bằng AND với `co_di_nguyen_nghi_ngo` như bảng gốc. Không dùng truthiness của `Enum` hoặc ép `UNKNOWN` thành `False`. Rule chắc chắn đúng không mất hiệu lực chỉ vì rule khác chưa biết. [TA §§1–5; L]

#### 4.2.2. Xét các khả năng khi thiếu thông tin

Với input hợp lệ `p`, `C(p)` là tập các **completion**: mỗi completion là một cách xét `True`/`False` cho các boolean chưa biết, giữ nguyên giá trị đã biết. Có từ 1 đến 64 completion với sáu boolean. Chỉ xét biểu thức R01/R02/R03 gốc; không tự hoàn thiện trường số và không ghi dữ liệu giả vào input.

| Ký hiệu | Ý nghĩa |
|---|---|
| **Def** — definite | Các rule `TRUE` trong mọi completion: rule chắc chắn đúng. |
| **Poss** — possible | Các rule `TRUE` trong ít nhất một completion: rule có thể đúng. |
| **AllPV** | Mọi completion đều khớp ít nhất một rule Tầng 2. |
| **AnyPV** | Có ít nhất một completion khớp rule Tầng 2. |
| **Mixed** | Có completion khớp và có completion không khớp rule Tầng 2: `AnyPV` đúng nhưng `AllPV` không đúng. |

Các tập/ký hiệu chỉ dùng nội bộ để mô tả lựa chọn và kiểm thử; không thêm khóa output hoặc audit.

#### 4.2.3. Thứ tự chọn kết quả

Các bước sau mô tả việc **chọn kết quả**. Sau đó `classify()` phải hoàn tất audit `SUCCESS` trước khi trả bất kỳ kết quả phân loại hợp lệ nào; các trường hợp lỗi và thứ tự ưu tiên lỗi tuân theo §4.4.

1. Kiểm tra mọi trường theo D04. Nếu tuổi missing/null, chọn `THEO_DOI / null` và nêu thiếu tuổi theo TA; kết thúc phần lựa chọn và chuyển sang audit, không áp dụng các bước 2–6.
2. Nếu **Def không rỗng**, nhóm chọn rule chắc chắn theo `R01 > R02 > R03`; một rule chỉ possible có ưu tiên cao hơn không thay rule definite theo chính sách nhóm. Đây là cách gắn mã **DIRECT**.
3. Nếu **Def rỗng nhưng AllPV**, phản vệ được chứng minh qua các khả năng. Khi chưa đủ bằng chứng sốc, chọn `PHAN_VE` và rule ưu tiên cao nhất trong Poss làm mã đại diện **CANONICAL**.
4. Nếu đã đủ bằng chứng phản vệ theo bước 2 hoặc 3 **và** điều kiện tụt HATT theo bảng là `TRUE`, chọn `SOC_PHAN_VE / R-SOC`; kết quả này ưu tiên hơn mã phản vệ ở bước 2–3. Chỉ có tụt HATT không đủ để kết luận sốc phản vệ. Thiếu HATT không phải bằng chứng sốc; nếu có tuổi và phản vệ đã được chứng minh thì giữ `PHAN_VE`, giải thích thông tin còn thiếu.
5. Nếu **AnyPV nhưng không AllPV — Mixed**, chọn `THEO_DOI / null` và nêu chưa đủ thông tin; không coi giá trị đang `UNKNOWN` thực ra là `False`.
6. Nếu **không AnyPV**, chọn `THEO_DOI / null` với lý do không khớp. Kết quả cùng nhãn với Mixed nhưng lý do cần phân biệt.

Trạng thái tụt HATT của người lớn được xét theo cả hai nhánh của bảng: HATT `<90` đủ chứng minh nhánh tuyệt đối; khi HATT `≥90` và thiếu nền, nhánh giảm `>30%` chưa đánh giá được, không được xem là đã thỏa. [D; TA §§2–5]

#### 4.2.4. Mã trực tiếp và mã đại diện

**DIRECT**: mã phản vệ được chọn từ rule đã được xác nhận chắc chắn. **CANONICAL**: mã đại diện của các khả năng, chỉ dùng cho `PHAN_VE` khi Def rỗng và AllPV. Đây là thông tin nội bộ để tạo `ly_do`, không tạo khóa output/audit mới.

Với CANONICAL, `ly_do` **phải** nêu mã là đại diện và thông tin còn thiếu; không nói rule đại diện đã được xác nhận độc lập hoặc khẳng định trường chưa biết đã được quan sát là `False`. Không khẳng định người bệnh an toàn hoặc đưa lời khuyên điều trị/dữ liệu thô. [D06; L]

Theo [làm rõ Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002), khi các khả năng của khóa boolean thiếu cùng dẫn tới một mức nhưng khác rule, chọn mã ưu tiên cao nhất trong các rule có thể thỏa theo `R01-PV > R02-PV > R03-PV` và nêu trong `ly_do` rằng đó là mã đại diện do thiếu khóa. Phán quyết áp dụng chung Track A. Với ví dụ nhóm hỏi là `MISS-009` (Def rỗng), thầy xác nhận `PHAN_VE / R01-PV`. Thầy yêu cầu ghi quy tắc vào `DECISIONS.md` và có ít nhất một test cho ca thiếu khóa. [TA31]

Theo D13-E Leader đã chốt, khi có rule chắc chắn đúng, nhóm chọn trong Def trước. Ví dụ, [`MISS-013/014`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/912ad0847409002de195a91483dcf8fba4c073d9/docs/m1-hai/M1/TEST_CASES.csv) có R03 chắc chắn và R02 có thể thỏa; expected thiết kế của nhóm là `PHAN_VE / R03-PV` với giải thích DIRECT theo [ADR §5.8.2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/912ad0847409002de195a91483dcf8fba4c073d9/DECISIONS.md#L232). Issue #31 không nêu trực tiếp ví dụ có đồng thời rule chắc chắn và rule chỉ có thể thỏa nhưng ưu tiên cao hơn; cần đối chiếu phạm vi áp dụng khi tích hợp. Không coi phần definite-first hoặc toàn bộ chi tiết triển khai D13-E là đã được TA xác nhận riêng. [TA31; L]

#### 4.2.5. Ví dụ: thiếu dị nguyên nghi ngờ

Với input synthetic của `MISS-009`: tuổi 15, HATT 110; `co_di_nguyen_nghi_ngo` chưa có; da/niêm mạc và hô hấp `TRUE`; đường hít `TRUE`; tuần hoàn và tiêu hóa nặng `FALSE`:

| Khả năng của trường chưa có | Rule Tầng 2 khớp |
|---|---|
| `co_di_nguyen_nghi_ngo = False` | R01 |
| `co_di_nguyen_nghi_ngo = True` | R02; R03 không khớp |

Cả hai khả năng đều phản vệ: AllPV đúng, nhưng R01/R02 mỗi rule đều `UNKNOWN` khi xét riêng và Def rỗng. Theo chính sách đã duyệt và làm rõ TA, kết quả ví dụ là `PHAN_VE / R01-PV` với giải thích mã đại diện cho khả năng R01/R02; không sửa helper R01 thành `TRUE` và không khẳng định trường thiếu thực tế là `False`. Nếu HATT đủ thấp theo ngưỡng tuổi: `SOC_PHAN_VE / R-SOC`; nếu thiếu HATT: giữ `PHAN_VE` và nêu thiếu số đo; nếu thiếu tuổi: `THEO_DOI / null`. [TA31; L]

**Rủi ro cần kiểm soát:** người chỉ nhìn `rule_id` có thể hiểu nhầm mã đại diện đã được xác nhận độc lập; lời giải thích và test phải ngăn cách hiểu đó. Leader đã chấp nhận rủi ro này tại thời điểm phê duyệt D13-E. Phán quyết mới xác nhận phạm vi đã nêu, không tự biến rule đại diện thành rule definite. Không thêm rule hoặc ngưỡng lâm sàng; coverage chỉ xét các rule gốc. [TA; TA31; L]

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
| D13 | `UNKNOWN`, definite-first, AllPV, Mixed và mã đại diện theo §4.2 | Leader đã duyệt D13-E; Issue #31 làm rõ lựa chọn mã đại diện trong phạm vi nêu. Chưa có bằng chứng runtime. |

D11 giữ clinical rules/ngưỡng; D12 giữ chín tên input, ba output, bốn audit fields và privacy. Các phương án OPEN đã được Leader lựa chọn trong phạm vi ghi ở ADR; không tự thay đổi khi triển khai mà chưa đối chiếu quyết định. Đường dẫn audit mặc định vẫn là đề xuất chờ peer review; cách xử lý lỗi nội bộ bất ngờ vẫn là điểm cần review. [TA; L]

### 4.4. Nghĩa vụ audit và hành vi lỗi đã phê duyệt

Audit là nhật ký thao tác, tách khỏi kết quả phân loại; JSONL là định dạng mỗi bản ghi JSON trên một dòng. `SUCCESS` cho biết thao tác hoàn tất, không có nghĩa kết quả phân loại là an toàn. Fail-closed ở đây nghĩa là không báo phân loại thành công nếu ghi audit bắt buộc thất bại.

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
| Mọi input hợp lệ, audit thành công | Hoàn tất audit `SUCCESS` rồi mới trả ba trường kết quả, kể cả `THEO_DOI` do thiếu tuổi hoặc Mixed |
| Validation lỗi thực sự theo D04, audit thành công | Có record INVALID_INPUT, raise TypeError/ValueError đúng D04; không trả THEO_DOI |
| Validation thành công, audit lỗi | Raise lỗi audit vận hành an toàn, không trả thành công và không mặc định record đã lưu |
| Validation và audit cùng lỗi | Ưu tiên lỗi audit an toàn ra public boundary, không giả định record INVALID_INPUT tồn tại; message/chaining không lộ raw input |

Fail-closed có kiểm soát chỉ áp dụng module bài thi synthetic; không mặc nhiên áp dụng sản phẩm y tế thực tế. Path audit cấu hình ngoài input, trong vùng dữ liệu sinh của lần chạy, độc lập working directory; test dùng file/thư mục riêng, không commit runtime log. V1 ghi tuần tự, quyền sở hữu writer/file rõ; không cam kết thread/process-safe khi ghi chung file. [L OPEN-03–OPEN-06]

Writer M2 hoàn tất open append/write/close theo từng record trước khi public call báo thành công; lỗi write/flush/close phải được nhận biết theo fail-closed. Không retry vô hạn, không tạo trường/status mới hoặc mặc định fsync/durability sau mất điện. [L OPEN-09]

**Kiểm chứng tích hợp M2 — còn cần peer review:** direct `classify(patient)` khi chưa cấu hình audit path phải được đưa vào kế hoạch kiểm chứng. Cơ chế chọn path mặc định ổn định ngoài repository, không phụ thuộc working directory, là đề xuất chưa được Leader duyệt; cần kiểm tra override ngoài PatientInput cho test/demo, fail-closed khi không tạo/ghi được file và hướng dẫn nơi lưu/cấu hình trong README khi triển khai. Giữ nguyên signature và chín input keys. [TASK 02C.4 Patch A]

## 5. Đặc tả dữ liệu đầu ra

Một kết quả phân loại hợp lệ có đúng ba khóa `muc_do`, `rule_id`, `ly_do`. Dữ liệu thiếu/null được cho phép không tự là lỗi; dữ liệu invalid theo D04 phát sinh lỗi validation khi ghi audit thành công, hoặc lỗi audit an toàn nếu writer thất bại. [D; TA; L]

| Trường | Kiểu | Ý nghĩa và giá trị |
|---|---|---|
| `muc_do` | Chuỗi | `SOC_PHAN_VE`: đã chứng minh phản vệ và đủ bằng chứng tụt HATT theo tuổi. `PHAN_VE`: đã chứng minh phản vệ nhưng chưa xác nhận điều kiện sốc. `THEO_DOI`: thiếu tuổi, hoặc Mixed/không có khả năng khớp Tầng 2 theo §4.2. Không diễn đạt `THEO_DOI` thành kết luận an toàn. |
| `rule_id` | Chuỗi hoặc `null` | `R-SOC` khi xác định Tầng 1. Với `PHAN_VE`, rule chắc chắn được chọn trực tiếp theo thứ tự R01/R02/R03; nếu Def rỗng và AllPV, chọn mã đại diện ưu tiên cao nhất trong Poss theo §4.2. `THEO_DOI` dùng `null`; D13-E không chọn `PHAN_VE / null`. |
| `ly_do` | Chuỗi | Giải thích ngắn gắn với kết quả và rule. Với mã đại diện, nêu rõ mã đại diện và dữ liệu thiếu, không nói rule được xác nhận riêng. Phân biệt Mixed với không khớp; nêu thiếu tuổi/HATT/nền khi phù hợp. Không đưa dữ liệu lâm sàng thô, khẳng định dữ liệu chưa biết, kết luận an toàn hoặc lời khuyên điều trị. |

`reason` trong đề tương ứng `ly_do`. `UNKNOWN`, `DIRECT` và `CANONICAL` là khái niệm nội bộ, không phải khóa hoặc mức phân loại bổ sung. Không khẳng định “không có sốc” chỉ vì thiếu số đo; chỉ nêu chưa có bằng chứng xác nhận sốc. [D; TA; TA31; L]

### 5.1. Ma trận kiểm chứng tài liệu theo TA — không phải kết quả chạy engine

Ký hiệu rút gọn trong các ví dụ: **S** = `co_di_nguyen_nghi_ngo`, **I** = `di_nguyen_qua_duong_hit`, **K** = `co_ton_thuong_da_niem_mac`, **H** = `co_trieu_chung_ho_hap`, **C** = `co_trieu_chung_tuan_hoan`, **G** = `co_trieu_chung_tieu_hoa_nang`. Các dữ liệu và kết quả là synthetic và expected để đối chiếu, không phải kết quả chạy.

| ID | Tình huống synthetic | Expected / yêu cầu | Giải thích và ánh xạ bàn giao |
|---|---|---|---|
| TA-EX-01 | R02/R03 TRUE, tuổi 15, HATT 110, không sốc | PHAN_VE / R02-PV | Ưu tiên chính thức; ly_do có thể nêu thêm R03; PEND-001 |
| TA-EX-02 | R01 TRUE, tuổi thiếu, HATT có | THEO_DOI / null | Nêu thiếu tuổi, không chọn được ngưỡng; PEND-002 |
| TA-EX-03 | R01 TRUE, tuổi null, HATT có | THEO_DOI / null | Không TypeError chỉ vì tuổi null; `TA15-AGE-NULL` có R01 thỏa. `INV-001` là ca tuổi null hợp lệ riêng, không có R01 thỏa. |
| TA-EX-04 | R01 TRUE, tuổi 15, HATT hiện tại null | PHAN_VE / R01-PV | Nêu chưa xác nhận sốc vì thiếu số đo; PEND-003 |
| TA-EX-05 | Như trên, khóa HATT hiện tại thiếu | PHAN_VE / R01-PV | Missing tương đương null; PEND-004 |
| TA-EX-06 | Tuổi 25, HATT 110, nền null, R02 TRUE | PHAN_VE / R02-PV | Nêu chưa đánh giá được giảm >30%; PEND-005 |
| TA-EX-07 | Như trên, khóa HATT nền thiếu | PHAN_VE / R02-PV | Không suy/gán nền mặc định; PEND-006 |
| TA-EX-08 | Tuổi 25, HATT 89, nền thiếu, R01 TRUE | SOC_PHAN_VE / R-SOC | Nhánh tuyệt đối đủ bằng chứng; `BP-026` thiếu khóa nền; `BP-025` là biến thể nền null cùng mức/mã. |
| TA-EX-09 | Tuổi 25, HATT 140, nền 200, R01 TRUE | PHAN_VE / R01-PV | Giảm đúng 30%, không HATT tuyệt đối thấp; BP-022 |
| TA-EX-10 | Tuổi 15, HATT 110, S=FALSE, K=H=TRUE, C=FALSE, G=null | PHAN_VE / R01-PV; không exception/hạ mức | `TA15-BOOL6-NULL` là ca tương ứng. `INV-037/043` là ca nullable khác và phải tính theo fixture riêng. |
| TA-EX-11 | Như TA-EX-10, G thiếu khóa | PHAN_VE / R01-PV; không exception/hạ mức | `TA15-BOOL6-MISSING` là ca tương ứng; `MISS-007` là ca bổ sung cùng tình huống. Không đổi UNKNOWN thành bằng chứng âm. |
| TA-EX-12 | Tuổi 15, HATT 110, S=TRUE, I=TRUE, K=TRUE, H=C=FALSE, G thiếu/null | THEO_DOI / null | Mixed: G=False không rule, G=True R02; fallback D13-E đã duyệt; MISS-012 |
| TA-EX-13 | Tuổi 15, HATT 110, S thiếu/null, I=TRUE, K=H=TRUE, C=G=FALSE | PHAN_VE / R01-PV | CANONICAL: AllPV/Def rỗng; ly_do bắt buộc nêu mã đại diện R01/R02, không xác nhận S=False; MISS-009/TA15-BOOL1-* |

TA-EX-01–11 đối chiếu Issue #15; TA-EX-12 thể hiện fallback Mixed theo chính sách nhóm. Với TA-EX-13, trường hợp thiếu khóa tương ứng MISS-009 đã được thầy xác nhận mức và mã tại Issue #31; nhánh `null` tương ứng là chính sách nhóm cùng xử lý boolean không có sẵn. Không gán việc thầy duyệt toàn bộ D13-E. Đây là đối chiếu tài liệu, chưa chạy engine. Valid unavailable sau phân loại và audit hoàn tất dùng SUCCESS; không INVALID_INPUT chỉ vì missing/null. Không khóa nguyên văn template, nhưng nghĩa attribution/uncertainty là bắt buộc.

## 6. Yêu cầu phi chức năng

NFR (*Non-functional Requirement*) mô tả chất lượng và ràng buộc khi triển khai, ví dụ hiệu năng, riêng tư, khả năng kiểm thử và CI. Bằng chứng ghi trong bảng là thứ cần thu, không mặc định đã đạt.

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

Trạng thái dưới đây phản ánh bằng chứng của từng tiêu chí. `NOT IMPLEMENTED` là chưa có chức năng hoặc tài liệu cần thiết. `PARTIALLY AVAILABLE` là có khung nhưng thiếu bằng chứng nghiệp vụ. `TA CONFIRMED` ghi nhận yêu cầu đã được TA làm rõ. `VERIFIED` ghi nhận điều kiện nghiệm thu của tiêu chí đã được đối chiếu trực tiếp với bằng chứng được dẫn. A-11 được kiểm tra bằng README. Các tiêu chí về thực thi vẫn cần kết quả runtime, test nghiệp vụ, CI hoặc benchmark tương ứng.

| AC | Yêu cầu | Điều kiện nghiệm thu | Bằng chứng cần có | Nguồn | Trạng thái hiện tại |
|---|---|---|---|---|---|
| A-01 | Phân loại đúng contract | classify() thực thi bảng và làm rõ TA, hết NotImplementedError | Rule–code/test mapping gồm priority, age override và BP unavailable | E A-01; D; TA | NOT IMPLEMENTED |
| A-02 | Không hard-code fixture ID | Kết quả dựa trên dữ liệu đặc tả | Review code và fixture synthetic độc lập | E A-02; C | NOT IMPLEMENTED |
| A-03 | Đủ mức phân loại | SOC_PHAN_VE/PHAN_VE/THEO_DOI theo bảng và TA | Tầng 1/2, overlap, missing/null và TA-EX | E A-03; D; TA | NOT IMPLEMENTED |
| A-04 | Policy dữ liệu công bố và thực thi | Giữ missing/null theo TA và strict D04 cho invalid thực sự. D13-E đã duyệt: UNKNOWN, definite-first/coverage, Mixed fallback và canonical disclosure. | Policy/source review; test null/missing, invalid và cả sáu ca approved §8.2 | E A-04; TA; D04/D13-E; L | NOT IMPLEMENTED — policy đã duyệt, chưa có implementation evidence |
| A-05 | Explanation truy vết | ly_do DIRECT/CANONICAL đúng §4.2/§5; canonical không giả rule đã xác nhận độc lập, không raw input/điều trị. | Output/negative explanation assertions cho TA và D13-E | E A-05; D; TA; D06/D13-E | NOT IMPLEMENTED |
| A-06 | Audit an toàn đúng schema | Bốn trường; CLASSIFY, SUCCESS/INVALID_INPUT theo nghĩa thao tác; không INVALID_INPUT chỉ vì allowed unavailable | Schema/UTC/UUID/status, failure paths, dữ liệu cấm | E A-06; D07/D08; TA §5 | NOT IMPLEMENTED |
| A-07 | Test nghiệp vụ đủ nhóm | Normal/boundary/invalid/missing/null; thay/chỉnh test stub | Bộ test được review và map TA-EX/FR | E A-07; T | PARTIALLY AVAILABLE — mới có test minh họa NotImplementedError; chưa có bộ test nghiệp vụ đạt |
| A-08 | Chạy đạt từ clean checkout | pytest -q đạt với test nghiệp vụ đã thay/chỉnh stub | Lệnh, môi trường, kết quả thực chạy; [pytest.ini](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/pytest.ini) là bằng chứng cấu hình | E A-08; R | PARTIALLY AVAILABLE — có cấu hình và lệnh, chưa có bằng chứng test nghiệp vụ clean checkout đạt |
| A-09 | CI trên PR | GitHub Actions thực sự chạy bộ test cho PR | PR run URL và bước test thực tế | E A-09; W | PARTIALLY AVAILABLE — có workflow, chưa có bằng chứng CI chạy đạt với bộ test nghiệp vụ |
| A-10 | Benchmark đúng protocol | N≥1.000 sau 100 warm-up; nearest-rank p50/p95; p95 <100 ms, công bố máy và I/O full-path | Phương pháp và số liệu thật | E A-10; D10 | NOT IMPLEMENTED — protocol đã duyệt, chưa có số liệu |
| A-11 | Disclaimer README | Có chính xác educational/synthetic — not for clinical use | Đã đối chiếu nguyên văn tại [README.md dòng 43 ở commit `4482e4f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/README.md#L43). | E A-11; R | VERIFIED — disclaimer trong README |

Việc test stub có thể chạy đạt chỉ chứng minh stub; không chứng minh yêu cầu nghiệp vụ. Test Plan và QA Matrix hiện hành đã được tích hợp qua PR #3 và #4. Bộ pytest nghiệp vụ, kết quả chạy, bằng chứng audit/CI và cập nhật QA theo thực thi vẫn thuộc M2/M3. [P; L]

## 8. Ma trận truy vết yêu cầu

Bảng này nối mỗi FR/NFR với tiêu chí nghiệm thu, rule và cách kiểm chứng dự kiến, để biết phải kiểm tra yêu cầu nào ở đâu. Đây là liên kết truy vết, không phải kết quả chạy test.

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

Nguồn thiết kế hiện hành: [PR #3 — đã merge](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) có [175 ca chính](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv) theo [Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_PLAN.md) và bộ [81 ca logic nội bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTERNAL_STATE_CASES.csv) riêng. [PR #4 — đã merge](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) có [QA Matrix tại commit của PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d7f7e34860c3878cdbc07b4486f785cf4ae1ca99/docs/m1-qa/QA_MATRIX_M1_CODEX_FINAL_CANDIDATE.xlsx) để truy vết A-01–A-11. Workbook sau đổi tên: [QA Matrix hiện hành](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/912ad0847409002de195a91483dcf8fba4c073d9/docs/m1-qa/QA_MATRIX.xlsx); link tại commit PR #4 ở trên được giữ để truy vết lịch sử. Các mục thực thi trong workbook vẫn `NOT RUN`. PEND-001→PHAN_VE/R02-PV; PEND-002/007→THEO_DOI/null; PEND-003/004→PHAN_VE/R01-PV; PEND-005/006→PHAN_VE/R02-PV theo TA.

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

SUCCESS chỉ khi thao tác phân loại hợp lệ và writer hoàn tất. Các dòng trên không tạo status audit mới. Thiết kế và expected hiện hành tiếp tục yêu cầu helper của MISS-009 giữ R01/R02 UNKNOWN, không đổi thành TRUE chỉ để khớp `rule_id` canonical; khi triển khai M2 phải có negative explanation assertions tương ứng. Thầy yêu cầu cập nhật quy tắc Issue #31 trong `DECISIONS.md` và có ít nhất một test tự động cho ca thiếu khóa. `MISS-009` là ca thiết kế để triển khai; [Integration Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/912ad0847409002de195a91483dcf8fba4c073d9/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md) ghi `INT-018` kiểm mức/mã, helper và audit, còn `INT-021` kiểm nội dung `ly_do`. Đây là kế hoạch kiểm chứng, chưa phải kết quả chạy.

Ba cặp mức/mã từ baseline Hải được giữ nguyên và Leader phê duyệt. Sau đó thầy xác nhận `PHAN_VE / R01-PV` cho trường hợp thiếu khóa của MISS-009 tại Issue #31; không suy rộng xác nhận đó thành phê duyệt toàn bộ sáu ca hoặc toàn bộ D13-E.

## 9. Cơ sở yêu cầu và trạng thái phê duyệt

Đã đọc toàn bộ [bình luận fossbk-spec](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) tại Issue #15, tạo/cập nhật lúc 14:01:50 UTC ngày 08/11/2026. Làm rõ áp dụng chung cho Track A; D01–D03 trong phạm vi đã trả lời không còn chờ TA. Không biến phê duyệt TA về hành vi thành phê duyệt toàn bộ kiến trúc nhóm.

| ID | Hành vi hiện hành | Trạng thái và nguồn |
|---|---|---|
| D01 | Khi nhiều rule Tầng 2 TRUE, PHAN_VE và chọn R01>R02>R03; sốc xác nhận thì SOC_PHAN_VE/R-SOC | TA CONFIRMED — [TA §1](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D02 | Tuổi missing/null: THEO_DOI/null; giải thích thiếu tuổi | TA CONFIRMED — [TA §§2,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D03 | Tuổi có, Tầng 2 TRUE: current BP missing/null vẫn PHAN_VE; người lớn HATT ≥90 thiếu/null nền vẫn PHAN_VE; HATT <90 có thể xác nhận sốc không cần nền | TA CONFIRMED — [TA §§3–5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |

TA-05 bắt buộc missing/null boolean không tự gây exception và không hạ kết luận khi một rule đã được dữ liệu còn lại chứng minh trọn vẹn. Issue #31 xác nhận cách chọn mã đại diện cho trường hợp thiếu khóa được nêu, yêu cầu ghi quyết định trong ADR và có test tương ứng. [TA31] TA-06 cho phép policy nội bộ trong khoảng chưa quy định, phải công bố/test/giải trình và không đổi rule/ngưỡng/schema.

**D13-E hiện hành: APPROVED BY LEAD — D13-E — 09/11/2026.** Normalization, coverage, definite-first, Mixed fallback và canonical semantics §3.2/§4.2/§5/§8.2 đã được phê duyệt nội bộ; không còn chờ Leader cho D13. Leader đã chấp nhận rủi ro về cách hiểu mã đại diện khi duyệt D13-E. Làm rõ Issue #31 xác nhận quy tắc mã đại diện trong phạm vi nêu; definite-first và các chi tiết biểu diễn/triển khai vẫn ghi đúng là chính sách nhóm. Với tình huống vừa có rule chắc chắn vừa có rule ưu tiên cao hơn chỉ có thể thỏa, cần đối chiếu cách áp dụng chính sách nhóm với phạm vi phán quyết và ca kiểm thử khi tích hợp. Không coi phản hồi hoặc phê duyệt là bằng chứng triển khai.

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
| Nhầm review tài liệu với nghiệm thu | Ghi nhận `VERIFIED` cho A-11 theo README tại §7. A-01 đến A-10 tiếp tục cần bằng chứng theo từng tiêu chí. Nghiệm thu phạm vi của TA cần xác nhận riêng. |
| Nguồn snapshot lịch sử còn policy cũ | Giữ snapshot là lịch sử; source TA và Revision 04/D13-E ưu tiên hơn. Bản M1-02/QA hiện hành đã được đồng bộ và merge trong PR #3/#4; không dùng snapshot cũ làm policy hiện hành |
| AI-use hoặc phối hợp thiếu bằng chứng | Ghi công cụ/phạm vi/kiểm chứng/quyết định và người chịu trách nhiệm thực tế; Huy review nguồn, Hải M1-02, Việt Đức M1-03 |

| Ký hiệu | Nguồn và phiên bản |
|---|---|
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung hiển thị v1.0.2 dù tên URL ghi v1.0.0, đối chiếu ngày 08/11/2026 qua HTML xuất bản của fossbk-spec/ktpmud-book. Áp dụng §§4–7, 9, 11–12. |
| D | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag starter chính thức `bkt-2026-v1`. |
| TA | [Trả lời chính thức Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), §§1–6, áp dụng chung Track A. |
| TA31 | [Làm rõ chính thức Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002): chọn mã đại diện khi thiếu khóa boolean trong phạm vi nêu; yêu cầu ghi ADR và test. |
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

Nguồn D, TA và TA31 là các nguồn quy định/làm rõ theo phạm vi tương ứng; G/P là snapshot phân công và lịch sử. D13-E là policy nhóm đã duyệt, trong đó lựa chọn mã đại diện cho tình huống được nêu đã có làm rõ tại Issue #31; không gán toàn bộ chi tiết D13-E cho TA. Đường dẫn audit mặc định và lỗi nội bộ giữ trạng thái review riêng. Việc duyệt D13 không tự thay miền validation hoặc các quyết định OPEN.

### 10.1. Lịch sử thay đổi

| Phiên bản | Nội dung | Tình trạng bằng chứng |
|---|---|---|
| Revision 02, 08/11/2026 — lịch sử tại 662c47be9eba076bf9ca551403cc3e961f421d42 | D01–D03 khi đó PENDING TA CONFIRMATION; tuổi/boolean null bị coi invalid theo policy cũ | Snapshot trước trả lời TA, không phải policy hiện hành |
| Revision 03, 08/11/2026 — TASK 02C.6 | Đồng bộ TA-01–06, thay thế một phần D04/D13, cập nhật FR/AC/truy vết và 12 ví dụ; extension null → UNKNOWN chờ Leader | **Trạng thái lịch sử tại 08/11:** Draft/chờ review; chưa có implementation/test/benchmark evidence |
| Revision 04, 09/11/2026 — TASK 02G | APPROVED BY LEAD — D13-E — 09/11/2026; chuẩn hóa missing/null, Def/Poss/AllPV, definite-first, canonical attribution và Mixed fallback; chốt sáu expected, đồng bộ nguồn/bàn giao TASK 02E | **Trạng thái lịch sử tại 09/11:** Draft/chờ peer review; chưa có implementation verification; default path/internal exception còn review | 
| Đồng bộ trạng thái sau merge, 10–11/11/2026 *(không đổi Revision 04 hoặc chính sách kỹ thuật)* | Xác nhận PR #1–#4 đã merge vào `track-a-development`; chỉnh tham chiếu SHA, trạng thái peer review và bàn giao M2 | Có Leader self-review và review APPROVED từ `nvldvc`; chưa có lượt review thành viên còn lại; chưa có TA scope acceptance hoặc bằng chứng runtime/test/CI/benchmark đạt |
| Cập nhật đề xuất sau Issue #31, đối chiếu 12/11/2026 | Diễn đạt lại để dễ đọc; bổ sung nguồn và phạm vi làm rõ về mã đại diện; chỉnh liên kết fixture và trạng thái audit | Giữ expected thiết kế đã duyệt; ADR và test tự động cho ca thiếu khóa còn cần được cập nhật/triển khai. |

