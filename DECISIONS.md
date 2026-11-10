# Hồ sơ quyết định kiến trúc — Track A (ADR)

> **Mục đích:** Ghi lại *vì sao* nhóm lựa chọn kiến trúc và cách kiểm chứng. Chi tiết trường dữ liệu, FR/NFR/AC ở [`REQUIREMENTS.md`](REQUIREMENTS.md); toàn bộ test cases ở `docs/m1-hai/`, QA Matrix ở `docs/m1-qa/`. Đây là **thiết kế**, không phải báo cáo engine đã chạy.

## 1. Thông tin và trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Nhóm / sản phẩm | `173820_n27` · Dr May Day Rule Engine — Track A |
| Phiên bản | M1 Revision 04; bản biên tập rút gọn sau tích hợp, 11/11/2026 |
| Chủ trì | Lead (Huy Đức); Dev (Hải); QA (Việt Đức) |
| Starter | `fossbk-spec/ktpmud-bkt-ruleengine-starter`, tag `bkt-2026-v1`, SHA `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Trạng thái tài liệu | PR #1–#4 đã merge vào `track-a-development` ngày 10/11/2026; HEAD tích hợp M1 `9bc4fc186415d7a13cd9d49692c50f3c945ddf7b` |
| Phê duyệt và giới hạn | Leader phê duyệt D13-E ngày 09/11; có approval PR từ `nvldvc` và comment của Leader; chưa có bằng chứng peer technical review của Hải/Việt Đức ở vòng cuối. Chưa có code, pytest nghiệp vụ, CI nghiệm thu hay benchmark. |

**Thứ tự thẩm quyền:** Decision Table V1 và [trả lời TA tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) > policy nội bộ đã duyệt > phương án còn đề xuất. D01–D03 được TA làm rõ; TA không phê duyệt riêng thuật toán D13-E hay kiến trúc audit. Các mốc merge PR không đồng nghĩa TA nghiệm thu hoặc đạt AC.

**Nhãn trạng thái:** `TA CONFIRMED` = hành vi đã được TA xác nhận; `APPROVED BY LEAD` = quyết định nhóm; `PENDING PEER TECHNICAL REVIEW` = chưa có xác nhận kỹ thuật cuối của thành viên; `PROPOSED` = chưa phê duyệt. `OPEN-01`–`OPEN-10` là mã lịch sử, **đã chọn phương án** nhưng chưa nghiệm thu bằng code.

## 2. Bối cảnh, phạm vi và các ràng buộc

Starter chỉ cung cấp `classify(patient)` còn `NotImplementedError`. Nhóm xây Rule Engine Python từ [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md) bằng dữ liệu synthetic; không kết nối production hoặc đưa lời khuyên điều trị. Mục tiêu là phân loại đúng, giải thích có thể truy vết và audit không lộ input lâm sàng. Thiết kế ưu tiên **validation → logic thuần → lựa chọn output → audit**; chi tiết chức năng xem Requirements FR-01–FR-09.

**Bất biến phải giữ:** `classify(patient)`; 9 trường input; 3 output `muc_do`, `rule_id`, `ly_do`; điều kiện R01/R02/R03 và R-SOC cùng ngưỡng/ưu tiên từ Decision Table; audit đúng 4 trường `Timestamp`, `User_UUID`, `Action_Type`, `Status`; không thêm rule/ngưỡng lâm sàng hoặc dữ liệu thật. Các nghĩa vụ test, CI và benchmark theo A-01–A-11 vẫn bắt buộc.

## 3. Danh mục quyết định D01–D13

| ID | Quyết định chính | Trạng thái / nguồn |
|---|---|---|
| D01 | Khi nhiều rule Tầng 2 cùng TRUE: ưu tiên R01 > R02 > R03; R-SOC ưu tiên nếu có sốc xác nhận | **TA CONFIRMED** |
| D02 | Tuổi missing/null → `THEO_DOI/null`, nêu thiếu tuổi | **TA CONFIRMED** |
| D03 | Tuổi có và Tầng 2 TRUE: HATT hiện tại/nền unavailable không tự chặn `PHAN_VE`; HATT <90 ở người lớn đủ nhánh tuyệt đối | **TA CONFIRMED** |
| D04 | Phân biệt unavailable với invalid; non-null sai kiểu → TypeError, sai miền/khóa lạ → ValueError; strict validation mọi trường | APPROVED BY LEAD; policy cũ về tuổi/boolean null bị TA thay thế |
| D05 | Public `classify()` điều phối, helper rule thuần và writer audit riêng | APPROVED BY LEAD |
| D06 | `ly_do` tất định, giải thích DIRECT/CANONICAL, không raw input hoặc lời khuyên điều trị | APPROVED BY LEAD; tôn trọng TA |
| D07 | JSONL audit riêng, ContextVar/UUID ngoài patient input, file theo lần chạy | APPROVED BY LEAD |
| D08 | Audit `CLASSIFY` với `SUCCESS/INVALID_INPUT`; fail-closed, lỗi kép ưu tiên audit | APPROVED BY LEAD |
| D09 | Test nghiệp vụ normal/boundary/missing/invalid, ngữ nghĩa D13-E; test isolation | APPROVED BY LEAD |
| D10 | Benchmark `perf_counter_ns`, 100 warm-up, ≥1.000 mẫu, nearest-rank p50/p95, full-path I/O thật | APPROVED BY LEAD |
| D11 | Không đổi clinical rules/ngưỡng từ Decision Table | FACT / SPECIFIED |
| D12 | Giữ input/output/audit schema và giới hạn privacy | FACT / SPECIFIED |
| D13 | Boolean missing/null→UNKNOWN, Enum/Kleene/T-U, Def trước Poss, AllPV, Mixed fallback và CANONICAL disclosure | **APPROVED BY LEAD — D13-E, 09/11/2026**; có residual risk |

**Quan trọng:** D04/D13-E là policy nội bộ ở những chỗ được TA cho phép nhóm chọn, không phải quy tắc TA tự bổ sung. Chi tiết lập luận ở §5, phân công và phương án triển khai ở §8.

## 4. Kiến trúc dự kiến và hành vi công khai

```text
Caller -> classify(patient)
  -> validate toàn bộ trường (invalid khác missing/null hợp lệ)
  -> tuổi thiếu/null? THEO_DOI/null, giải thích thiếu tuổi
  -> tuổi có? evaluate original R01/R02/R03 trên dữ liệu Boolean
       -> Def có: chọn definite rule ưu tiên R01 > R02 > R03 (DIRECT)
       -> Def rỗng, AllPV: positive qua coverage, PHAN_VE dùng CANONICAL
       -> Mixed / không khớp: THEO_DOI/null, phân biệt lý do
       -> positive + hypotension TRUE: SOC_PHAN_VE/R-SOC
       -> positive nhưng chưa chứng minh sốc: PHAN_VE
  -> ghi audit SUCCESS thành công rồi trả đúng 3 trường
  -> invalid: ghi INVALID_INPUT thành công rồi raise TypeError/ValueError
  -> audit lỗi (kể cả lỗi kép): lỗi audit an toàn, không trả thành công
```

**UUID và audit:** Explicit session ngoài input dùng cùng UUID trong scope; direct call không có session dùng UUID synthetic mới cho riêng call và reset bằng token/finally. JSONL chỉ chứa bốn trường bắt buộc; writer open/append/write/close theo lần gọi và fail-closed. `ContextVar` không bảo đảm ghi file đồng thời. Đường dẫn mặc định khi direct call **chưa được phê duyệt** (§5.4.1); unexpected internal exception vẫn là mục cần review.

**Mốc kiểm chứng thực tế:** `rule_engine/classifier.py` hiện vẫn là stub; test starter chưa chứng minh nghiệp vụ, CI chưa có run nghiệp vụ được kiểm chứng và benchmark chưa chạy. Phê duyệt tài liệu không được dùng làm bằng chứng PASS các AC.

## 5. Các quyết định kiến trúc (Architecture Decision Records)

Các phương án thay thế và lập luận dưới đây là hồ sơ thiết kế đã tích hợp vào M1. Hướng lựa chọn đã được Leader duyệt qua nguồn ghi ở mỗi ADR; phần kiểm chứng kỹ thuật của Hải/Việt Đức và chi tiết triển khai còn cần review thực chất. Tích hợp tài liệu không đồng nghĩa AC được nghiệm thu.

### 5.1. D04 — Validation input nghiêm ngặt

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Sai kiểu và unavailable khác nhau. Ép kiểu có thể biến dữ liệu chưa xác nhận thành bằng chứng. TA cho phép null/thiếu ở tuổi, HATT và boolean; không được giữ validation cũ loại null tuổi/boolean. TypedDict chưa validation runtime. |
| Quyết định | Giữ tuổi int/float hữu hạn ≥0, cho số lẻ, loại bool; current BP int ≥0; baseline int >0; HATT loại bool/float/chuỗi. Missing/null ba số unavailable. Boolean True/False hợp lệ, missing/null→UNKNOWN theo D13-E đã Leader duyệt; non-null sai kiểu TypeError, sai miền/khóa thừa ValueError. Kiểm mọi field, không ép kiểu/đổi invalid thành UNKNOWN hoặc THEO_DOI; invalid vẫn audit D08. |
| Phương án khác | Tự chuyển chuỗi/số thành kiểu mong muốn để nhận được nhiều dạng dữ liệu hơn. Phương án này giảm lỗi tích hợp ban đầu nhưng cần quy ước diễn giải và có thể che lỗi bên gọi. |
| Lý do lựa chọn | Đầu vào nhỏ, cố định và giả lập cho phép yêu cầu bên gọi cung cấp đúng kiểu. Validation nghiêm giúp tìm lỗi sớm và giữ bằng chứng phân loại theo dữ liệu thực nhận. Các miền số là policy dữ liệu của nhóm, tách khỏi ngưỡng lâm sàng trong D. |
| Hệ quả / đánh đổi | Giữ kiểm tra số hữu hạn, loại bool khỏi miền số và phân biệt unavailable với invalid thực sự. Tuổi missing/null có output TA quy định; thiếu current BP/nền không tự hạ Tầng 2 đã xác nhận. Không tự đổi current BP=0 thành invalid; baseline=0 vẫn ValueError theo policy số đã duyệt. |
| Rủi ro / giảm thiểu | Validator cũ có thể nhận bool như số hoặc còn loại age/boolean null. Kiểm tra toàn bộ input, không bỏ qua field invalid không liên quan dù đã chứng minh rule; giữ message/chaining không chứa giá trị lâm sàng thô. Không gán INVALID_INPUT chỉ vì missing/null được phép. |
| Kiểm chứng dự kiến | Test missing/null/non-null invalid, miền số/tuổi lẻ/khóa lạ/unrelated invalid và privacy. Nguồn Hải hiện có 36 invalid=28 TypeError+8 ValueError khi audit thành công; INV nullable và AUD-002 fixture đã thay được bàn giao ở §9.3. Lỗi kép vẫn OPEN-03. Chưa implementation/test evidence. |
| Truy vết | Q FR-07; NFR-02, NFR-03, NFR-05; A-04, A-07. |
| Nguồn / trạng thái | APPROVED BY LEAD — PARTIALLY SUPERSEDED BY TA. TA §§2–5 thay chính sách null tuổi/boolean cũ; mapping lỗi, miền số và OPEN-03 giữ phần đã duyệt. [TA](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248); Q §§3, 4.3, 8.1; L. Không coi toàn bộ D04 bị hủy. |

### 5.2. D05 — Thiết kế Python tối giản, dễ bảo trì

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | `classify(patient)` phải phối hợp validation, đánh giá rule, ưu tiên và output, còn audit thêm I/O. Gom mọi trách nhiệm làm khó review AND/OR và khó khoanh vùng lỗi. |
| Quyết định | Giữ classify(patient) điều phối validation, rule evaluation, lựa chọn kết quả/explanation và audit, kể cả direct call. Ít helper theo trách nhiệm: validation, R01/R02/R03, điều kiện sốc, ưu tiên kết quả, explanation; writer I/O riêng. Không bắt mỗi trách nhiệm thành một function/file, không framework/plugin system. Context/provider theo OPEN-01–OPEN-02, helper theo OPEN-07. |
| Phương án khác | Một hàm lớn giảm số điểm gọi nhưng trộn nhánh nghiệp vụ với I/O. Một hệ thống lớp/plugin tổng quát hỗ trợ mở rộng nhưng thêm abstraction và chi phí bảo trì chưa có nhu cầu trong bài. |
| Lý do lựa chọn | Ranh giới theo validation, rule, quyết định kết quả, giải thích và audit cho phép review trực tiếp từng phần theo Q. Số quy tắc nhỏ nên chưa có căn cứ xây framework rule tổng quát. |
| Hệ quả / đánh đổi | Các phần thuần dễ unit test, lỗi dễ định vị. Chi phí là định nghĩa ranh giới và bảo đảm các hàm phối hợp đúng, không tạo nhiều bước chỉ để chuyển dữ liệu qua lại. |
| Rủi ro / giảm thiểu | Helper quá vụn hoặc trạng thái ẩn làm khó review. Hải chọn số lượng/tên helper tối thiểu; Việt Đức review testability và đường giao thoa core/audit. Kiểm chứng public orchestration cùng provider, không chỉ helper. |
| Kiểm chứng dự kiến | Review signature không đổi; gọi trực tiếp vẫn audit; explicit session dùng cùng UUID, call độc lập dùng UUID mới và reset sau exception; rule test thuần và public integration test. Chưa có code hoặc kết quả chạy. |
| Truy vết | Q FR-01–FR-09; NFR-04, NFR-05; A-01, A-02, A-07–A-09. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D05, Q §4.3 và L; OPEN-01/02/07 ngày 08/11/2026 là APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW. Tên helper/module là chi tiết triển khai nhỏ, không phải hướng kiến trúc chưa chọn. |

### 5.3. D06 — Giải thích tất định, liên kết rule

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Output phải cho biết rule nào dẫn đến kết quả và giải thích ngắn. Nội dung tự do có thể đưa dữ liệu thô hoặc lời khuyên điều trị vào `ly_do`. |
| Quyết định | Giữ template tất định, không LLM/raw clinical input/điều trị. DIRECT nêu rule definite; CANONICAL chỉ ở PHAN_VE/Def rỗng/AllPV, MUST nêu mã đại diện và chưa xác nhận rule độc lập, không claim unknown=False đã quan sát. Mixed nêu insufficient information; thiếu tuổi/current BP/nền diễn đạt theo TA. Không thêm output key. |
| Phương án khác | Ghép câu từ toàn bộ triệu chứng và số đo tạo nhiều chi tiết nhưng tăng nguy cơ rò dữ liệu. Sinh câu linh hoạt làm tăng độ biến thiên và khó kiểm chứng nội dung đúng giới hạn. |
| Lý do lựa chọn | Bộ mã rule nhỏ, output cố định và dữ liệu synthetic đủ để dùng template. Reviewer đối chiếu được mã rule với câu giải thích mà không cần tái tạo dữ liệu input trong output. |
| Hệ quả / đánh đổi | Template ổn định và dễ đối chiếu một rule_id. D01 đã có priority chính thức R01 > R02 > R03; trường hợp overlap có thể nêu thêm rule khớp trong ly_do nhưng không thêm mã output. Cần phân biệt thiếu tuổi, thiếu current BP và thiếu baseline. |
| Rủi ro / giảm thiểu | Không diễn đạt THEO_DOI thành an toàn, hoặc chưa xác nhận sốc thành bằng chứng không có sốc. Nêu lý do unavailable theo TA, không suy số đo hay lộ input qua explanation/lỗi. D01–D03 không còn phụ thuộc phản hồi TA cho ca đã trả lời. |
| Kiểm chứng dự kiến | Ba output keys, priority/attribution theo D13-E, TA-EX-01–13 và sáu expected §9.4; negative reason assertions bắt câu khẳng định S=False hoặc R01 definite ở canonical. Missing age/BP/nền đúng TA. Chưa có output runtime được nghiệm thu. |
| Truy vết | Q FR-08; NFR-07; A-05, liên quan A-01. |
| Nguồn / trạng thái | Template APPROVED BY LEAD theo L; nội dung kỳ vọng D01–D03 theo TA §§1–5 và Q FR-08. D dòng 49–55/E A-05 giữ contract; TA không phê duyệt công nghệ template. |

### 5.4. D07 — Audit writer JSONL riêng, bảo vệ dữ liệu

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Cần audit bốn trường cho thao tác nhưng pure rule evaluation không cần UUID hay file I/O. Thêm UUID vào `PatientInput` sẽ vượt danh sách khóa đã khóa. |
| Quyết định | Writer JSONL riêng với đúng Timestamp, User_UUID, Action_Type, Status; Timestamp ISO 8601 có timezone UTC, UUID synthetic hợp lệ, CLASSIFY, SUCCESS/INVALID_INPUT. Public classify() tự điều phối audit. ContextVar ngoài PatientInput cung cấp UUID phiên tường minh hoặc UUID tạm một call. Path được cấu hình ngoài input, vùng dữ liệu sinh của lần chạy; V1 ghi tuần tự, file được sở hữu rõ. Mỗi bản ghi open append/write/close trước khi báo hoàn tất. Chi tiết vòng đời tại OPEN-01/02/04/05/09. |
| Phương án khác | Ghi file trực tiếp trong từng nhánh rule dễ bắt đầu nhưng lặp code và khiến test logic phụ thuộc I/O. CSV cũng lưu được bốn trường nhưng cần thống nhất escaping và kiểm tra kiểu/schema, trong khi JSONL cho từng bản ghi dạng object rõ hơn. |
| Lý do lựa chọn | Writer riêng tập trung kiểm soát dữ liệu được phép, hỗ trợ kiểm tra riêng format và I/O. JSONL đủ cho phạm vi bài thi, tránh kéo thêm cơ sở dữ liệu hoặc hạ tầng. Ranh giới writer tạo điểm thay cách lưu về sau, không phải mục tiêu tích hợp production hiện tại. |
| Hệ quả / đánh đổi | Rule test được thuần, writer tập trung schema/privacy và path độc lập working directory. Có overhead mở/đóng từng record và quản lý context; chấp nhận để giảm state M2, đo thực tế trước khi đề xuất tối ưu. Không bảo đảm fsync/durability sau mất điện. |
| Rủi ro / giảm thiểu | I/O lỗi có thể để lại bản ghi chưa hoàn chỉnh; fail-closed không chứng minh audit đã lưu. Không truyền payload cho writer; không commit runtime log. Test dùng file riêng; không cam kết thread/process-safe ghi chung file. ContextVar không tạo atomicity cho JSONL. Mở rộng concurrency phải review riêng. |
| Kiểm chứng dự kiến | Đọc lại JSONL, đúng bốn trường/UTC/UUID, explicit và single-call scope, reset sau exception; thử open/write/flush/close failure, path độc lập cwd và isolation bằng tmp_path. Benchmark chính giữ I/O thực. Chưa có audit runtime hoặc kết quả thử. |
| Truy vết | Q FR-09; NFR-02, NFR-03, NFR-04; A-06. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D07, Q FR-09/NFR-03 và L. E §§7.2–7.3 A-06 quy định bốn trường. OPEN-01/02/04/05/09 được Leader chọn ngày 08/11/2026, PENDING PEER TECHNICAL REVIEW; đường dẫn file thực tế chưa đặt. |

#### 5.4.1. Direct call chưa cấu hình audit path — đề xuất tích hợp M2

**PROPOSED — AWAITING PEER REVIEW.** Cần kiểm chứng `classify(patient)` khi bên gọi chưa thiết lập audit path. OPEN-04 đã duyệt cấu hình ngoài input và độc lập working directory; cơ chế chọn path mặc định dưới đây là đề xuất bổ sung, chưa được Leader phê duyệt.

Đề xuất dùng một gốc tuyệt đối từ thư mục người dùng do hệ điều hành xác định, ví dụ `<user-home>/.173820_n27/dr_may_day/runs/<run-id>/audit.jsonl`. Gốc ổn định không suy ra từ current working directory; thư mục con theo lần chạy giữ ownership/file riêng theo OPEN-05. `run-id` chỉ tổ chức file, không thêm input hoặc trường audit. Hải/Việt Đức cần review cách xác định gốc, vòng đời run-id, quyền truy cập và kiểm tra đích nằm ngoài repository trước khi chọn đường dẫn thực tế.

Cho phép override path qua cấu hình provider/writer bên ngoài PatientInput cho test/demo; không đổi `classify(patient)` hoặc chín input keys. Mặc định và override đều phải tránh lưu runtime audit vào repository. Nếu không xác định/tạo/ghi được đích hợp lệ thì giữ fail-closed, không bỏ audit hoặc fallback về working directory/repository để báo thành công.

Kiểm chứng M2: direct call không cấu hình path; đổi working directory vẫn xác định đúng gốc; override test/demo ở thư mục riêng ngoài repository; lỗi tạo thư mục/mở/ghi/đóng vẫn không báo thành công. README khi triển khai phải mô tả nơi lưu mặc định, cách cấu hình/override và hành vi khi không tạo/ghi được file. Hải chủ trì public integration; Việt Đức review path/privacy/isolation và phối hợp kiểm chứng; Huy xem kết quả review trước khi phê duyệt cơ chế đề xuất này.

### 5.5. D08 — Audit lần thành công và lần thử input lỗi

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Chỉ ghi lần thành công bỏ sót dấu vết các yêu cầu invalid. Ghi đầy đủ exception/payload có thể tiết lộ triệu chứng hoặc số đo. |
| Quyết định | Ghi CLASSIFY/SUCCESS khi xử lý thành công và CLASSIFY/INVALID_INPUT khi validation lỗi thực sự; missing/null được TA cho phép không tự là INVALID_INPUT, giữ đúng bốn trường, không payload/exception details. Fail-closed có kiểm soát: invalid + audit thành công thì raise TypeError/ValueError; valid + audit thất bại thì raise lỗi audit an toàn; lỗi kép cũng ưu tiên lỗi audit, không giả định đã có INVALID_INPUT. Không để message/chaining lộ input. Xem OPEN-03. |
| Phương án khác | Chỉ audit thành công giảm số bản ghi nhưng thiếu truy vết lỗi input. Ghi lỗi chi tiết thuận debug nhưng vượt giới hạn dữ liệu và schema. |
| Lý do lựa chọn | Trạng thái tổng quát đủ cho mục đích nhận biết một lần thử đã thành công/thất bại mà không tái tạo dữ liệu input. Phạm vi mở rộng sang invalid là quyết định nội bộ, tách khỏi yêu cầu chính thức audit mỗi lần phân loại. |
| Hệ quả / đánh đổi | Tăng khả năng truy vết và giảm rò dữ liệu, nhưng giảm chi tiết debug. Hai Status đã duyệt mô tả xử lý thao tác, không ánh xạ trực tiếp mức phản vệ. Fail-closed có thể ngăn trả kết quả dù logic đã tính xong. Schema không có trường thứ năm hoặc status mới cho lỗi writer. |
| Rủi ro / giảm thiểu | Exception chaining hoặc logging mặc định có thể lộ input; nhiều lớp ghi có thể gây trùng. Public boundary chịu trách nhiệm điều phối và làm sạch lỗi, writer chỉ nhận allowlist. Không retry vô hạn, không tự coi lỗi ghi là có bản ghi, không thêm telemetry hoặc trường thứ năm. |
| Kiểm chứng dự kiến | Kiểm tra bốn đường ở phần 4, đặc biệt ba ca OPEN-03; loại lỗi validation khi audit thành công, lỗi audit công khai khi audit thất bại; không lộ input trong message/chaining, không trả kết quả thành công và không giả định record tồn tại sau lỗi ghi. Chưa có bằng chứng chạy. |
| Truy vết | Q FR-07, FR-09; NFR-02, NFR-03; A-04, A-06. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D08, Q §§4, 6 và L; OPEN-03 ngày 08/11/2026 là APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW. Tên exception audit cụ thể có thể hoàn thiện khi implement. |

### 5.6. D09 — Kiểm thử theo hành vi và ranh giới

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Một số biểu thức gần giống nhau nhưng khác ngoặc, đường hít, số hệ hoặc dấu so sánh. Test mẫu chỉ mong đợi `NotImplementedError`, chưa kiểm tra nghiệp vụ. |
| Quyết định | Giữ normal/boundary/missing/null/invalid/overlap/tuổi lẻ/output/audit/privacy. Stub NotImplementedError thay/chỉnh bằng business tests M2. tmp_path/fixtures/reset/file riêng/độc lập thứ tự giữ nguyên. Expected D01–D03 theo TA; sáu D13-E §9.4 đã được Leader chốt policy, không còn awaiting approval. Thêm coverage/select/explanation tests, TA-EX-01–13. |
| Phương án khác | Chỉ dùng ca điển hình và một ví dụ cho mỗi nhãn nhanh hơn nhưng dễ bỏ qua sai dấu và dữ liệu thiếu. Chỉ đo tỷ lệ dòng code được chạy cũng chưa chứng minh các điều kiện rule được hiểu đúng. |
| Lý do lựa chọn | Nhóm ca bám yêu cầu A-07 và các đường rủi ro thực tế. Giá trị bằng ngưỡng thất bại nhánh so sánh nghiêm ngặt, nên các ca tại/sát biên cần được review, kể cả biên tuổi và giảm đúng 30%. |
| Hệ quả / đánh đổi | Dễ phát hiện lỗi nhỏ làm đổi kết quả, nhưng cần thời gian lập kỳ vọng và bảo trì dữ liệu synthetic. Kiểm tra helper hỗ trợ chẩn đoán lỗi, vẫn cần kiểm tra từ interface công khai. |
| Rủi ro / giảm thiểu | Không copy implementation thành oracle, giữ null expected cũ hoặc coi approval là PASS runtime. Bộ thiết kế ban đầu 157 ca đã được mở rộng lên 175 ca chính trong M1-02; 81 ca logic nội bộ vẫn là tập riêng. Hải/Việt Đức cần review kỹ thuật và mapping QA/AC/status, canonical reason và nguồn hiện hành. Leader đã phê duyệt policy; chưa có runtime verification. |
| Kiểm chứng dự kiến | Giữ public/core/audit/context/error/fixture coverage, 81 Enum/count rows. Thêm raw normalization, Def trước Poss, AllPV/Def rỗng, Mixed, numeric crossovers và đủ six approved expected. Sau code cần pytest -q từ clean checkout với business tests và PR CI evidence riêng; không nghiệm thu từ số hàng tài liệu. |
| Truy vết | Q FR-01–FR-09; NFR-05, NFR-06; A-01–A-09. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D09, Q NFR-05, L; OPEN-06 ngày 08/11/2026 đã được chọn, PENDING PEER TECHNICAL REVIEW. E A-07–A-09, T dòng 9–17, W dòng 1–12 là căn cứ hiện trạng. Hải và Việt Đức review chéo fixture/đường lỗi. |

### 5.7. D10 — Benchmark toàn luồng và phép đo phụ logic thuần

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Phép đo chỉ một biểu thức rule có thể bỏ qua validation, explanation và audit. Số liệu như vậy không đại diện đường gọi nhóm định nghiệm thu. |
| Quyết định | Dùng time.perf_counter_ns(), warm-up đúng 100 lượt và loại khỏi N ≥1.000 mẫu đo thực. Sắp xếp mẫu tăng dần; nearest-rank lấy vị trí ceil(p×N) theo chỉ số từ 1, p50: p=0,50, p95: p=0,95; nanosecond / 1.000.000 = millisecond. Đo toàn public classify() gồm open/write/close audit thực, không mock writer. Logic thuần là phép đo phụ riêng. Báo môi trường và giữ p95 <100 ms theo đề. Xem OPEN-09–OPEN-10. |
| Phương án khác | Chỉ đo logic thuần giúp phân tích CPU nhưng bỏ qua I/O và điều phối. Chỉ báo thời gian trung bình che đuôi chậm và không đủ p50/p95 theo đề. |
| Lý do lựa chọn | Hai phép đo tách nhãn cho phép biết chi phí ở rule hay phần hỗ trợ, đồng thời giữ số liệu nghiệm thu gắn đường chạy thực tế. Warm-up và môi trường được khai báo giúp người khác tái lập phép đo. |
| Hệ quả / đánh đổi | Full-path phản ánh overhead và biến thiên I/O/máy. Nearest-rank dễ tái tính nhưng có bước nhảy theo mẫu; 100 warm-up cố định giúp protocol rõ. Công bố Python version, OS, CPU/hardware, số lượt warm-up/mẫu, dữ liệu synthetic và cấu hình I/O. Không tạo ngưỡng nghiệm thu mới. |
| Rủi ro / giảm thiểu | Bỏ chi phí open/close, dùng writer giả, chọn lọc mẫu hoặc sai chỉ số/đơn vị làm sai kết quả. Giữ toàn bộ public path, loại 100 warm-up, kiểm tra công thức độc lập. Protocol đã chốt; nếu tối ưu cần dữ liệu và review riêng, không tự thay semantics ghi. |
| Kiểm chứng dự kiến | Review instrumentation, timing boundary và nearest-rank trên tập mẫu kiểm tra có kết quả tính tay; chạy benchmark full-path thực với N ≥1.000, môi trường công bố, báo p50/p95. Protocol đã duyệt nhưng chưa thực đo; không có số liệu hoặc A-10 PASSED. |
| Truy vết | Q NFR-01; A-10. Phụ thuộc D05, D07, D08 và đường gọi FR-01/FR-09. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D10, Q NFR-01 và L; OPEN-09/10 được chốt ngày 08/11/2026, PENDING PEER TECHNICAL REVIEW. E A-10 là nguồn tối thiểu mẫu, p50/p95 và p95 <100 ms; 100 warm-up/nearest-rank là protocol nội bộ đã duyệt. |

### 5.8. D13-E — Evidence-first Boolean Coverage with Canonical Attribution

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Missing/null boolean được TA cho phép; S xuất hiện âm ở R01 và dương ở R02/R03. Rule riêng UNKNOWN chưa chứng minh disjunction không khớp. Có AllPV nhưng không rule riêng definite nên phải định nghĩa cả selection level lẫn attribution. |
| Quyết định | APPROVED BY LEAD — D13-E — 09/11/2026. Boolean missing/null→UNKNOWN; giữ Enum/Kleene/T-U và strict D04 cho non-null invalid. Duyệt 1–64 consistent completions bằng original R01/R02/R03; Def trước Poss. Def có: chọn rule definite ưu tiên. Def rỗng/AllPV: giữ positive; PHAN_VE dùng canonical ưu tiên trong Poss, MUST disclose chưa xác nhận rule độc lập. Mixed/all-negative→THEO_DOI/null với reason khác nhau; positive+hypotension→SOC_PHAN_VE/R-SOC; age/BP theo TA. |
| Phương án khác | Đã cân nhắc: A chỉ Kleene fallback làm mất positive bất biến; B chọn false representative tương đương output hiện tại nhưng dễ bị hiểu imputation; C possible-first có thể bỏ definite; D PV/null hợp kiểu nhưng semantics không được current mapping chọn. Không mở lại Enum/toán tử hoặc các architecture khác. |
| Lý do lựa chọn | E giữ definite evidence, bảo toàn disjunction bất biến mà không tạo clinical criterion mới; lựa chọn canonical tất định, công bố attribution uncertainty. Quyền công bố policy theo TA §§5–6; convention không do TA chỉ định cho từng missing case. |
| Hệ quả / đánh đổi | Thêm coverage/selector/explanation tests; chỉ dùng mã canonical ở PHAN_VE khi Def rỗng/AllPV, DIRECT/CANONICAL là provenance private. Không schema/field/status mới, không fill raw input hoặc numeric. Thiếu tuổi vẫn TD/null; thiếu BP không chặn positive đã chứng minh. |
| Rủi ro / giảm thiểu | Leader chấp nhận residual risk strict activated-rule semantics: rule canonical chỉ possible, consumer bỏ ly_do có thể hiểu quá mức. Disclosure và negative assertions bắt buộc nhưng không biến possible thành definite/TA approval. Mixed fallback có thể bỏ một positive completion, không gọi là an toàn. |
| Kiểm chứng dự kiến | Giữ 81 helper rows; thêm null/missing, Def/Poss/AllPV/Mixed, canonical reason, all-worlds/order/multi-U/max64, age/BP crossovers. Sáu expected §9.4 approved policy. Phân tích độc lập 729 states/18 cấu hình số là bằng chứng thiết kế, không runtime; cần business tests, clean checkout/CI và benchmark audit thật. |
| Truy vết | Q FR-02–FR-08; NFR-04, NFR-05, NFR-07; A-01, A-03–A-05, A-07. Q §§3.2,4.2,5,8.2. |
| Nguồn / trạng thái | APPROVED BY LEAD — D13-E — 09/11/2026; Huy Đức phê duyệt trong TASK 02G sau khuyến nghị TASK 02F, chấp nhận risk canonical. TA §§5–6 cho quyền policy, không TA-approved convention. Các trạng thái D13 proposed ở Revision 03 là lịch sử; chưa peer approval/M1 acceptance/implementation verification. |

Bảng dưới mô tả ngữ nghĩa đã được Leader duyệt, không phải test case hoặc API mới.

| X | Y | X AND Y | X OR Y |
|---|---|---|---|
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | UNKNOWN | UNKNOWN | TRUE |
| FALSE | TRUE | FALSE | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN |
| UNKNOWN | TRUE | UNKNOWN | TRUE |
| UNKNOWN | FALSE | FALSE | UNKNOWN |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

| X | NOT X |
|---|---|
| TRUE | FALSE |
| FALSE | TRUE |
| UNKNOWN | UNKNOWN |

Đối với phần ít nhất hai trong bốn hệ của R02, T là số TRUE và U là số UNKNOWN. T ≥2 cho điều kiện đếm TRUE. T + U <2 cho điều kiện đếm FALSE. Còn lại UNKNOWN. Kết quả đếm vẫn phải AND với `co_di_nguyen_nghi_ngo` đúng biểu thức D dòng 42. [Q §4.2; L]

**Định nghĩa và thứ tự lựa chọn đã duyệt.** C(p) gồm mọi assignment True/False cho boolean unavailable, giữ known values; numeric không được completion. Def là giao tập rule TRUE qua C(p); Poss là hợp; AllPV là mọi completion có ít nhất một rule; AnyPV là tồn tại completion có rule. Không dùng OR các UNKNOWN riêng lẻ thay phép kiểm coverage. Không dùng Python truthiness của Enum.

1. Validate mọi trường; tuổi missing/null → THEO_DOI/null theo TA.
2. Def có: chọn ưu tiên R01 > R02 > R03 trong Def, attribution DIRECT. Possible ưu tiên cao hơn không thay definite.
3. Def rỗng/AllPV: positive đã chứng minh bằng disjunction; nếu PHAN_VE thì chọn rule ưu tiên trong Poss làm CANONICAL.
4. Positive theo bước 2/3 + bằng chứng hypotension TRUE → SOC_PHAN_VE/R-SOC; low BP đơn độc không đủ.
5. Mixed (AnyPV, không AllPV): THEO_DOI/null, nêu insufficient information; không AnyPV: THEO_DOI/null theo không khớp.
6. PHAN_VE/CANONICAL MUST nói mã đại diện theo policy và chưa xác nhận rule riêng; không claim unavailable=False là quan sát. Giữ đúng ba output; audit status theo thao tác.

DIRECT/CANONICAL là nhãn nội bộ hỗ trợ ly_do, không public key, mã rule hoặc audit status mới. Canonical dùng cùng thứ tự priority là convention nhóm, không chứng minh các possible rules đồng thời TRUE. Q §5 ghi chính xác nghĩa rule_id; không chọn PHAN_VE/null theo policy này.

#### 5.8.1. Trạng thái HATT và output theo TA/D13-E

Raw missing/null khác Enum. Tuổi missing/null không chọn được ngưỡng: THEO_DOI/null dù AllPV. Tuổi có, positive definite hoặc coverage nhưng current BP unavailable: chưa chứng minh sốc, vẫn PHAN_VE theo DIRECT/CANONICAL; không diễn đạt thành chắc chắn không có sốc. [TA §§2–3,5; Q FR-05–FR-08]

Adult giữ HATT <90 HOẶC giảm >30%, tức current <0.7×baseline (BP int có thể so 10×current <7×baseline). Absolute TRUE đủ dù thiếu nền; positive + absolute TRUE→SOC_PHAN_VE/R-SOC. Current ≥90, baseline unavailable: relative chưa xác nhận, không tính là đã thỏa khi chọn Tier1, không chặn PHAN_VE đã chứng minh. Đúng30 không đạt. Không ép mọi UNKNOWN thành FALSE, không đổi ngưỡng/miền số hoặc suy numeric. [D dòng 35; TA §4]

#### 5.8.2. S-correlation và attribution đã được Leader chọn

S=co_di_nguyen_nghi_ngo; I=di_nguyen_qua_duong_hit; K/H/C/G=da/hô hấp/tuần hoàn/tiêu hóa. Tuổi15/HATT110, S unavailable, K=H=I=TRUE,C=G=FALSE: Kleene R01=R02=UNKNOWN,R03=FALSE. S=False khớp R01; S=True khớp R02, nên AllPV và Def rỗng. D13-E trả PHAN_VE/R01-PV CANONICAL theo priority trong Poss. Không sửa helper R01 thành TRUE hoặc nói S=False đã biết. ly_do phải công bố đại diện R01/R02 và attribution chưa độc lập. [D dòng 41–43; Q §4.2/§5.1 TA-EX-13; L]

Cùng boolean + hypotension được chứng minh→SOC_PHAN_VE/R-SOC; thiếu BP→PHAN_VE canonical; thiếu tuổi→THEO_DOI/null. Nếu có rule definite như R03 và R02 chỉ possible thì chọn R03, không áp possible-first. Mixed ví dụ G hoặc I quyết định có rule hay không thì TD/null với lý do thiếu thông tin.

Residual risk vẫn tồn tại dù đã approved: mã representative có thể bị consumer đọc là rule thật đã khớp. Leader chấp nhận risk này ngày 09/11/2026; disclosure/test bắt buộc, không claim TA đã trả lời riêng ví dụ hoặc peer review đã xong. Không cần một approval D13 mới trước khi cập nhật task tiếp theo; các thay đổi policy sau này vẫn cần review.

## 6. Ràng buộc không được thay đổi — D11/D12

- **D11:** Không thêm, thay hoặc suy diễn quy tắc y khoa/ngưỡng ngoài `docs/decision-table.md`. Biên tuổi: `0–<1`, `1–<11`, `11–<18`, `≥18`; các so sánh HATT dùng dấu `<`, giảm tương đối người lớn phải **>30%**, đúng 30% không đủ. D04 là miền kiểm tra input, không thay điều kiện lâm sàng.
- **D12:** Không đổi chín tên input, ba khóa output và bốn trường audit. UUID là thông tin phiên synthetic **ngoài** `PatientInput`. Không log raw clinical input, PII hoặc secret; không đưa dữ liệu thực hay kết nối production. Ranh giới chi tiết nằm trong Requirements §§3–5.

## 7. Kết luận TA được áp dụng (Issue #15, 08/11/2026)

| ID | Kết luận được xác nhận | Bài test cần có |
|---|---|---|
| D01 | Nhiều rule Tầng 2 TRUE thì chọn R01 > R02 > R03; sốc được xác nhận thì dùng R-SOC | Overlap R02/R03, R01/khác, shock override |
| D02 | Tuổi thiếu hoặc null: `THEO_DOI/null`, nêu thiếu tuổi, không TypeError chỉ vì thiếu/null | Cặp missing/null tuổi; tuổi lẻ và ngưỡng |
| D03 | Tuổi có, Tầng 2 TRUE: thiếu/null HATT hiện tại hoặc nền người lớn vẫn có thể `PHAN_VE`; HATT <90 đủ chứng minh sốc người lớn dù thiếu nền | Missing/null HATT/nền; HATT 89, 90; giảm đúng/trên 30% |

**TA §§5–6:** Boolean missing/null không tự gây exception hay hạ mức khi một rule đã được chứng minh đủ; nhóm có thể công bố policy cho trường hợp chưa định nghĩa, nhưng không được đổi rule/ngưỡng/schema. D13-E là **lựa chọn nhóm**, không phải một lời chỉ định của TA. Đối chiếu đầy đủ 13 ví dụ `TA-EX-01`–`TA-EX-13` trong [`REQUIREMENTS.md`](REQUIREMENTS.md) §5.1, không nhân bản bảng trong ADR.

## 8. Các lựa chọn thiết kế chi tiết (OPEN-01–OPEN-10)

Toàn bộ 10 hướng dưới đây **đã được Leader lựa chọn ngày 08/11/2026**, tiếp tục cần peer technical review và bằng chứng triển khai. Chúng là *quyết định nhóm*, không phải yêu cầu TA. Owner/reviewer mô tả trách nhiệm kiểm tra; không phải xác nhận đã review.

### 8.2. OPEN-01 — UUID context provider

- **Lựa chọn và lý do:** Python ContextVar, set/reset bằng token ở ranh giới phiên ngoài input. Thư viện chuẩn đáp ứng ngữ cảnh cục bộ mà giữ classify(patient) và chín input keys; phù hợp quy mô M2. [PY1]
- **Phương án khác:** Đã cân nhắc provider có state chung cho lần chạy tuần tự: ít cơ chế, dễ hiểu nhưng dễ giữ nhầm phiên và rò state giữa tests. Mutable global UUID dùng chung không được chọn.
- **Đánh đổi và rủi ro:** Quản lý scope/token rõ hơn state dùng chung nhưng phải xử lý mở/kết thúc phiên và teardown. Kế thừa context sang tác vụ mới có thể mang theo UUID; ContextVar không tự giải quyết session management hoặc concurrency toàn diện.
- **Kiểm chứng cần có:** Set/reset khôi phục context trước đó khi thoát scope; kiểm tra các execution context độc lập không rò UUID, gồm đường exception. Không suy ra khả năng ghi chung file đồng thời.
- **Phụ trách/review:** Hải chủ trì; Việt Đức, Huy Đức review.

### 8.3. OPEN-02 — Không có UUID context

- **Lựa chọn và lý do:** Explicit session dùng chung UUID trong scope; thiếu phiên tạo UUID tạm mới cho từng call, reset trong finally. Một call không có explicit session được định nghĩa là phiên synthetic đơn thao tác, vẫn audit từ public entry point. UUID không phải định danh bệnh nhân/danh tính thật.
- **Phương án khác:** Đã loại cơ chế tạo UUID mặc định rồi giữ lại cho mọi call độc lập vì gắn nhầm các phiên. Bắt buộc caller mở phiên và báo lỗi khi thiếu scope làm direct call không hoàn thành audit; không chọn.
- **Đánh đổi và rủi ro:** Tạo UUID mới cho mỗi call độc lập có chi phí nhỏ và không liên kết chúng thành một phiên dài; muốn liên kết thao tác phải mở explicit session. Quên reset khi exception hoặc giữ UUID tạm trong default/provider sẽ nối nhầm phiên. Reset/khôi phục token trong finally; không tái sử dụng UUID tạm giữa hai call độc lập.
- **Kiểm chứng cần có:** Nhiều classify trong một explicit scope có cùng UUID; hai call không scope có UUID hợp lệ khác nhau; validation/audit exception vẫn reset; không rò giữa tests hoặc execution contexts.
- **Phụ trách/review:** Hải chủ trì; Việt Đức, Huy Đức review.

### 8.4. OPEN-03 — Ưu tiên lỗi validation và audit

- **Lựa chọn và lý do:** Lỗi kép ưu tiên lỗi audit an toàn ở public boundary. Fail-closed phải biểu đạt nghĩa vụ audit chưa hoàn tất. Giữ bề mặt lỗi nhỏ, không thêm trường thứ năm/status mới.
- **Phương án khác:** Giữ TypeError/ValueError công khai khi audit cũng lỗi giúp caller nhận lỗi input trước, nhưng cần kênh vận hành khác và có thể che thất bại audit. Không chọn; không thêm telemetry.
- **Đánh đổi và rủi ro:** Trong lỗi kép caller nhận lỗi audit thay vì loại lỗi input đầu tiên; test riêng validation để không che mapping D04. Exception chaining hoặc message có thể lộ raw input; public error phải an toàn, không giả định INVALID_INPUT đã được lưu.
- **Kiểm chứng cần có:** (1) Invalid + audit thành công: có INVALID_INPUT, raise TypeError/ValueError. (2) Valid + audit thất bại: lỗi audit, không trả thành công. (3) Invalid + audit thất bại: lỗi audit ưu tiên, không cam kết record, không lộ input qua message/chaining. Tên exception audit là chi tiết implement.
- **Phụ trách/review:** Việt Đức chủ trì; Hải, Huy Đức review.

### 8.5. OPEN-04 — Vị trí file JSONL

- **Lựa chọn và lý do:** Path cấu hình ngoài PatientInput, vùng dữ liệu sinh của lần chạy, độc lập cwd. Một cấu hình writer nhỏ đáp ứng demo, test và lần chạy tái lập; không mở rộng contract.
- **Phương án khác:** Path tương đối cố định theo working directory ít cấu hình nhưng phụ thuộc nơi chạy, dễ trộn log hoặc đưa log vào checkout. Không chọn; chưa cần database/logging service.
- **Đánh đổi và rủi ro:** Cần cung cấp/kiểm tra cấu hình path và quyền ghi; đổi lại test có thể chọn thư mục riêng. Path sai hoặc không ghi được gây fail-closed. Không commit audit runtime; chỉ đề xuất .gitignore ở M2 nếu cần, không sửa trong task này.
- **Kiểm chứng cần có:** Đổi cwd nhưng dùng cấu hình path vẫn ghi đúng nơi; test path riêng bằng tmp_path; lỗi mở/ghi không trả thành công. Đường dẫn cụ thể sẽ đặt khi triển khai.
- **Phụ trách/review:** Việt Đức chủ trì; Hải, Huy Đức review.

### 8.6. OPEN-05 — Phạm vi ghi đồng thời

- **Lựa chọn và lý do:** V1 ghi tuần tự, writer/file có quyền sở hữu rõ theo lần chạy. Đề không yêu cầu concurrent file writes; giảm cơ chế để hoàn thiện core/audit trong M2.
- **Phương án khác:** Lock trong tiến trình có thể bảo vệ nhiều thread nhưng thêm state/test và vẫn không bảo vệ nhiều process; không chọn cho V1.
- **Đánh đổi và rủi ro:** Không cam kết thread-safe hoặc process-safe khi cùng ghi một file. Test cần cách ly dùng file khác nhau. ContextVar chỉ cô lập ngữ cảnh, không bảo đảm atomicity của JSONL write. Nếu cần nhiều tác vụ dùng chung file, phải review lại phạm vi trước khi mở rộng.
- **Kiểm chứng cần có:** Kiểm tra writer/file thuộc lần chạy tuần tự đã công bố; test/context khác dùng file riêng. Không dùng kiểm chứng ContextVar để tuyên bố file thread/process-safe.
- **Phụ trách/review:** Việt Đức chủ trì; Hải, Huy Đức review.

### 8.7. OPEN-06 — Test isolation

- **Lựa chọn và lý do:** pytest tmp_path và fixture quản lý/reset context kể cả khi test lỗi. Tận dụng pytest sẵn có và thư mục riêng từng test, không cần hạ tầng mới. [PY2]
- **Phương án khác:** Dùng chung file rồi xóa trước mỗi test ít fixture nhưng dễ phụ thuộc thứ tự, đè dữ liệu nhau và khó debug; không chọn.
- **Đánh đổi và rủi ro:** Phải viết teardown/fixture rõ, đổi lại test có thể độc lập thứ tự và quan sát I/O thật. Fixture lỗi trước teardown hoặc scope quá rộng có thể giữ context/file dùng chung. Hải và Việt Đức review chéo core/audit fixtures.
- **Kiểm chứng cần có:** Mỗi test dùng tmp_path phù hợp; reset cả khi test/validation/audit lỗi; direct call và explicit session; writer thành công/thất bại. Rule test thuần được phép, public integration tests kiểm tra audit thật khi cần; không dùng runtime file chung ngoài kiểm soát.
- **Phụ trách/review:** Việt Đức chủ trì; Hải, Huy Đức review.

### 8.8. OPEN-07 — Ranh giới helper

- **Lựa chọn và lý do:** Ít helper theo trách nhiệm, rule evaluation tách I/O, classify điều phối công khai. Trách nhiệm validation, R01/R02/R03, điều kiện sốc, ưu tiên kết quả, explanation, writer và public orchestration bám contract và dễ test trong M2.
- **Phương án khác:** Một lõi thuần lớn giảm số điểm nối nhưng khó review nhiều nhánh validation/UNKNOWN. Framework hoặc plugin system tăng abstraction chưa có nhu cầu; không chọn.
- **Đánh đổi và rủi ro:** Cần thống nhất dữ liệu truyền giữa helper; không bắt mỗi trách nhiệm thành một function/file riêng. Hải chọn tên và số lượng tối thiểu dễ hiểu. Tách vụn hoặc helper có side effect ẩn làm luồng khó theo dõi. Review sơ đồ gọi và trách nhiệm trước code.
- **Kiểm chứng cần có:** Helper rule không file I/O; public signature giữ nguyên, direct call vẫn audit; kiểm chứng cả kết quả helper và phối hợp public, không chỉ test chiếu theo implementation.
- **Phụ trách/review:** Hải chủ trì; Việt Đức, Huy Đức review.

### 8.9. OPEN-08 — Representation logic ba trạng thái

- **Lựa chọn và lý do:** Enum TRUE/FALSE/UNKNOWN nội bộ; AND/OR/NOT tường minh theo D13. Một Enum trạng thái cho kết quả điều kiện boolean/HATT giúp đọc và review theo bảng logic; giữ raw input riêng.
- **Phương án khác:** Bool kèm sentinel UNKNOWN hoặc tuple giá trị/độ xác định ít cấu trúc nhưng trộn kiểu, dễ đảo nghĩa và dùng nhầm truthiness. Không chọn.
- **Đánh đổi và rủi ro:** Thêm kiểu/toán tử nội bộ; Enum Python vẫn có truthiness nên phải so sánh trạng thái tường minh, không dùng if state hoặc and/or/not của Python để suy diễn Enum. Raw missing/null khác Enum; UNKNOWN không lọt output. HATT UNKNOWN khác lựa chọn output theo TA; D13-E giữ Def/Poss và canonical provenance, không nói rule đại diện là definite. Peer review/test chưa chứng minh runtime.
- **Kiểm chứng cần có:** Giữ AND/OR/NOT/R02 T-U; mapping missing/null→UNKNOWN đã duyệt D13-E; test Def trước Poss, AllPV/Def rỗng, Mixed, canonical explanation và age/BP. TA-EX-01–13/sáu expected §9.4; không field/output/status mới, không truthiness.
- **Phụ trách/review:** Hải chủ trì; Việt Đức, Huy Đức review.

### 8.10. OPEN-09 — Vòng đời ghi audit

- **Lựa chọn và lý do:** Mỗi record open append/write/close bằng cơ chế quản lý tài nguyên an toàn. Vòng đời tài nguyên ngắn giảm lỗi quên đóng và vừa sức M2; chấp nhận overhead có thể đo. [PY3]
- **Phương án khác:** Giữ stream theo phiên và flush mỗi record giảm open/close nhưng thêm state và đường teardown; chưa chọn cho M2. Chỉ cân nhắc tối ưu qua đề xuất/review sau số liệu.
- **Đánh đổi và rủi ro:** Mở/đóng từng record tốn I/O hơn stream dài; close/flush không đồng nghĩa dữ liệu bền vững sau mất điện. Không mặc định fsync hoặc durability production. Lỗi write/flush/close phải được nhận biết theo fail-closed; có thể có dòng chưa hoàn chỉnh. Không báo thành công trước hoàn tất bước ghi theo policy.
- **Kiểm chứng cần có:** Thử lỗi mở/write/flush/close và xác nhận public không báo hoàn tất thành công; benchmark chính đo open/write/close audit thực, không mock writer hoặc giữ record đến cuối lô rồi coi call trước đã hoàn tất.
- **Phụ trách/review:** Việt Đức chủ trì; Hải, Huy Đức review.

### 8.11. OPEN-10 — Warm-up và percentile benchmark

- **Lựa chọn và lý do:** perf_counter_ns; 100 warm-up; N≥1.000; nearest-rank p50/p95; full-path audit thực. Công thức đơn giản, reviewer tính lại được; phù hợp thời gian M2 và yêu cầu A-10, không thêm ngưỡng nghiệm thu.
- **Phương án khác:** Số warm-up khác có lý do và percentile nội suy tuyến tính là phương án khả thi đã cân nhắc, nhưng có thêm quy ước và khó so tái lập nếu dùng mặc định thư viện. Leader chọn 100/nearest-rank.
- **Đánh đổi và rủi ro:** Nearest-rank lấy một mẫu nên percentile có bước nhảy. Warm-up cố định không bảo đảm loại mọi nhiễu; phải công bố môi trường/cấu hình và không chọn lọc mẫu. Sai ceil/chỉ số từ 1, tính cả warm-up, chia nhầm ns/ms hoặc bỏ I/O làm sai kết quả. Chưa có benchmark thực hoặc kết luận A-10 đạt.
- **Kiểm chứng cần có:** Sắp N mẫu tăng dần, vị trí ceil(p×N) theo chỉ số 1; p=0,50/0,95, ns chia 1.000.000 ra ms. Loại 100 warm-up; đo N≥1.000 full public path có open/write/close thật. Công bố Python, OS, CPU/hardware, số lượt, dữ liệu synthetic và I/O; báo p50/p95, kiểm tra p95<100 ms. Logic thuần báo riêng.
- **Phụ trách/review:** Việt Đức chủ trì; Hải, Huy Đức review.

## 9. Ma trận truy vết và bằng chứng kiểm chứng

| ID | FR/NFR chính | AC | Bằng chứng còn phải thu |
|---|---|---|---|
| D01 | FR-03/04/06/08 | A-01/05/07 | Test rule priority, overlap và shock override |
| D02 | FR-05/06/07 | A-01/04/07 | Test tuổi missing/null và reason |
| D03 | FR-05/06/07 | A-01/04/07 | Test HATT/nền unavailable và các boundary |
| D04 | FR-07; NFR-02/03 | A-04/07 | TypeError/ValueError, allowed unavailable, lỗi unrelated field |
| D05 | FR-01–09; NFR-04/05 | A-01/02/07–09 | Public orchestration + helper, UUID scope, CI từ PR |
| D06 | FR-08; NFR-07 | A-05 | DIRECT/CANONICAL reason và negative assertions |
| D07 | FR-09; NFR-02/03 | A-06 | JSONL 4 trường/UTC/UUID, path/cwd, writer failures |
| D08 | FR-07/09; NFR-03 | A-04/06 | 3 đường lỗi audit/validation, error precedence, privacy |
| D09 | FR-01–09; NFR-05/06 | A-07/08/09 | Test nghiệp vụ, `pytest -q` clean checkout, PR CI run |
| D10 | NFR-01 | A-10 | Benchmark ≥1.000 mẫu sau warm-up, p50/p95, môi trường |
| D11 | FR-02–06 | A-01/03/07 | Review rule/ngưỡng và boundary theo Decision Table |
| D12 | FR-01/07–09; NFR-02/08 | A-04–06/11 | Schema/privacy và disclaimer README |
| D13 | FR-02–08; NFR-04/05/07 | A-01/03–05/07 | Enum/T-U, Def/Poss/AllPV, Mixed, canonical reason |

**Lưu ý:** Không AC nào ở bảng này được xem là verified chỉ từ hồ sơ M1. Riêng A-11 yêu cầu README có câu `educational/synthetic — not for clinical use`; A-08/A-09 cần bằng chứng test/CI chạy thật, A-10 cần số liệu benchmark thật.

### 9.1. Những nhóm kiểm thử quan trọng

Ưu tiên các tình huống: (1) rule overlap và ngưỡng biên; (2) null/missing/invalid kiểu và khóa; (3) missing age/BP/nền; (4) Enum, T/U, definite-vs-possible, AllPV/Mixed; (5) đúng `ly_do` và không tiết lộ dữ liệu; (6) explicit/single-call UUID, reset `finally` và context isolation; (7) writer open/write/flush/close thất bại, lỗi kép, path ngoài repo; (8) benchmark full-path. Các case cụ thể nằm ở `docs/m1-hai/M1/TEST_CASES.csv`, `docs/m1-hai/M2/INTERNAL_STATE_CASES.csv` và QA Matrix; không cần tái chép tất cả trong ADR.

### 9.2. Các ví dụ chính thức và giới hạn thẩm quyền

Xem `REQUIREMENTS.md` §5.1 cho `TA-EX-01`–`TA-EX-13`. Các expected 01–11 đối chiếu phản hồi TA, còn 12–13 phản ánh policy D13-E; **không gán cả 13 ca là TA đã phê duyệt từng expected**. Ví dụ đầu vào unavailable hợp lệ sau phân loại và audit thành công dùng `SUCCESS`, không tự `INVALID_INPUT`.

### 9.3. Tình trạng tài liệu kiểm thử M1-02 và QA M1-03

- [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) đã tích hợp **175 ca thiết kế chính** (từ baseline 157 ca) và **81 ca logic nội bộ**; [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) đã tích hợp QA Matrix ánh xạ A-01–A-11. Đây là **test design**, chưa phải pytest thực thi.
- Bộ ca hiện hành được đối chiếu có **36 invalid** (28 TypeError, 8 ValueError), **8 ca nullable hợp lệ** `INV-001/017/021/025/029/033/037/043`; riêng `INV-043` kỳ vọng `SOC_PHAN_VE/R-SOC`. `AUD-002` nay dùng chuỗi `"true"` nên là TypeError/INVALID_INPUT nếu audit thành công. Các số lịch sử 35 invalid/9 nullable là bản fixture cũ.
- Thành viên phụ trách đã đóng góp bản M1-02/M1-03 gốc; Leader có sửa/tích hợp có hỗ trợ AI. Approval PR và tài liệu đã merge **không** chứng minh Hải/Việt Đức đã review kỹ thuật vòng cuối, hoặc CI/runtime đạt. Cần lưu review thực chất và bằng chứng chạy.

### 9.4. Sáu expected D13-E đã được Leader phê duyệt — bàn giao TASK 02E

**Chỉ là expected theo policy D13-E được Leader duyệt ngày 09/11/2026**, dựa trên fixture gốc của Hải. CSV/QA đã tích hợp qua PR #3/#4; chưa chạy engine hoặc hoàn tất peer technical review.

| Test ID | muc_do | rule_id | Attribution / explanation bắt buộc |
|---|---|---|---|
| MISS-009 | PHAN_VE | R01-PV | CANONICAL: AllPV qua R01/R02, Def rỗng; nêu mã đại diện và thiếu attribution, không claim S=False/riêng R01 đã được xác nhận |
| TA15-BOOL1-NULL | PHAN_VE | R01-PV | CANONICAL như MISS-009; null tương đương missing; không chỉ generic reason |
| TA15-BOOL1-MISSING | PHAN_VE | R01-PV | CANONICAL như cặp null; không bắt UUID/reason nguyên văn bằng nhau |
| MISS-012 | THEO_DOI | null | Mixed do G unavailable; nêu chưa đủ thông tin, không nói G=False hoặc R02 chắc chắn FALSE |
| TA15-DEPENDENT_INHALATION-NULL | THEO_DOI | null | Mixed do I unavailable; không ép I hoặc kết luận an toàn |
| TA15-DEPENDENT_INHALATION-MISSING | THEO_DOI | null | Cùng fallback/uncertainty như cặp null |

SUCCESS chỉ khi thao tác phân loại hợp lệ và writer hoàn tất. Các dòng trên không tạo status audit mới. Ở `MISS-009`, helper R01/R02 vẫn UNKNOWN; chỉ output `rule_id` dùng mã CANONICAL theo D13-E. Không biến mã đại diện thành rule definite. Các expected này do nhóm duyệt, **không phải TA chỉ định**.

## 10. Rủi ro và việc còn chờ

| Hạng mục | Trạng thái / hành động kiểm chứng |
|---|---|
| **Canonical attribution D13-E** | Leader chấp nhận residual risk rule đại diện có thể bị hiểu là rule definite; bắt buộc disclosure trong `ly_do` và negative tests, không coi là TA approval. |
| **Default audit path** | Đề xuất §5.4.1 **chưa được duyệt**; review quyền truy cập, vị trí ngoài repo, tính độc lập cwd và hành vi fail-closed trước khi triển khai. |
| **Unexpected internal exception** | Chưa chốt cách audit/propagate khi helper lỗi trước ghi audit; không tự gán SUCCESS/INVALID_INPUT, thêm status hoặc log input; cần review Dev/QA. |
| **UUID/concurrency, writer failure** | Kiểm reset, không rò context và không hứa thread/process-safe; kiểm open/write/flush/close, lỗi kép và privacy. |
| **Kiểm thử/CI/benchmark** | Chưa có engine chạy thật, clean-checkout pytest nghiệp vụ, CI được kiểm chứng hay số liệu latency. Bổ sung `pytest.ini` theo Issue #16. |
| **Review của nhóm** | Leader tiếp tục hậu kiểm thủ công; Hải và Việt Đức đối chiếu core/audit/Test Plan/QA, ghi lại nhận xét thực tế trước các thay đổi tiếp theo. |

**Thực hiện sau M1:** Dev ưu tiên classifier + tests; QA phụ trách audit/privacy/CI/benchmark; Lead kiểm yêu cầu, đối chiếu Rule Design và nghiệm thu thực tế. Không tuyên bố pass chỉ từ tài liệu; các thay đổi policy phải được review và duyệt lại bởi người phụ trách. Không để AI tự merge/phát hành/xác nhận bài đạt.

## 11. Nguồn và lịch sử

| Nguồn | Liên kết / ý nghĩa |
|---|---|
| **E** | [Đề Hack Marathon chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung v1.0.2 |
| **D** | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), nguồn quy tắc/ngưỡng đã khóa |
| **TA** | [Phản hồi chung Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), D01–D03 và null/missing |
| **Q** | [`REQUIREMENTS.md`](REQUIREMENTS.md) — FR/NFR/AC và 13 ví dụ đối chiếu |
| **G/P** | [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md) / [`docs/TEAM_PLAN.md`](docs/TEAM_PLAN.md), phân công/bối cảnh nội bộ; snapshot lịch sử không ghi đè TA |
| **PY** | [contextvars](https://docs.python.org/3.12/library/contextvars.html), [pytest tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html), [Python I/O](https://docs.python.org/3.12/library/io.html), [perf_counter_ns](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns) |
| **PR** | [#1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [#2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [#3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [#4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4), merge ngày 10/11/2026; không phải TA nghiệm thu |

| Mốc | Thay đổi chính |
|---|---|
| 07–08/11, Draft/Revision 02 | Khởi tạo ADR, nhóm chọn 10 hướng OPEN; phần null/missing lúc đầu chờ phản hồi TA |
| 08/11, Revision 03 | Đồng bộ phản hồi TA về priority, tuổi/BP/boolean unavailable; cập nhật policy cũ |
| 09/11, Revision 04 | Leader duyệt D13-E, chấp nhận canonical residual risk; cập nhật expected và test design |
| 10–11/11, sau merge | PR #1–#4 tích hợp M1; biên tập gọn để rà soát thủ công, **không** thay đổi quyết định kỹ thuật hoặc giả định test đã đạt |

*Lưu ý tài liệu:* Chi tiết từng bước phê duyệt, các SHA trước merge và bản nội dung dài vẫn có thể truy vết qua lịch sử Git của `DECISIONS.md`; không xóa hoặc viết lại lịch sử đó.
