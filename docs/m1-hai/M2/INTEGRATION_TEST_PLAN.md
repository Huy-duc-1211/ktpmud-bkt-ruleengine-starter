# Kế hoạch public integration, context và audit

Nguồn Q/A Revision 04 pin trong [sources](../M1/sources/README.md): Q §§4.4,6,8.2; A §§4,5.4.1,8,9.4. Đây là kế hoạch chuẩn bị ở M1 để triển khai sau, **chưa thực thi**. Tên helper/session factory/exception audit là chi tiết triển khai, không đổi signature `classify(patient)`. T15 ưu tiên diễn giải nullable/selection mới; không coi null tuổi hoặc boolean là invalid. D13-E đã Leader duyệt, canonical không phải TA-defined rule; xem [ISSUE15_SYNC](../M1/ISSUE15_SYNC.md).

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
| INT-018 | MISS-009/TA15-BOOL1 và D13E-001/002; writer thật | PV/R01 canonical và SUCCESS; helper R01/R02 UNKNOWN không bị đổi TRUE; ly_do nói đại diện/chưa độc lập, không observed S=False; 3 output/4 audit keys | D13-E APPROVED; Hải, Việt Đức review |
| INT-019 | MISS-012, TA15-DEPENDENT_INHALATION và D13E-008–013 | Mixed TD/null, insufficient information; không khẳng định an toàn hoặc unavailable=False; SUCCESS nếu writer hoàn tất | D13-E APPROVED; Hải/Việt Đức |
| INT-020 | D13E-003–007/015–018 và RULE-020, các cặp null/missing | AllPV+HATT proof SOC; missing BP PV; missing age TD; lowBP/noPV TD; 17.99/18 không làm tròn; TIER1_MATCH không lẫn HATT evidence | TA + D13-E; Hải |
| INT-021 | Actual ly_do của DIRECT/CANONICAL/MIXED; positive và mutated unsafe message | Áp required_patterns_all/forbidden_patterns_any, đúng rule/provenance; không tự coi regex là proof ngôn ngữ tự nhiên; peer review raw-data/privacy | D06/D13-E; Việt Đức, Hải review |

Tên exception audit không bị tự đặt ở tài liệu này; M2 assert theo lớp public an toàn đã được chọn khi triển khai. Không mở lại precedence. Với explicit session, reset ở scope ngoài, không làm mất UUID phiên sau mỗi successful call; với UUID tạm phải reset sau từng call.

## 3. Đối chiếu QA Matrix

QA Matrix chưa được cung cấp/xác minh trong nguồn TASK 02E. Bảng chuẩn bị theo A §8, còn cần Việt Đức review/map khi nhận nguồn. Các ID INT/AUD-001–003 cần được map sang A-04/A-06/A-07/A-08 và nơi lưu kết quả. Hải review provider/helpers/public path theo phân công; Việt Đức review writer/privacy/lỗi kép/isolation. Bản remediation là Leader-owned, không tuyên bố hai bạn đã review. Các phát hiện cần đổi policy sẽ chuyển Huy xem xét.

Khi có matrix, giữ cùng ID, fixture và expected; bổ sung link commit của matrix cùng kết quả review vào HANDOFF. Phần đối chiếu này hiện còn chờ, chưa tính là đã hoàn tất review chéo.
