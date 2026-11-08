# Áp dụng làm rõ Issue #15 — comment 6722429248

**Thứ tự áp dụng:** Decision Table + T15 là contract chính thức; T15 thay các diễn giải mâu thuẫn về D01–D03, null và missing trong Q/A Revision 02. Các phần Q/A không mâu thuẫn (Enum, ContextVar, audit fail-closed, benchmark, sai kiểu/miền không phải null...) vẫn giữ. Snapshot Q/A và bình luận cũ không bị sửa; Leader cần đồng bộ Requirements/ADR ở PR riêng sau khi review bản bổ sung này.

## 1. Quy định chung đã được chốt

| Điểm | Cách xử lý bắt buộc / nguồn |
|---|---|
| D01, nhiều rule Tầng 2 | Không sốc: PHAN_VE, chọn một rule theo R01-PV > R02-PV > R03-PV. Có đủ bằng chứng Tầng 1: SOC_PHAN_VE/R-SOC. [T15 §1] |
| D02, tuổi không có dữ liệu | Thiếu khóa hoặc null tuổi: THEO_DOI/null; reason nói thiếu tuổi, kể cả biểu hiện đủ rule. Tuổi thiếu ưu tiên hơn nhánh thiếu HATT. [T15 §§2,5] |
| D03, HATT hiện tại không có | Tuổi có, đủ phản vệ nhưng HATT thiếu/null: PHAN_VE và mã Tầng 2 theo thứ tự; reason nên nói chưa đánh giá tiêu chí sốc vì thiếu số đo. [T15 §3] |
| D03, người lớn thiếu nền | b>=90, nền thiếu/null: không coi nhánh giảm tương đối đã thỏa; PHAN_VE nếu đủ Tầng 2. Không gán nền mặc định; reason nên nói thiếu nền. b<90 vẫn đủ nhánh tuyệt đối. [T15 §4] |
| Numeric null/missing | tuoi, HATT, HATT nền: cả hai đều không có dữ liệu, cùng muc_do/rule_id; không coi null tuổi là TypeError. [T15 §5] |
| Boolean null/missing | Không raise vì thiếu/null; không hạ mức khi dữ liệu hiện có đã đủ rule bất kể phần còn thiếu. Chính sách cho phần phụ thuộc dữ liệu thiếu do nhóm công bố và test. [T15 §5] |

Không ghi D01–D03 là PENDING TA CONFIRMATION nữa. Giữ tên PEND-001–007 để truy vết lịch sử, cột Pending trống và cột Resolved decision ghi D01/D02/D03. Kết quả vẫn DRAFT_NOT_EXECUTED vì chưa chạy runtime.

## 2. Các thay đổi chính trong test case

| ID | Expected mới |
|---|---|
| PEND-001 | PHAN_VE/R02-PV |
| PEND-002 | THEO_DOI/null, thiếu tuổi |
| PEND-003/004 | PHAN_VE/R01-PV, thiếu HATT hiện tại |
| PEND-005/006 | PHAN_VE/R02-PV, thiếu nền |
| PEND-007 | THEO_DOI/null, thiếu tuổi dù HATT cũng thiếu |
| INV-001 | Tuổi null là dữ liệu thiếu: THEO_DOI/null trong ca này, không TypeError |
| INV-017/021/025/029/033/037 | Boolean null không invalid; với biểu hiện còn lại của các ca này trả THEO_DOI/null |
| INV-043 | R01 và số đo đã đủ sốc: SOC_PHAN_VE/R-SOC dù tiêu hóa null, không hạ mức |
| AUD-002 | Giữ mục tiêu audit invalid bằng boolean chuỗi "true", không còn dùng null làm dữ liệu invalid |

CSV chung có 157 ca: giữ 135 ca gốc và gộp thêm 22 ca T15. Mã Test ID đã khôi phục về mã gốc. Số invalid hiện còn **36 =28 TypeError+8 ValueError**; không cố giữ 44 invalid trái quy định mới. INV/PEND trong ID là lịch sử, không quyết định hành vi.

[các ca T15 trong TEST_CASES.csv](TEST_CASES.csv) chứa chung **22 ca bổ sung /11 cặp null-vs-missing** cho ba trường số, cả sáu boolean, không hạ sốc và ca thực sự phụ thuộc đường hít. Các cặp phải có cùng muc_do/rule_id; không assert hai phiên có cùng UUID hoặc reason nguyên văn giống nhau.

## 3. D13 giữ ở tầng thông tin; không dùng UNKNOWN để trì hoãn D02/D03

Policy nhóm được dùng trong bộ test này: boolean thiếu/null -> Enum UNKNOWN; True/False -> TRUE/FALSE. Số/chuỗi sai kiểu vẫn invalid theo D04 nhóm, không ép thành bool. Bảng AND/OR/NOT và R02 T/U không thay đổi.

HYPOTENSION UNKNOWN có thể diễn tả chưa biết điều kiện huyết áp về mặt dữ liệu. **SHOCK_EVIDENCE chỉ TRUE khi có bằng chứng**, còn UNKNOWN dữ liệu không làm thỏa Tầng 1. Không suy đó là “HATT bình thường”; reason phải phản ánh thiếu số đo/nền. Sau đó selector áp dụng tuổi thiếu -> THEO_DOI và đủ Tầng 2 nhưng thiếu bằng chứng sốc -> PHAN_VE đúng T15. Không giữ final output pending vì Enum UNKNOWN.

Khi có một rule chắc chắn TRUE, lấy mức tương ứng (trừ override thiếu tuổi), giữ priority nếu nhiều rule TRUE. Khi mức thực sự phụ thuộc boolean thiếu/null, giữ D13 theo policy nhóm: THEO_DOI và reason chưa đủ thông tin. Đây là policy nhóm được T15 cho phép, không phải thầy bắt buộc dùng Enum/UNKNOWN/THEO_DOI cho mọi input thiếu.

## 4. Tương quan dị nguyên và đề xuất BOOL-COVERAGE

MISS-009 có S thiếu, da+hô hấp TRUE: S=False dẫn R01; S=True dẫn R02. Vì vậy không có một rule riêng chắc chắn TRUE theo phép tính ba trạng thái, nhưng **mọi completion đều đủ phản vệ**. Chỉ kiểm từng rule rồi trả THEO_DOI có nguy cơ hạ mức dù kết luận không còn phụ thuộc S.

Tôi đề xuất cách xử lý dưới đây để Huy review:

1. Kiểm tính phủ của các rule gốc trên các khả năng True/False của boolean chưa biết, tối đa 64 tổ hợp; đây là phân tích kiến thức, không thêm rule/ngưỡng y khoa.
2. Nếu một rule đã chắc chắn TRUE, dùng rule đó theo thứ tự bắt buộc, không bỏ bằng chứng vì trường không liên quan thiếu.
3. Nếu không rule riêng chắc chắn TRUE nhưng mọi completion đều phản vệ, bảo toàn mức; với bằng chứng HATT thấp thì sốc. Với PHAN_VE mà mã khác nhau giữa các completion, đề xuất mã đại diện từ completion đặt các UNKNOWN=False rồi chọn theo thứ tự bảng; MISS-009 là R01-PV. Reason nêu thiếu thông tin và quy ước mã đại diện, không nói đã xác nhận S=False.
4. Nếu các completion có cả phản vệ và không phản vệ thì kết quả thực sự phụ thuộc dữ liệu thiếu; giữ THEO_DOI theo D13 nhóm và giải trình rủi ro bỏ sót. Không tự giả số đo hoặc thêm dữ liệu input.

**Policy BOOL-COVERAGE/mã đại diện còn PROPOSED FOR LEADER REVIEW.** Cột Policy review của MISS-009 và cặp TA15-BOOL1 ghi rõ điều này; expected mã là bản đề xuất để review, không phải nguồn T15 đã chốt. Không còn pending TA cho D01–D03. Nếu Leader chọn cách diễn đạt/mã khác, sửa đúng các dòng policy này và ghi lại trong ADR, không đổi phần bắt buộc §§1–5.

## 5. Phần không thay đổi và phạm vi lượt sửa

Không đổi ngưỡng tuổi/HATT, dấu < và >30%, chín tên khóa input, ba output, bốn audit fields hoặc protocol benchmark. Miền số không phải null và khóa lạ giữ policy nhóm trước; T15 §6 cho nhóm công bố policy ở chỗ chưa quy định, không tự dùng ví dụ của thầy để thay mọi miền số.

ContextVar/UUID, audit error precedence, privacy và benchmark đã duyệt vẫn áp dụng. Null/missing được xử lý hợp lệ thì audit SUCCESS, không INVALID_INPUT chỉ vì thiếu dữ liệu. Có invalid khác hoặc audit failure vẫn theo đường lỗi đã duyệt. Default path proposal/internal exception residual không được phản hồi này giải quyết thay.

Phạm vi là tài liệu/data M1 và các kế hoạch giai đoạn sau đã tách ở M2; chưa viết classify()/loader/audit runtime. Tôi đã review phần M1 và bàn giao lên nhánh `docs/m1-tests-hai`, không tạo PR hoặc merge. Việt Đức chưa có QA Matrix nên phần đối chiếu còn chờ.
