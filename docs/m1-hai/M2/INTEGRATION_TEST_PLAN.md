# Kế hoạch public integration, context và audit

Nguồn Q §§4.4,6; A §§4,5.4.1,8,9.1. Đây là kế hoạch chuẩn bị ở M1 để triển khai sau, **chưa thực thi**. Tên helper/session factory/exception audit là chi tiết triển khai, không đổi signature `classify(patient)`. T15 ưu tiên diễn giải nullable/selection mới; không coi null tuổi hoặc boolean là invalid. Xem ISSUE15_SYNC.md.

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
| INT-017 | Chạy các cặp numeric/boolean null-vs-missing T15; writer thật thành công | Không raise vì nullable; đúng mức/mã theo T15, không hạ SOC khi đã đủ bằng chứng; record CLASSIFY/SUCCESS, không INVALID_INPUT do null. AUD-002 invalid dùng chuỗi, không null | T15 §§2–5; Hải/Việt Đức review |

Tên exception audit không bị tự đặt ở tài liệu này; M2 assert theo lớp public an toàn đã được chọn khi triển khai. Không mở lại precedence. Với explicit session, reset ở scope ngoài, không làm mất UUID phiên sau mỗi successful call; với UUID tạm phải reset sau từng call.

## 3. Đối chiếu QA Matrix

Việt Đức chưa có QA Matrix. Tôi chuẩn bị bảng trên theo phân công A §8 để đối chiếu khi matrix có. Các ID INT/AUD-001–003 cần được map sang A-04/A-06/A-07/A-08 và nơi lưu kết quả. Tôi sẽ review provider, helper và phạm vi public call; Việt Đức review writer, privacy, lỗi kép và isolation. Các phát hiện cần đổi policy sẽ chuyển Huy xem xét.

Khi có matrix, giữ cùng ID, fixture và expected; bổ sung link commit của matrix cùng kết quả review vào HANDOFF. Phần đối chiếu này hiện còn chờ, chưa tính là đã hoàn tất review chéo.
