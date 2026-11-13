# Kế hoạch public integration, context và audit

Nguồn hiện hành: [Requirements](../../../REQUIREMENTS.md), [ADR](../../../DECISIONS.md), [Decision Table](../../decision-table.md), [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002); snapshot lịch sử ở [sources](../M1/sources/README.md). Đây là kế hoạch, **chưa thực thi**. Tên helper/session factory/exception audit là chi tiết triển khai, không đổi signature `classify(patient)`. Missing/null hợp lệ theo T15; cách chọn mã được Leader cập nhật sau Issue #31. Thầy xác nhận trực tiếp MISS-009, còn overlap definite/possible là cách nhóm áp dụng quy tắc chung.

## 1. Fixture và oracle chung

- Base input: RULE-001 (tuổi 15, HATT 110, boolean False), hoặc RULE-002/INV-003/INV-041 khi cần. Dùng input đủ dữ liệu để cô lập integration; D01–D03 đã có kết quả theo T15, không còn pending.
- Provider ContextVar và writer/path cấu hình ngoài PatientInput. Dùng pytest tmp_path; assert path đã resolve nằm ngoài repo, không mặc định mọi cấu hình --basetemp đều an toàn.
- File riêng theo run/test; fixture reset token trong finally/teardown cả khi assertion/engine/writer lỗi. V1 ghi tuần tự; không tuyên bố file concurrent-safe.
- Audit đúng bốn key; Timestamp ISO 8601 UTC, UUID synthetic hợp lệ, CLASSIFY, SUCCESS/INVALID_INPUT. Count theo delta của file riêng, không dựa audit cũ.
- Test double/fault injection được dùng cho đường lỗi; đường success integration phải có kiểm chứng writer thật. Chặn stdout/stderr trong harness không đủ chứng minh privacy: cần quan sát log thật của module.
- Không cam kết không tồn tại file/record sau writer failure: write/flush/close có thể để lại dòng hoàn chỉnh hoặc không hoàn chỉnh; chỉ khóa fail-closed và không tuyên bố đã lưu thành công.

## 2. Các tình huống cần kiểm thử

| ID | Setup / thao tác | Assertion và evidence cần thu | Trạng thái policy / chủ trì |
|---|---|---|---|
| INT-001 | Direct classify(RULE-002), path override hợp lệ, không wrapper audit bên ngoài | Kết quả ba trường và một CLASSIFY/SUCCESS ghi hoàn tất trước return; direct entry tự audit | APPROVED; Hải, Việt Đức review |
| INT-002 | Explicit session A, gọi hai lần, thoát scope | Hai record cùng UUID A hợp lệ; context sau scope khôi phục đúng trạng thái trước; UUID không nằm trong PatientInput | OPEN-01/02; Hải |
| INT-003 | Hai call độc lập không mở session | UUID tạm hợp lệ khác nhau; mỗi call dọn token; không tái dùng default UUID; record riêng cho từng call | OPEN-02; Hải |
| INT-004 | Nested scope A/B; exception trong B; chạy thêm execution context độc lập | B reset về A, thoát A về context cũ. Context được khởi tạo độc lập không rò UUID; không nhầm copy_context kế thừa với context mới | OPEN-01/02; Hải |
| INT-005 | INV-003 TypeError và INV-041 ValueError; writer thật thành công; thử cả no-session/explicit | CLASSIFY/INVALID_INPUT và đúng lớp lỗi D04; không THEO_DOI; finally reset/restore context sau exception | D04/OPEN-03; Việt Đức, Hải review |
| INT-006 | Valid input; fault injection ở mkdir/open/write/flush/close, từng stage riêng | Lỗi audit an toàn, không trả classification thành công; dọn tài nguyên/context; không giả định record đã lưu; không retry vô hạn | OPEN-03/09; Việt Đức |
| INT-007 | Invalid kiểu/miền đồng thời writer lỗi, parameterize stage | Public ưu tiên lỗi audit an toàn thay TypeError/ValueError; không cam kết INVALID_INPUT tồn tại; không payload trong message, rendered exception chaining/traceback hoặc log | OPEN-03; Việt Đức, Hải review |
| INT-008 | Success với writer thật, quan sát thứ tự lifecycle | Open append/write/close hoàn tất trước return; flush nếu có nằm trong lifecycle. Lỗi flush/close không bị nuốt. Không gom record đến cuối lô rồi báo từng call thành công sớm | OPEN-09; Việt Đức |
| INT-009 | Cấu hình path tuyệt đối ngoài input; đổi cwd rồi call | Vẫn ghi đúng path cấu hình, không sinh audit trong checkout; file thuộc đúng run | OPEN-04/05; Việt Đức |
| INT-010 | Direct call chưa cấu hình audit path, đổi cwd | Kiểm chứng đề xuất A §5.4.1: gốc ổn định ngoài repo, override được, không fallback về cwd/repo; không tạo/ghi được thì fail-closed. Chưa khóa path cụ thể hoặc expected output khi cơ chế chưa duyệt | PROPOSED — AWAITING PEER REVIEW; Hải/Việt Đức, Huy quyết định |
| INT-011 | Override path test/demo ngoài input; path bị từ chối hoặc không có quyền | Giữ signature/chín keys; override hợp lệ vào file riêng; lỗi cấu hình/I/O không được bỏ audit để báo success | OPEN-04 đã duyệt; path cụ thể là chi tiết M2 |
| INT-012 | Nhiều tests đổi thứ tự, một test lỗi, test sau mở phiên mới | Không rò context/file; teardown vẫn chạy; UUID/file đúng scope; không xem kết quả kiểm context là bằng chứng concurrent-safe writer | OPEN-05/06; Việt Đức |
| INT-013 | Input valid nhưng helper phát sinh unexpected internal exception trước audit | Invariants: không tự gọi SUCCESS/INVALID_INPUT, không thêm status/schema, không payload. Cơ chế audit/propagation cụ thể chưa được chốt, giữ residual review item, không invent expected exception | RESIDUAL REVIEW ITEM; Hải/Việt Đức |
| INT-014 | Thêm UUID/path như khóa input synthetic | ValueError khóa thừa khi audit INVALID_INPUT thành công; cấu hình phải ở context/provider, không mở rộng PatientInput | D04/D12; Hải |
| INT-015 | Synthetic canary trong giá trị lỗi/cause; thu audit/log/public error | Không raw clinical input/canary nhạy cảm qua audit, stdout/stderr, message hoặc rendered chain; không trường/status ngoài allowlist | D06/D07/D08; Việt Đức |
| INT-016 | Review README runtime sau M2 | Mô tả nơi lưu/cấu hình/override, lỗi ghi và disclaimer; cơ chế default path chỉ mô tả như đã chọn sau khi Huy duyệt | A §5.4.1; Huy/Việt Đức |
| INT-017 | Chạy các cặp numeric/boolean null-vs-missing T15; writer thật thành công | Không raise vì nullable; đúng mức/mã theo T15 và D13-E, disclosure canonical khi tương ứng; không hạ SOC khi đã đủ bằng chứng; record CLASSIFY/SUCCESS, không INVALID_INPUT do null. AUD-002 invalid dùng chuỗi, không null | T15 §§2–5; D13-E theo Q/A Revision 04; Hải/Việt Đức review |
| INT-018 | MISS-009 với khóa dị nguyên thực sự vắng mặt; TA15-BOOL1 và D13E-001/002; writer thật | PV/R01 canonical và SUCCESS; helper R01/R02 UNKNOWN không bị đổi TRUE; ly_do nói đại diện/chưa độc lập, không observed S=False; 3 output/4 audit keys. Đây là test cần triển khai theo Issue #31 | D13-E APPROVED; Hải, Việt Đức review |
| INT-019 | MISS-012, TA15-DEPENDENT_INHALATION và D13E-008–013 | Mixed TD/null, insufficient information; không khẳng định an toàn hoặc unavailable=False; SUCCESS nếu writer hoàn tất | D13-E APPROVED; Hải/Việt Đức |
| INT-020 | D13E-003–007/015–018 và RULE-020, các cặp null/missing | AllPV+HATT proof SOC; missing BP PV; missing age TD; lowBP/noPV TD; 17.99/18 không làm tròn; TIER1_MATCH không lẫn HATT evidence | TA + D13-E; Hải |
| INT-021 | Actual ly_do của DIRECT/CANONICAL/MIXED; MISS-013/014, TA15-BOOL3 null/missing, D13E-014 và các câu đối chứng | Overlap: PV/R02 CANONICAL, R03 TRUE/R02 UNKNOWN; D13E-014: PV/R01 DIRECT. Kiểm mã đại diện, dữ liệu thiếu và ngữ nghĩa toàn câu; regex chỉ hỗ trợ. Kiểm câu mâu thuẫn, trường chưa biết, HATT thiếu, raw-data/privacy và lời khuyên điều trị | D06/D13-E; Việt Đức, Hải review |

Tên exception audit không bị tự đặt ở tài liệu này; M2 assert theo lớp public an toàn đã được chọn khi triển khai. Không mở lại precedence. Với explicit session, reset ở scope ngoài, không làm mất UUID phiên sau mỗi successful call; với UUID tạm phải reset sau từng call.

## 3. Đối chiếu QA Matrix

Tại thời điểm TASK 02E, QA Matrix chưa được cung cấp/xác minh trong nguồn. Bảng INT/AUD được chuẩn bị theo A §8. Bản remediation M1-02 do Huy phụ trách trên baseline của Hải.

**TASK 02Q và cập nhật sau Issue #31:** Mapping dưới đây được đối chiếu với [QA Matrix cùng phiên bản](../../m1-qa/QA_MATRIX.xlsx). [QA Matrix tại commit PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d7f7e34860c3878cdbc07b4486f785cf4ae1ca99/docs/m1-qa/QA_MATRIX_M1_CODEX_FINAL_CANDIDATE.xlsx) là mốc lịch sử. Các nhóm liên kết theo fixture hoặc assertion tương ứng và không thay expected của §2.

| Ca QA / checklist | Mục INT tương ứng và phạm vi |
|---|---|
| `QA-022`, `QA-023`, `CHK-059` | `INT-017`: nullable hợp lệ, writer hoàn tất → `SUCCESS`. `INT-005`: validation lỗi, writer hoàn tất → `INVALID_INPUT`. INV-001, INV-002 và AUD-002 là các fixture riêng. |
| `QA-020`, `QA-040/041`, `QA-057` | `INT-018` cho MISS-009, TA15-BOOL1 và D13E-001/002: AllPV/CANONICAL. `INT-021` kiểm mã đại diện và disclosure trên `ly_do` thực tế. |
| `QA-044/045`, `CHK-056` | `INT-017/021` cho TA15-BOOL3 null/missing và MISS-013/014: R02-PV CANONICAL, R03 chắc chắn/R02 chưa chắc chắn; D13E-014 là đối chứng R01 DIRECT. Helper và output kiểm riêng. |
| `QA-054–056`, `QA-061/062` | `INT-019` cho cặp dependent inhalation, MISS-012 và D13E-008–013: Mixed. `INT-021` kiểm lý do thiếu thông tin và các diễn giải sai cần loại. |
| `QA-058–060`, `QA-064` | `INT-020` cho AllPV có bằng chứng sốc, đối chứng RULE-020, thiếu HATT/tuổi, thiếu HATT nền và biên 17,99/18. `INT-021` kiểm `ly_do` ở các ca explanation tương ứng trong QA-059/064. |
| `QA-063`, `CHK-058` | `INT-021` kiểm DIRECT ở D13E-014 và kiểm assertion dương/âm cho DIRECT/CANONICAL/MIXED. `INT-015` bổ sung kiểm raw-data/privacy ở các đường message, log và exception chaining trong CHK-058. |
| `CHK-060` | Gate người thật review mapping/oracle/nguồn theo SHA. Liên quan `INT-016` cho README runtime ở M2, không phải kết quả chạy INT. |

Giữ ID, fixture và expected riêng theo từng ca. Mapping thiết kế đã có. Review người thật, kết quả thực thi và nghiệm thu vẫn chờ bằng chứng. Hải review provider/helpers/public path, Việt Đức review writer/privacy/lỗi kép/isolation. Mọi đề xuất đổi policy chuyển Huy xem xét.
