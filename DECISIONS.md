# Quyết định kiến trúc ban đầu — Track A

## 1. Thông tin tài liệu và trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Dự án | KTPMUD Hack Marathon 2026 — Track A, Dr May Day Rule Engine Sprint |
| Nhóm | `173820_n27` |
| Owner | Huy Đức, Leader, điều phối M1-04 |
| Technical Owner | Hải |
| QA / Traceability Owner | Việt Đức |
| Phiên bản | Draft 0.1 — Revision 03, đồng bộ làm rõ TA ngày 08/11/2026 |
| Cập nhật | 08/11/2026 |
| Trạng thái | Draft PR / Awaiting Peer Review — chưa có peer approval của Hải/Việt Đức |
| Mốc | M1 — Understand, Checkpoint 1 ngày 08/11/2026 |
| Nhánh làm việc | `docs/m1-decisions-huy` |
| HEAD nền tích hợp | `b65032f94ec3ce600df07d81b5df6b9b4bd203d1` trên `track-a-development` |
| Starter khóa | Tag `bkt-2026-v1`, commit `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Requirements tham chiếu | [Revision 03 trên PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/c855c6d4f2135a14ad94485734d4d2e604cb9cff/REQUIREMENTS.md), commit `c855c6d4f2135a14ad94485734d4d2e604cb9cff` đã push và xác minh; PR vẫn Open/Draft, chưa merge |
| Làm rõ TA chính thức | [fossbk-spec — Issue #15 comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), 08/11/2026, áp dụng chung Track A |
| Trạng thái nguồn khi kiểm tra | TASK 02C.6 ngày 08/11/2026: PR #1 đã nhận Revision 03, PR #2 Open/Draft chưa merge; chưa có peer approval tại preflight. Issue #15 có câu hỏi nhóm và phản hồi chính thức fossbk-spec; D01–D03 đã được trả lời. |

ADR ghi vấn đề, lựa chọn, lý do, đánh đổi và bằng chứng cần thu. Nguồn hiện hành theo thứ tự: Decision Table V1 + làm rõ TA [TA] > quyết định nội bộ đã duyệt > đề xuất. TA thay thế các policy cũ trái lời làm rõ; không phê duyệt toàn bộ kiến trúc nhóm. Tám ADR và mười lựa chọn OPEN giữ phần không bị thay thế, còn peer technical review. Chưa có implementation/test/benchmark evidence hoặc nghiệm thu AC.

**PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION:** extension D13 cho boolean missing/null → UNKNOWN, đặc biệt explicit null, và áp dụng cho trường hợp kết quả phụ thuộc unavailable. Quy định TA bắt buộc không raise chỉ vì boolean missing/null đã có hiệu lực; Enum/toán tử là lựa chọn nhóm đã duyệt, còn extension null là đề xuất; TA không chỉ định công nghệ đó.


| Nhãn | Ý nghĩa |
|---|---|
| FACT / SPECIFIED | Yêu cầu chính thức hoặc hiện trạng có nguồn kiểm tra |
| APPROVED BY LEAD | Hướng thiết kế nội bộ đã được Leader phê duyệt |
| TA CONFIRMED | Hành vi chính thức đã được fossbk-spec làm rõ; D01–D03 trong phạm vi trả lời đã được xác nhận |
| APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Leader đã chọn hướng; Hải/Việt Đức còn review khả thi, xung đột và rủi ro |
| OPEN-01–OPEN-10 | Mã theo dõi được giữ từ Revision 01; không còn biểu thị phương án chưa được chọn |
| Chi tiết triển khai nhỏ | Tên helper/exception/path thực tế sẽ hoàn thiện khi triển khai, trong approved policy |

Ký hiệu nguồn E, D, TA, Q, Q2, Q0, G, P, C, T, W, R, I, L ở phần 11. Q là Requirements Revision 03 đã đọc lại từ GitHub tại c855c6d4f2135a14ad94485734d4d2e604cb9cff; Q2/Q0 là snapshot lịch sử. Mã FR/NFR/AC giữ nguyên. Dùng URL theo commit cho tài liệu ở hai nhánh PR độc lập. Các câu D01–D03 từng pending hoặc null từng invalid chỉ còn có nghĩa lịch sử trước phản hồi TA.

## 2. Bối cảnh và vấn đề thiết kế

Theo thông tin Leader cung cấp, Dr May Day có định hướng thử nghiệm và ứng dụng thực tế trong bối cảnh phát triển rộng hơn. Bài thi giao một Rule Engine Python độc lập dùng dữ liệu synthetic. Module bài thi chưa có bằng chứng kiểm định lâm sàng hoặc triển khai production. Contract kỹ thuật được khóa bằng Decision Table V1. [Q §§1–2; L; D dòng 57–62]

Ba vấn đề chính cần giải quyết là giữ đúng phép suy luận, giải thích được kết quả và truy vết thao tác mà không lộ dữ liệu. Việc thiếu dữ liệu làm tăng nguy cơ kết luận quá mức. Vì vậy, kiến trúc cần ranh giới rõ giữa kiểm tra input, đánh giá điều kiện và lựa chọn output. Audit còn tạo thêm I/O và một đường lỗi cần được thiết kế. [D dòng 8–55; E §7; Q FR-01–FR-09]

| Ràng buộc | Căn cứ |
|---|---|
| Giữ `classify(patient)`, chín tên khóa input và ba khóa output | C dòng 11–30; D dòng 8–23, 49–55 |
| Giữ R01/R02/R03, điều kiện R-SOC và ưu tiên Tầng 1 | D dòng 25–47 |
| Giữ các biên tuổi 0–<1, 1–<11, 11–<18, ≥18, dấu HATT < và mức giảm >30% | D dòng 30–35 |
| Audit đúng `Timestamp`, `User_UUID`, `Action_Type`, `Status`, không input lâm sàng thô | E §§7.2–7.3 A-06 |
| Dữ liệu synthetic, bảo vệ PII/secret, không tích hợp production hoặc đưa lời khuyên điều trị | E §§5, 7.4; D dòng 22–23; Q NFR-02 |
| Test, clean checkout, PR CI và benchmark là các nghĩa vụ có bằng chứng riêng | E §7.3 A-07–A-10 |
| Requirements, ADR, hồ sơ test, privacy, AI-use và đóng góp thuộc bộ bàn giao | E §§6, 11 |

M1 tập trung phân tích và thiết kế. Theo E §4, M2 là 09–15/11, M3 là 16–19/11, freeze lúc 23:59 ngày 19/11, nộp ngày 20/11 và demo/viva ngày 21/11. E §9 dành 18 điểm cho kiến trúc và quyết định thiết kế trong 80 điểm core, Track A có thêm 20 điểm cho đúng bảng, giải thích/audit và benchmark. Các mốc và rubric giải thích nhu cầu lập luận có kiểm chứng, không tạo thêm tính năng.

## 3. Danh mục quyết định

| ID | Quyết định hoặc câu hỏi | Trạng thái | Nhóm vấn đề | FR/NFR/AC liên quan |
|---|---|---|---|---|
| D01 | Chọn R01-PV > R02-PV > R03-PV khi nhiều rule TRUE; sốc xác nhận ưu tiên R-SOC [TA §1](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) | TA CONFIRMED — R01 > R02 > R03 | Ưu tiên trong Tầng 2 | FR-03, FR-04, FR-06, FR-08; A-01, A-05, A-07 |
| D02 | Tuổi missing/null → THEO_DOI / null, nêu thiếu tuổi [TA §§2,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) | TA CONFIRMED — missing/null age leads to THEO_DOI with null rule_id | Dữ liệu thiếu | FR-05–FR-07; A-01, A-04, A-07 |
| D03 | Tuổi có, Tầng 2 TRUE: current BP missing/null hoặc thiếu nền người lớn không chặn PHAN_VE; HATT <90 có thể xác nhận sốc không cần nền [TA §§3–5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) | TA CONFIRMED — missing/null current BP or unavailable adult baseline does not suppress confirmed Tier 2 classification | Khả năng kết luận sốc | FR-05–FR-07; A-01, A-04, A-07 |
| D04 | Strict TypeError cho non-null sai kiểu, ValueError cho sai miền/khóa thừa; null tuổi/boolean không còn invalid chỉ vì null | APPROVED BY LEAD — PARTIALLY SUPERSEDED BY TA | Chất lượng input và lỗi | FR-07; NFR-02, NFR-03; A-04, A-07 |
| D05 | Thiết kế tối giản, public classify() điều phối audit; ít helper theo trách nhiệm | APPROVED BY LEAD | Phân chia trách nhiệm | FR-01–FR-09; NFR-04, NFR-05; A-01, A-02 |
| D06 | Explanation tất định theo rule/kết quả và lý do thiếu tuổi/HATT/nền theo TA | APPROVED BY LEAD + TA | Khả năng giải thích | FR-08; NFR-07; A-05 |
| D07 | Writer JSONL riêng; ContextVar, phiên tường minh/UUID tạm một lời gọi; path cấu hình ngoài input; ghi tuần tự | APPROVED BY LEAD | Audit và riêng tư | FR-09; NFR-02, NFR-03; A-06 |
| D08 | CLASSIFY, SUCCESS/INVALID_INPUT; fail-closed, ưu tiên lỗi audit khi lỗi kép; hoàn tất ghi trước trả kết quả | APPROVED BY LEAD | Truy vết và bảo vệ dữ liệu | FR-07, FR-09; NFR-03; A-04, A-06 |
| D09 | Test nghiệp vụ thay stub; tmp_path/fixture reset context; kiểm chứng cả core, audit và D13 | APPROVED BY LEAD | Kiểm chứng | FR-01–FR-09; NFR-05, NFR-06; A-01–A-09 |
| D10 | perf_counter_ns(); warm-up 100; ≥1.000 mẫu; nearest-rank p50/p95; full-path với open/write/close audit thực | APPROVED BY LEAD | Hiệu năng | NFR-01; A-10 |
| D11 | Giữ clinical rules/ngưỡng theo bảng đã khóa | FACT / SPECIFIED | Giới hạn nghiệp vụ | FR-02–FR-06; A-01, A-03 |
| D12 | Giữ schema input/output/audit và giới hạn privacy | FACT / SPECIFIED | Contract và an toàn | FR-01, FR-07–FR-09; NFR-02, NFR-03, NFR-08; A-04–A-06, A-11 |
| D13 | Enum, toán tử/T-U giữ nguyên; extension missing/null boolean → UNKNOWN cần Leader xác nhận | APPROVED CORE; NULL EXTENSION PROPOSED | Input một phần | FR-02–FR-08; NFR-04, NFR-05; A-01, A-03–A-05, A-07 |

Nguồn trạng thái gồm D + TA, Q và L; G/P là snapshot lịch sử/phân công. D01–D03 đã TA CONFIRMED; D04/D13 được thay thế một phần như §5.1/§5.8. Mười OPEN vẫn là lựa chọn đã duyệt, không thêm D14–D23. D11–D12 là FACT / SPECIFIED. Không coi làm rõ TA hoặc publish tài liệu là bằng chứng triển khai.

## 4. Tổng quan kiến trúc Revision 03 — chưa triển khai

Public classify(patient) giữ trách nhiệm validation, rule evaluation, lựa chọn classification/explanation và audit kể cả direct call. Logic rule tách file I/O, writer riêng; không thay signature hoặc thêm input. Cập nhật TA nằm ở phân biệt unavailable/invalid và lựa chọn kết quả, không viết lại audit architecture. [TA; Q FR-01–FR-09; L]

```text
Provider ngoài input: explicit session hoặc UUID tạm một call, reset an toàn
classify(patient)
  -> validate mọi trường: unavailable được phép khác invalid thực sự
     + invalid thực sự -> audit INVALID_INPUT -> TypeError/ValueError
     + valid -> tuổi missing/null? -> THEO_DOI / null, nêu thiếu tuổi
             -> tuổi có -> đánh giá R01/R02/R03 và bằng chứng sốc
                 + Tầng 2 TRUE và điều kiện HATT sốc TRUE -> SOC_PHAN_VE / R-SOC
                 + rule Tầng 2 TRUE, chưa xác nhận sốc -> PHAN_VE
                     chọn một rule TRUE: R01 > R02 > R03
                 + mọi rule FALSE -> THEO_DOI / null
                 + phụ thuộc boolean unavailable -> policy D13 đề xuất ở §5.8
  -> audit SUCCESS cho kết quả phân loại hợp lệ, rồi return ba trường
Mọi audit failure -> lỗi vận hành audit an toàn; không return thành công
```

Nhánh policy đề xuất là ghi chú thiết kế để Leader review, không là return/exception runtime mới. Không chặn các kết quả TA đã xác định chỉ vì extension còn chờ xác nhận. Một field invalid khác vẫn bị validation phát hiện trước khi chọn kết quả.

**Vòng đời UUID.** Phiên tường minh được mở/kết thúc ngoài input; nhiều call trong cùng scope dùng một UUID synthetic hợp lệ. Nếu không có scope, mỗi call độc lập là một phiên đơn thao tác, có UUID tạm mới; reset bằng token trong `finally` cả khi validation hoặc audit lỗi. Hai call độc lập không dùng lại UUID tạm. Cách này tránh gắn nhầm thao tác của các phiên khác nhau; UUID không phải định danh bệnh nhân hoặc danh tính thật. ContextVar không tự quản lý toàn bộ vòng đời phiên hay bảo đảm ghi file đồng thời. [L OPEN-01–OPEN-02; PY1]

| Đường xử lý dự kiến | Nghĩa vụ audit | Kết quả công khai |
|---|---|---|
| Valid, phân loại hoàn tất gồm dữ liệu unavailable được TA cho phép | Hoàn tất CLASSIFY/SUCCESS | Return ba trường theo TA; không INVALID_INPUT chỉ vì missing/null |
| Validation lỗi thực sự, audit thành công | Có CLASSIFY/INVALID_INPUT | TypeError/ValueError đúng D04, không giả THEO_DOI |
| Validation thành công, audit thất bại | Không mặc định record đã lưu | Lỗi audit an toàn, không return thành công |
| Validation và audit cùng thất bại | Không giả định INVALID_INPUT tồn tại | Ưu tiên lỗi audit, không lộ input qua message/chaining |

Giữ fail-closed cho module synthetic, open append/write/close mỗi record, nhận biết write/flush/close failure trước khi báo hoàn tất. Không retry vô hạn hoặc thêm status/schema. Tuổi missing/null có quy tắc riêng THEO_DOI; tuổi có nhưng HATT hiện tại/nền unavailable chỉ làm chưa đủ bằng chứng sốc, không ngăn Tầng 2 đã xác nhận. [TA §§2–5; D07/D08]

| Trách nhiệm | Hiện có tại baseline | Hướng cần triển khai/kiểm chứng |
|---|---|---|
| Interface | PatientInput, ClassificationResult, classify(patient) | Giữ 9 input / 3 output |
| Validation | TypedDict, chưa validation runtime | D04 đã cập nhật null/missing theo TA |
| Rule/ưu tiên | Stub NotImplementedError | Biểu thức gốc, priority TA; Enum/T-U đã duyệt |
| Explanation | Khai báo ba trường | Nêu rule, thiếu tuổi/BP/nền; không raw input/điều trị |
| Audit | Chưa có | ContextVar, hai scope UUID, writer JSONL, tuần tự/fail-closed giữ nguyên |
| Test/CI | Stub test và workflow | Thay/chỉnh stub, cập nhật expected/QA theo TA; chưa có bằng chứng nghiệp vụ |
| Benchmark | Mục tiêu README | Protocol đã duyệt, chưa có số liệu |

Hiện trạng theo C/T/W/R không đổi do patch tài liệu. Tên helper/exception audit, path thực tế là chi tiết triển khai; default path vẫn đề xuất và unexpected internal exception vẫn residual review item.

## 5. Các ADR cho hướng thiết kế đã được duyệt

Các phương án thay thế và lập luận dưới đây là phân tích kiến trúc trong bản nháp này. Hướng lựa chọn đã được Leader duyệt qua nguồn ghi ở mỗi ADR, còn lập luận và chi tiết triển khai vẫn chờ human review.

### 5.1. D04 — Validation input nghiêm ngặt

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Sai kiểu và unavailable khác nhau. Ép kiểu có thể biến dữ liệu chưa xác nhận thành bằng chứng. TA cho phép null/thiếu ở tuổi, HATT và boolean; không được giữ validation cũ loại null tuổi/boolean. TypedDict chưa validation runtime. |
| Quyết định | Giữ tuổi int/float hữu hạn ≥0, cho số lẻ, loại bool; current BP int ≥0; baseline int >0; HATT loại bool/float/chuỗi. Missing/null ở cả ba số là unavailable. Sáu boolean: True/False hợp lệ; missing/null không tự gây lỗi theo TA, extension → UNKNOWN mang nhãn PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION. Non-null sai kiểu → TypeError, sai miền/khóa thừa → ValueError; kiểm tra mọi trường, không ép kiểu hoặc đổi invalid thành UNKNOWN/THEO_DOI. Invalid thực sự vẫn audit D08. |
| Phương án khác | Tự chuyển chuỗi/số thành kiểu mong muốn để nhận được nhiều dạng dữ liệu hơn. Phương án này giảm lỗi tích hợp ban đầu nhưng cần quy ước diễn giải và có thể che lỗi bên gọi. |
| Lý do lựa chọn | Đầu vào nhỏ, cố định và giả lập cho phép yêu cầu bên gọi cung cấp đúng kiểu. Validation nghiêm giúp tìm lỗi sớm và giữ bằng chứng phân loại theo dữ liệu thực nhận. Các miền số là policy dữ liệu của nhóm, tách khỏi ngưỡng lâm sàng trong D. |
| Hệ quả / đánh đổi | Giữ kiểm tra số hữu hạn, loại bool khỏi miền số và phân biệt unavailable với invalid thực sự. Tuổi missing/null có output TA quy định; thiếu current BP/nền không tự hạ Tầng 2 đã xác nhận. Không tự đổi current BP=0 thành invalid; baseline=0 vẫn ValueError theo policy số đã duyệt. |
| Rủi ro / giảm thiểu | Validator cũ có thể nhận bool như số hoặc còn loại age/boolean null. Kiểm tra toàn bộ input, không bỏ qua field invalid không liên quan dù đã chứng minh rule; giữ message/chaining không chứa giá trị lâm sàng thô. Không gán INVALID_INPUT chỉ vì missing/null được phép. |
| Kiểm chứng dự kiến | Test riêng missing/null/non-null sai kiểu, miền số, tuổi lẻ, khóa thừa, unrelated invalid và privacy. Tính lại chín ca null cũ trong Q §8.1; 35 invalid còn lại giữ mapping TypeError/ValueError. Invalid + audit thành công mới INVALID_INPUT/lỗi validation; lỗi kép ưu tiên audit theo OPEN-03. Chưa có test runtime evidence. |
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
| Quyết định | Dùng template tất định theo rule/kết quả. Tuổi missing/null: nêu thiếu tuổi nên chưa chọn được ngưỡng sốc. Current BP unavailable: nêu chưa xác nhận sốc, vẫn nêu rule Tầng 2 đã chứng minh. Người lớn thiếu nền: nêu chưa đánh giá được giảm >30% khi cần nhánh tương đối. Không raw input/điều trị hoặc LLM cho classification/explanation. |
| Phương án khác | Ghép câu từ toàn bộ triệu chứng và số đo tạo nhiều chi tiết nhưng tăng nguy cơ rò dữ liệu. Sinh câu linh hoạt làm tăng độ biến thiên và khó kiểm chứng nội dung đúng giới hạn. |
| Lý do lựa chọn | Bộ mã rule nhỏ, output cố định và dữ liệu synthetic đủ để dùng template. Reviewer đối chiếu được mã rule với câu giải thích mà không cần tái tạo dữ liệu input trong output. |
| Hệ quả / đánh đổi | Template ổn định và dễ đối chiếu một rule_id. D01 đã có priority chính thức R01 > R02 > R03; trường hợp overlap có thể nêu thêm rule khớp trong ly_do nhưng không thêm mã output. Cần phân biệt thiếu tuổi, thiếu current BP và thiếu baseline. |
| Rủi ro / giảm thiểu | Không diễn đạt THEO_DOI thành an toàn, hoặc chưa xác nhận sốc thành bằng chứng không có sốc. Nêu lý do unavailable theo TA, không suy số đo hay lộ input qua explanation/lỗi. D01–D03 không còn phụ thuộc phản hồi TA cho ca đã trả lời. |
| Kiểm chứng dự kiến | Ba khóa output, một rule_id đúng priority, nội dung ly_do phù hợp TA-EX-01–12, không raw input/điều trị. Kiểm tra reason riêng tuổi/current BP/baseline unavailable. Chưa có output nghiệp vụ đã chạy. |
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
| Quyết định | Giữ nhóm normal/boundary/missing/invalid/overlap/tuổi lẻ/output/audit privacy/D13. Thay/chỉnh test stub NotImplementedError bằng test nghiệp vụ M2; tmp_path và fixture reset context kể cả lỗi, file riêng/độc lập thứ tự. D01–D03 dùng expected TA đã xác nhận, bao phủ TA-EX-01–12. Trường hợp boolean phụ thuộc unavailable theo extension đề xuất phải được Leader xác nhận trước khi đóng expected. |
| Phương án khác | Chỉ dùng ca điển hình và một ví dụ cho mỗi nhãn nhanh hơn nhưng dễ bỏ qua sai dấu và dữ liệu thiếu. Chỉ đo tỷ lệ dòng code được chạy cũng chưa chứng minh các điều kiện rule được hiểu đúng. |
| Lý do lựa chọn | Nhóm ca bám yêu cầu A-07 và các đường rủi ro thực tế. Giá trị bằng ngưỡng thất bại nhánh so sánh nghiêm ngặt, nên các ca tại/sát biên cần được review, kể cả biên tuổi và giảm đúng 30%. |
| Hệ quả / đánh đổi | Dễ phát hiện lỗi nhỏ làm đổi kết quả, nhưng cần thời gian lập kỳ vọng và bảo trì dữ liệu synthetic. Kiểm tra helper hỗ trợ chẩn đoán lỗi, vẫn cần kiểm tra từ interface công khai. |
| Rủi ro / giảm thiểu | Không sao chép công thức lỗi từ implementation, giữ expected cũ cho null hoặc tự gán nhóm pending thành PASS. Hải cập nhật 135-case plan theo D + TA; Việt Đức review QA/AC và audit SUCCESS/INVALID_INPUT. Leader chỉ duyệt policy nhóm còn đề xuất, không duyệt lại kết luận TA. |
| Kiểm chứng dự kiến | Giữ public/core/audit/context/fixture/error-precedence coverage, Enum AND/OR/NOT và R02 T/U. Q §8.1 chỉ rõ bảy PEND đã có đáp án, chín null cũ cần rời invalid, 35 invalid còn lại cần giữ strict mapping. Sau code cần pytest -q từ clean checkout với business tests và PR CI evidence riêng; chưa có bằng chứng đạt. |
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

### 5.8. D13 — Đánh giá input một phần với logic ba trạng thái

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Missing/null boolean không tự gây exception theo TA. Một rule được chứng minh bằng dữ liệu hiện có không được hạ mức chỉ vì boolean khác unavailable; riêng tuổi missing/null theo TA vẫn THEO_DOI. S=co_di_nguyen_nghi_ngo xuất hiện cả dương và âm trong các rule, cần review tương quan khi S UNKNOWN. |
| Quyết định | Giữ Enum nội bộ TRUE/FALSE/UNKNOWN, AND/OR/NOT tường minh và R02 T/U đã duyệt; không Python truthiness. True→TRUE, False→FALSE. Mapping missing→UNKNOWN đã có trước; extension kết hợp missing/null→UNKNOWN, đặc biệt explicit null, là PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION. Bỏ quy tắc cũ null boolean invalid theo TA; non-null sai kiểu vẫn D04. Không thêm field/nhãn hoặc thay biểu thức. |
| Phương án khác | Mặc định missing/null=False có thể tạo bằng chứng âm, sai rule hoặc hạ mức đã chứng minh; bắt đủ sáu khóa hoặc reject null trái TA. Không mở lại Enum/toán tử đã duyệt. Chi tiết mapping explicit null và fallback ca output-dependent là đề xuất tối thiểu để Leader review, không phải duy nhất được TA chỉ định. |
| Lý do lựa chọn | UNKNOWN giữ khác biệt chưa biết với FALSE. TRUE OR UNKNOWN vẫn TRUE nên không chặn rule độc lập đã chứng minh. Enum/Kleene/T-U là thiết kế nội bộ đã duyệt; TA chỉ quy định hành vi và quyền công bố policy, không yêu cầu công nghệ hay xác nhận mapping này là duy nhất. |
| Hệ quả / đánh đổi | Giữ biểu thức và cấu trúc helper, cần mở rộng null cases thay invalid expectations cũ. Kết quả TA đã rõ phải áp dụng ngay; phần output phụ thuộc boolean unavailable cần policy nhóm công bố/test được và Leader xác nhận. Không dùng đề xuất còn chờ để giữ các expected trái TA. |
| Rủi ro / giảm thiểu | UNKNOWN bị ép False, làm mất rule; hoặc chỉ nhìn từng rule Kleene mà bỏ tương quan S giữa NOT S ở R01 và S ở R02. Phân tích ví dụ §5.8.2, không chốt output mơ hồ thành quy tắc mới. Không suy không có sốc chỉ từ tuổi/HATT thiếu; lựa chọn nhãn theo TA khác trạng thái điều kiện nội bộ. |
| Kiểm chứng dự kiến | Bảng AND/OR/NOT và R02 T/U giữ nguyên, không truthiness; missing/null tương đương theo mapping đề xuất; non-null sai kiểu vẫn lỗi. TA-EX-10/11 giữ rule chắc chắn; TA-EX-12 và S-correlation cần Leader review policy trước khi đóng expected. Tuổi/BP unavailable có test TA-EX-02–09, không còn TA-pending. Chưa triển khai. |
| Truy vết | Q FR-02–FR-08; NFR-04, NFR-05, NFR-07; A-01, A-03–A-05, A-07. |
| Nguồn / trạng thái | APPROVED CORE: Enum/toán tử/R02 T-U và OPEN-08 theo L. TA §§2–5 thay null-invalid và quyết định D01–D03. Extension explicit null→UNKNOWN / policy ca phụ thuộc unavailable: PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION. [TA](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248); Q §§3.2, 4.2–4.3, 9. |

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

TRUE xác nhận rule khớp, FALSE xác nhận không khớp, UNKNOWN giữ chưa đủ thông tin. Rule chắc chắn TRUE vẫn TRUE dù boolean không liên quan UNKNOWN. Với tuổi có và chưa đủ bằng chứng sốc, rule Tầng 2 TRUE cho PHAN_VE, chọn R01 > R02 > R03; sốc đã xác nhận ưu tiên SOC_PHAN_VE/R-SOC. Tuổi missing/null theo TA là THEO_DOI/null dù Tầng 2 TRUE. Các trường hợp mọi rule FALSE cho THEO_DOI/null; fallback THEO_DOI/null khi còn rule UNKNOWN và không rule TRUE thuộc extension policy đề xuất, phải phân biệt thiếu thông tin với không khớp. [TA §§1–5; Q §§4.2, 5.1]

#### 5.8.1. Trạng thái nội bộ của điều kiện huyết áp và lựa chọn output

TRUE/FALSE/UNKNOWN dùng cho kết quả điều kiện; raw missing/null không phải Enum và không đổi schema. Thiếu tuổi chưa chọn được ngưỡng; TA quy định output THEO_DOI/null, không phải TypeError. Tuổi có, thiếu current BP thì chưa chứng minh sốc; Tầng 2 TRUE vẫn PHAN_VE/selected rule. Không diễn đạt chưa xác nhận sốc thành chắc chắn không sốc. [TA §§2–3,5; Q FR-05–FR-08]

Ở người ≥18 tuổi, giữ HATT <90 HOẶC giảm >30%, tức current <0.7×baseline. Nhánh tuyệt đối TRUE đủ chứng minh dù thiếu nền; khi Tầng 2 TRUE thì SOC_PHAN_VE/R-SOC. Nếu current ≥90 và thiếu nền, nhánh tương đối chưa xác nhận, trạng thái đánh giá nội bộ có thể UNKNOWN; theo TA xem nhánh này chưa thỏa để chọn Tầng 1, không chặn PHAN_VE đã chứng minh. Không đổi mọi UNKNOWN thành FALSE. Giảm đúng 30% không đạt. [D dòng 35; TA §4; Q §§4,5.1]

#### 5.8.2. Rủi ro tương quan của co_di_nguyen_nghi_ngo

S là co_di_nguyen_nghi_ngo, K/H/C/G lần lượt là da-niêm mạc/hô hấp/tim mạch/tiêu hóa, I là sau_tiep_xuc_di_nguyen_trong_2_gio. Ví dụ tuổi 15, HATT 110, S unavailable, K=H=I=TRUE, C=G=FALSE: đánh giá Kleene từng rule cho R01=UNKNOWN, R02=UNKNOWN, R03=FALSE. Nếu S=FALSE, R01 TRUE; nếu S=TRUE, R02 TRUE. Như vậy cả hai hoàn thiện dữ liệu đều có thể PHAN_VE nhưng rule_id khác nhau. Mặc định S=FALSE có thể gán sai rule; fallback THEO_DOI máy móc có thể hạ mức so với kết quả chung của hai hoàn thiện. [D dòng 41–43; TA §5; Q §4.2]

Đây là rủi ro cần Hải/Việt Đức phản biện khi Leader xem extension, không phải một rule lâm sàng, nhãn output mới hay đáp án do TA chỉ định riêng. Không tự chọn rule_id hoặc thuật toán bổ sung cho ví dụ này trong patch. PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION; công bố rõ policy output-dependent sau khi Leader xác nhận và bổ sung test, không tạo một câu hỏi TA pending mới.


## 6. Ràng buộc chính thức — D11 và D12

| ID | Ràng buộc | Ý nghĩa đối với thiết kế và kiểm chứng |
|---|---|---|
| D11 | Không tự sửa clinical rules hoặc ngưỡng ngoài Decision Table | Review các điều kiện từ D dòng 25–47, gồm dấu so sánh nghiêm ngặt, các nhóm tuổi và ưu tiên sốc. Validation số học D04 không được thay tiêu chí lâm sàng. |
| D12 | Giữ chín tên khóa input, ba khóa output, bốn trường audit và bảo vệ dữ liệu | Input theo D dòng 12–20. Output đúng `muc_do`, `rule_id`, `ly_do` và nhãn D dòng 52–54. Audit theo E §7.2, A-06. UUID phiên không thêm vào patient input. |

D11/D12 là cách nhóm gắn ID cho ràng buộc bắt buộc, không phải phương án nhóm được quyền thay bằng lựa chọn khác. Sáu boolean thiếu theo D13 không thêm tên khóa hoặc giá trị input mới. Mô tả `TypedDict` và việc tuổi nhận cả int/float cần phân biệt với kiểu khai báo `float` trong Data Dictionary. Q §3 ghi rõ đây là policy nhóm đã duyệt. [D; C dòng 11–27; Q §§3, 4.3]

## 7. D01–D03 đã được TA xác nhận

Ngày 08/11/2026, fossbk-spec trả lời toàn bộ nhóm câu hỏi tại [comment chính thức 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), tạo/cập nhật lúc 14:01:50 UTC (21:01:50 UTC+7). Issue còn mở không đồng nghĩa câu hỏi còn pending. Preflight Revision 03 đã đọc đầy đủ issue và cả hai comments: câu hỏi nhóm và câu trả lời TA. Không đăng/sửa comment trong TASK 02C.6. [TA; I]

| ID | Kết luận hiện hành | Trạng thái và nguồn |
|---|---|---|
| D01 | Nhiều rule Tầng 2 TRUE: chọn R01-PV > R02-PV > R03-PV, chỉ một rule_id. Tầng 1 xác nhận vẫn SOC_PHAN_VE / R-SOC. | TA CONFIRMED — [TA §1](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D02 | Tuổi missing/null là unavailable, không tự TypeError. Tầng 2 TRUE vẫn THEO_DOI / null; ly_do nêu thiếu tuổi, không đánh giá được ngưỡng. | TA CONFIRMED — [TA §§2,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| D03 | Tuổi có, current BP missing/null không chặn PHAN_VE theo rule Tầng 2 đã chứng minh; nêu chưa xác nhận sốc. Adult current ≥90, baseline missing/null: nhánh giảm chưa xác nhận không chặn Tầng 2. Current <90 đủ nhánh tuyệt đối dù thiếu nền. | TA CONFIRMED — [TA §§3–5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |

### 7.1. Ánh xạ sáu nhóm làm rõ chính thức

| TA item | Kết luận/giới hạn | Nơi áp dụng |
|---|---|---|
| TA-01 | Priority R01 > R02 > R03; sốc đã xác nhận ưu tiên R-SOC | §3 D01; §4; §5.3; Q FR-06; [TA §1](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| TA-02 | Missing/null tuổi tương đương, THEO_DOI/null khi Tầng 2 thỏa; nêu thiếu tuổi | §5.1/5.3/5.8.1; Q §§3,4,5.1; [TA §§2,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| TA-03 | Missing/null current BP không hạ Tầng 2 TRUE khi tuổi có | §4; §5.3/5.8.1; Q FR-05–08; [TA §§3,5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| TA-04 | Adult baseline unavailable không chặn Tầng 2; absolute <90 đủ, relative phải >30%, bằng 30% không đạt | §5.8.1; Q FR-05, §5.1; [TA §4](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| TA-05 | Boolean missing/null không tự exception/hạ rule đã chứng minh; policy output-dependent phải công bố/test được. Enum/Kleene/UNKNOWN mapping là lựa chọn nhóm, không yêu cầu công nghệ từ TA | §5.1/5.8/8.9/9; Q §§3.2,4.2; [TA §5](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |
| TA-06 | Policy khoảng trống được phép nếu không đổi rule/ngưỡng/schema và có tài liệu/test; ví dụ BP≤0 không buộc đổi miền số đã duyệt | §5.1/6/10; Q §§3,9; [TA §§5–6](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) |

### 7.2. Lịch sử câu hỏi D03 và phần thực sự còn review

[Bình luận D03 của nhóm](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6719840642) đăng 09:31:14 UTC ngày 08/11/2026, Huy-duc-1211. Trước phản hồi 14:01:50 UTC, Revision 02 ghi câu hỏi chờ TA; trạng thái đó chỉ là lịch sử và đã được Revision 03 thay thế. Ví dụ tuổi 25/current 110/nền giả định 140 so với 160 minh họa nhánh giảm khác nhau, không cho phép suy số đo nền. TA đã xác nhận current 110/nền unavailable/Tầng 2 TRUE → PHAN_VE theo rule khớp. Không cần Leader duyệt lại kết luận này.

Phần còn chờ là extension boolean-null→UNKNOWN/policy output-dependent mang nhãn **PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION**, cùng peer review mười lựa chọn đã duyệt và residual implementation risks. Không tạo D01–D03 pending mới hoặc nhãn runtime “pending”.

## 8. Detailed Design Register — mười lựa chọn đã chốt

### 8.1. Trạng thái và bảng tóm tắt

Cả 10 lựa chọn dưới đây được Huy Đức phê duyệt ngày 08/11/2026 trong L. Giữ mã OPEN-01–OPEN-10 để truy vết lịch sử; không còn pending lựa chọn kiến trúc. Tất cả là **APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW**. Chưa có code/test evidence, không phải TA approval. Hải/Việt Đức phản biện chéo; Huy chịu trách nhiệm quyết định cuối khi có phát hiện cần thay policy, AI không phê duyệt.

TypeError/ValueError cho invalid thực sự, public orchestration, fail-closed và bốn trường/giá trị audit đã duyệt tiếp tục có hiệu lực. TA thay ngữ nghĩa unavailable và D01–D03; không mở lại mười lựa chọn. Extension boolean-null→UNKNOWN thuộc §5.8 chờ Leader, không được gán APPROVED bởi trạng thái Enum OPEN-08. Các “alternatives considered” là phân tích phương án từng cân nhắc, không mở lại chính sách. Các lựa chọn Python tối giản này nằm trong phạm vi module synthetic.

| ID | Selected Approach | Leader Status | Technical Owner | Reviewer | Verification |
|---|---|---|---|---|---|
| OPEN-01 | Python ContextVar, set/reset bằng token ở ranh giới phiên ngoài input | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Hải | Việt Đức, Huy Đức | Scope/token, cách ly context, chưa chạy |
| OPEN-02 | Explicit session dùng chung UUID trong scope; thiếu phiên tạo UUID tạm mới cho từng call, reset trong finally | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Hải | Việt Đức, Huy Đức | Cùng phiên/call riêng/reset lỗi, chưa chạy |
| OPEN-03 | Lỗi kép ưu tiên lỗi audit an toàn ở public boundary | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Việt Đức | Hải, Huy Đức | Ba ca lỗi, message/chaining, chưa chạy |
| OPEN-04 | Path cấu hình ngoài PatientInput, vùng dữ liệu sinh của lần chạy, độc lập cwd | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Việt Đức | Hải, Huy Đức | Path/cwd, thư mục riêng, chưa chạy |
| OPEN-05 | V1 ghi tuần tự, writer/file có quyền sở hữu rõ theo lần chạy | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Việt Đức | Hải, Huy Đức | File riêng, không hứa concurrent, chưa chạy |
| OPEN-06 | pytest tmp_path và fixture quản lý/reset context kể cả khi test lỗi | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Việt Đức | Hải, Huy Đức | Teardown/order, writer thật/lỗi, chưa chạy |
| OPEN-07 | Ít helper theo trách nhiệm, rule evaluation tách I/O, classify điều phối công khai | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Hải | Việt Đức, Huy Đức | Ranh giới/core-public path, chưa chạy |
| OPEN-08 | Enum TRUE/FALSE/UNKNOWN nội bộ; AND/OR/NOT tường minh theo D13 | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Hải | Việt Đức, Huy Đức | Bảng logic, R02 T/U, HATT, chưa chạy |
| OPEN-09 | Mỗi record open append/write/close bằng cơ chế quản lý tài nguyên an toàn | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Việt Đức | Hải, Huy Đức | Write/flush/close, timing thật, chưa chạy |
| OPEN-10 | perf_counter_ns; 100 warm-up; N≥1.000; nearest-rank p50/p95; full-path audit thực | APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Việt Đức | Hải, Huy Đức | Chỉ số/đơn vị, protocol/thực đo, chưa chạy |

### 8.2. OPEN-01 — UUID context provider

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Python ContextVar, set/reset bằng token ở ranh giới phiên ngoài input.
- **Alternatives considered:** Đã cân nhắc provider có state chung cho lần chạy tuần tự: ít cơ chế, dễ hiểu nhưng dễ giữ nhầm phiên và rò state giữa tests. Mutable global UUID dùng chung không được chọn.
- **Rationale:** Thư viện chuẩn đáp ứng ngữ cảnh cục bộ mà giữ classify(patient) và chín input keys; phù hợp quy mô M2. [PY1]
- **Trade-offs:** Quản lý scope/token rõ hơn state dùng chung nhưng phải xử lý mở/kết thúc phiên và teardown.
- **Residual risk:** Kế thừa context sang tác vụ mới có thể mang theo UUID; ContextVar không tự giải quyết session management hoặc concurrency toàn diện.
- **Tests / evidence required:** Set/reset khôi phục context trước đó khi thoát scope; kiểm tra các execution context độc lập không rò UUID, gồm đường exception. Không suy ra khả năng ghi chung file đồng thời.
- **Owner and reviewer:** Hải chủ trì; Việt Đức, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.3. OPEN-02 — Không có UUID context

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Explicit session dùng chung UUID trong scope; thiếu phiên tạo UUID tạm mới cho từng call, reset trong finally.
- **Alternatives considered:** Đã loại cơ chế tạo UUID mặc định rồi giữ lại cho mọi call độc lập vì gắn nhầm các phiên. Bắt buộc caller mở phiên và báo lỗi khi thiếu scope làm direct call không hoàn thành audit; không chọn.
- **Rationale:** Một call không có explicit session được định nghĩa là phiên synthetic đơn thao tác, vẫn audit từ public entry point. UUID không phải định danh bệnh nhân/danh tính thật.
- **Trade-offs:** Tạo UUID mới cho mỗi call độc lập có chi phí nhỏ và không liên kết chúng thành một phiên dài; muốn liên kết thao tác phải mở explicit session.
- **Residual risk:** Quên reset khi exception hoặc giữ UUID tạm trong default/provider sẽ nối nhầm phiên. Reset/khôi phục token trong finally; không tái sử dụng UUID tạm giữa hai call độc lập.
- **Tests / evidence required:** Nhiều classify trong một explicit scope có cùng UUID; hai call không scope có UUID hợp lệ khác nhau; validation/audit exception vẫn reset; không rò giữa tests hoặc execution contexts.
- **Owner and reviewer:** Hải chủ trì; Việt Đức, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.4. OPEN-03 — Ưu tiên lỗi validation và audit

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Lỗi kép ưu tiên lỗi audit an toàn ở public boundary.
- **Alternatives considered:** Giữ TypeError/ValueError công khai khi audit cũng lỗi giúp caller nhận lỗi input trước, nhưng cần kênh vận hành khác và có thể che thất bại audit. Không chọn; không thêm telemetry.
- **Rationale:** Fail-closed phải biểu đạt nghĩa vụ audit chưa hoàn tất. Giữ bề mặt lỗi nhỏ, không thêm trường thứ năm/status mới.
- **Trade-offs:** Trong lỗi kép caller nhận lỗi audit thay vì loại lỗi input đầu tiên; test riêng validation để không che mapping D04.
- **Residual risk:** Exception chaining hoặc message có thể lộ raw input; public error phải an toàn, không giả định INVALID_INPUT đã được lưu.
- **Tests / evidence required:** (1) Invalid + audit thành công: có INVALID_INPUT, raise TypeError/ValueError. (2) Valid + audit thất bại: lỗi audit, không trả thành công. (3) Invalid + audit thất bại: lỗi audit ưu tiên, không cam kết record, không lộ input qua message/chaining. Tên exception audit là chi tiết implement.
- **Owner and reviewer:** Việt Đức chủ trì; Hải, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.5. OPEN-04 — Vị trí file JSONL

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Path cấu hình ngoài PatientInput, vùng dữ liệu sinh của lần chạy, độc lập cwd.
- **Alternatives considered:** Path tương đối cố định theo working directory ít cấu hình nhưng phụ thuộc nơi chạy, dễ trộn log hoặc đưa log vào checkout. Không chọn; chưa cần database/logging service.
- **Rationale:** Một cấu hình writer nhỏ đáp ứng demo, test và lần chạy tái lập; không mở rộng contract.
- **Trade-offs:** Cần cung cấp/kiểm tra cấu hình path và quyền ghi; đổi lại test có thể chọn thư mục riêng.
- **Residual risk:** Path sai hoặc không ghi được gây fail-closed. Không commit audit runtime; chỉ đề xuất .gitignore ở M2 nếu cần, không sửa trong task này.
- **Tests / evidence required:** Đổi cwd nhưng dùng cấu hình path vẫn ghi đúng nơi; test path riêng bằng tmp_path; lỗi mở/ghi không trả thành công. Đường dẫn cụ thể sẽ đặt khi triển khai.
- **Owner and reviewer:** Việt Đức chủ trì; Hải, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.6. OPEN-05 — Phạm vi ghi đồng thời

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** V1 ghi tuần tự, writer/file có quyền sở hữu rõ theo lần chạy.
- **Alternatives considered:** Lock trong tiến trình có thể bảo vệ nhiều thread nhưng thêm state/test và vẫn không bảo vệ nhiều process; không chọn cho V1.
- **Rationale:** Đề không yêu cầu concurrent file writes; giảm cơ chế để hoàn thiện core/audit trong M2.
- **Trade-offs:** Không cam kết thread-safe hoặc process-safe khi cùng ghi một file. Test cần cách ly dùng file khác nhau.
- **Residual risk:** ContextVar chỉ cô lập ngữ cảnh, không bảo đảm atomicity của JSONL write. Nếu cần nhiều tác vụ dùng chung file, phải review lại phạm vi trước khi mở rộng.
- **Tests / evidence required:** Kiểm tra writer/file thuộc lần chạy tuần tự đã công bố; test/context khác dùng file riêng. Không dùng kiểm chứng ContextVar để tuyên bố file thread/process-safe.
- **Owner and reviewer:** Việt Đức chủ trì; Hải, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.7. OPEN-06 — Test isolation

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** pytest tmp_path và fixture quản lý/reset context kể cả khi test lỗi.
- **Alternatives considered:** Dùng chung file rồi xóa trước mỗi test ít fixture nhưng dễ phụ thuộc thứ tự, đè dữ liệu nhau và khó debug; không chọn.
- **Rationale:** Tận dụng pytest sẵn có và thư mục riêng từng test, không cần hạ tầng mới. [PY2]
- **Trade-offs:** Phải viết teardown/fixture rõ, đổi lại test có thể độc lập thứ tự và quan sát I/O thật.
- **Residual risk:** Fixture lỗi trước teardown hoặc scope quá rộng có thể giữ context/file dùng chung. Hải và Việt Đức review chéo core/audit fixtures.
- **Tests / evidence required:** Mỗi test dùng tmp_path phù hợp; reset cả khi test/validation/audit lỗi; direct call và explicit session; writer thành công/thất bại. Rule test thuần được phép, public integration tests kiểm tra audit thật khi cần; không dùng runtime file chung ngoài kiểm soát.
- **Owner and reviewer:** Việt Đức chủ trì; Hải, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.8. OPEN-07 — Ranh giới helper

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Ít helper theo trách nhiệm, rule evaluation tách I/O, classify điều phối công khai.
- **Alternatives considered:** Một lõi thuần lớn giảm số điểm nối nhưng khó review nhiều nhánh validation/UNKNOWN. Framework hoặc plugin system tăng abstraction chưa có nhu cầu; không chọn.
- **Rationale:** Trách nhiệm validation, R01/R02/R03, điều kiện sốc, ưu tiên kết quả, explanation, writer và public orchestration bám contract và dễ test trong M2.
- **Trade-offs:** Cần thống nhất dữ liệu truyền giữa helper; không bắt mỗi trách nhiệm thành một function/file riêng. Hải chọn tên và số lượng tối thiểu dễ hiểu.
- **Residual risk:** Tách vụn hoặc helper có side effect ẩn làm luồng khó theo dõi. Review sơ đồ gọi và trách nhiệm trước code.
- **Tests / evidence required:** Helper rule không file I/O; public signature giữ nguyên, direct call vẫn audit; kiểm chứng cả kết quả helper và phối hợp public, không chỉ test chiếu theo implementation.
- **Owner and reviewer:** Hải chủ trì; Việt Đức, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.9. OPEN-08 — Representation logic ba trạng thái

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Enum TRUE/FALSE/UNKNOWN nội bộ; AND/OR/NOT tường minh theo D13.
- **Alternatives considered:** Bool kèm sentinel UNKNOWN hoặc tuple giá trị/độ xác định ít cấu trúc nhưng trộn kiểu, dễ đảo nghĩa và dùng nhầm truthiness. Không chọn.
- **Rationale:** Một Enum trạng thái cho kết quả điều kiện boolean/HATT giúp đọc và review theo bảng logic; giữ raw input riêng.
- **Trade-offs:** Thêm kiểu/toán tử nội bộ; Enum Python vẫn có truthiness nên phải so sánh trạng thái tường minh, không dùng if state hoặc and/or/not của Python để suy diễn Enum.
- **Residual risk:** Raw missing/null bị nhầm với Enum hoặc UNKNOWN lọt vào output. Trạng thái HATT UNKNOWN khác lựa chọn output TA đã quy định: thiếu tuổi → THEO_DOI; tuổi có/thiếu BP vẫn giữ Tầng 2 TRUE. Review tương quan S tại §5.8.2 và extension null còn đề xuất.
- **Tests / evidence required:** Toàn bộ AND/OR/NOT, R02 T≥2 / T+U<2 / còn lại rồi AND dị nguyên; boolean missing/null không exception theo TA, mapping UNKNOWN là extension chờ Leader. Điều kiện HATT unavailable không tự thành FALSE hoặc hạ Tầng 2 đã chứng minh; TA-EX-01–12. Không thêm input/nhãn muc_do.
- **Owner and reviewer:** Hải chủ trì; Việt Đức, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.10. OPEN-09 — Vòng đời ghi audit

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** Mỗi record open append/write/close bằng cơ chế quản lý tài nguyên an toàn.
- **Alternatives considered:** Giữ stream theo phiên và flush mỗi record giảm open/close nhưng thêm state và đường teardown; chưa chọn cho M2. Chỉ cân nhắc tối ưu qua đề xuất/review sau số liệu.
- **Rationale:** Vòng đời tài nguyên ngắn giảm lỗi quên đóng và vừa sức M2; chấp nhận overhead có thể đo. [PY3]
- **Trade-offs:** Mở/đóng từng record tốn I/O hơn stream dài; close/flush không đồng nghĩa dữ liệu bền vững sau mất điện. Không mặc định fsync hoặc durability production.
- **Residual risk:** Lỗi write/flush/close phải được nhận biết theo fail-closed; có thể có dòng chưa hoàn chỉnh. Không báo thành công trước hoàn tất bước ghi theo policy.
- **Tests / evidence required:** Thử lỗi mở/write/flush/close và xác nhận public không báo hoàn tất thành công; benchmark chính đo open/write/close audit thực, không mock writer hoặc giữ record đến cuối lô rồi coi call trước đã hoàn tất.
- **Owner and reviewer:** Việt Đức chủ trì; Hải, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.11. OPEN-10 — Warm-up và percentile benchmark

**Trạng thái:** APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW.

- **Selected approach:** perf_counter_ns; 100 warm-up; N≥1.000; nearest-rank p50/p95; full-path audit thực.
- **Alternatives considered:** Số warm-up khác có lý do và percentile nội suy tuyến tính là phương án khả thi đã cân nhắc, nhưng có thêm quy ước và khó so tái lập nếu dùng mặc định thư viện. Leader chọn 100/nearest-rank.
- **Rationale:** Công thức đơn giản, reviewer tính lại được; phù hợp thời gian M2 và yêu cầu A-10, không thêm ngưỡng nghiệm thu.
- **Trade-offs:** Nearest-rank lấy một mẫu nên percentile có bước nhảy. Warm-up cố định không bảo đảm loại mọi nhiễu; phải công bố môi trường/cấu hình và không chọn lọc mẫu.
- **Residual risk:** Sai ceil/chỉ số từ 1, tính cả warm-up, chia nhầm ns/ms hoặc bỏ I/O làm sai kết quả. Chưa có benchmark thực hoặc kết luận A-10 đạt.
- **Tests / evidence required:** Sắp N mẫu tăng dần, vị trí ceil(p×N) theo chỉ số 1; p=0,50/0,95, ns chia 1.000.000 ra ms. Loại 100 warm-up; đo N≥1.000 full public path có open/write/close thật. Công bố Python, OS, CPU/hardware, số lượt, dữ liệu synthetic và I/O; báo p50/p95, kiểm tra p95<100 ms. Logic thuần báo riêng.
- **Owner and reviewer:** Việt Đức chủ trì; Hải, Huy Đức review. Huy Đức đã phê duyệt hướng, giữ quyền quyết định cuối khi phát hiện cần thay đổi.

### 8.12. Thời điểm review và bằng chứng

Mười hướng đều đã chọn; không còn yêu cầu “chờ quyết định” cho OPEN-01–OPEN-10. Trước code M2, Hải/Việt Đức cần peer review những ranh giới ảnh hưởng provider, public path, validation, audit và logic ba trạng thái; nếu thấy xung đột nguồn thì báo Leader, không tự triển khai khác policy.

OPEN-10 cũng đã chốt protocol ngay trong M1. Chạy benchmark và thu bằng chứng đầy đủ có thể thực hiện M3; không trì hoãn phê duyệt protocol sang M3. Hoàn thiện coverage, clean-checkout và CI evidence tiếp tục theo kế hoạch nhóm. Concurrency mở rộng không là nhiệm vụ M3 bắt buộc.

D01–D03 đã TA CONFIRMED phần 7; không còn gate WAITING FOR TA cho ca đã trả lời. Extension null policy cần Leader xác nhận trước code phần bị ảnh hưởng; default path chờ peer/Leader review như §5.4.1, lỗi nội bộ còn residual implementation review. Các mốc review là quản lý công việc nội bộ, không phải AC/deadline mới. Tên helper, tên exception audit, path thực tế, hoặc UTC dùng Z/+00:00 là chi tiết nhỏ cần nhất quán khi code, không thành vòng phê duyệt kiến trúc mới nếu giữ approved policy.

## 9. Truy vết quyết định đến yêu cầu

Bằng chứng implementation/test/benchmark dưới đây là DỰ KIẾN hoặc CHƯA TRIỂN KHAI. Phản hồi TA là nguồn expected chính thức; không phải bằng chứng implementation đạt. Owner/Reviewer theo P, cụ thể hóa quyết định mà không đổi phân công nhóm. Không đánh dấu A-01–A-11 VERIFIED từ việc duyệt tài liệu.

| Decision ID | FR/NFR | AC | Bằng chứng cần có | Owner / Reviewer |
|---|---|---|---|---|
| D01 | FR-03, FR-04, FR-06, FR-08; NFR-07 | A-01, A-05, A-07 | TA đã xác nhận priority; cần test overlap R01/R02/R03, R02/R03 và shock override; TA-EX-01 | Hải logic / Huy, Việt Đức truy vết |
| D02 | FR-05–FR-07; NFR-05 | A-01, A-04, A-07 | TA đã xác nhận; test tuổi missing/null tương đương THEO_DOI/null, reason thiếu tuổi, không TypeError; TA-EX-02/03 | Huy / Hải, Việt Đức |
| D03 | FR-05–FR-07; NFR-05 | A-01, A-04, A-07 | TA đã xác nhận current BP/baseline missing/null; test giữ Tầng 2, absolute <90 thiếu nền, strict >30%, reason đúng; TA-EX-04–09 | Huy / Hải, Việt Đức |
| D04 | FR-07; NFR-02, NFR-03, NFR-05 | A-04, A-07 | Chưa triển khai; test strict invalid thực sự và validation mọi trường, 35 invalid cũ giữ 27 TypeError/8 ValueError nếu audit thành công; chín null cũ không còn invalid chỉ vì null, xem Q §8.1 | Hải / Huy, Việt Đức |
| D05 | FR-01–FR-09; NFR-04, NFR-05 | A-01, A-02, A-07–A-09 | Chưa triển khai: direct classify vẫn audit; helper thuần; explicit scope dùng chung UUID, hai call độc lập UUID mới; reset kể cả exception | Hải phần core/public orchestration, Việt Đức audit/CI / Huy và review chéo |
| D06 | FR-08; NFR-07 | A-05 | Chưa triển khai; template/reason thiếu tuổi, current BP, baseline theo TA; priority một rule_id và privacy | Hải / Huy, Việt Đức |
| D07 | FR-09; NFR-02, NFR-03, NFR-04 | A-06 | Chưa triển khai: bốn trường/UTC/UUID hợp lệ; JSONL; ContextVar/token, path ngoài input độc lập cwd, file riêng/ghi tuần tự, open/write/close thực và lỗi an toàn | Hải provider, Việt Đức writer / Huy và review chéo |
| D08 | FR-07, FR-09; NFR-02, NFR-03 | A-04, A-06 | Chưa triển khai: allowed missing/null sau phân loại/audit thành công → SUCCESS; invalid thực sự → INVALID_INPUT nếu ghi được. Giữ ba ca lỗi OPEN-03, audit ưu tiên lỗi kép, privacy/fail-closed và không giả định record tồn tại | Việt Đức / Hải, Huy |
| D09 | FR-01–FR-09; NFR-05, NFR-06 | A-01–A-07, A-08, A-09 | Chưa có bằng chứng: cần Test Plan/QA Matrix, tmp_path/fixture teardown, độc lập thứ tự và public/audit tests. Riêng A-08: `pytest -q` phải chạy đạt từ clean checkout với test nghiệp vụ đã thay/chỉnh stub `NotImplementedError`; lưu lệnh, môi trường và kết quả thực chạy trước khi đánh dấu VERIFIED. A-09 cần PR CI riêng | Hải test logic, Việt Đức QA/CI / Huy và review chéo |
| D10 | NFR-01 | A-10 | Chưa thực đo: perf_counter_ns(), 100 warm-up loại khỏi N≥1.000, nearest-rank ceil(p×N) chỉ số 1, ns→ms, full-path I/O thật; môi trường, p50/p95 và p95<100 ms | Việt Đức / Hải, Huy |
| D11 | FR-02–FR-06; NFR-04 | A-01, A-03, A-07 | Dự kiến review biểu thức/ngưỡng theo tag và test biên | Hải / Huy, Việt Đức |
| D12 | FR-01, FR-07–FR-09; NFR-02, NFR-03, NFR-07, NFR-08 | A-04–A-06, A-11 | Dự kiến review schema, audit, dữ liệu, disclaimer và hồ sơ bàn giao | Huy tài liệu, Việt Đức privacy / Hải và review chéo |
| D13 | FR-02–FR-08; NFR-04, NFR-05, NFR-07 | A-01, A-03–A-05, A-07 | Chưa triển khai: giữ Enum AND/OR/NOT/R02 T-U; TA cấm reject null/hạ rule đã chứng minh. Extension null→UNKNOWN/fallback output-dependent chờ Leader; test TA-EX-10–12 và S-correlation §5.8.2, raw input khác state HATT | Hải / Huy, Việt Đức |

Các ID hiện có FR-01–FR-09, NFR-01–NFR-08 và A-01–A-11 đều được liên kết trong ma trận. NFR-08/A-11 cần bằng chứng tài liệu riêng, không chỉ code. Chưa có bằng chứng để đóng các AC từ ADR này. Chi tiết test ID và ma trận QA sẽ thuộc công việc Hải/Việt Đức. [Q §§6–8; P §3]

### 9.1. Nhóm tình huống để lập Test Plan và QA Matrix

Đây là verification scenarios cần chuyển thành test ID/bằng chứng bởi Hải và Việt Đức, không phải AC mới và chưa có kết quả chạy.

| Tình huống | Điều cần kiểm chứng | Liên kết |
|---|---|---|
| Nhiều call trong explicit session rồi thoát scope | Cùng UUID trong scope; reset/khôi phục token khi kết thúc | OPEN-01–02; D05/D07/D09 |
| Hai direct call độc lập không mở phiên | Mỗi call có UUID tạm hợp lệ mới, khác nhau; scope tạm được dọn | OPEN-02; D07/D09 |
| Direct call chưa cấu hình audit path | Kiểm chứng đề xuất phần 5.4.1: gốc ổn định ngoài repository, không phụ thuộc cwd; override test/demo; không tạo/ghi được vẫn fail-closed; README có hướng dẫn | D07/D09; phần 5.4.1 PROPOSED |
| Exception validation/audit và context/test tiếp theo | Reset trong finally; không rò UUID hoặc file giữa test/execution context | OPEN-01/02/06 |
| Invalid + audit thành công | Record INVALID_INPUT; sai kiểu TypeError, sai miền/khóa thừa ValueError; không trả THEO_DOI | OPEN-03; D04/D08 |
| Valid + audit thất bại | Lỗi audit an toàn, không trả thành công, không cam kết record đã lưu | OPEN-03/09; D07/D08 |
| Invalid + audit thất bại | Lỗi audit ưu tiên; không lộ raw input qua message/chaining; không giả định INVALID_INPUT tồn tại | OPEN-03; D08 |
| Input hợp lệ nhưng rule/helper phát sinh exception nội bộ trước audit thành công | Residual implementation risk: không SUCCESS, không tự gán INVALID_INPUT hoặc thêm status/trường; không lộ payload/exception nhạy cảm. Hải/Việt Đức review cách xử lý, chưa chốt cơ chế audit/propagation | D05/D07/D08/D09; phần 10 |
| Writer/path và tài nguyên | Path cấu hình ngoài input độc lập cwd; thử open/write/flush/close lỗi; JSONL đúng bốn trường | OPEN-04/09; D07/D08 |
| Isolation/ghi tuần tự | tmp_path riêng, fixture reset kể cả test lỗi, độc lập thứ tự; không suy ra file concurrent-safe | OPEN-05/06; D09 |
| Enum và R02 T/U | Đủ bảng AND/OR/NOT, không truthiness; T≥2 TRUE, T+U<2 FALSE, còn lại UNKNOWN rồi AND dị nguyên | OPEN-08; D13 |
| Raw boolean và điều kiện huyết áp | Missing/null đều được TA cho phép; null→UNKNOWN là extension đề xuất. Tuổi thiếu có output riêng, HATT unavailable không tự chặn Tầng 2 TRUE; kiểm tra §5.8.1 | D04/D13; TA-EX-02–12 |
| Benchmark protocol và thực đo | 100 warm-up ngoài mẫu, N≥1.000, nearest-rank kiểm tra độc lập chỉ số/đơn vị; public path có open/write/close thật, báo đủ môi trường | OPEN-09/10; D10; A-10 |

Fixture và error-path cần Hải/Việt Đức review chéo. Bằng chứng runtime, benchmark và CI sẽ được thu trong task triển khai/kiểm chứng riêng, không chạy trong task tài liệu này.

### 9.2. Ma trận đối chiếu tài liệu theo TA

Mười hai hàng dưới giống Q §5.1, dùng để review expected bằng nguồn; không phải engine tests đã chạy hoặc AC đã VERIFIED. TA-EX-12 kiểm tra việc công bố đề xuất, không tuyên bố Leader đã chấp thuận expected cuối.

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

### 9.3. Bàn giao tác động M1-02/M1-03, chưa sửa file của thành viên

Nguồn đối chiếu Test Plan: nhánh docs/m1-tests-hai, commit 2c6685e55af47eea55ffeea63c250272a4e71fe3, 135 ca. Q §8.1 ghi ánh xạ chi tiết. PEND-001→PHAN_VE/R02-PV; PEND-002/007→THEO_DOI/null; PEND-003/004→PHAN_VE/R01-PV; PEND-005/006→PHAN_VE/R02-PV. Các nhãn PENDING_TA_CONFIRMATION cho những ca này phải được Hải cập nhật, không dùng để chỉ lỗi implementation.

Chín ca cũ không còn invalid chỉ vì null: INV-001, INV-017/021/025/029/033/037, INV-043 và AUD-002. Theo input hiện có, INV-043 có tuổi 15/HATT 80/R01 TRUE → SOC_PHAN_VE/R-SOC; tám ca còn lại THEO_DOI/null, không TypeError. Audit SUCCESS sau khi phân loại và ghi thành công, không INVALID_INPUT. Không suy kết quả từ tên test: Hải phải tính lại từng fixture, exception expectation và status từ D + TA.

35 ca invalid thực sự còn lại trong nhóm 44 vẫn giữ strict validation: 27 TypeError, 8 ValueError nếu audit thành công; lỗi kép vẫn ưu tiên audit. Tám ValueError: INV-002/005/006/007/008/012/016/041. Non-null boolean sai kiểu, invalid unrelated và extra keys không được bỏ qua. Hải bổ sung TA-EX-01–12, giữ truth tables/T-U và đưa MISS-009/MISS-012 cùng null variants vào review extension/S-correlation.

Việt Đức cập nhật QA workbook A-01–A-11 theo expected mới/ID Hải xác nhận, nhất là A-04 null/missing và A-06 SUCCESS/INVALID_INPUT; giữ GAP/pending cho thiếu test/CI/benchmark evidence, không giữ pending TA cho câu đã trả lời. Peer review schema/privacy/fixture/exception precedence như trước. TASK 02C.6 không sửa nhánh Hải, CSV, RULE_DESIGN, TEST_PLAN hoặc QA spreadsheet, không tuyên bố các file đó đã đồng bộ.

## 10. Hệ quả, rủi ro và bước tiếp theo

| Rủi ro còn lại sau phê duyệt | Kiểm soát đã chọn và trách nhiệm review |
|---|---|
| Giữ expected trước TA hoặc sai ngoặc/ngưỡng | Hải đối chiếu D + TA/Q Revision 03, Việt Đức kiểm tra TA-EX-01–12; D01–D03 đã có expected, không gọi pending. Thiếu BP khác thiếu tuổi; không gán không sốc từ unavailable |
| Extension null→UNKNOWN/fallback hoặc S-correlation bị hiểu đã approved | Leader xác nhận extension sau phản biện Hải/Việt Đức; giữ nhãn PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION, không thêm rule/nhãn hay mặc định FALSE; §5.8.2 |
| UUID tạm tồn tại sau lỗi hoặc bị kế thừa nhầm context | Hải thiết kế token/finally và explicit/single-call scope; Việt Đức review privacy, cách ly tests/contexts |
| Rò input qua message/chaining hoặc exception logging | Việt Đức kiểm tra public error boundary, Hải review propagation và error precedence OPEN-03 |
| Writer lỗi, dòng chưa hoàn chỉnh, cấu hình path sai | Fail-closed; không cam kết đã lưu; file riêng/vùng sinh dữ liệu; Việt Đức review open/write/flush/close và path, Hải review thời điểm public trả/lỗi |
| Direct call chưa có audit path | Cơ chế mặc định ở phần 5.4.1 chỉ PROPOSED — AWAITING PEER REVIEW; Hải/Việt Đức review gốc ổn định, override ngoài input, đích ngoài repository và README; không thay OPEN-04 đã duyệt |
| Input hợp lệ nhưng rule/helper gặp unexpected internal exception trước audit thành công | Residual implementation risk / review item: không coi là SUCCESS hoặc tự phân loại INVALID_INPUT; không thêm ERROR/FAILED/INTERNAL_ERROR, không đổi bốn trường và không ghi raw patient payload/exception nhạy cảm. Nghĩa vụ audit đã duyệt vẫn giữ nguyên; cách audit/propagate cho lỗi nội bộ chưa chốt, Hải/Việt Đức review chéo, không suy rộng từ policy validation/audit failure |
| Dùng cùng file đồng thời ngoài phạm vi | V1 tuần tự, ownership rõ; ContextVar không bảo đảm file atomicity. Nhu cầu shared-file concurrency phải review riêng |
| Test phản chiếu implementation, null cũ bị giữ invalid hoặc fixture không reset | Hải tính kỳ vọng từ D + TA, review lại 44 ca cũ theo §9.3; Việt Đức kiểm tra tmp_path/teardown/QA. Tách chờ Leader policy khỏi chờ bằng chứng runtime |
| Benchmark sai chỉ số/đơn vị, bỏ I/O hoặc tối ưu ngầm | Protocol 100 warm-up/nearest-rank đã chốt; Việt Đức soạn phép đo thật, Hải review timing/full-path; không số liệu giả |
| Tài liệu Draft PR bị hiểu nhầm đã được tích hợp/nghiệm thu | Requirements Revision 03 đã xác minh tại c855c6d4f2135a14ad94485734d4d2e604cb9cff; ADR nhánh độc lập. Publish không chứng minh peer approval/AC; không merge trong task này |

**Chi tiết nhỏ còn hoàn thiện khi triển khai:** tên/số lượng helper tối thiểu, tên exception audit, đường dẫn log được cấu hình thực tế, cách biểu diễn UTC hợp lệ nhất quán. Hải và Việt Đức đề xuất trong approved policy; không cần mở lại một vòng lựa chọn kiến trúc lớn nếu không đổi contract/phạm vi. Mọi thay đổi policy cần báo Huy; AI không quyết định thay.

Trước code M2, Hải/Việt Đức cần peer review các lựa chọn và lập Test Plan/QA Matrix theo phần 9.1. Bằng chứng runtime/CI/benchmark vẫn chưa có; có thể hoàn thiện thực đo trong M3 theo phân công đã có. D01–D03 đã TA CONFIRMED; extension boolean-null→UNKNOWN vẫn chờ Leader, còn default path và unexpected internal exception giữ đúng trạng thái review riêng. Đây chưa phải lệnh triển khai M2.

### 10.1. Đối chiếu nguồn và đồng bộ tài liệu

| Phát hiện | Cách xử lý và giới hạn |
|---|---|
| G/P hoặc Q2/Q0 còn pending TA/null invalid | G/P dùng cho phân công và lịch sử; Q2/Q0 là snapshot trước phản hồi. D + TA và Q Revision 03 hiện hành thay phát biểu trái TA. Không sửa Guide/Plan ngoài phạm vi |
| D ghi tuổi float, nhóm nhận int/float hữu hạn | Giữ D04 nội bộ và miền số đã duyệt; age null/missing nay unavailable, không tự TypeError |
| Q2/ADR Revision 02 từng giữ D01–D03 pending, null tuổi/boolean invalid | Revision 03 sửa register, contract, flow, ADR, OPEN-08 verification, traceability/risks/sources; history ghi rõ trạng thái trước 14:01:50 UTC |
| Q2 trước đây đồng bộ context/audit/protocol | Giữ ContextVar/hai scope UUID, JSONL/fail-closed/error precedence/isolation/benchmark đã duyệt; không mở lại 10 OPEN. Link Q đã đổi sang Requirements Revision 03 c855c6d4f2135a14ad94485734d4d2e604cb9cff |
| TA cho phép policy khoảng trống và nêu ví dụ BP≤0 | Không tự biến ví dụ thành yêu cầu mới: current BP=0 vẫn valid, baseline=0 vẫn invalid theo D04; không đổi threshold y khoa |
| Tách writer khỏi rule dễ bị hiểu benchmark bỏ audit | Benchmark chính vẫn toàn public path/open-write-close thực; logic thuần báo riêng |
| R03 tiêu đề dị nguyên đã biết nhưng biểu thức dùng nghi ngờ | Giữ biểu thức chính thức/chín input; không thêm field |
| Hai tài liệu ở hai nhánh Draft độc lập | Link nguồn Q theo commit cố định đã xác minh, không liên kết tương đối đến file chưa tồn tại trên branch đó |
| Stub/CI đã tồn tại ở starter | Không suy từ kiểm tra tài liệu rằng business tests/clean-checkout/PR CI/benchmark đã đạt |

### 10.2. Review và phê duyệt còn cần

- Hải review nguồn TA + Q Revision 03, core/helpers/provider và cập nhật 135-case plan theo §9.3; đặc biệt null/unavailable, overlap, strict validation và S-correlation.
- Việt Đức review audit/privacy/error paths/isolation và QA A-01–A-11; tính lại status theo input thực, đối chiếu ID Hải sửa; benchmark protocol giữ nguyên, evidence chưa có.
- Hải/Việt Đức review chéo mười lựa chọn đã duyệt; default path §5.4.1 vẫn PROPOSED — AWAITING PEER REVIEW, unexpected internal exception vẫn residual implementation review, không tự nâng thành approved.
- Huy xác nhận extension explicit boolean null→UNKNOWN và policy output-dependent sau phản biện. Không yêu cầu Huy duyệt lại kết luận TA hoặc gán TA đã duyệt Enum/Kleene. Nếu đổi policy khác đã duyệt phải review riêng.
- Kiểm tra Markdown/UTF-8/liên kết/Git scope và ma trận §9.2 chỉ chứng minh nhất quán tài liệu. Peer review/merge và nghiệm thu triển khai là các việc riêng; TASK 02C.6 không merge hoặc bắt đầu code.

## 11. Nguồn và lịch sử thay đổi

| Ký hiệu | Nguồn đã kiểm tra |
|---|---|
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), tiêu đề v1.0.2, tên URL v1.0.0. §§4–7, 9, 11–12, đối chiếu ngày 08/11/2026 qua HTML xuất bản trên nhánh gh-pages của fossbk-spec/ktpmud-book. |
| D | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag `bkt-2026-v1` trỏ commit `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469`. |
| TA | [Phản hồi chính thức fossbk-spec — comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), tạo/cập nhật 08/11/2026 14:01:50 UTC, đọc đầy đủ cả sáu nhóm trả lời và đối chiếu issue/comments trong TASK 02C.6. Làm rõ hành vi Track A, không chỉ định Enum/Kleene hoặc thay schema/ngưỡng. |
| Q | [REQUIREMENTS.md Revision 03 trên PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/c855c6d4f2135a14ad94485734d4d2e604cb9cff/REQUIREMENTS.md), commit c855c6d4f2135a14ad94485734d4d2e604cb9cff đã push và đọc lại từ GitHub trong TASK 02C.6 ngày 08/11/2026 trước khi sửa ADR. PR #1 Open/Draft/chưa merge; ID FR/NFR/AC không đổi. |
| Q2 | [Requirements Revision 02 lịch sử](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/662c47be9eba076bf9ca551403cc3e961f421d42/REQUIREMENTS.md), HEAD preflight PR #1 trước patch, trước phản hồi TA; mọi pending/null-invalid trái TA đã được Q Revision 03 thay thế. |
| Q0 | [REQUIREMENTS.md baseline trước đồng bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/673aaef3c320475196366103289c7c174e2d3b54/REQUIREMENTS.md), Revision 01 có D03 bổ sung, commit lịch sử `673aaef3c320475196366103289c7c174e2d3b54`; không phải HEAD sau publish. |
| G | [PROJECT_GUIDE.md tại integration](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/PROJECT_GUIDE.md), đọc cùng [bản cập nhật trong PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/673aaef3c320475196366103289c7c174e2d3b54/docs/PROJECT_GUIDE.md). |
| P | [TEAM_PLAN.md tại integration](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/TEAM_PLAN.md), đọc cùng [bản cập nhật trong PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/673aaef3c320475196366103289c7c174e2d3b54/docs/TEAM_PLAN.md). |
| C | [classifier.py](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/rule_engine/classifier.py), baseline tích hợp. |
| T | [test_classifier.py](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/tests/test_classifier.py), baseline tích hợp. |
| W | [test.yml](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/.github/workflows/test.yml), baseline tích hợp. |
| R | [README.md](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/README.md), baseline tích hợp. |
| I | [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15), vẫn mở, hai comments tại preflight Revision 03: [câu hỏi D03 của nhóm](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6719840642), Huy-duc-1211, 09:31:14 UTC ngày 08/11/2026; [câu trả lời fossbk-spec](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), 14:01:50 UTC cùng ngày. D01–D03 đã trả lời; TASK 02C.6 không đăng/sửa comment. |
| L | Phê duyệt Leader qua TASK 02A Revision 01/02A.5/02C.1/02C.3 ngày 08/11/2026; 02C.3 chọn mười OPEN, 02C.4 final patch, 02C.5 publish Draft peer review. TASK 02C.6 cho sửa/publish đúng Requirements và ADR Revision 03, cập nhật hai PR descriptions; không merge/code/tests/CI/Issue comment. TA thay policy trái làm rõ; extension null→UNKNOWN vẫn PROPOSED TEAM POLICY — AWAITING LEADER CONFIRMATION. Nguồn hội thoại không có URL repository. |
| PY1 | [Python 3.12 — contextvars](https://docs.python.org/3.12/library/contextvars.html), đối chiếu get/set/reset và token. Nguồn kỹ thuật phục vụ phương án OPEN-01, không phải nguồn clinical rule. |
| PY2 | [pytest — tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html), đối chiếu thư mục riêng cho từng test. Dùng làm căn cứ phương án isolation, chưa cài hoặc thay đổi pytest. |
| PY3 | [Python 3.12 — I/O](https://docs.python.org/3.12/library/io.html), đối chiếu flush/close. Nguồn kỹ thuật cho chi tiết writer, không tạo yêu cầu durability mới. |
| PY4 | [Python 3.12 — perf_counter_ns](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns), đồng hồ đo thời gian độ phân giải cao bằng số nguyên nanosecond, phù hợp công cụ đo Leader đã chọn. |
| PR | [Draft PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1) đã kiểm tra head c855c6d4f2135a14ad94485734d4d2e604cb9cff, Open/Draft/unmerged, base track-a-development; [Draft PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2) Open/Draft/unmerged tại preflight, baseline trước Revision 03 d6ba079df62a9494160ca4224f87439d5b9e7ae6. Integration b65032f94ec3ce600df07d81b5df6b9b4bd203d1. Không coi publish là peer approval hoặc bằng chứng nghiệm thu. |

Các hàng trước Revision 03 là snapshot lịch sử; mọi từ pending trong các hàng đó mô tả thời điểm trước phản hồi TA, không phải trạng thái hiện hành.

| Phiên bản | Nội dung | Trạng thái |
|---|---|---|
| Draft 0.1 — 07/11/2026 | Initial Architecture Decision Records cho D04–D10, D13, register D01–D13, constraints, pending, chi tiết OPEN và truy vết | Awaiting human review |
| Draft 0.1 — Revision 01, 07/11/2026 | Đồng bộ chính sách Leader xác nhận, làm rõ trạng thái điều kiện HATT, bổ sung comment D03 để copy, 10 OPEN có phương án/khuyến nghị/Owner/Reviewers/Decision Gate, cập nhật ADR/register/traceability/risks | Awaiting human review |
| Draft 0.1 — Revision 02, 08/11/2026 | Ghi nhận Leader chọn 10 OPEN; chỉnh single-call UUID/ưu tiên lỗi/Enum/isolation/writer/protocol; đổi Section 8 thành bảng sáu cột và tiểu mục, cập nhật tám ADR/register/traceability/risks; đăng một comment D03 có xác minh; chuẩn bị Requirements trên worktree riêng, PR #1 vẫn chưa đồng bộ | Awaiting peer review; chưa có implementation/test evidence |
| Revision 02 — final patch TASK 02C.4, 08/11/2026 | Bổ sung đề xuất tích hợp audit path cho direct call, residual risk của unexpected internal exception, A-08 tường minh; đồng bộ metadata Q-local và rút gọn bản chép comment D03 thành tóm tắt/liên kết | Snapshot lịch sử: Awaiting peer review; đề xuất path chưa được Leader duyệt, xử lý lỗi nội bộ còn review; khi đó chưa commit/push |
| Revision 02 — xuất bản peer review TASK 02C.5, 08/11/2026 | Chuẩn hóa trạng thái Draft PR và nguồn Q theo Requirements Revision 02 đã xác minh tại 662c47be9eba076bf9ca551403cc3e961f421d42; giữ Q0 cho baseline, giữ nguyên thiết kế/constraints/pending và chuẩn bị ADR ở nhánh độc lập | Draft PR / Awaiting Peer Review; chưa merge, chưa có implementation/test/benchmark evidence |
| Revision 03 — TASK 02C.6, 08/11/2026 | Áp dụng đầy đủ TA §§1–6; D01–D03 chuyển TA CONFIRMED; thay một phần D04/D13 null-invalid, giữ strict validation/Enum/toán tử và 10 OPEN. Đồng bộ nguồn Q Revision 03, flow/tám ADR/traceability/risks/history, 12 ví dụ và bàn giao 135-case/QA. | Draft PR / Awaiting Peer Review; extension boolean-null→UNKNOWN chờ Leader; default path còn đề xuất, internal error còn review; không code/tests/CI/benchmark evidence hoặc merge |
