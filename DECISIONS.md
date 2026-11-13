# Hồ sơ quyết định kiến trúc — Track A (ADR)

> **Mục đích:** Ghi lại *vì sao* nhóm lựa chọn kiến trúc và cách kiểm chứng. Chi tiết trường dữ liệu, FR/NFR/AC ở [`REQUIREMENTS.md`](REQUIREMENTS.md); toàn bộ test cases ở `docs/m1-hai/`, QA Matrix ở `docs/m1-qa/`. Đây là **thiết kế**, không phải báo cáo engine đã chạy.

## 1. Thông tin và trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Nhóm / sản phẩm | `173820_n27` · Dr May Day Rule Engine — Track A |
| Phiên bản | M1 Revision 04 — cập nhật lựa chọn mã sau Issue #31 và rà soát tài liệu |
| Chủ trì | Lead (Huy Đức); Dev (Hải); QA (Việt Đức) |
| Starter | `fossbk-spec/ktpmud-bkt-ruleengine-starter`, tag `bkt-2026-v1`, SHA `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Trạng thái tài liệu | PR #1–#4 đã merge ngày 10/11/2026; mốc tích hợp M1 `9bc4fc186415d7a13cd9d49692c50f3c945ddf7b`. ADR ghi nhận cập nhật chọn mã sau Issue #31, đối chiếu Requirements tại `45e0870e0cae2c95b070c424e0de38e3c763bc9d`. |
| Phê duyệt và giới hạn | Leader phê duyệt D13-E ngày 09/11 và sau Issue #31 cập nhật cách chọn mã; có approval PR từ `nvldvc` và comment của Leader; chưa có bằng chứng cả Hải và Việt Đức đã review kỹ thuật vòng cuối. Chưa có classifier nghiệp vụ, pytest nghiệp vụ, CI nghiệm thu hay benchmark được kiểm chứng. |

**Thứ tự nguồn:** Đề/Decision Table và làm rõ chính thức tại [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002) được ưu tiên trong phạm vi nội dung được làm rõ; tiếp theo là chính sách nhóm đã duyệt và các đề xuất. D01–D03 được TA làm rõ. Issue #31 làm rõ lựa chọn mã đại diện khi thiếu khóa boolean; việc áp dụng vào ca vừa có rule chắc chắn vừa có rule ưu tiên cao hơn chỉ có thể thỏa là quyết định nhóm. Không coi toàn bộ D13-E hoặc kiến trúc audit được TA phê duyệt. Merge PR không đồng nghĩa TA nghiệm thu hoặc mọi AC đạt.

## Hướng dẫn đọc tài liệu

ADR (*Architecture Decision Record*) là hồ sơ giải thích **nhóm chọn cách làm nào, vì sao chọn và cần kiểm chứng điều gì**. Requirements mô tả phần mềm phải đáp ứng gì; ADR ghi lý do và các phương án đã cân nhắc.

- **§2–4:** bối cảnh, danh mục D01–D13 và luồng xử lý tổng quan.
- **§5–7:** từng quyết định, phương án khác, rủi ro, cách kiểm chứng và các làm rõ của GV/TA.
- **§8:** chi tiết 10 lựa chọn OPEN; **§9–11:** truy vết, rủi ro, nguồn và lịch sử.

| Thuật ngữ | Cách hiểu trong tài liệu |
|---|---|
| **Validation / invalid** | Kiểm tra đầu vào / dữ liệu sai kiểu, sai miền hoặc có khóa không cho phép. Missing là thiếu khóa; null là có khóa nhưng không có giá trị. |
| **UNKNOWN** | Trạng thái nội bộ “chưa biết”; khác `FALSE`, không phải kết quả đầu ra mới. |
| **Def / Poss** | Def là tập rule chắc chắn đúng; Poss là tập rule có thể đúng trong ít nhất một cách xét dữ liệu thiếu. |
| **AllPV / Mixed** | AllPV: mọi khả năng boolean thiếu đều khớp ít nhất một rule phản vệ. Mixed: có khả năng khớp và khả năng không khớp. |
| **DIRECT / CANONICAL** | DIRECT gắn mã rule chắc chắn; CANONICAL là mã đại diện trong trường hợp được quy định ở §5.8. |
| **Audit / JSONL / writer** | Audit là nhật ký thao tác; JSONL lưu mỗi bản ghi JSON trên một dòng; writer là thành phần ghi nhật ký. |
| **Fail-closed** | Nếu audit bắt buộc thất bại, hàm không báo thao tác phân loại đã hoàn tất thành công. |
| **Runtime / evidence** | Runtime là khi chương trình thực sự chạy; hồ sơ thiết kế hoặc approval không tự chứng minh test, CI hay benchmark đã đạt. |
| **Fixture / expected** | Bộ dữ liệu giả lập của một ca kiểm thử / kết quả dự kiến của ca đó. |
| **Coverage / attribution** | Xét các khả năng của dữ liệu thiếu / giải thích cơ sở lựa chọn mã rule. |
| **FR / NFR / AC** | Yêu cầu chức năng / yêu cầu phi chức năng / tiêu chí nghiệm thu, được giải thích ở Requirements. |
| **Scope / context / isolation** | Phạm vi phiên / ngữ cảnh đang hoạt động / việc tách dữ liệu giữa các lần chạy hoặc ca test. |
| **Public / helper / writer** | Hàm được gọi từ ngoài / hàm hỗ trợ bên trong / thành phần ghi audit. |

**Nhãn trạng thái:** `TA CONFIRMED` = hành vi đã được TA xác nhận; `APPROVED BY LEAD` = quyết định nhóm; `PENDING PEER TECHNICAL REVIEW` = chưa có xác nhận kỹ thuật cuối của thành viên; `PROPOSED` = chưa phê duyệt. `OPEN-01`–`OPEN-10` là mã lịch sử, **đã chọn phương án** nhưng chưa nghiệm thu bằng code.

## 2. Bối cảnh, phạm vi và các ràng buộc

Starter chỉ cung cấp `classify(patient)` còn `NotImplementedError`. Nhóm xây Rule Engine Python từ [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md) bằng dữ liệu synthetic; không kết nối production hoặc đưa lời khuyên điều trị. Mục tiêu là phân loại đúng, giải thích có thể truy vết và audit không lộ input lâm sàng. Thiết kế ưu tiên **validation → logic thuần → lựa chọn output → audit**; chi tiết chức năng xem Requirements FR-01–FR-09.

**Bất biến phải giữ:** `classify(patient)`; 9 trường input; 3 output `muc_do`, `rule_id`, `ly_do`; điều kiện R01/R02/R03 và R-SOC cùng ngưỡng/ưu tiên từ Decision Table; audit đúng 4 trường `Timestamp`, `User_UUID`, `Action_Type`, `Status`; không thêm rule/ngưỡng lâm sàng hoặc dữ liệu thật. Các nghĩa vụ test, CI và benchmark theo A-01–A-11 vẫn bắt buộc.

## 3. Danh mục quyết định D01–D13

| ID | Quyết định chính | Trạng thái / nguồn |
|---|---|---|
| D01 | Khi nhiều rule Tầng 2 cùng TRUE: ưu tiên R01 > R02 > R03; R-SOC ưu tiên nếu có sốc xác nhận | **TA CONFIRMED** |
| D02 | Tuổi missing/null → `THEO_DOI/null`, nêu thiếu tuổi | **TA CONFIRMED** |
| D03 | Có tuổi và đã chứng minh phản vệ: thiếu HATT hiện tại → `PHAN_VE`; ở người lớn, HATT ≥90 và thiếu nền → `PHAN_VE`. HATT <90 ở người lớn thỏa nhánh huyết áp; xác định sốc cần cả điều kiện phản vệ. | **TA CONFIRMED** |
| D04 | Phân biệt unavailable với invalid; non-null sai kiểu → TypeError, sai miền/khóa lạ → ValueError; strict validation mọi trường | APPROVED BY LEAD; policy cũ về tuổi/boolean null bị TA thay thế |
| D05 | Public `classify()` điều phối, helper rule thuần và writer audit riêng | APPROVED BY LEAD |
| D06 | `ly_do` tất định, giải thích DIRECT/CANONICAL, không raw input hoặc lời khuyên điều trị | APPROVED BY LEAD; tôn trọng TA |
| D07 | JSONL audit riêng, ContextVar/UUID ngoài patient input, file theo lần chạy | APPROVED BY LEAD |
| D08 | Audit `CLASSIFY` với `SUCCESS/INVALID_INPUT`; fail-closed, lỗi kép ưu tiên audit | APPROVED BY LEAD |
| D09 | Test nghiệp vụ normal/boundary/missing/invalid, ngữ nghĩa D13-E; test isolation | APPROVED BY LEAD |
| D10 | Benchmark `perf_counter_ns`, 100 warm-up, ≥1.000 mẫu, nearest-rank p50/p95, full-path I/O thật | APPROVED BY LEAD |
| D11 | Không đổi clinical rules/ngưỡng từ Decision Table | FACT / SPECIFIED |
| D12 | Giữ input/output/audit schema và giới hạn privacy | FACT / SPECIFIED |
| D13 | Boolean thiếu/null → UNKNOWN; khi AllPV chọn rule ưu tiên cao nhất trong Poss, phân biệt mã trực tiếp và mã đại diện; Mixed theo §5.8 | Leader cập nhật cách chọn mã sau Issue #31; ADR và test vẫn cần review và kiểm chứng runtime. |

**Quan trọng:** D04 và các chi tiết triển khai D13-E là chính sách nhóm trong phạm vi được phép; các làm rõ chung của TA vẫn áp dụng theo nguồn tương ứng. Issue #31 đã xác nhận cách chọn mã đại diện trong trường hợp nêu; không suy ra TA đã duyệt toàn bộ thuật toán, kiến trúc hoặc mọi expected của nhóm. Chi tiết ở §5, phân công và phương án ở §8.

## 4. Kiến trúc dự kiến và hành vi công khai

`classify(patient)` là hàm được gọi từ bên ngoài. Theo thiết kế, hàm điều phối các bước sau:

1. **Kiểm tra đầu vào:** kiểm tra tất cả trường theo D04. Dữ liệu thiếu/null được cho phép khác dữ liệu sai kiểu hoặc sai miền.
2. **Kiểm tra tuổi:** thiếu/null tuổi thì chọn `THEO_DOI / null`, nêu thiếu tuổi và chuyển sang audit. Nếu có tuổi, đánh giá R01/R02/R03 theo Decision Table và D13-E (§5.8).
3. **Đánh giá các khả năng:** nếu mọi khả năng dữ liệu boolean chưa biết đều khớp ít nhất một rule Tầng 2 (AllPV), phản vệ đã được chứng minh. Nếu là Mixed hoặc không khả năng nào khớp, chọn `THEO_DOI / null`, giải thích phù hợp và chuyển sang audit.
4. **Ưu tiên xét sốc:** khi AllPV và điều kiện tụt HATT theo tuổi đã được xác nhận, chọn `SOC_PHAN_VE / R-SOC`, rồi chuyển sang audit. Huyết áp thấp riêng lẻ không đủ để kết luận sốc phản vệ.
5. **Chọn mã nếu là PHAN_VE:** khi AllPV nhưng chưa xác nhận sốc, chọn rule có ưu tiên cao nhất trong tập các rule có thể thỏa (Poss). Nếu rule mang mã đó chưa chắc chắn đúng, `ly_do` phải nói rõ mã là đại diện, kể cả khi rule ưu tiên thấp hơn chắc chắn đúng.
6. **Ghi audit rồi trả:** với input hợp lệ, hoàn tất ghi `CLASSIFY / SUCCESS` trước khi trả đúng ba trường. Với input invalid, ghi `INVALID_INPUT` thành công rồi phát sinh `TypeError` hoặc `ValueError` theo D04. Nếu audit thất bại, kể cả lỗi kép, ưu tiên lỗi audit an toàn và không báo thành công (§5.5, OPEN-03).

**Phiên và audit:** Các lần gọi trong phiên tường minh dùng chung UUID synthetic; một lần gọi độc lập không có phiên dùng UUID tạm mới rồi reset trong `finally`. UUID/context ở ngoài input. Writer JSONL ghi đúng bốn trường, mở/ghi/đóng theo từng lần; `ContextVar` không bảo đảm nhiều tiến trình/luồng ghi chung file an toàn. Đường dẫn mặc định khi gọi trực tiếp **chưa được duyệt** (§5.4.1); lỗi helper nội bộ bất ngờ vẫn cần review.

Tại mốc đối chiếu, `rule_engine/classifier.py` vẫn là stub; test starter chưa chứng minh nghiệp vụ. Chưa có bằng chứng test/CI nghiệp vụ hoặc benchmark thực tế đạt. A-11 đã được đối chiếu riêng bằng disclaimer trong README (§9).

## 5. Các quyết định kiến trúc (Architecture Decision Records)

Các phương án thay thế và lập luận dưới đây là hồ sơ thiết kế đã tích hợp vào M1. Hướng lựa chọn đã được Leader duyệt qua nguồn ghi ở mỗi ADR; phần kiểm chứng kỹ thuật của Hải/Việt Đức và chi tiết triển khai còn cần review thực chất. Tích hợp tài liệu không đồng nghĩa AC được nghiệm thu.

### 5.1. D04 — Validation input nghiêm ngặt

**Đọc nhanh:** Dữ liệu thiếu/null được phép khác dữ liệu sai. Nhóm kiểm tra mọi trường trước khi phân loại; sai kiểu và sai miền được báo bằng loại lỗi khác nhau.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Sai kiểu và unavailable khác nhau. Ép kiểu có thể biến dữ liệu chưa xác nhận thành bằng chứng. TA cho phép null/thiếu ở tuổi, HATT và boolean; không được giữ validation cũ loại null tuổi/boolean. TypedDict chưa validation runtime. |
| Quyết định | Giữ tuổi là int/float hữu hạn ≥0, cho phép số lẻ nhưng loại bool; HATT hiện tại là int ≥0, HATT nền là int >0. Hai trường HATT không nhận bool/float/chuỗi. Missing/null ở ba trường số nghĩa là không có dữ liệu. Boolean True/False hợp lệ; missing/null → UNKNOWN theo D13-E. Sai kiểu non-null → TypeError; sai miền hoặc khóa lạ → ValueError. Kiểm tra mọi trường, không ép kiểu hay đổi dữ liệu invalid thành UNKNOWN/THEO_DOI; lần invalid vẫn phải audit theo D08. |
| Phương án khác | Tự chuyển chuỗi/số thành kiểu mong muốn để nhận được nhiều dạng dữ liệu hơn. Phương án này giảm lỗi tích hợp ban đầu nhưng cần quy ước diễn giải và có thể che lỗi bên gọi. |
| Lý do lựa chọn | Đầu vào nhỏ, cố định và giả lập cho phép yêu cầu bên gọi cung cấp đúng kiểu. Validation nghiêm giúp tìm lỗi sớm và giữ bằng chứng phân loại theo dữ liệu thực nhận. Các miền số là policy dữ liệu của nhóm, tách khỏi ngưỡng lâm sàng trong D. |
| Hệ quả / đánh đổi | Giữ kiểm tra số hữu hạn, loại bool khỏi miền số và phân biệt unavailable với invalid thực sự. Tuổi missing/null có output TA quy định; thiếu current BP/nền không tự hạ Tầng 2 đã xác nhận. Không tự đổi current BP=0 thành invalid; baseline=0 vẫn ValueError theo policy số đã duyệt. |
| Rủi ro / giảm thiểu | Validator cũ có thể nhận bool như số hoặc còn loại age/boolean null. Kiểm tra toàn bộ input, không bỏ qua field invalid không liên quan dù đã chứng minh rule; giữ message/chaining không chứa giá trị lâm sàng thô. Không gán INVALID_INPUT chỉ vì missing/null được phép. |
| Kiểm chứng dự kiến | Test missing/null/non-null invalid, miền số/tuổi lẻ/khóa lạ/unrelated invalid và privacy. Nguồn Hải hiện có 36 invalid=28 TypeError+8 ValueError khi audit thành công; INV nullable và AUD-002 fixture đã thay được bàn giao ở §9.3. Lỗi kép vẫn OPEN-03. Chưa implementation/test evidence. |
| Truy vết | Q FR-07; NFR-02, NFR-03, NFR-05; A-04, A-07. |
| Nguồn / trạng thái | APPROVED BY LEAD — PARTIALLY SUPERSEDED BY TA. TA §§2–5 thay chính sách null tuổi/boolean cũ; mapping lỗi, miền số và OPEN-03 giữ phần đã duyệt. [TA](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248); Q §§3, 4.3, 8.1; L. Không coi toàn bộ D04 bị hủy. |

### 5.2. D05 — Thiết kế Python tối giản, dễ bảo trì

**Đọc nhanh:** Hàm công khai điều phối các bước; logic đánh giá rule tách khỏi việc ghi file để dễ hiểu và kiểm thử.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | `classify(patient)` phải phối hợp validation, đánh giá rule, ưu tiên và output, còn audit thêm I/O. Gom mọi trách nhiệm làm khó review AND/OR và khó khoanh vùng lỗi. |
| Quyết định | Giữ chữ ký classify(patient); hàm này điều phối validation, rule, chọn kết quả, giải thích và audit kể cả khi gọi trực tiếp. Tách một số helper theo trách nhiệm: validation, R01/R02/R03, điều kiện sốc, chọn kết quả và explanation; writer I/O riêng. Không bắt mỗi trách nhiệm thành một hàm/file và không thêm framework/plugin. Context/provider theo OPEN-01/02, helper theo OPEN-07. |
| Phương án khác | Một hàm lớn giảm số điểm gọi nhưng trộn nhánh nghiệp vụ với I/O. Một hệ thống lớp/plugin tổng quát hỗ trợ mở rộng nhưng thêm abstraction và chi phí bảo trì chưa có nhu cầu trong bài. |
| Lý do lựa chọn | Ranh giới theo validation, rule, quyết định kết quả, giải thích và audit cho phép review trực tiếp từng phần theo Q. Số quy tắc nhỏ nên chưa có căn cứ xây framework rule tổng quát. |
| Hệ quả / đánh đổi | Các phần thuần dễ unit test, lỗi dễ định vị. Chi phí là định nghĩa ranh giới và bảo đảm các hàm phối hợp đúng, không tạo nhiều bước chỉ để chuyển dữ liệu qua lại. |
| Rủi ro / giảm thiểu | Helper quá vụn hoặc trạng thái ẩn làm khó review. Hải chọn số lượng/tên helper tối thiểu; Việt Đức review testability và đường giao thoa core/audit. Kiểm chứng public orchestration cùng provider, không chỉ helper. |
| Kiểm chứng dự kiến | Review signature không đổi; gọi trực tiếp vẫn audit; explicit session dùng cùng UUID, call độc lập dùng UUID mới và reset sau exception; rule test thuần và public integration test. Chưa có code hoặc kết quả chạy. |
| Truy vết | Q FR-01–FR-09; NFR-04, NFR-05; A-01, A-02, A-07–A-09. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D05, Q §4.3 và L; OPEN-01/02/07 ngày 08/11/2026 là APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW. Tên helper/module là chi tiết triển khai nhỏ, không phải hướng kiến trúc chưa chọn. |

### 5.3. D06 — Giải thích tất định, liên kết rule

**Đọc nhanh:** Dùng cách giải thích ổn định gắn với kết quả; nếu mã chỉ là đại diện thì phải nói rõ, đồng thời không đưa dữ liệu thô hoặc lời khuyên điều trị.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Output phải cho biết rule nào dẫn đến kết quả và giải thích ngắn. Nội dung tự do có thể đưa dữ liệu thô hoặc lời khuyên điều trị vào `ly_do`. |
| Quyết định | Dùng mẫu giải thích ổn định; không dùng LLM, không đưa input lâm sàng thô hoặc điều trị. Với `PHAN_VE`, DIRECT là mã đã chọn và rule mang mã đó chắc chắn đúng. CANONICAL là mã ưu tiên cao nhất trong Poss nhưng rule mang mã chưa chắc chắn, áp dụng khi AllPV kể cả nếu rule ưu tiên thấp hơn đã chắc chắn đúng; bắt buộc nói mã là đại diện và chưa được xác nhận độc lập, không nói giá trị UNKNOWN=False đã được quan sát. Mixed nêu chưa đủ thông tin; thiếu tuổi/HATT hiện tại/nền giải thích theo TA. Không thêm khóa output. |
| Phương án khác | Ghép câu từ toàn bộ triệu chứng và số đo tạo nhiều chi tiết nhưng tăng nguy cơ rò dữ liệu. Sinh câu linh hoạt làm tăng độ biến thiên và khó kiểm chứng nội dung đúng giới hạn. |
| Lý do lựa chọn | Bộ mã rule nhỏ, output cố định và dữ liệu synthetic đủ để dùng template. Reviewer đối chiếu được mã rule với câu giải thích mà không cần tái tạo dữ liệu input trong output. |
| Hệ quả / đánh đổi | Template ổn định và dễ đối chiếu một rule_id. D01 đã có priority chính thức R01 > R02 > R03; trường hợp overlap có thể nêu thêm rule khớp trong ly_do nhưng không thêm mã output. Cần phân biệt thiếu tuổi, thiếu current BP và thiếu baseline. |
| Rủi ro / giảm thiểu | Không diễn đạt THEO_DOI thành an toàn, hoặc chưa xác nhận sốc thành bằng chứng không có sốc. Nêu lý do unavailable theo TA, không suy số đo hay lộ input qua explanation/lỗi. D01–D03 không còn phụ thuộc phản hồi TA cho ca đã trả lời. |
| Kiểm chứng dự kiến | Ba output keys, priority/attribution theo D13-E, TA-EX-01–13 và sáu expected §9.4; negative reason assertions bắt câu khẳng định S=False hoặc R01 definite ở canonical. Missing age/BP/nền đúng TA. Chưa có output runtime được nghiệm thu. |
| Truy vết | Q FR-08; NFR-07; A-05, liên quan A-01. |
| Nguồn / trạng thái | Template APPROVED BY LEAD theo L; nội dung kỳ vọng D01–D03 theo TA §§1–5 và Q FR-08. D dòng 49–55/E A-05 giữ contract; TA không phê duyệt công nghệ template. |

### 5.4. D07 — Audit writer JSONL riêng, bảo vệ dữ liệu

**Đọc nhanh:** Thành phần writer riêng ghi audit đúng bốn trường. UUID là thông tin phiên giả lập nằm ngoài input bệnh nhân.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Cần audit bốn trường cho thao tác nhưng pure rule evaluation không cần UUID hay file I/O. Thêm UUID vào `PatientInput` sẽ vượt danh sách khóa đã khóa. |
| Quyết định | Writer JSONL riêng ghi đúng Timestamp, User_UUID, Action_Type, Status. Timestamp ISO 8601 có timezone UTC; UUID synthetic hợp lệ; Action_Type=CLASSIFY, Status=SUCCESS/INVALID_INPUT. classify() công khai tự điều phối audit. ContextVar nằm ngoài PatientInput để cấp UUID cho phiên tường minh hoặc một call tạm. Path cấu hình ngoài input, trong vùng dữ liệu sinh của lần chạy; V1 ghi tuần tự và có chủ sở hữu file rõ. Mỗi record hoàn tất open/append/write/close trước khi báo xong. Xem OPEN-01/02/04/05/09. |
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

**Đọc nhanh:** Ghi SUCCESS khi xử lý hợp lệ hoàn tất; ghi INVALID_INPUT cho lỗi đầu vào thực sự nếu audit thành công. Lỗi audit được xử lý fail-closed.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Chỉ ghi lần thành công bỏ sót dấu vết các yêu cầu invalid. Ghi đầy đủ exception/payload có thể tiết lộ triệu chứng hoặc số đo. |
| Quyết định | Ghi CLASSIFY/SUCCESS khi thao tác hợp lệ hoàn tất; CLASSIFY/INVALID_INPUT khi validation lỗi thực sự. Missing/null được TA cho phép không tự là INVALID_INPUT. Giữ bốn trường, không ghi payload/chi tiết exception. Invalid + audit thành công → raise TypeError/ValueError; valid + audit thất bại → lỗi audit an toàn; lỗi kép ưu tiên lỗi audit và không giả định đã lưu INVALID_INPUT. Không để message/chaining lộ input. Xem OPEN-03. |
| Phương án khác | Chỉ audit thành công giảm số bản ghi nhưng thiếu truy vết lỗi input. Ghi lỗi chi tiết thuận debug nhưng vượt giới hạn dữ liệu và schema. |
| Lý do lựa chọn | Trạng thái tổng quát đủ cho mục đích nhận biết một lần thử đã thành công/thất bại mà không tái tạo dữ liệu input. Phạm vi mở rộng sang invalid là quyết định nội bộ, tách khỏi yêu cầu chính thức audit mỗi lần phân loại. |
| Hệ quả / đánh đổi | Tăng khả năng truy vết và giảm rò dữ liệu, nhưng giảm chi tiết debug. Hai Status đã duyệt mô tả xử lý thao tác, không ánh xạ trực tiếp mức phản vệ. Fail-closed có thể ngăn trả kết quả dù logic đã tính xong. Schema không có trường thứ năm hoặc status mới cho lỗi writer. |
| Rủi ro / giảm thiểu | Exception chaining hoặc logging mặc định có thể lộ input; nhiều lớp ghi có thể gây trùng. Public boundary chịu trách nhiệm điều phối và làm sạch lỗi, writer chỉ nhận allowlist. Không retry vô hạn, không tự coi lỗi ghi là có bản ghi, không thêm telemetry hoặc trường thứ năm. |
| Kiểm chứng dự kiến | Kiểm tra bốn đường ở phần 4, đặc biệt ba ca OPEN-03; loại lỗi validation khi audit thành công, lỗi audit công khai khi audit thất bại; không lộ input trong message/chaining, không trả kết quả thành công và không giả định record tồn tại sau lỗi ghi. Chưa có bằng chứng chạy. |
| Truy vết | Q FR-07, FR-09; NFR-02, NFR-03; A-04, A-06. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D08, Q §§4, 6 và L; OPEN-03 ngày 08/11/2026 là APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW. Tên exception audit cụ thể có thể hoàn thiện khi implement. |

### 5.6. D09 — Kiểm thử theo hành vi và ranh giới

**Đọc nhanh:** Kiểm tra ca thường, biên, thiếu, sai và giao nhau giữa các rule; test mẫu của starter chưa phải test nghiệp vụ.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Một số biểu thức gần giống nhau nhưng khác ngoặc, đường hít, số hệ hoặc dấu so sánh. Test mẫu chỉ mong đợi `NotImplementedError`, chưa kiểm tra nghiệp vụ. |
| Quyết định | Giữ các nhóm ca thường, biên, thiếu/null, sai, overlap, tuổi lẻ, output, audit và privacy. Thay/chỉnh test NotImplementedError của starter bằng test nghiệp vụ M2. Giữ tmp_path/fixtures/reset/file riêng và độc lập thứ tự. Expected D01–D03 theo TA; sáu expected D13-E tại §9.4 đã được Leader chốt policy. Bổ sung kiểm coverage, chọn mã, explanation và TA-EX-01–13. |
| Phương án khác | Chỉ dùng ca điển hình và một ví dụ cho mỗi nhãn nhanh hơn nhưng dễ bỏ qua sai dấu và dữ liệu thiếu. Chỉ đo tỷ lệ dòng code được chạy cũng chưa chứng minh các điều kiện rule được hiểu đúng. |
| Lý do lựa chọn | Nhóm ca bám yêu cầu A-07 và các đường rủi ro thực tế. Giá trị bằng ngưỡng thất bại nhánh so sánh nghiêm ngặt, nên các ca tại/sát biên cần được review, kể cả biên tuổi và giảm đúng 30%. |
| Hệ quả / đánh đổi | Dễ phát hiện lỗi nhỏ làm đổi kết quả, nhưng cần thời gian lập kỳ vọng và bảo trì dữ liệu synthetic. Kiểm tra helper hỗ trợ chẩn đoán lỗi, vẫn cần kiểm tra từ interface công khai. |
| Rủi ro / giảm thiểu | Không copy implementation thành oracle, giữ null expected cũ hoặc coi approval là PASS runtime. Bộ thiết kế ban đầu 157 ca đã được mở rộng lên 175 ca chính trong M1-02; 81 ca logic nội bộ vẫn là tập riêng. Hải/Việt Đức cần review kỹ thuật và mapping QA/AC/status, canonical reason và nguồn hiện hành. Leader đã phê duyệt policy; chưa có runtime verification. |
| Kiểm chứng dự kiến | Giữ public/core/audit/context/error/fixture coverage, 81 Enum/count rows. Kiểm raw normalization, Def/Poss/AllPV/Mixed, chọn rule ưu tiên cao nhất trong Poss và trường hợp rule definite cùng rule ưu tiên cao hơn chỉ possible, numeric crossovers và đủ six approved expected. Sau code cần pytest -q từ clean checkout với business tests và PR CI evidence riêng; không nghiệm thu từ số hàng tài liệu. |
| Truy vết | Q FR-01–FR-09; NFR-05, NFR-06; A-01–A-09. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D09, Q NFR-05, L; OPEN-06 ngày 08/11/2026 đã được chọn, PENDING PEER TECHNICAL REVIEW. E A-07–A-09, T dòng 9–17, W dòng 1–12 là căn cứ hiện trạng. Hải và Việt Đức review chéo fixture/đường lỗi. |

### 5.7. D10 — Benchmark toàn luồng và phép đo phụ logic thuần

**Đọc nhanh:** Đo thời gian của cả lần gọi công khai, bao gồm audit thật; phép đo logic thuần chỉ báo riêng để tham khảo.

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Phép đo chỉ một biểu thức rule có thể bỏ qua validation, explanation và audit. Số liệu như vậy không đại diện đường gọi nhóm định nghiệm thu. |
| Quyết định | Dùng time.perf_counter_ns(); chạy đúng 100 lượt warm-up, loại khỏi N ≥1.000 mẫu đo. Sắp mẫu tăng dần, nearest-rank lấy vị trí ceil(p×N) theo chỉ số từ 1; p50 dùng p=0,50 và p95 dùng p=0,95. Chia nanosecond cho 1.000.000 để ra millisecond. Phép đo chính bao gồm toàn bộ classify() công khai và open/write/close audit thật, không mock writer; báo phép đo logic thuần riêng. Công bố môi trường và giữ p95 <100 ms theo đề. Xem OPEN-09/10. |
| Phương án khác | Chỉ đo logic thuần giúp phân tích CPU nhưng bỏ qua I/O và điều phối. Chỉ báo thời gian trung bình che đuôi chậm và không đủ p50/p95 theo đề. |
| Lý do lựa chọn | Hai phép đo tách nhãn cho phép biết chi phí ở rule hay phần hỗ trợ, đồng thời giữ số liệu nghiệm thu gắn đường chạy thực tế. Warm-up và môi trường được khai báo giúp người khác tái lập phép đo. |
| Hệ quả / đánh đổi | Full-path phản ánh overhead và biến thiên I/O/máy. Nearest-rank dễ tái tính nhưng có bước nhảy theo mẫu; 100 warm-up cố định giúp protocol rõ. Công bố Python version, OS, CPU/hardware, số lượt warm-up/mẫu, dữ liệu synthetic và cấu hình I/O. Không tạo ngưỡng nghiệm thu mới. |
| Rủi ro / giảm thiểu | Bỏ chi phí open/close, dùng writer giả, chọn lọc mẫu hoặc sai chỉ số/đơn vị làm sai kết quả. Giữ toàn bộ public path, loại 100 warm-up, kiểm tra công thức độc lập. Protocol đã chốt; nếu tối ưu cần dữ liệu và review riêng, không tự thay semantics ghi. |
| Kiểm chứng dự kiến | Review instrumentation, timing boundary và nearest-rank trên tập mẫu kiểm tra có kết quả tính tay; chạy benchmark full-path thực với N ≥1.000, môi trường công bố, báo p50/p95. Protocol đã duyệt nhưng chưa thực đo; không có số liệu hoặc A-10 PASSED. |
| Truy vết | Q NFR-01; A-10. Phụ thuộc D05, D07, D08 và đường gọi FR-01/FR-09. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D10, Q NFR-01 và L; OPEN-09/10 được chốt ngày 08/11/2026, PENDING PEER TECHNICAL REVIEW. E A-10 là nguồn tối thiểu mẫu, p50/p95 và p95 <100 ms; 100 warm-up/nearest-rank là protocol nội bộ đã duyệt. |

### 5.8. D13-E — Xử lý boolean thiếu và chọn mã rule

**Vấn đề:** Khi một thông tin đúng/sai bị thiếu, từng rule có thể chưa xác định; tuy nhiên, có những trường hợp dù điền thông tin thiếu theo cách nào thì kết quả vẫn là phản vệ. Nhóm cần cách chọn mức và giải thích mã mà không tự coi giá trị thiếu là `False`.

| Thành phần ADR | Nội dung |
|---|---|
| Quyết định | Leader duyệt D13-E ngày 09/11/2026: missing/null boolean → `UNKNOWN`; giữ D04 với giá trị non-null sai. Sau Issue #31, Leader cập nhật cách chọn mã: nếu AllPV và chưa xác nhận sốc, chọn rule ưu tiên cao nhất trong Poss theo R01 > R02 > R03; nếu rule mang mã đó chưa chắc chắn, mã là CANONICAL và phải giải thích, kể cả khi rule ưu tiên thấp hơn đã chắc chắn. Mixed hoặc không khả năng nào khớp → `THEO_DOI / null` với lý do khác nhau. Đã chứng minh phản vệ và tụt HATT theo tuổi → `SOC_PHAN_VE / R-SOC`. Tuổi/HATT thiếu xử lý theo TA. |
| Các phương án khác đã cân nhắc | A: chỉ dùng Kleene và fallback có thể bỏ kết luận phản vệ đúng trong mọi khả năng. B: chọn một giá trị `False` đại diện dễ bị hiểu là tự điền dữ liệu. C: chọn rule có thể thỏa theo ưu tiên có rủi ro người đọc hiểu nhầm rule đã chắc chắn. D: `PHAN_VE / null` hợp kiểu nhưng không phải cách gắn mã nhóm chọn. Phương án E trước đây chọn definite trước possible; Leader đã thay phần chọn mã đó sau Issue #31. Không thay đổi Enum/toán tử hoặc kiến trúc khác. |
| Lý do lựa chọn | Giữ kết luận phản vệ khi mọi khả năng đều có ít nhất một rule thỏa; khi chọn mã `PHAN_VE`, áp dụng thứ tự ưu tiên R01 > R02 > R03 cho các rule có thể thỏa theo cách nhóm áp dụng Issue #31. Nếu mã được chọn chưa chắc chắn, giải thích rõ mã đại diện và có thể nêu thêm rule đã chắc chắn. Không tạo tiêu chí lâm sàng mới; R01/R02/R03 đều thuộc mức `PHAN_VE`. |
| Hệ quả / đánh đổi | Cần thêm kiểm thử coverage, chọn mã và giải thích. CANONICAL dùng cho `PHAN_VE` khi AllPV và rule được chọn chưa chắc chắn, kể cả nếu Def không rỗng; DIRECT/CANONICAL là nhãn nội bộ, không thêm trường hay status. Không tự điền input hoặc số đo. Thiếu tuổi vẫn `THEO_DOI / null`; thiếu HATT không xóa kết luận phản vệ đã chứng minh. |
| Rủi ro / giảm thiểu | Rule đại diện chỉ là possible; người chỉ đọc `rule_id` có thể hiểu là rule chắc chắn. Leader đã chấp nhận rủi ro, yêu cầu giải thích và kiểm tra không khẳng định sai. Mixed có thể chứa một khả năng phản vệ, nên không diễn đạt kết quả `THEO_DOI` là an toàn. |
| Kiểm chứng dự kiến | Rà 81 ca logic nội bộ; kiểm null/missing, Def/Poss/AllPV/Mixed, lời giải thích, thứ tự, nhiều UNKNOWN và tối đa 64 khả năng; kiểm cả thiếu tuổi/HATT. Sáu expected §9.4 là thiết kế đã duyệt. Phân tích độc lập 729 trạng thái/18 cấu hình số là bằng chứng thiết kế theo chính sách trước cập nhật; cần đối chiếu lại selector mới, không coi là runtime. Cần test nghiệp vụ, clean checkout/CI và benchmark audit thật. |
| Truy vết | Requirements FR-02–FR-08, NFR-04/05/07, A-01, A-03–A-05, A-07; Requirements §§3.2, 4.2, 5, 8.2. |
| Nguồn / trạng thái | D13-E được Huy Đức duyệt ngày 09/11/2026 trong TASK 02G sau khuyến nghị TASK 02F; sau Issue #31, Leader cập nhật cách chọn mã. Issue #15 làm rõ dữ liệu thiếu và phạm vi policy; Issue #31 nêu quy tắc mã đại diện và xác nhận trực tiếp ví dụ MISS-009. Cách nhóm áp dụng cho MISS-013/014 không được TA xác nhận riêng. Chưa có bằng chứng thực thi hoặc peer technical review đầy đủ. |

#### Quy tắc logic và các khả năng

`UNKNOWN` là trạng thái nội bộ chưa biết. Không dùng truthiness của Enum hoặc ép `UNKNOWN` thành `False`. Bảng dưới mô tả AND/OR/NOT theo logic ba trạng thái (Kleene), không tạo API hoặc test case mới:

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

Với điều kiện R02 “ít nhất 2 trong 4 hệ”, **T** là số hệ TRUE, **U** là số hệ UNKNOWN. `T ≥ 2` → TRUE; `T + U < 2` → FALSE; còn lại → UNKNOWN. Kết quả đếm vẫn phải kết hợp AND với `co_di_nguyen_nghi_ngo` theo Decision Table. [Q §4.2; L]

Với input hợp lệ `p`, `C(p)` là các cách xét True/False cho boolean chưa có, giữ nguyên giá trị đã biết. Có 1–64 cách; không hoàn thiện số đo và không ghi dữ liệu giả vào input. Các ký hiệu là nội bộ:

| Ký hiệu | Ý nghĩa |
|---|---|
| **Def** | Các rule TRUE trong mọi cách xét: rule chắc chắn. |
| **Poss** | Các rule TRUE trong ít nhất một cách xét: rule có thể thỏa. |
| **AllPV** | Mỗi cách xét đều có ít nhất một rule Tầng 2 thỏa. |
| **AnyPV** | Ít nhất một cách xét có rule Tầng 2 thỏa. |
| **Mixed** | Có cách xét thỏa và cách xét không thỏa: AnyPV đúng nhưng AllPV không đúng. |

Không dùng phép OR giữa các trạng thái UNKNOWN riêng lẻ để thay phép kiểm coverage trên các cách xét.

#### Thứ tự chọn kết quả và giải thích

1. Kiểm tra mọi trường; nếu tuổi missing/null thì chọn `THEO_DOI / null` và nêu thiếu tuổi, sau đó chuyển sang audit.
2. Khi có tuổi, xét các khả năng boolean chưa biết để xác định Def, Poss, AllPV và AnyPV. Nếu **AllPV**, đã chứng minh phản vệ dù có thể không rule riêng nào chắc chắn đúng.
3. Nếu AllPV và điều kiện tụt HATT theo tuổi là TRUE, chọn `SOC_PHAN_VE / R-SOC`. Chỉ có huyết áp thấp không đủ để kết luận sốc phản vệ.
4. Nếu AllPV nhưng chưa đủ bằng chứng sốc, chọn `PHAN_VE` và rule ưu tiên cao nhất trong **Poss** theo `R01 > R02 > R03`. Nếu rule được chọn thuộc Def, mã là **DIRECT**; nếu chưa chắc chắn, mã là **CANONICAL**, kể cả khi có một rule ưu tiên thấp hơn thuộc Def.
5. **Mixed** → chọn `THEO_DOI / null`, nêu thiếu thông tin; **không AnyPV** → cùng mức/mã nhưng nêu không khớp.
6. Với CANONICAL, `ly_do` phải nói mã là đại diện vì dữ liệu thiếu và rule chưa được xác nhận riêng; không khẳng định giá trị chưa biết đã được quan sát là False. DIRECT/CANONICAL không phải khóa output, mã rule hay audit status mới. Không chọn `PHAN_VE / null` theo policy này.

Các bước trên chọn kết quả; `classify()` phải hoàn tất audit SUCCESS trước khi trả kết quả hợp lệ. Lỗi validation/audit và thứ tự ưu tiên lỗi theo D08/OPEN-03. [Q §4.2–5; L]

**Làm rõ Issue #31:** GV nêu rằng khi các khả năng của khóa boolean thiếu cùng dẫn tới một mức nhưng khác rule, chọn mã ưu tiên cao nhất trong các rule có thể thỏa theo `R01-PV > R02-PV > R03-PV` và ghi lý do mã đại diện vì thiếu khóa. Với ví dụ nhóm hỏi tương ứng `MISS-009` (Def rỗng), GV xác nhận `PHAN_VE / R01-PV`. Phán quyết áp dụng chung Track A; GV yêu cầu ghi quy tắc trong ADR và có ít nhất một test cho ca thiếu khóa. [TA31]

#### 5.8.1. Trạng thái HATT và output theo TA/D13-E

Tuổi thiếu/null → `THEO_DOI / null`, kể cả AllPV. Nếu có tuổi, đã chứng minh phản vệ nhưng HATT hiện tại thiếu/null: chưa chứng minh sốc, giữ `PHAN_VE` với DIRECT hoặc CANONICAL phù hợp; không nói chắc chắn không có sốc. [TA §§2–3,5]

Người từ 18 tuổi: HATT hiện tại <90 **hoặc** giảm >30% so với nền. Nhánh giảm tương đương `current < 0.7 × baseline`; với hai số nguyên có thể so `10 × current < 7 × baseline`. Nhánh <90 đã đúng thì không cần nền; nếu current ≥90 mà thiếu nền thì nhánh giảm chưa xác nhận, không được coi là đã thỏa để xếp Tầng 1. Đúng 30% không đạt. Không ép mọi UNKNOWN thành FALSE, đổi ngưỡng/miền số hay tự suy số đo. [D; TA §4]

#### 5.8.2. Ví dụ chọn mức và mã khi thiếu boolean

Ký hiệu trong fixture: S = `co_di_nguyen_nghi_ngo`, I = `di_nguyen_qua_duong_hit`; K/H/C/G lần lượt là da/niêm mạc, hô hấp, tuần hoàn và tiêu hóa nặng. Cùng một trường S xuất hiện trong R01 và R02, nên khi xét từng khả năng phải dùng nhất quán cùng giá trị S cho cả hai rule; không giả định S vừa True vừa False.

Ví dụ `MISS-009`: tuổi 15, HATT 110; thiếu `co_di_nguyen_nghi_ngo`; da, hô hấp và đường hít TRUE; tuần hoàn và tiêu hóa nặng FALSE. Nếu trường thiếu là False thì R01 thỏa; nếu True thì R02 thỏa, R03 không thỏa. Từng helper R01/R02 vẫn UNKNOWN, nhưng AllPV và Def rỗng; kết quả `PHAN_VE / R01-PV` CANONICAL, giải thích đại diện R01/R02 và chưa xác nhận rule độc lập. Không sửa helper R01 thành TRUE hoặc nói dị nguyên=False đã được quan sát. [TA31; Q §5.1]

Với cùng dữ liệu boolean: đủ bằng chứng tụt HATT → `SOC_PHAN_VE / R-SOC`; thiếu HATT → `PHAN_VE` CANONICAL; thiếu tuổi → `THEO_DOI / null`. Với Mixed, ví dụ G hoặc I quyết định một rule có thỏa không, chọn `THEO_DOI / null` và giải thích thiếu thông tin.

**Ví dụ vừa có rule chắc chắn vừa có rule ưu tiên cao hơn có thể thỏa:** Với `MISS-013/014`, R03 chắc chắn và R02 có thể thỏa. Sau Issue #31, Leader chọn `PHAN_VE / R02-PV` CANONICAL; `ly_do` nói R02 là mã đại diện do dữ liệu thiếu và chưa được xác nhận riêng, có thể nêu thêm R03 đã chắc chắn đúng. Issue #31 nêu quy tắc chung và xác nhận trực tiếp MISS-009; thầy chưa xác nhận riêng hai fixture này. Bản test cases đang ghi expected cũ và cần đồng bộ. [TA31; L; Q §4.2]

Trong hai fixture này, trường còn thiếu lần lượt là hô hấp ở `MISS-013` và da/niêm mạc ở `MISS-014`; các trường khác giữ theo [Test Cases ghim tại commit `ee409e4`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/ee409e4c06187199fad671da1c5d273d6b1bfcc1/docs/m1-hai/M1/TEST_CASES.csv). Đây là mốc của fixture, trước cập nhật Requirements tại `45e0870`:

| Giá trị giả định của trường còn thiếu | Rule thỏa |
|---|---|
| `False` | R03 |
| `True` | R02 và R03 |

Vì R03 thỏa ở cả hai khả năng nên là rule chắc chắn; R02 chỉ có thể thỏa. Theo quyết định cập nhật, R02 ưu tiên cao hơn R03 nên được chọn làm mã đại diện; mức vẫn là `PHAN_VE`. Các expected R03-PV/DIRECT trong CSV tại mốc cũ là thiết kế trước cập nhật, chưa phải kết quả chạy. Các ca `TA15-BOOL3-NULL` và `TA15-BOOL3-MISSING` cùng cần rà expected và assertion khi đồng bộ.

Rủi ro mã đại diện bị hiểu nhầm là rule chắc chắn vẫn cần kiểm soát qua `ly_do` và negative assertions. Nhóm không thêm rule/ngưỡng; kết quả thiết kế và phản hồi thầy không thay cho kiểm thử thực tế hoặc peer review. Các thay đổi policy về sau cần được review và duyệt bởi người phụ trách.

## 6. Ràng buộc không được thay đổi — D11/D12

- **D11:** Không thêm, thay hoặc suy diễn quy tắc y khoa/ngưỡng ngoài `docs/decision-table.md`. Biên tuổi: `0–<1`, `1–<11`, `11–<18`, `≥18`; các so sánh HATT dùng dấu `<`, giảm tương đối người lớn phải **>30%**, đúng 30% không đủ. D04 là miền kiểm tra input, không thay điều kiện lâm sàng.
- **D12:** Không đổi chín tên input, ba khóa output và bốn trường audit. UUID là thông tin phiên synthetic **ngoài** `PatientInput`. Không log raw clinical input, PII hoặc secret; không đưa dữ liệu thực hay kết nối production. Ranh giới chi tiết nằm trong Requirements §§3–5.

## 7. Kết luận TA được áp dụng (Issue #15, 08/11/2026)

| ID | Kết luận được xác nhận | Bài test cần có |
|---|---|---|
| D01 | Nhiều rule Tầng 2 TRUE thì chọn R01 > R02 > R03; sốc được xác nhận thì dùng R-SOC | Overlap R02/R03, R01/khác, shock override |
| D02 | Tuổi thiếu hoặc null: `THEO_DOI/null`, nêu thiếu tuổi, không TypeError chỉ vì thiếu/null | Cặp missing/null tuổi; tuổi lẻ và ngưỡng |
| D03 | Có tuổi và đã chứng minh phản vệ: nếu thiếu HATT hiện tại, giữ `PHAN_VE`; nếu người lớn có HATT ≥90 nhưng thiếu nền, cũng giữ `PHAN_VE` vì chưa đánh giá được nhánh giảm >30%. Ở người lớn, HATT <90 đủ thỏa nhánh huyết áp tuyệt đối; kết luận `SOC_PHAN_VE / R-SOC` cần thêm điều kiện phản vệ. | Missing/null HATT/nền; HATT 89, 90; giảm đúng/trên 30%; đối chứng chỉ tụt HATT không đủ phản vệ |

**Issue #15 §§5–6:** Boolean missing/null không tự gây exception hay hạ mức khi một rule đã được chứng minh đủ; nhóm có thể công bố policy cho phần chưa định nghĩa nhưng không được đổi rule/ngưỡng/schema.

**Issue #31:** Thầy làm rõ quy tắc chọn mã đại diện khi thiếu khóa boolean; ví dụ nhóm hỏi cho `PHAN_VE / R01-PV`, lý do nêu đây là mã đại diện vì thiếu khóa. Phán quyết áp dụng chung Track A; ADR ghi quy tắc và nhóm cần ít nhất một test cho ca thiếu khóa. D13-E gồm cả quyết định nhóm; ví dụ rule definite cùng rule ưu tiên cao hơn chỉ possible được giải thích tại §5.8.2, không coi đã được thầy xác nhận riêng. [TA31]

Xem 13 ví dụ `TA-EX-01`–`TA-EX-13` trong [`REQUIREMENTS.md`](REQUIREMENTS.md) §5.1; các ví dụ là expected thiết kế, không phải kết quả chạy.

## 8. Các lựa chọn thiết kế chi tiết (OPEN-01–OPEN-10)

### 8.1. Trạng thái và bảng tóm tắt

Mười hướng OPEN được Leader lựa chọn ngày 08/11/2026; giữ mã OPEN-01–OPEN-10 để truy vết. Các hướng này đã được duyệt nội bộ nhưng vẫn cần **peer technical review** và bằng chứng triển khai, không phải TA phê duyệt. Người phụ trách và người review là phân công dự kiến, không chứng minh đã review.

TypeError/ValueError cho invalid thực sự, public orchestration, fail-closed và schema audit đã duyệt tiếp tục có hiệu lực. Các phương án khác trong §8.2–8.11 là những lựa chọn đã từng cân nhắc. D13-E được duyệt riêng và cách chọn mã đã được Leader cập nhật tại §5.8; OPEN-08 chỉ là lựa chọn biểu diễn, không tự phê duyệt chính sách chọn mã.

| Mã | Lựa chọn để đọc nhanh | Phụ trách | Review | Kiểm chứng dự kiến |
|---|---|---|---|---|
| OPEN-01 | ContextVar, set/reset bằng token ở ranh giới phiên ngoài input. | Hải | Việt Đức, Huy Đức | Scope/token, cách ly context. |
| OPEN-02 | Phiên tường minh dùng chung UUID; không có phiên thì tạo UUID tạm cho từng lần gọi, reset trong `finally`. | Hải | Việt Đức, Huy Đức | Cùng phiên, call riêng, reset khi lỗi. |
| OPEN-03 | Validation và audit cùng lỗi: ưu tiên lỗi audit an toàn ở public boundary. | Việt Đức | Hải, Huy Đức | Ba đường lỗi, message/chaining. |
| OPEN-04 | Cấu hình path ngoài input, dùng vùng dữ liệu sinh của lần chạy, độc lập cwd. | Việt Đức | Hải, Huy Đức | Path/cwd, thư mục riêng. |
| OPEN-05 | V1 ghi tuần tự; writer/file có chủ sở hữu theo lần chạy, không hứa concurrent an toàn. | Việt Đức | Hải, Huy Đức | File riêng, không hứa concurrent. |
| OPEN-06 | Test dùng `tmp_path`, dữ liệu/file riêng và reset context kể cả khi lỗi. | Việt Đức | Hải, Huy Đức | Teardown/order, writer thật và lỗi. |
| OPEN-07 | Số lượng helper vừa đủ; tách logic rule khỏi I/O và giữ public orchestration. | Hải | Việt Đức, Huy Đức | Ranh giới helper/core/public path. |
| OPEN-08 | Enum nội bộ TRUE/FALSE/UNKNOWN; so sánh tường minh, dùng AND/OR/NOT theo D13. | Hải | Việt Đức, Huy Đức | Bảng logic, R02 T/U, HATT. |
| OPEN-09 | Mỗi record open append/write/close bằng cơ chế quản lý tài nguyên. | Việt Đức | Hải, Huy Đức | Write/flush/close, timing thật. |
| OPEN-10 | `perf_counter_ns`; 100 warm-up; N≥1.000; nearest-rank p50/p95; full-path audit thật. | Việt Đức | Hải, Huy Đức | Chỉ số, đơn vị, protocol và thực đo. |

Đường dẫn audit **mặc định cụ thể khi gọi trực tiếp** ở §5.4.1 vẫn là đề xuất chờ review; không nhầm với nguyên tắc cấu hình path ngoài input đã chọn tại OPEN-04.

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
- **Kiểm chứng cần có:** Giữ AND/OR/NOT/R02 T-U; mapping missing/null→UNKNOWN đã duyệt D13-E; test chọn ưu tiên cao nhất trong Poss khi AllPV, trường hợp definite cùng possible ưu tiên cao hơn, Mixed, canonical explanation và age/BP. TA-EX-01–13/sáu expected §9.4; không field/output/status mới, không truthiness.
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

### 8.12. Thời điểm review và bằng chứng

Mười hướng OPEN đã chọn; trước code M2, Hải và Việt Đức cần peer review các ranh giới provider, public path, validation, audit và logic ba trạng thái. Nếu thấy xung đột nguồn hoặc thiết kế, báo Leader để quyết định; việc phân công không phải xác nhận review đã hoàn tất.

OPEN-10 đã chốt protocol trong M1; benchmark và bằng chứng đầy đủ có thể thực hiện M3. Coverage, clean-checkout và CI evidence tiếp tục theo kế hoạch nhóm. Concurrency mở rộng không tự trở thành nhiệm vụ M3 bắt buộc.

D01–D03 đã được TA làm rõ trong phạm vi Issue #15. D13-E có cập nhật chọn mã theo §5.8 và cần peer/test review khi triển khai. Default path vẫn chờ review theo §5.4.1; lỗi nội bộ bất ngờ còn cần review. Đây là mốc quản lý nội bộ, không tạo AC hoặc deadline mới. Tên helper, exception audit, path cụ thể hoặc UTC dùng `Z`/`+00:00` cần nhất quán khi code; không tự tạo vòng phê duyệt kiến trúc mới nếu giữ chính sách đã duyệt.

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

**Lưu ý:** Bảng truy vết này không tự chứng minh AC đạt. Riêng A-11 đã được đối chiếu trực tiếp bằng [disclaimer trong README tại commit `4482e4f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/README.md#L43). A-08/A-09 vẫn cần bằng chứng test/CI nghiệp vụ chạy thật; A-10 cần số liệu benchmark thật.

### 9.1. Những nhóm kiểm thử quan trọng

Ưu tiên các tình huống: (1) rule overlap và ngưỡng biên; (2) null/missing/invalid kiểu và khóa; (3) missing age/BP/nền; (4) Enum, T/U, AllPV/Mixed; khi AllPV, chọn mã ưu tiên cao nhất trong Poss, rồi kiểm DIRECT/CANONICAL theo việc rule mang mã có thuộc Def; (5) đúng `ly_do` và không tiết lộ dữ liệu; (6) explicit/single-call UUID, reset `finally` và context isolation; (7) writer open/write/flush/close thất bại, lỗi kép, path ngoài repo; (8) benchmark full-path. Các case cụ thể nằm ở `docs/m1-hai/M1/TEST_CASES.csv`, `docs/m1-hai/M2/INTERNAL_STATE_CASES.csv` và QA Matrix; không cần tái chép tất cả trong ADR.

### 9.2. Các ví dụ chính thức và giới hạn thẩm quyền

Xem `REQUIREMENTS.md` §5.1 cho `TA-EX-01`–`TA-EX-13`. Các expected 01–11 đối chiếu Issue #15; ca 12 phản ánh Mixed theo policy nhóm. Với ca 13, nhánh thiếu khóa tương ứng MISS-009 đã được thầy xác nhận mức/mã tại Issue #31; nhánh null tương ứng theo policy nhóm. Không coi thầy đã phê duyệt riêng mọi expected. Đầu vào thiếu/null hợp lệ, sau phân loại và audit thành công, dùng `SUCCESS`, không tự `INVALID_INPUT`.

Theo [Integration Test Plan ghim tại commit `ee409e4`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/ee409e4c06187199fad671da1c5d273d6b1bfcc1/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md), `INT-018` dự kiến kiểm mức/mã, helper và audit của MISS-009; `INT-021` dự kiến kiểm nội dung `ly_do`. Đây là thiết kế kiểm thử, chưa phải bằng chứng các test đã được thực thi.

### 9.3. Tình trạng tài liệu kiểm thử M1-02 và QA M1-03

- [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) đã tích hợp **175 ca thiết kế chính** (từ baseline 157 ca) và **81 ca logic nội bộ**; [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) đã tích hợp QA Matrix ánh xạ A-01–A-11. Đây là **test design**, chưa phải pytest thực thi.
- Bộ ca được đối chiếu tại mốc có **36 invalid** (28 TypeError, 8 ValueError), **8 ca nullable hợp lệ** `INV-001/017/021/025/029/033/037/043`; riêng `INV-043` kỳ vọng `SOC_PHAN_VE/R-SOC`. `AUD-002` nay dùng chuỗi `"true"` nên là TypeError/INVALID_INPUT nếu audit thành công. Các số lịch sử 35 invalid/9 nullable là bản fixture cũ.
- Hải là tác giả bản M1-02 gốc; Việt Đức là tác giả QA M1-03 gốc. Huy Đức phụ trách các bản sửa và tích hợp với công cụ AI hỗ trợ. Approval PR và tài liệu đã merge **không** chứng minh Hải/Việt Đức đã review kỹ thuật vòng cuối, hoặc CI/runtime đạt. Cần lưu review thực chất và bằng chứng chạy. Sau cập nhật chọn mã, cần rà và đồng bộ Test Plan, CSV, QA Matrix cùng các tài liệu phụ thuộc; trước mắt đã thấy `MISS-013`, `MISS-014`, `TA15-BOOL3-NULL` và `TA15-BOOL3-MISSING` còn expected `R03-PV`/DIRECT cũ, trong khi chính sách mới chọn `R02-PV`/CANONICAL.

**Những tài liệu cần đồng bộ theo selector mới** (chưa phải kết quả test):

- **Test Cases và Test Plan:** rà bốn ca `MISS-013`, `MISS-014`, `TA15-BOOL3-NULL`, `TA15-BOOL3-MISSING`; giữ mức `PHAN_VE`, đổi mã dự kiến từ `R03-PV` sang `R02-PV` và cập nhật assertion `ly_do` theo CANONICAL. Giữ input và kiểm chứng helper. `D13E-014` vẫn là ca đối chứng DIRECT.
- **Rule Design và kế hoạch M2:** rà selector trong `RULE_DESIGN.md` và public oracle trong `INTERNAL_STATE_TEST_PLAN.md`; giữ 81 ca helper nếu phép toán và expected helper không đổi. Giữ phạm vi `INT-018` cho MISS-009; rà và bổ sung bốn ca overlap vào kiểm `ly_do` của `INT-021`.
- **QA Matrix:** rà `QA-044/045`, `CHK-056`, mô tả selector ở `AC_MATRIX` và `QA-063`; giữ kết quả DIRECT của `D13E-014` và CANONICAL của `QA-020` khi fixture không đổi. Giữ trạng thái thực thi theo bằng chứng, không đánh dấu PASS chỉ vì sửa thiết kế.

A-11 đã được đối chiếu disclaimer tại commit README `4482e4f` (§9), còn dòng A-11 trong QA Matrix tại mốc này vẫn `NOT RUN` cho việc kiểm README ở SHA nghiệm thu. Cần đối chiếu phạm vi và cập nhật bằng chứng phù hợp khi đồng bộ, không tự coi hai trạng thái là một kết quả chạy.

### 9.4. Sáu expected D13-E đã được Leader phê duyệt — bàn giao TASK 02E

**Expected theo D13-E được Leader duyệt ngày 09/11/2026**, dựa trên fixture gốc của Hải. Với MISS-009 thiếu khóa, thầy xác nhận mức và mã tại Issue #31. CSV/QA đã tích hợp qua PR #3/#4; chưa có bằng chứng chạy engine hoặc peer technical review đầy đủ.

| Test ID | muc_do | rule_id | Attribution / explanation bắt buộc |
|---|---|---|---|
| MISS-009 | PHAN_VE | R01-PV | CANONICAL: AllPV qua R01/R02, Def rỗng; nêu mã đại diện và rule mang mã chưa được xác nhận riêng, không claim S=False/riêng R01 đã được xác nhận |
| TA15-BOOL1-NULL | PHAN_VE | R01-PV | CANONICAL như MISS-009; null tương đương missing; không chỉ generic reason |
| TA15-BOOL1-MISSING | PHAN_VE | R01-PV | CANONICAL như cặp null; không bắt UUID/reason nguyên văn bằng nhau |
| MISS-012 | THEO_DOI | null | Mixed do G unavailable; nêu chưa đủ thông tin, không nói G=False hoặc R02 chắc chắn FALSE |
| TA15-DEPENDENT_INHALATION-NULL | THEO_DOI | null | Mixed do I unavailable; không ép I hoặc kết luận an toàn |
| TA15-DEPENDENT_INHALATION-MISSING | THEO_DOI | null | Cùng fallback/uncertainty như cặp null |

SUCCESS chỉ khi thao tác phân loại hợp lệ và writer hoàn tất. Các dòng trên không tạo status audit mới. Ở `MISS-009`, helper R01/R02 vẫn UNKNOWN; chỉ output `rule_id` dùng mã CANONICAL theo D13-E. Không biến mã đại diện thành rule definite. Các expected do nhóm duyệt; riêng mức/mã của MISS-009 thiếu khóa đã được thầy xác nhận tại Issue #31. Không suy rộng thành TA duyệt toàn bộ sáu ca.

## 10. Rủi ro và việc còn chờ

| Hạng mục | Trạng thái / hành động kiểm chứng |
|---|---|
| **Mã đại diện D13-E** | Thầy làm rõ cách chọn mã trong Issue #31. Khi mã chỉ possible được chọn, người đọc có thể hiểu nhầm là rule chắc chắn; `ly_do` và negative tests phải phân biệt. Leader đã cập nhật cách chọn mã cho overlap definite/possible tại §5.8.2; cần đồng bộ ca thiết kế và review kỹ thuật. |
| **Default audit path** | Đề xuất §5.4.1 **chưa được duyệt**; review quyền truy cập, vị trí ngoài repo, tính độc lập cwd và hành vi fail-closed trước khi triển khai. |
| **Unexpected internal exception** | Chưa chốt cách audit/propagate khi helper lỗi trước ghi audit; không tự gán SUCCESS/INVALID_INPUT, thêm status hoặc log input; cần review Dev/QA. |
| **UUID/concurrency, writer failure** | Kiểm reset, không rò context và không hứa thread/process-safe; kiểm open/write/flush/close, lỗi kép và privacy. |
| **Kiểm thử/CI/benchmark** | Đã có [`pytest.ini`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/pytest.ini) theo Issue #16. Chưa có bằng chứng engine nghiệp vụ, pytest nghiệp vụ từ clean checkout, CI nghiệp vụ được kiểm chứng hay số liệu latency. |
| **Review của nhóm** | Leader tiếp tục hậu kiểm thủ công; Hải và Việt Đức đối chiếu core/audit/Test Plan/QA, ghi lại nhận xét thực tế trước các thay đổi tiếp theo. |

**Thực hiện sau M1:** Dev ưu tiên classifier + tests; QA phụ trách audit/privacy/CI/benchmark; Lead kiểm yêu cầu, đối chiếu Rule Design và nghiệm thu thực tế. Không tuyên bố pass chỉ từ tài liệu; các thay đổi policy phải được review và duyệt lại bởi người phụ trách. Không để AI tự merge/phát hành/xác nhận bài đạt.

## 11. Nguồn và lịch sử

| Nguồn | Liên kết / ý nghĩa |
|---|---|
| **E** | [Đề Hack Marathon chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung v1.0.2 |
| **D** | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), nguồn quy tắc/ngưỡng đã khóa |
| **TA** | [Phản hồi chung Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), D01–D03 và null/missing |
| **TA31** | [Phản hồi chung Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002), chọn mã đại diện khi thiếu khóa boolean; yêu cầu ghi ADR và có test |
| **Q** | [`REQUIREMENTS.md`](REQUIREMENTS.md) — FR/NFR/AC và 13 ví dụ đối chiếu; [bản tại mốc đối chiếu `45e0870`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/45e0870e0cae2c95b070c424e0de38e3c763bc9d/REQUIREMENTS.md) |
| **G/P** | [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md) / [`docs/TEAM_PLAN.md`](docs/TEAM_PLAN.md), phân công/bối cảnh nội bộ; snapshot lịch sử không ghi đè TA |
| **T** | [Test starter `tests/test_classifier.py` tại `45e0870`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/45e0870e0cae2c95b070c424e0de38e3c763bc9d/tests/test_classifier.py); chỉ là test stub, không chứng minh nghiệp vụ. |
| **W** | [Workflow `test.yml` tại `45e0870`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/45e0870e0cae2c95b070c424e0de38e3c763bc9d/.github/workflows/test.yml); cấu hình không thay bằng chứng lượt chạy. |
| **L** | Quyết định Leader, gồm [D13-E tại ADR trước cập nhật](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/45e0870e0cae2c95b070c424e0de38e3c763bc9d/DECISIONS.md#L178) và [cập nhật chọn mã trong Requirements §9](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/45e0870e0cae2c95b070c424e0de38e3c763bc9d/REQUIREMENTS.md#L376); phân biệt với phán quyết GV/TA. |
| **PY1** | [Python contextvars](https://docs.python.org/3.12/library/contextvars.html) |
| **PY2** | [pytest tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html) |
| **PY3** | [Python I/O](https://docs.python.org/3.12/library/io.html) |
| **PY4** | [perf_counter_ns](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns), dùng cho protocol benchmark |
| **PR** | [#1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [#2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [#3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [#4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4), merge ngày 10/11/2026; không phải TA nghiệm thu |

| Mốc | Thay đổi chính |
|---|---|
| 07–08/11, Draft/Revision 02 | Khởi tạo ADR, nhóm chọn 10 hướng OPEN; phần null/missing lúc đầu chờ phản hồi TA |
| 08/11, Revision 03 | Đồng bộ phản hồi TA về priority, tuổi/BP/boolean unavailable; cập nhật policy cũ |
| 09/11, Revision 04 | Leader duyệt D13-E, chấp nhận canonical residual risk; cập nhật expected và test design |
| 10–11/11, sau merge | PR #1–#4 tích hợp M1; biên tập gọn để rà soát thủ công, **không** thay đổi quyết định kỹ thuật hoặc giả định test đã đạt |
| 12/11, cập nhật cách trình bày | Diễn đạt lại ADR để dễ đọc, bổ sung nguồn Issue #31, đồng bộ A-11 và tình trạng `pytest.ini`; ghi nhận trạng thái tại thời điểm rà soát. |
| 13/11, cập nhật và rà soát tài liệu | Đồng bộ quyết định chọn rule ưu tiên cao nhất trong Poss, làm rõ D03 và thứ tự chọn kết quả; khôi phục mục 8.1/8.12, ghi nhận các nguồn test cần đồng bộ. Vẫn cần review kỹ thuật và bằng chứng thực thi. |

*Lưu ý tài liệu:* Chi tiết từng bước phê duyệt, các SHA trước merge và bản nội dung dài vẫn có thể truy vết qua lịch sử Git của `DECISIONS.md`; không xóa hoặc viết lại lịch sử đó.
