# Quyết định kiến trúc ban đầu — Track A

## 1. Thông tin tài liệu và trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Dự án | KTPMUD Hack Marathon 2026 — Track A, Dr May Day Rule Engine Sprint |
| Nhóm | `173820_n27` |
| Owner | Huy Đức, Leader, điều phối M1-04 |
| Technical Owner | Hải |
| QA / Traceability Owner | Việt Đức |
| Phiên bản | Draft 0.1 — Revision 02, đồng bộ phê duyệt Leader ngày 08/11/2026 |
| Cập nhật | 08/11/2026 |
| Trạng thái | Draft PR / Awaiting Peer Review — chưa có peer approval của Hải/Việt Đức |
| Mốc | M1 — Understand, Checkpoint 1 ngày 08/11/2026 |
| Nhánh làm việc | `docs/m1-decisions-huy` |
| HEAD nền tích hợp | `b65032f94ec3ce600df07d81b5df6b9b4bd203d1` trên `track-a-development` |
| Starter khóa | Tag `bkt-2026-v1`, commit `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Requirements tham chiếu | [Revision 02 trên PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/662c47be9eba076bf9ca551403cc3e961f421d42/REQUIREMENTS.md), commit `662c47be9eba076bf9ca551403cc3e961f421d42` đã push và xác minh; PR vẫn Draft, chưa merge |
| Trạng thái nguồn khi kiểm tra | TASK 02C.5 ngày 08/11/2026: PR #1 Open/Draft đã nhận Requirements Revision 02; chưa merge, 0 reviews/0 inline comments/0 conversation comments tại preflight. Issue #15 mở, có một comment D03, chưa có phản hồi TA. |

ADR ghi vấn đề, lựa chọn, lý do, phương án khác, đánh đổi và bằng chứng cần thu. D04–D10, D13 và cả 10 chi tiết OPEN-01–OPEN-10 đã được Leader chọn phương án ngày 08/11/2026. Trạng thái các chi tiết là APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW. Peer review nhằm phát hiện xung đột/rủi ro trước code, không có nghĩa Leader chưa quyết định. Chưa có implementation/test/benchmark evidence; phê duyệt này không phải TA approval hoặc nghiệm thu AC.

| Nhãn | Ý nghĩa |
|---|---|
| FACT / SPECIFIED | Yêu cầu chính thức hoặc hiện trạng có nguồn kiểm tra |
| APPROVED BY LEAD | Hướng thiết kế nội bộ đã được Leader phê duyệt |
| PENDING TA CONFIRMATION | Điểm phụ thuộc giảng viên/TA, chưa chốt hành vi |
| APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW | Leader đã chọn hướng; Hải/Việt Đức còn review khả thi, xung đột và rủi ro |
| OPEN-01–OPEN-10 | Mã theo dõi được giữ từ Revision 01; không còn biểu thị phương án chưa được chọn |
| Chi tiết triển khai nhỏ | Tên helper/exception/path thực tế sẽ hoàn thiện khi triển khai, trong approved policy |

Ký hiệu nguồn E, D, Q, Q0, G, P, C, T, W, R, I, L được giải thích ở phần 11. Q là Requirements Revision 02 đã được push và đọc lại từ PR #1 tại commit 662c47be9eba076bf9ca551403cc3e961f421d42; Q0 là baseline Revision 01 trước đồng bộ. Mã FR/NFR/AC giữ nguyên. Dùng URL theo commit cho nguồn cố định vì hai tài liệu nằm trên hai nhánh PR độc lập; PR #1 vẫn Draft, chưa merge. Nhãn Q-local chỉ còn xuất hiện trong lịch sử TASK 02C.3–02C.4, không mô tả trạng thái hiện hành.

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
| D01 | Chọn một mã khi R02/R03 cùng khớp | PENDING TA CONFIRMATION | Ưu tiên trong Tầng 2 | FR-03, FR-04, FR-06, FR-08; A-01, A-05, A-07 |
| D02 | Thiếu tuổi khi Tầng 2 có thể khớp | PENDING TA CONFIRMATION | Dữ liệu thiếu | FR-05–FR-07; A-01, A-04, A-07 |
| D03 | HATT hiện tại null/thiếu, hoặc người lớn thiếu nền khi cần xét giảm tương đối | PENDING TA CONFIRMATION | Khả năng kết luận sốc | FR-05–FR-07; A-01, A-04, A-07 |
| D04 | Validation nghiêm ngặt, TypeError cho sai kiểu, ValueError cho sai miền/khóa thừa | APPROVED BY LEAD | Chất lượng input và lỗi | FR-07; NFR-02, NFR-03; A-04, A-07 |
| D05 | Thiết kế tối giản, public classify() điều phối audit; ít helper theo trách nhiệm | APPROVED BY LEAD | Phân chia trách nhiệm | FR-01–FR-09; NFR-04, NFR-05; A-01, A-02 |
| D06 | Giải thích tất định theo rule | APPROVED BY LEAD | Khả năng giải thích | FR-08; NFR-07; A-05 |
| D07 | Writer JSONL riêng; ContextVar, phiên tường minh/UUID tạm một lời gọi; path cấu hình ngoài input; ghi tuần tự | APPROVED BY LEAD | Audit và riêng tư | FR-09; NFR-02, NFR-03; A-06 |
| D08 | CLASSIFY, SUCCESS/INVALID_INPUT; fail-closed, ưu tiên lỗi audit khi lỗi kép; hoàn tất ghi trước trả kết quả | APPROVED BY LEAD | Truy vết và bảo vệ dữ liệu | FR-07, FR-09; NFR-03; A-04, A-06 |
| D09 | Test nghiệp vụ thay stub; tmp_path/fixture reset context; kiểm chứng cả core, audit và D13 | APPROVED BY LEAD | Kiểm chứng | FR-01–FR-09; NFR-05, NFR-06; A-01–A-09 |
| D10 | perf_counter_ns(); warm-up 100; ≥1.000 mẫu; nearest-rank p50/p95; full-path với open/write/close audit thực | APPROVED BY LEAD | Hiệu năng | NFR-01; A-10 |
| D11 | Giữ clinical rules/ngưỡng theo bảng đã khóa | FACT / SPECIFIED | Giới hạn nghiệp vụ | FR-02–FR-06; A-01, A-03 |
| D12 | Giữ schema input/output/audit và giới hạn privacy | FACT / SPECIFIED | Contract và an toàn | FR-01, FR-07–FR-09; NFR-02, NFR-03, NFR-08; A-04–A-06, A-11 |
| D13 | Logic ba trạng thái bằng Enum nội bộ; AND/OR/NOT tường minh; không chốt D02–D03 | APPROVED BY LEAD | Input một phần | FR-02–FR-08; NFR-04, NFR-05; A-01, A-03–A-05, A-07 |

Nguồn trạng thái gồm Q, G/P và phê duyệt Leader trong L ngày 08/11/2026. Cả 10 OPEN ở phần 8 đã được chọn; không thêm D14–D23. D01–D03 tiếp tục PENDING TA CONFIRMATION; D11–D12 là FACT / SPECIFIED. Mọi kiểm chứng triển khai vẫn chưa có bằng chứng.

## 4. Tổng quan kiến trúc đã chọn, chưa triển khai

Luồng dưới đây mô tả hướng được Leader duyệt, chưa phải code đã có. Public `classify(patient)` vẫn điều phối validation, đánh giá rule, chọn classification/explanation và audit khi được gọi trực tiếp. Logic rule nội bộ tách khỏi file I/O; writer là thành phần riêng. [L; Q FR-01, FR-09]

```text
Bên ngoài PatientInput: ContextVar provider + đường dẫn writer được cấu hình
   |
   +-- Phiên tường minh: dùng UUID của scope, reset khi kết thúc scope
   +-- Không có phiên: tạo UUID tạm cho một call, reset trong finally
   |
classify(patient)
   -> validation
      +-- valid -> rule TRUE/FALSE/UNKNOWN -> ưu tiên -> output/explanation
      |                                               -> audit SUCCESS
      |                                               -> trả ba trường
      +-- invalid -> audit INVALID_INPUT -> raise TypeError/ValueError
   Mọi lỗi audit -> lỗi vận hành audit an toàn, không trả thành công
```

**Vòng đời UUID.** Phiên tường minh được mở/kết thúc ngoài input; nhiều call trong cùng scope dùng một UUID synthetic hợp lệ. Nếu không có scope, mỗi call độc lập là một phiên đơn thao tác, có UUID tạm mới; reset bằng token trong `finally` cả khi validation hoặc audit lỗi. Hai call độc lập không dùng lại UUID tạm. Cách này tránh gắn nhầm thao tác của các phiên khác nhau; UUID không phải định danh bệnh nhân hoặc danh tính thật. ContextVar không tự quản lý toàn bộ vòng đời phiên hay bảo đảm ghi file đồng thời. [L OPEN-01–OPEN-02; PY1]

| Đường xử lý dự kiến | Nghĩa vụ audit | Kết quả công khai |
|---|---|---|
| Input hợp lệ, phân loại đủ kết luận, audit thành công | Hoàn tất ghi `CLASSIFY/SUCCESS` | Trả đúng ba trường output |
| Validation thất bại, audit thành công | Có bản ghi `CLASSIFY/INVALID_INPUT` | Raise `TypeError` hoặc `ValueError` theo D04; không trả THEO_DOI |
| Validation thành công, audit thất bại | Không mặc định bản ghi đã lưu | Raise lỗi vận hành audit an toàn; không trả thành công |
| Validation và audit cùng thất bại | Không giả định có bản ghi INVALID_INPUT | Ưu tiên lỗi audit an toàn ở public boundary, không lộ input qua message/chaining |

Fail-closed là policy của module bài thi synthetic, không mặc nhiên áp dụng sản phẩm y tế thực tế. Một bản ghi được open append/write/close trong vòng đời tài nguyên rõ; lỗi write/flush/close phải được nhận biết trước khi báo bước ghi hoàn tất. Không retry vô hạn hoặc thêm trường/status mới. [L OPEN-03, OPEN-09]

D01–D03 là điểm dừng xác định kỳ vọng cho các tình huống tương ứng, chưa có cơ chế runtime mới được duyệt cho “pending”. Sơ đồ không chốt output cho các ca này.

| Trách nhiệm | Hiện có tại baseline | Hướng đã chọn, chờ triển khai |
|---|---|---|
| Interface và mô tả kiểu | PatientInput, ClassificationResult, classify(patient) | Giữ nguyên signature, chín input và ba output |
| Validation | TypedDict mô tả kiểu, chưa validation runtime | D04; invalid khác missing/UNKNOWN |
| Rule và ưu tiên | Thân hàm raise NotImplementedError | Ít helper theo trách nhiệm, Enum ba trạng thái; pending theo phần 7 |
| Output và giải thích | Có khai báo ba trường | Template D06, không dữ liệu lâm sàng thô |
| Audit | Chưa có | ContextVar, hai kiểu scope UUID, writer JSONL riêng, path ngoài input, ghi tuần tự, fail-closed |
| Test / CI | Test minh họa stub, workflow push/PR Python 3.12 | Thay/chỉnh stub bằng test nghiệp vụ, tmp_path và fixture reset, thu bằng chứng thực tế |
| Benchmark | README nêu mục tiêu | Protocol warm-up 100/nearest-rank đã chốt, chưa có số liệu |

Hiện trạng theo C dòng 11–36, T dòng 9–17, W dòng 1–12, R dòng 25–28. Chỉ tên/số lượng helper tối thiểu, tên exception audit và path cấu hình thực tế còn hoàn thiện khi code; không mở lại các policy đã duyệt.

## 5. Các ADR cho hướng thiết kế đã được duyệt

Các phương án thay thế và lập luận dưới đây là phân tích kiến trúc trong bản nháp này. Hướng lựa chọn đã được Leader duyệt qua nguồn ghi ở mỗi ADR, còn lập luận và chi tiết triển khai vẫn chờ human review.

### 5.1. D04 — Validation input nghiêm ngặt

| Thành phần ADR | Nội dung |
|---|---|
| Bối cảnh / vấn đề | Sai kiểu, thiếu khóa và null có ý nghĩa khác nhau. Ép kiểu có thể biến chuỗi hoặc số thành triệu chứng đã xác nhận, làm thay đổi điều kiện phân loại. `TypedDict` hiện chưa thực thi kiểm tra khi chạy. |
| Quyết định | Tuổi nhận `int`/`float` hữu hạn ≥0, cho phép số lẻ và loại `bool`. HATT hiện tại nhận `int` ≥0 hoặc `None`. HATT nền có số thì là `int` >0, hoặc `None`, không dùng nền 0 làm mẫu số. HATT loại bool, chuỗi và số thực. Sáu boolean có mặt phải là `True`/`False`, null là invalid, khóa vắng theo D13. Sai kiểu phát sinh `TypeError`, sai miền hoặc có khóa thừa phát sinh `ValueError`. Không ép kiểu, đổi invalid thành UNKNOWN hoặc trả `THEO_DOI` cho invalid. Input invalid vẫn đi qua audit D08. |
| Phương án khác | Tự chuyển chuỗi/số thành kiểu mong muốn để nhận được nhiều dạng dữ liệu hơn. Phương án này giảm lỗi tích hợp ban đầu nhưng cần quy ước diễn giải và có thể che lỗi bên gọi. |
| Lý do lựa chọn | Đầu vào nhỏ, cố định và giả lập cho phép yêu cầu bên gọi cung cấp đúng kiểu. Validation nghiêm giúp tìm lỗi sớm và giữ bằng chứng phân loại theo dữ liệu thực nhận. Các miền số là policy dữ liệu của nhóm, tách khỏi ngưỡng lâm sàng trong D. |
| Hệ quả / đánh đổi | Dễ kiểm chứng và giải thích lỗi kiểu, nhưng bên gọi phải chuẩn bị dữ liệu đúng. Có thêm công việc kiểm tra số hữu hạn và loại bool khỏi miền số trong Python. Thiếu tuổi/HATT hợp lệ về cấu trúc vẫn có thể để lại khả năng kết luận pending. |
| Rủi ro / giảm thiểu | Kiểm tra kiểu quá rộng nhận bool như số, hoặc validator vô tình bắt buộc đủ sáu boolean. Review loại dữ liệu thực nhận, phối hợp D13 và giữ thông báo lỗi không chứa giá trị đầu vào. Không suy invalid từ một giá trị null được phép của HATT. |
| Kiểm chứng dự kiến | Test mapping sai kiểu/sai miền/khóa thừa, số hữu hạn, tuổi lẻ, missing/null/invalid và lỗi không lộ input. Với invalid + audit thành công, xác minh INVALID_INPUT và lỗi validation; với lỗi kép, xác minh ưu tiên audit theo OPEN-03. Không thay ngưỡng lâm sàng. Chưa có implementation/test evidence. |
| Truy vết | Q FR-07; NFR-02, NFR-03, NFR-05; A-04, A-07. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G §5, Q §3 và L. D dòng 8–23, E A-04 là nguồn bắt buộc. Mapping lỗi là policy nội bộ; lỗi kép đã chốt ở OPEN-03 ngày 08/11/2026, còn peer technical review. |

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
| Quyết định | Dùng mẫu giải thích ngắn theo rule hoặc tình trạng chưa khớp/chưa đủ thông tin. Không dùng LLM cho phân loại hoặc giải thích, không đưa giá trị lâm sàng thô, thông tin nhạy cảm hay điều trị vào output. |
| Phương án khác | Ghép câu từ toàn bộ triệu chứng và số đo tạo nhiều chi tiết nhưng tăng nguy cơ rò dữ liệu. Sinh câu linh hoạt làm tăng độ biến thiên và khó kiểm chứng nội dung đúng giới hạn. |
| Lý do lựa chọn | Bộ mã rule nhỏ, output cố định và dữ liệu synthetic đủ để dùng template. Reviewer đối chiếu được mã rule với câu giải thích mà không cần tái tạo dữ liệu input trong output. |
| Hệ quả / đánh đổi | Nội dung ổn định, dễ kiểm tra và ít công xử lý ngôn ngữ. Câu trả lời ít cá nhân hóa, cần mẫu phân biệt trường hợp không khớp và thiếu thông tin. D01 ảnh hưởng mã và mẫu được chọn khi overlap. |
| Rủi ro / giảm thiểu | Mẫu đúng mã nhưng diễn đạt quá chắc chắn khi dữ liệu thiếu, hoặc lộ input qua chuỗi lỗi. Review bộ mẫu và kiểm tra cả nội dung cấm, đồng thời giữ D01–D03 pending. |
| Kiểm chứng dự kiến | Kiểm tra ba khóa output, tập nhãn, quan hệ `rule_id`–`ly_do`, tính ổn định và sự vắng mặt của dữ liệu thô/điều trị. Chưa có output nghiệp vụ để nghiệm thu. |
| Truy vết | Q FR-08; NFR-07; A-05, liên quan A-01. |
| Nguồn / trạng thái | APPROVED BY LEAD theo G D06, Q §§4–6 và L. D dòng 49–55, E A-05 là ràng buộc. Explanation thuộc output, audit lưu dấu thao tác theo schema riêng. |

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
| Quyết định | Ghi CLASSIFY/SUCCESS khi xử lý thành công và CLASSIFY/INVALID_INPUT khi validation lỗi, giữ đúng bốn trường, không payload/exception details. Fail-closed có kiểm soát: invalid + audit thành công thì raise TypeError/ValueError; valid + audit thất bại thì raise lỗi audit an toàn; lỗi kép cũng ưu tiên lỗi audit, không giả định đã có INVALID_INPUT. Không để message/chaining lộ input. Xem OPEN-03. |
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
| Quyết định | Giữ nhóm ca normal, boundary, missing, invalid, overlap, tuổi lẻ, output, audit privacy và D13. Thay/chỉnh test stub mong đợi NotImplementedError bằng test nghiệp vụ trong M2. Dùng pytest tmp_path và fixtures quản lý/reset context kể cả test thất bại; độc lập thứ tự, file riêng. Rule tests có thể thuần; public integration tests kiểm tra audit thực khi cần. Ca D01–D03 chưa gán expected chắc chắn. |
| Phương án khác | Chỉ dùng ca điển hình và một ví dụ cho mỗi nhãn nhanh hơn nhưng dễ bỏ qua sai dấu và dữ liệu thiếu. Chỉ đo tỷ lệ dòng code được chạy cũng chưa chứng minh các điều kiện rule được hiểu đúng. |
| Lý do lựa chọn | Nhóm ca bám yêu cầu A-07 và các đường rủi ro thực tế. Giá trị bằng ngưỡng thất bại nhánh so sánh nghiêm ngặt, nên các ca tại/sát biên cần được review, kể cả biên tuổi và giảm đúng 30%. |
| Hệ quả / đánh đổi | Dễ phát hiện lỗi nhỏ làm đổi kết quả, nhưng cần thời gian lập kỳ vọng và bảo trì dữ liệu synthetic. Kiểm tra helper hỗ trợ chẩn đoán lỗi, vẫn cần kiểm tra từ interface công khai. |
| Rủi ro / giảm thiểu | Copy công thức lỗi từ code vào test hoặc ép ca pending thành pass. Hải tính kỳ vọng từ D, Việt Đức review ánh xạ AC, Leader xử lý phụ thuộc TA. Không dùng test ẩn làm nguồn hay đối tượng suy đoán. |
| Kiểm chứng dự kiến | Test Plan/QA Matrix cần bao phủ writer thành công/thất bại, direct call/explicit session, reset sau exception và giữa tests/contexts, error precedence, Enum AND/OR/NOT và R02 T/U. Sau triển khai cần pytest -q từ checkout sạch và PR run. Chưa có bằng chứng test nghiệp vụ đạt. |
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
| Bối cảnh / vấn đề | Khóa boolean vắng mặt chưa chứng minh triệu chứng không có. Bắt buộc đủ sáu khóa loại bỏ dữ liệu vẫn có thể chứng minh một rule, còn mặc định thiếu thành False có thể bỏ sót rule. |
| Quyết định | Sáu boolean được thiếu khóa: True → TRUE, False → FALSE, missing → UNKNOWN; null/sai kiểu là validation error. Dùng Enum nội bộ TRUE/FALSE/UNKNOWN và AND/OR/NOT tường minh theo bảng dưới, không dùng Python truthiness của Enum. Raw input khác trạng thái điều kiện boolean/HATT. Không thêm input/output hoặc thay rule; D01–D03 vẫn pending. Xem OPEN-08. |
| Phương án khác | Bắt buộc đủ sáu boolean đơn giản hóa đánh giá nhưng từ chối thông tin đủ cho một số nhánh OR. Mặc định missing=False dễ viết nhưng thêm bằng chứng âm tính không được input xác nhận. |
| Lý do lựa chọn | Logic ba trạng thái giữ sự khác biệt giữa “không có” và “chưa biết”, cho phép kết luận khi những điều kiện đã xác nhận đủ chứng minh. Đây là lựa chọn nội bộ của nhóm, chưa được TA xác nhận như diễn giải chính thức của bảng. |
| Hệ quả / đánh đổi | Xử lý được input một phần mà giữ cấu trúc biểu thức. Đổi lại, số nhánh đánh giá, coverage test và giải thích tăng. Một số input vẫn không đủ kết luận hoặc chịu D01–D03, cần được nhận diện rõ. |
| Rủi ro / giảm thiểu | False negative do đổi UNKNOWN thành False, kết luận không có sốc khi thiếu tuổi/HATT, hoặc nhãn `THEO_DOI` bị diễn đạt thành “an toàn”. Giữ trạng thái nội bộ, review quy tắc suy luận dưới đây, giữ ly_do có mức chắc chắn phù hợp và các output phụ thuộc TA ở trạng thái chờ. |
| Kiểm chứng dự kiến | Toàn bộ bảng AND/OR/NOT, Enum không bị dùng như bool, R02 T/U, boolean missing/null/invalid và trạng thái điều kiện HATT; input đầy đủ tương đương biểu thức gốc, output vẫn ba nhãn. Kiểm tra ranh giới D02–D03 không bị chốt ngầm. Chưa có implementation/test evidence. |
| Truy vết | Q FR-02–FR-08; NFR-04, NFR-05, NFR-07; A-01, A-03–A-05, A-07. |
| Nguồn / trạng thái | APPROVED BY LEAD theo Q §§3.2, 4.2–4.3 và L; representation Enum OPEN-08 được chọn ngày 08/11/2026, PENDING PEER TECHNICAL REVIEW. D dòng 41–43 khóa biểu thức; Q §9 và I giữ D01–D03 pending. |

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

TRUE xác nhận rule khớp, FALSE xác nhận không khớp, UNKNOWN giữ việc chưa đủ thông tin. TRUE OR UNKNOWN vẫn TRUE nên một trường thiếu không luôn ngăn kết luận. Nếu không có rule Tầng 2 chắc chắn TRUE, hướng D13 là `THEO_DOI`, với giải thích phân biệt chưa khớp và thiếu thông tin. Nếu Tầng 2 TRUE, tiếp tục xét sốc, giữ D02–D03 khi tuổi/HATT chưa đủ xác định. [Q FR-05–FR-08, §4.2]

Đặc biệt ở tuổi ≥18, nhánh HATT <90 và nhánh giảm >30% nối OR. Nếu nhánh thứ nhất TRUE, dữ liệu nền không cần để chứng minh riêng phép OR này. Nếu HATT ≥90 nhưng thiếu nền để xét nhánh còn lại, kết luận cuối thuộc D03 bổ sung. Đây là phân tích cấu trúc điều kiện, không tự chốt output cho ca pending. [D dòng 35; Q §9]

#### 5.8.1. Trạng thái nội bộ của điều kiện huyết áp

Theo xác nhận Leader, TRUE/FALSE/UNKNOWN cũng được dùng để diễn đạt khả năng xác định điều kiện huyết áp. TRUE nghĩa là dữ liệu hợp lệ đã đủ chứng minh điều kiện tụt HATT theo nhóm tuổi. FALSE nghĩa là đủ dữ liệu để chứng minh điều kiện không thỏa. UNKNOWN nghĩa là thông tin cần thiết còn thiếu, nên chưa xác định được. Đây là trạng thái đánh giá điều kiện nội bộ, không thay kiểu dữ liệu huyết áp và không bổ sung output. [D dòng 25–35; L Revision 01]

Ở trẻ em, cần tuổi để chọn đúng nhóm/ngưỡng và HATT hiện tại để so sánh. Ở người lớn, áp dụng bảng OR ba trạng thái giữa nhánh HATT <90 và nhánh giảm >30%. Nhánh tuyệt đối TRUE đủ chứng minh điều kiện huyết áp TRUE. Nhánh tuyệt đối FALSE cùng nhánh tương đối UNKNOWN cho UNKNOWN, không phải FALSE. Khi dữ liệu hợp lệ đủ cho cả hai nhánh và cả hai FALSE, điều kiện huyết áp FALSE. Dữ liệu invalid phải được xử lý theo D04 trước khi suy luận.

Nếu tuổi thiếu hoặc dữ liệu huyết áp cần thiết chưa xác định, việc mô tả UNKNOWN không tự quyết định nhãn cuối. Tầng 2 TRUE kết hợp điều kiện huyết áp UNKNOWN vẫn chịu D02–D03. Không chốt `PHAN_VE`/`THEO_DOI` hoặc thêm nhãn thứ tư. Enum TRUE/FALSE/UNKNOWN dùng cho kết quả điều kiện boolean và HATT đã được Leader chọn ở OPEN-08; raw None của HATT vẫn là dữ liệu input, không phải chính Enum UNKNOWN.

## 6. Ràng buộc chính thức — D11 và D12

| ID | Ràng buộc | Ý nghĩa đối với thiết kế và kiểm chứng |
|---|---|---|
| D11 | Không tự sửa clinical rules hoặc ngưỡng ngoài Decision Table | Review các điều kiện từ D dòng 25–47, gồm dấu so sánh nghiêm ngặt, các nhóm tuổi và ưu tiên sốc. Validation số học D04 không được thay tiêu chí lâm sàng. |
| D12 | Giữ chín tên khóa input, ba khóa output, bốn trường audit và bảo vệ dữ liệu | Input theo D dòng 12–20. Output đúng `muc_do`, `rule_id`, `ly_do` và nhãn D dòng 52–54. Audit theo E §7.2, A-06. UUID phiên không thêm vào patient input. |

D11/D12 là cách nhóm gắn ID cho ràng buộc bắt buộc, không phải phương án nhóm được quyền thay bằng lựa chọn khác. Sáu boolean thiếu theo D13 không thêm tên khóa hoặc giá trị input mới. Mô tả `TypedDict` và việc tuổi nhận cả int/float cần phân biệt với kiểu khai báo `float` trong Data Dictionary. Q §3 ghi rõ đây là policy nhóm đã duyệt. [D; C dòng 11–27; Q §§3, 4.3]

## 7. Các câu hỏi chờ xác nhận — D01 đến D03

Issue #15 vẫn mở. Ngày 08/11/2026, đã đọc issue gốc và toàn bộ comments: trước khi đăng có 0 comment, không có nội dung bổ sung D03 tương đương hoặc phản hồi TA. Lần đọc lại ngay sau đăng xác nhận đúng một comment từ Huy-duc-1211, khớp nguyên văn nội dung Leader cho phép. Lần kiểm tra cuối thấy ba dòng xưng hô đã được cập nhật trên GitHub, phần câu hỏi/số liệu giữ nguyên; Codex không sửa hoặc đăng thêm comment. D01–D03 vẫn PENDING TA CONFIRMATION, chưa có expected output cuối được phê duyệt. [I; L]

| ID | Tình huống | Các cách diễn giải và hệ quả | Trạng thái |
|---|---|---|---|
| D01 | R02/R03 cùng TRUE và không đạt sốc | Ưu tiên theo thứ tự bảng hoặc ưu tiên R03 dẫn đến cùng mức phản vệ nhưng khác rule_id/ly_do. Hướng dự phòng G là R02 trước R03, thuộc PENDING ASSUMPTION. | PENDING TA CONFIRMATION |
| D02 | Thiếu tuổi nhưng Tầng 2 có thể khớp | Chuyển `THEO_DOI` theo câu nhắc thiếu tuổi hoặc giữ `PHAN_VE` theo điều kiện Tầng 2 cho kết quả khác nhau. Hướng dự phòng G là `THEO_DOI`, chưa được TA xác nhận. | PENDING TA CONFIRMATION |
| D03 | HATT hiện tại null/thiếu khóa khi Tầng 2 khớp | Giữ `PHAN_VE` hoặc `THEO_DOI`, và phân biệt null với thiếu khóa, ảnh hưởng mức kết luận. Hướng dự phòng G cho null là `PHAN_VE`, thuộc PENDING ASSUMPTION. | PENDING TA CONFIRMATION |
| D03 bổ sung | Người ≥18 tuổi, HATT hiện tại ≥90 mmHg, thiếu HATT nền, Tầng 2 TRUE | Nhánh giảm >30% chưa xác định. Chính sách bỏ nhánh không có dữ liệu và chính sách giữ khả năng sốc chưa rõ có hệ quả khác nhau. Chưa chọn `PHAN_VE` hoặc `THEO_DOI`. | PENDING TA CONFIRMATION |

D03 bổ sung đã được gửi trên kênh chính thức, không sửa issue gốc hoặc tạo issue mới. D13 và trạng thái UNKNOWN không được dùng để tự đóng D01–D03. Cách xử lý runtime cho những ca chịu ảnh hưởng vẫn phải chờ xác nhận và Leader review trước khi triển khai.

### 7.1. Bình luận D03 đã đăng, chờ TA

- Trạng thái câu hỏi: `QUESTION POSTED — AWAITING TA RESPONSE`; quyết định D03 vẫn `PENDING TA CONFIRMATION`.
- URL trực tiếp: [Bình luận bổ sung D03](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6719840642); [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15).
- Theo lần kiểm tra TASK 02C.3: đăng lúc 09:31:14 UTC ngày 08/11/2026 bằng Huy-duc-1211; updated_at 09:37:45 UTC chỉ đổi ba dòng xưng hô từ “thầy/TA” thành “thầy”, câu hỏi/số liệu giữ nguyên. Chưa có phản hồi TA tại lần kiểm tra đó. TASK 02C.4 không truy vấn remote hoặc đăng/sửa/xóa comment.

**Tóm tắt câu hỏi, không chốt expected output:**

- Dữ liệu synthetic: tuổi 25, Tầng 2 chắc chắn thỏa R02-PV, HATT hiện tại 110, HATT nền null hoặc thiếu. Điều kiện người ≥18 tuổi là HATT <90 **HOẶC** giảm >30% so với nền; nhánh tuyệt đối không thỏa nhưng nhánh tương đối chưa xác định.
- Nền giả định 140 cho mức giảm ≈21,43%, không đạt >30%; nền 160 cho 31,25%, đạt >30%. Hai giá trị chỉ minh họa, không được suy đoán/bổ sung vào input.
- Hỏi expected output PHAN_VE hay THEO_DOI cùng rule_id/ly_do; phân biệt null và missing đối với cả HATT hiện tại/nền; hỏi quyền công bố policy nội bộ hay phải chờ quy định chung. Không đánh đồng thiếu HATT hiện tại với thiếu nền, không đổi ngưỡng và không tự giải quyết D03.

## 8. Detailed Design Register — mười lựa chọn đã chốt

### 8.1. Trạng thái và bảng tóm tắt

Cả 10 lựa chọn dưới đây được Huy Đức phê duyệt ngày 08/11/2026 trong L. Giữ mã OPEN-01–OPEN-10 để truy vết lịch sử; không còn pending lựa chọn kiến trúc. Tất cả là **APPROVED BY LEAD — PENDING PEER TECHNICAL REVIEW**. Chưa có code/test evidence, không phải TA approval. Hải/Việt Đức phản biện chéo; Huy chịu trách nhiệm quyết định cuối khi có phát hiện cần thay policy, AI không phê duyệt.

TypeError/ValueError, public orchestration, fail-closed và bốn trường/giá trị audit đã duyệt tiếp tục có hiệu lực. Các “alternatives considered” là phân tích phương án từng cân nhắc, không mở lại chính sách. Các lựa chọn Python tối giản này nằm trong phạm vi module synthetic.

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
- **Residual risk:** Raw None của HATT bị nhầm với UNKNOWN hoặc UNKNOWN lọt vào output. Thiếu tuổi/HATT có thể làm điều kiện UNKNOWN nhưng không giải quyết D02/D03.
- **Tests / evidence required:** Toàn bộ AND/OR/NOT, R02 T≥2 / T+U<2 / còn lại, kết hợp dị nguyên; boolean missing khác null invalid; điều kiện HATT UNKNOWN không thành FALSE. Không thêm input hoặc nhãn muc_do.
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

WAITING FOR TA chỉ áp dụng D01–D03 phần 7. Các mốc review là quản lý công việc nội bộ, không phải AC/deadline mới. Tên helper, tên exception audit, path thực tế, hoặc UTC dùng Z/+00:00 là chi tiết nhỏ cần nhất quán khi code, không thành vòng phê duyệt kiến trúc mới nếu giữ approved policy.

## 9. Truy vết quyết định đến yêu cầu

Bằng chứng implementation/test/benchmark dưới đây là DỰ KIẾN hoặc CHƯA TRIỂN KHAI. Comment D03 đã đăng là bằng chứng gửi câu hỏi, không phải câu trả lời TA. Owner/Reviewer theo P, cụ thể hóa quyết định mà không đổi phân công nhóm. Không đánh dấu A-01–A-11 VERIFIED từ việc duyệt tài liệu.

| Decision ID | FR/NFR | AC | Bằng chứng cần có | Owner / Reviewer |
|---|---|---|---|---|
| D01 | FR-03, FR-04, FR-06, FR-08; NFR-07 | A-01, A-05, A-07 | Dự kiến câu trả lời TA, policy tie-break và test sau xác nhận | Huy theo dõi TA, Hải kiểm tra logic, Việt Đức ánh xạ |
| D02 | FR-05–FR-07; NFR-05 | A-01, A-04, A-07 | Dự kiến xác nhận missing age và kỳ vọng được duyệt | Huy / Hải, Việt Đức |
| D03 | FR-05–FR-07; NFR-05 | A-01, A-04, A-07 | Đã đăng câu hỏi bổ sung; vẫn cần TA xác nhận null/missing HATT hiện tại và thiếu nền người lớn, cùng rule_id/ly_do | Huy / Hải, Việt Đức |
| D04 | FR-07; NFR-02, NFR-03, NFR-05 | A-04, A-07 | Chưa triển khai, cần test mapping TypeError/ValueError đã duyệt, kiểu/miền, khóa thừa và lỗi không lộ input | Hải / Huy, Việt Đức |
| D05 | FR-01–FR-09; NFR-04, NFR-05 | A-01, A-02, A-07–A-09 | Chưa triển khai: direct classify vẫn audit; helper thuần; explicit scope dùng chung UUID, hai call độc lập UUID mới; reset kể cả exception | Hải phần core/public orchestration, Việt Đức audit/CI / Huy và review chéo |
| D06 | FR-08; NFR-07 | A-05 | Chưa triển khai, cần mẫu giải thích được duyệt và output kiểm chứng | Hải / Huy, Việt Đức |
| D07 | FR-09; NFR-02, NFR-03, NFR-04 | A-06 | Chưa triển khai: bốn trường/UTC/UUID hợp lệ; JSONL; ContextVar/token, path ngoài input độc lập cwd, file riêng/ghi tuần tự, open/write/close thực và lỗi an toàn | Hải provider, Việt Đức writer / Huy và review chéo |
| D08 | FR-07, FR-09; NFR-02, NFR-03 | A-04, A-06 | Chưa triển khai: SUCCESS/INVALID_INPUT; ba ca lỗi OPEN-03, ưu tiên audit khi lỗi kép; fail-closed, message/chaining an toàn, không giả định record đã lưu | Việt Đức / Hải, Huy |
| D09 | FR-01–FR-09; NFR-05, NFR-06 | A-01–A-07, A-08, A-09 | Chưa có bằng chứng: cần Test Plan/QA Matrix, tmp_path/fixture teardown, độc lập thứ tự và public/audit tests. Riêng A-08: `pytest -q` phải chạy đạt từ clean checkout với test nghiệp vụ đã thay/chỉnh stub `NotImplementedError`; lưu lệnh, môi trường và kết quả thực chạy trước khi đánh dấu VERIFIED. A-09 cần PR CI riêng | Hải test logic, Việt Đức QA/CI / Huy và review chéo |
| D10 | NFR-01 | A-10 | Chưa thực đo: perf_counter_ns(), 100 warm-up loại khỏi N≥1.000, nearest-rank ceil(p×N) chỉ số 1, ns→ms, full-path I/O thật; môi trường, p50/p95 và p95<100 ms | Việt Đức / Hải, Huy |
| D11 | FR-02–FR-06; NFR-04 | A-01, A-03, A-07 | Dự kiến review biểu thức/ngưỡng theo tag và test biên | Hải / Huy, Việt Đức |
| D12 | FR-01, FR-07–FR-09; NFR-02, NFR-03, NFR-07, NFR-08 | A-04–A-06, A-11 | Dự kiến review schema, audit, dữ liệu, disclaimer và hồ sơ bàn giao | Huy tài liệu, Việt Đức privacy / Hải và review chéo |
| D13 | FR-02–FR-08; NFR-04, NFR-05, NFR-07 | A-01, A-03–A-05, A-07 | Chưa triển khai: Enum AND/OR/NOT, R02 T/U, raw input khác điều kiện HATT UNKNOWN; missing/null/invalid riêng; output ba nhãn và D02–D03 pending | Hải / Huy, Việt Đức |

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
| Raw boolean và điều kiện huyết áp | Missing boolean→UNKNOWN, null boolean invalid; HATT null hợp lệ có thể làm điều kiện UNKNOWN; D02/D03 vẫn chờ TA | D04/D13; D02/D03 |
| Benchmark protocol và thực đo | 100 warm-up ngoài mẫu, N≥1.000, nearest-rank kiểm tra độc lập chỉ số/đơn vị; public path có open/write/close thật, báo đủ môi trường | OPEN-09/10; D10; A-10 |

Fixture và error-path cần Hải/Việt Đức review chéo. Bằng chứng runtime, benchmark và CI sẽ được thu trong task triển khai/kiểm chứng riêng, không chạy trong task tài liệu này.

## 10. Hệ quả, rủi ro và bước tiếp theo

| Rủi ro còn lại sau phê duyệt | Kiểm soát đã chọn và trách nhiệm review |
|---|---|
| Chốt ngầm output khi tuổi/HATT thiếu hoặc sai ngoặc/ngưỡng | Hải review D13/FR-02–FR-06, Việt Đức kiểm tra coverage; Huy theo dõi D01–D03, không gán TA approval |
| UUID tạm tồn tại sau lỗi hoặc bị kế thừa nhầm context | Hải thiết kế token/finally và explicit/single-call scope; Việt Đức review privacy, cách ly tests/contexts |
| Rò input qua message/chaining hoặc exception logging | Việt Đức kiểm tra public error boundary, Hải review propagation và error precedence OPEN-03 |
| Writer lỗi, dòng chưa hoàn chỉnh, cấu hình path sai | Fail-closed; không cam kết đã lưu; file riêng/vùng sinh dữ liệu; Việt Đức review open/write/flush/close và path, Hải review thời điểm public trả/lỗi |
| Direct call chưa có audit path | Cơ chế mặc định ở phần 5.4.1 chỉ PROPOSED — AWAITING PEER REVIEW; Hải/Việt Đức review gốc ổn định, override ngoài input, đích ngoài repository và README; không thay OPEN-04 đã duyệt |
| Input hợp lệ nhưng rule/helper gặp unexpected internal exception trước audit thành công | Residual implementation risk / review item: không coi là SUCCESS hoặc tự phân loại INVALID_INPUT; không thêm ERROR/FAILED/INTERNAL_ERROR, không đổi bốn trường và không ghi raw patient payload/exception nhạy cảm. Nghĩa vụ audit đã duyệt vẫn giữ nguyên; cách audit/propagate cho lỗi nội bộ chưa chốt, Hải/Việt Đức review chéo, không suy rộng từ policy validation/audit failure |
| Dùng cùng file đồng thời ngoài phạm vi | V1 tuần tự, ownership rõ; ContextVar không bảo đảm file atomicity. Nhu cầu shared-file concurrency phải review riêng |
| Test phản chiếu implementation hoặc fixture không reset | Hải tính kỳ vọng từ D, Việt Đức review tmp_path/teardown và QA Matrix; giữ ca pending tách riêng |
| Benchmark sai chỉ số/đơn vị, bỏ I/O hoặc tối ưu ngầm | Protocol 100 warm-up/nearest-rank đã chốt; Việt Đức soạn phép đo thật, Hải review timing/full-path; không số liệu giả |
| Tài liệu Draft PR bị hiểu nhầm đã được tích hợp/nghiệm thu | Requirements Revision 02 đã xác minh trên PR #1 tại 662c47be9eba076bf9ca551403cc3e961f421d42; ADR xuất bản trên nhánh độc lập. Hai PR chưa merge, chưa có peer approval hoặc bằng chứng nghiệm thu từ việc publish; Huy quyết định sau review |

**Chi tiết nhỏ còn hoàn thiện khi triển khai:** tên/số lượng helper tối thiểu, tên exception audit, đường dẫn log được cấu hình thực tế, cách biểu diễn UTC hợp lệ nhất quán. Hải và Việt Đức đề xuất trong approved policy; không cần mở lại một vòng lựa chọn kiến trúc lớn nếu không đổi contract/phạm vi. Mọi thay đổi policy cần báo Huy; AI không quyết định thay.

Trước code M2, Hải/Việt Đức cần peer review các lựa chọn và lập Test Plan/QA Matrix theo phần 9.1. Bằng chứng runtime/CI/benchmark vẫn chưa có; có thể hoàn thiện thực đo trong M3 theo phân công đã có. D01–D03 là phụ thuộc WAITING FOR TA cho các đường chịu ảnh hưởng. Đây chưa phải lệnh triển khai M2.

### 10.1. Đối chiếu nguồn và đồng bộ tài liệu

| Phát hiện | Cách xử lý và giới hạn |
|---|---|
| G/P tại integration chưa có D13, PR #1 có bản cập nhật mới hơn | Đọc cả hai phiên bản bằng SHA cố định; không sửa integration hoặc phân công. G/P trong PR dẫn đến Requirements hiện hành |
| D ghi tuổi float, nhóm nhận int/float hữu hạn | Giữ policy validation là quyết định nội bộ D04, không gán là ngưỡng/rule của thầy |
| Q0 FR-07 từng nói chỉ boolean missing mới biểu diễn UNKNOWN, trong khi điều kiện HATT cũng có thể chưa xác định | Q Revision 02 đã sửa cách diễn đạt và có trên PR #1: raw boolean missing→UNKNOWN khác kết quả điều kiện HATT UNKNOWN; không đổi kiểu input hoặc chốt D02/D03 |
| Q0 từng ghi lỗi/context/audit/percentile là chi tiết chưa chốt | Q Revision 02 đã đồng bộ D04/D05/D07–D10/D13 và được đọc lại từ GitHub tại commit cố định ở phần 11. DECISIONS.md nằm ở nhánh độc lập, chưa có trên nhánh PR #1 nên không thêm liên kết tương đối bị thiếu |
| D03 bổ sung trước đây chưa đăng Issue #15 | Đã đăng đúng một comment theo L, đọc lại khớp nguyên văn; URL/ngày ở phần 7.1; vẫn chờ TA |
| Tách writer khỏi rule có thể bị hiểu là phép đo không gồm audit | Benchmark chính vẫn là full public path gồm open/write/close thực; logic thuần báo riêng |
| Tiêu đề R03 nói dị nguyên đã biết, biểu thức dùng dị nguyên nghi ngờ | Giữ biểu thức chính thức và chín input names, không bổ sung khóa |
| Starter có test và workflow | Giữ nguyên nhận định stub/cấu hình; không dùng kiểm tra tài liệu để tuyên bố test nghiệp vụ/CI/benchmark đạt |

### 10.2. Checklist review trước khi upload

- Hải review ContextVar/token, hai scope UUID, helper/public path, Enum và pending clinical cases theo D.
- Việt Đức review audit schema/privacy, cả ba ca OPEN-03, open/write/flush/close, isolation và protocol benchmark.
- Hải/Việt Đức review chéo các điểm core/audit; phản hồi khả thi hoặc xung đột cho Huy, không tự đổi phương án đã chọn.
- Hải/Việt Đức review riêng direct call chưa cấu hình audit path và unexpected internal exceptions: phân biệt đề xuất tích hợp/rủi ro còn lại với mười OPEN đã duyệt; chưa tự chốt cơ chế mới.
- Huy kiểm tra hai bản Revision 02, nội dung comment đã đăng và phản hồi peer review; tiếp tục theo dõi TA, quyết định merge sau review. Việc publish không thay bằng chứng M1-02/M1-03 hoặc xác nhận hoàn tất Checkpoint 1.
- Kiểm tra Markdown/UTF-8/liên kết và Git scope chỉ chứng minh chất lượng tài liệu, không nghiệm thu A-01–A-11.

## 11. Nguồn và lịch sử thay đổi

| Ký hiệu | Nguồn đã kiểm tra |
|---|---|
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), tiêu đề v1.0.2, tên URL v1.0.0. §§4–7, 9, 11–12, đối chiếu ngày 08/11/2026 qua HTML xuất bản trên nhánh gh-pages của fossbk-spec/ktpmud-book. |
| D | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag `bkt-2026-v1` trỏ commit `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469`. |
| Q | [REQUIREMENTS.md Revision 02 trên PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/662c47be9eba076bf9ca551403cc3e961f421d42/REQUIREMENTS.md), commit `662c47be9eba076bf9ca551403cc3e961f421d42` đã push và đọc lại trực tiếp từ GitHub trong TASK 02C.5 ngày 08/11/2026. PR #1 vẫn Open/Draft, chưa merge. ID FR/NFR/AC và contract giữ nguyên. |
| Q0 | [REQUIREMENTS.md baseline trước đồng bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/673aaef3c320475196366103289c7c174e2d3b54/REQUIREMENTS.md), Revision 01 có D03 bổ sung, commit lịch sử `673aaef3c320475196366103289c7c174e2d3b54`; không phải HEAD sau publish. |
| G | [PROJECT_GUIDE.md tại integration](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/PROJECT_GUIDE.md), đọc cùng [bản cập nhật trong PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/673aaef3c320475196366103289c7c174e2d3b54/docs/PROJECT_GUIDE.md). |
| P | [TEAM_PLAN.md tại integration](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/TEAM_PLAN.md), đọc cùng [bản cập nhật trong PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/673aaef3c320475196366103289c7c174e2d3b54/docs/TEAM_PLAN.md). |
| C | [classifier.py](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/rule_engine/classifier.py), baseline tích hợp. |
| T | [test_classifier.py](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/tests/test_classifier.py), baseline tích hợp. |
| W | [test.yml](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/.github/workflows/test.yml), baseline tích hợp. |
| R | [README.md](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/README.md), baseline tích hợp. |
| I | [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15), mở; trước đăng 0 comment; sau đăng có một [comment D03](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6719840642) ngày 08/11/2026 lúc 09:31:14 UTC, tài khoản Huy-duc-1211. Lần đầu đọc lại khớp nguyên văn; updated_at 09:37:45 UTC có ba dòng xưng hô đổi thành “thầy”, nội dung D03 giữ nguyên, Codex không sửa/đăng thêm. Chưa có phản hồi TA tại lần kiểm tra. |
| L | Phê duyệt Leader trong hội thoại TASK 02A Revision 01, TASK 02A.5, TASK 02C.1 Revision 01/Addendum và TASK 02C.3 ngày 08/11/2026. TASK 02C.3 chọn đủ 10 OPEN và cho phép một comment D03; TASK 02C.4 là final patch cục bộ. TASK 02C.5 cho phép commit/push Requirements và ADR, tạo Draft PR ADR độc lập; không merge hoặc sửa Issue/comment. Các quyền cục bộ trước đây là lịch sử, không phải trạng thái xuất bản hiện tại. Phê duyệt nội bộ không phải TA/peer approval; không có URL repository cho nguồn hội thoại. |
| PY1 | [Python 3.12 — contextvars](https://docs.python.org/3.12/library/contextvars.html), đối chiếu get/set/reset và token. Nguồn kỹ thuật phục vụ phương án OPEN-01, không phải nguồn clinical rule. |
| PY2 | [pytest — tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html), đối chiếu thư mục riêng cho từng test. Dùng làm căn cứ phương án isolation, chưa cài hoặc thay đổi pytest. |
| PY3 | [Python 3.12 — I/O](https://docs.python.org/3.12/library/io.html), đối chiếu flush/close. Nguồn kỹ thuật cho chi tiết writer, không tạo yêu cầu durability mới. |
| PY4 | [Python 3.12 — perf_counter_ns](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns), đồng hồ đo thời gian độ phân giải cao bằng số nguyên nanosecond, phù hợp công cụ đo Leader đã chọn. |
| PR | [Draft PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), xác minh sau push ngày 08/11/2026: open, draft=true, merged=false; head docs/m1-requirements-huy tại 662c47be9eba076bf9ca551403cc3e961f421d42; base track-a-development tại b65032f94ec3ce600df07d81b5df6b9b4bd203d1. Preflight có 0 reviews, 0 inline comments, 0 conversation comments; chưa có peer approval. |

| Phiên bản | Nội dung | Trạng thái |
|---|---|---|
| Draft 0.1 — 07/11/2026 | Initial Architecture Decision Records cho D04–D10, D13, register D01–D13, constraints, pending, chi tiết OPEN và truy vết | Awaiting human review |
| Draft 0.1 — Revision 01, 07/11/2026 | Đồng bộ chính sách Leader xác nhận, làm rõ trạng thái điều kiện HATT, bổ sung comment D03 để copy, 10 OPEN có phương án/khuyến nghị/Owner/Reviewers/Decision Gate, cập nhật ADR/register/traceability/risks | Awaiting human review |
| Draft 0.1 — Revision 02, 08/11/2026 | Ghi nhận Leader chọn 10 OPEN; chỉnh single-call UUID/ưu tiên lỗi/Enum/isolation/writer/protocol; đổi Section 8 thành bảng sáu cột và tiểu mục, cập nhật tám ADR/register/traceability/risks; đăng một comment D03 có xác minh; chuẩn bị Requirements trên worktree riêng, PR #1 vẫn chưa đồng bộ | Awaiting peer review; chưa có implementation/test evidence |
| Revision 02 — final patch TASK 02C.4, 08/11/2026 | Bổ sung đề xuất tích hợp audit path cho direct call, residual risk của unexpected internal exception, A-08 tường minh; đồng bộ metadata Q-local và rút gọn bản chép comment D03 thành tóm tắt/liên kết | Snapshot lịch sử: Awaiting peer review; đề xuất path chưa được Leader duyệt, xử lý lỗi nội bộ còn review; khi đó chưa commit/push |
| Revision 02 — xuất bản peer review TASK 02C.5, 08/11/2026 | Chuẩn hóa trạng thái Draft PR và nguồn Q theo Requirements Revision 02 đã xác minh tại 662c47be9eba076bf9ca551403cc3e961f421d42; giữ Q0 cho baseline, giữ nguyên thiết kế/constraints/pending và chuẩn bị ADR ở nhánh độc lập | Draft PR / Awaiting Peer Review; chưa merge, chưa có implementation/test/benchmark evidence |
