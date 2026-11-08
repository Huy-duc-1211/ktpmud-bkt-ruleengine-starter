# Yêu cầu và phạm vi Track A

| Thuộc tính | Giá trị |
|---|---|
| Cuộc thi | KTPMUD Hack Marathon 2026, Track A — Dr May Day: Rule Engine Sprint |
| Mã nhóm | `173820_n27` |
| Người phụ trách | Huy Đức |
| Mốc bàn giao | M1-01, Checkpoint 1, ngày 08/11/2026 |
| Trạng thái | Bản nháp Revision 01 để con người review, ngày 07/11/2026 |
| Mốc nguồn starter | `bkt-2026-v1` → `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| Mốc nguồn tích hợp | `track-a-development` tại `b65032f94ec3ce600df07d81b5df6b9b4bd203d1` |

**Quy ước nguồn.** FACT là yêu cầu từ nguồn chính thức hoặc hiện trạng đã kiểm tra. APPROVED DESIGN DECISION là quyết định nội bộ đã được Leader phê duyệt. PENDING ASSUMPTION là giả định đang cân nhắc, chưa đủ căn cứ để chốt kết quả nghiệm thu. Việc duyệt một hướng thiết kế không xác nhận chức năng đã triển khai hoặc tài liệu đã được nghiệm thu.

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

Danh sách cho phép gồm đúng chín tên khóa dưới đây. Việc cho phép một tên khóa khác với yêu cầu khóa đó luôn hiện diện. Null là giá trị của một khóa có mặt, còn missing là khóa vắng mặt. `TypedDict(total=False)` hiện có mô tả khóa có thể vắng mặt cho công cụ kiểm tra kiểu, chưa thực thi validation khi chạy. [D dòng 8–23, 45–47; C dòng 11–21]

| Tên trường chính xác | Kiểu theo nguồn chính thức | Mô tả | Chính sách null | Validation và khóa vắng mặt | Nguồn |
|---|---|---|---|---|---|
| `tuoi` | `float`, đơn vị năm | Tuổi, cho phép số lẻ như `0.5` | Nhóm xác định null là invalid | Nhóm nhận `int` hoặc `float` hữu hạn ≥ 0, loại `bool`, không ép chuỗi. Tuổi 0 thuộc nhóm tuổi đầu tiên. Kết quả khi thiếu tuổi và Tầng 2 khớp còn D02 pending. | D dòng 12, 30–35, 45–47; D04; L |
| `huyet_ap_tam_thu` | `int` hoặc null | HATT hiện tại, mmHg | Cho phép, nghĩa là chưa đo được | Nhóm nhận `int` ≥ 0 hoặc `None`, loại `bool`, chuỗi và số thực. Không đặt giới hạn trên. Khóa vắng mặt không được coi là HATT bình thường. Kết quả khi Tầng 2 khớp còn D03 pending. | D dòng 13, 27–35; D04; L |
| `huyet_ap_tam_thu_nen` | `int` hoặc null | HATT nền, dùng nhánh giảm tương đối ở tuổi ≥ 18 | Cho phép | Nếu có số thì phải là `int` > 0, loại `bool`, không ép kiểu hoặc đặt giới hạn trên. Thiếu khóa hoặc `None` nghĩa là không có dữ liệu nền cho nhánh giảm tương đối. Không dùng nền 0 làm mẫu số. | D dòng 14, 35; D04; L |
| `co_di_nguyen_nghi_ngo` | `bool` | Có dị nguyên nghi ngờ | Null là invalid | Có khóa thì phải đúng kiểu bool. Khóa vắng mặt là UNKNOWN trong đánh giá nội bộ D13. | D dòng 15, 41–43; L |
| `di_nguyen_qua_duong_hit` | `bool` | Dị nguyên qua đường hít | Null là invalid | Bool hoặc khóa vắng mặt theo D13. Ảnh hưởng nhánh hô hấp của R03. | D dòng 16, 43; L |
| `co_ton_thuong_da_niem_mac` | `bool` | Tổn thương da/niêm mạc | Null là invalid | Bool hoặc khóa vắng mặt theo D13. | D dòng 17, 41–42; L |
| `co_trieu_chung_ho_hap` | `bool` | Triệu chứng hô hấp | Null là invalid | Bool hoặc khóa vắng mặt theo D13. | D dòng 18, 41–43; L |
| `co_trieu_chung_tuan_hoan` | `bool` | Triệu chứng tuần hoàn | Null là invalid | Bool hoặc khóa vắng mặt theo D13. | D dòng 19, 41–43; L |
| `co_trieu_chung_tieu_hoa_nang` | `bool` | Triệu chứng tiêu hóa nặng | Null là invalid | Bool hoặc khóa vắng mặt theo D13. | D dòng 20, 42; L |

### 3.1. Chính sách validation đã được Leader duyệt

**APPROVED DESIGN DECISION D04 và bổ sung Revision 01.** Các miền số học trong bảng là chính sách kiểm tra dữ liệu của nhóm, không phải ngưỡng chẩn đoán mới. Giữ nguyên các ngưỡng phân loại ở phần 4. Không chấp nhận khóa ngoài danh sách chín trường. Input sai kiểu hoặc ngoài miền phải có lỗi được kiểm soát. Không đưa giá trị lâm sàng hoặc thông tin nhạy cảm vào thông báo lỗi, audit hay log. Không đổi dữ liệu sai thành UNKNOWN. Không tự chuyển chuỗi thành số hoặc boolean, hoặc chuyển `0`/`1` thành bool. [D dòng 22–23; E §7.3 A-04; G D04; L]

Phân biệt missing, explicit null và invalid trong toàn bộ xử lý. Kiểu lỗi cụ thể như `TypeError`, `ValueError` và cơ chế xử lý chi tiết sẽ được ghi trong thiết kế/ADR. Requirements chưa định nghĩa thêm API lỗi. [L]

### 3.2. D13 — Đánh giá input một phần bằng logic ba trạng thái

**APPROVED DESIGN DECISION D13.** Đây là chính sách suy luận nội bộ do Leader duyệt trong Revision 01. Với sáu trường boolean, không bắt buộc phải cung cấp đủ cả sáu khóa. [L]

| Dữ liệu nhận được | Cách xử lý |
|---|---|
| Có khóa với `True` | TRUE |
| Có khóa với `False` | FALSE |
| Khóa vắng mặt | UNKNOWN ở tầng đánh giá nội bộ |
| Có khóa với `None`/null, số hoặc chuỗi | Invalid, xử lý bằng validation |

UNKNOWN chỉ biểu diễn việc thiếu thông tin trong đánh giá nội bộ. Input vẫn theo chín khóa và các kiểu đã nêu. Output vẫn có ba nhãn quy định ở phần 5. Huyết áp được phép null theo Data Dictionary và được xử lý riêng với boolean. [D dòng 8–23, 49–55; L]

## 4. Yêu cầu phân loại

### 4.1. Yêu cầu chức năng

| ID | Yêu cầu | Phân loại nguồn và căn cứ |
|---|---|---|
| FR-01 | Thực thi `classify(patient)` theo hợp đồng đã khóa. Kết quả dựa trên các trường được phép, độc lập với ID của dữ liệu kiểm thử công khai. | FACT — C dòng 24–36; E §7.3 A-01–A-02 |
| FR-02 | R01-PV khớp khi `co_di_nguyen_nghi_ngo = false` **VÀ** `co_ton_thuong_da_niem_mac = true` **VÀ** (`co_trieu_chung_ho_hap = true` **HOẶC** `co_trieu_chung_tuan_hoan = true`). | FACT — D dòng 41. D13 quy định cách đánh giá khóa boolean vắng mặt. |
| FR-03 | R02-PV khớp khi `co_di_nguyen_nghi_ngo = true` **VÀ** ít nhất hai trong bốn nhóm da/niêm mạc, hô hấp, tuần hoàn, tiêu hóa nặng là true. | FACT — D dòng 42. D13 quy định cách xác định trạng thái điều kiện đếm khi thiếu dữ liệu. |
| FR-04 | R03-PV khớp khi `co_di_nguyen_nghi_ngo = true` **VÀ** ((`di_nguyen_qua_duong_hit = false` **VÀ** `co_trieu_chung_ho_hap = true`) **HOẶC** `co_trieu_chung_tuan_hoan = true`). Dùng đúng trường dị nguyên nghi ngờ trong biểu thức. | FACT — D dòng 43. Giữ nguyên ngoặc và AND/OR khi áp dụng D13. |
| FR-05 | R-SOC khớp khi ít nhất một rule Tầng 2 khớp **VÀ** có tụt HATT theo nhóm tuổi trong bảng dưới. Thiếu dữ liệu cần để xác định điều kiện huyết áp không tự chứng minh R-SOC là FALSE. | FACT — D dòng 25–35. APPROVED DESIGN DECISION — D13. Các đầu ra chịu D02–D03 vẫn pending. |
| FR-06 | Ưu tiên Tầng 1. Khi R-SOC chắc chắn TRUE, trả `SOC_PHAN_VE`. Khi không đạt sốc và Tầng 2 khớp theo dữ liệu đủ kết luận, trả `PHAN_VE`. Khi không có rule Tầng 2 chắc chắn TRUE, D13 dự kiến `THEO_DOI` với lý do phản ánh chưa khớp hoặc chưa đủ thông tin. Khi Tầng 2 TRUE nhưng kết quả cuối còn chịu D01–D03, giữ pending theo phần 9. | FACT — D dòng 25–47. APPROVED DESIGN DECISION — D13. |
| FR-07 | Áp dụng validation ở phần 3 và đánh giá input một phần theo D13 ở phần 4.2. Chỉ khóa boolean vắng mặt mới được biểu diễn UNKNOWN theo chính sách này. Phân biệt thiếu khóa, null được phép và invalid. D02–D03 tiếp tục chi phối các trường hợp chưa rõ về tuổi/HATT. | FACT — D dòng 8–23, 45–47; E §7.3 A-04. APPROVED DESIGN DECISION — D04, D13, L. |
| FR-08 | Trả schema phần 5. Giải thích ngắn, truy vết rule được chọn hoặc tình trạng chưa đủ điều kiện/thông tin, không chứa dữ liệu lâm sàng thô hoặc lời khuyên điều trị. | FACT — D dòng 49–55; E §7.3 A-05. APPROVED DESIGN DECISION — D06, D13. |
| FR-09 | Mỗi lần phân loại ghi audit đúng `Timestamp`, `User_UUID`, `Action_Type`, `Status`. Không ghi input lâm sàng thô, triệu chứng, điểm sức khỏe hoặc dữ liệu định danh. D08 mở rộng audit nội bộ cho lần thử input lỗi bằng trạng thái tổng quát. | FACT — E §§7.2–7.3 A-06. APPROVED DESIGN DECISION — D07–D08. |

| Tuổi tính bằng năm | Điều kiện tụt HATT cho FR-05 |
|---|---|
| 0 ≤ tuổi < 1 | HATT < 70 mmHg |
| 1 ≤ tuổi < 11 | HATT < 70 + 2 × tuổi, đơn vị mmHg |
| 11 ≤ tuổi < 18 | HATT < 90 mmHg |
| Tuổi ≥ 18 | HATT < 90 mmHg **HOẶC** giảm > 30% so với HATT nền |

Các so sánh là nghiêm ngặt. Bằng đúng ngưỡng không thỏa nhánh so sánh đó. Ở người lớn, nhánh còn lại của HOẶC vẫn có thể thỏa. HATT thấp đơn độc chưa đủ kết luận R-SOC vì còn điều kiện Tầng 2. `THEO_DOI` là trạng thái chưa đủ dữ kiện kết luận theo bảng. [D dòng 25–47]

### 4.2. Nguyên tắc đánh giá ba trạng thái theo D13

Giữ nguyên biểu thức của R01/R02/R03. Với AND, có một vế FALSE thì kết quả FALSE, mọi vế TRUE thì kết quả TRUE, các trường hợp còn lại UNKNOWN. Với OR, có một vế TRUE thì kết quả TRUE, mọi vế FALSE thì kết quả FALSE, các trường hợp còn lại UNKNOWN. Phủ định TRUE thành FALSE, FALSE thành TRUE và UNKNOWN vẫn là UNKNOWN. [L]

| Biểu thức minh họa | Trạng thái nội bộ |
|---|---|
| TRUE OR UNKNOWN | TRUE |
| FALSE OR UNKNOWN | UNKNOWN |
| FALSE AND UNKNOWN | FALSE |
| TRUE AND UNKNOWN | UNKNOWN |

Với điều kiện ít nhất hai hệ của R02, gọi T là số hệ chắc chắn TRUE và U là số hệ UNKNOWN. Nếu T ≥ 2 thì điều kiện đếm TRUE. Nếu T + U < 2 thì điều kiện đếm FALSE. Các trường hợp còn lại UNKNOWN. Tiếp tục kết hợp điều kiện đếm với `co_di_nguyen_nghi_ngo` bằng AND đúng như bảng gốc. [D dòng 42; L]

Rule TRUE xác nhận khớp, FALSE xác nhận không khớp, UNKNOWN là chưa đủ dữ liệu kết luận rule đó. Nếu Tầng 2 chắc chắn TRUE, tiếp tục xét Tầng 1. Không tự coi dữ liệu tuổi/HATT thiếu là bằng chứng R-SOC FALSE để chốt `PHAN_VE`. D13 không giải quyết D02 hoặc D03. Việc chọn một `rule_id` khi R02 và R03 cùng TRUE vẫn chịu D01. [L; I]

### 4.3. Quyết định nội bộ đã duyệt và ràng buộc chính thức

| ID | Nội dung | Yêu cầu liên quan |
|---|---|---|
| D04 | Validation nghiêm ngặt theo phần 3, cùng các chi tiết được Leader duyệt trong Revision 01. | FR-07 |
| D05 | Giữ `classify(patient)`, tách ít hàm hỗ trợ với trách nhiệm rõ. | FR-01; NFR-04 |
| D06 | Dùng mẫu `ly_do` gắn rule, không dùng LLM, không có dữ liệu thô hoặc khuyên điều trị. | FR-08; NFR-07 |
| D07 | Audit writer riêng, JSON Lines, UUID giả lập theo phiên người thao tác nằm ngoài `PatientInput`. | FR-09; NFR-03 |
| D08 | Audit xử lý thành công và lần thử input lỗi, chỉ trạng thái tổng quát, không payload hoặc exception lộ input. | FR-09; NFR-03 |
| D09 | Kiểm thử ca thường, biên, invalid, missing, overlap, output, audit, gồm tuổi số lẻ. D13 bổ sung căn cứ cho kiểm chứng thiếu boolean. | NFR-05 |
| D10 | Đo toàn luồng `classify()` và báo riêng phép đo phụ logic thuần. | NFR-01 |
| D13 | Cho phép boolean vắng mặt, đánh giá TRUE/FALSE/UNKNOWN như phần 3.2 và 4.2, giữ D01–D03 pending. | FR-02–FR-08; NFR-05 |

D04–D10 có căn cứ G §5 và P §3. L là căn cứ phê duyệt D13 và chi tiết validation mới. D11 giữ nguyên ràng buộc không đổi clinical rule/ngưỡng. D12 giữ danh sách chín khóa input, ba khóa output, bốn trường audit và giới hạn dữ liệu theo đề. D01–D03 được theo dõi riêng ở phần 9. [D dòng 8–62; E §§5, 7; G §5; L]

## 5. Hợp đồng dữ liệu đầu ra

Mọi kết quả phân loại trả về có đúng ba khóa dưới đây. Lỗi validation được xử lý bằng cơ chế có kiểm soát theo FR-07, chi tiết thuộc ADR. [D dòng 49–55; C dòng 24–27; L]

| Trường | Kiểu | Giá trị và điều kiện |
|---|---|---|
| `muc_do` | Chuỗi | `SOC_PHAN_VE`, `PHAN_VE` hoặc `THEO_DOI` theo FR-06, với các trường hợp D01–D03 ở trạng thái pending. |
| `rule_id` | Chuỗi hoặc null | `R-SOC` cho Tầng 1. `R01-PV`, `R02-PV` hoặc `R03-PV` cho rule Tầng 2 được chọn. Chọn mã khi R02/R03 cùng khớp còn D01 pending. Null là giá trị không có rule cho `THEO_DOI`. |
| `ly_do` | Chuỗi | Giải thích ngắn gắn rule hoặc tình trạng chưa khớp/chưa đủ thông tin. Không chứa giá trị lâm sàng thô hoặc lời khuyên điều trị. |

Từ “reason” trong đề tương ứng khóa `ly_do` của contract. UNKNOWN chỉ dùng nội bộ và không được thêm vào các giá trị `muc_do` hoặc `rule_id`. [D dòng 49–55; E §7.3 A-05; L]

## 6. Yêu cầu phi chức năng

| ID | Yêu cầu | Bằng chứng kiểm chứng dự kiến | Nguồn |
|---|---|---|---|
| NFR-01 | Benchmark ít nhất 1.000 lần đo sau warm-up, báo p50/p95 và máy đo, p95 < 100 ms. Theo D10, nêu riêng phép đo toàn luồng và phép đo phụ logic thuần. | Phương pháp tái lập, môi trường, số lần đo và các phân vị quan sát được | E §7.3 A-10; G D10 |
| NFR-02 | Chỉ dùng dữ liệu synthetic. Không có PII, dữ liệu bệnh nhân thật, thông tin xác thực hoặc secret trong input, dữ liệu test, log và hồ sơ bàn giao. | Review bảo mật/riêng tư trên file được theo dõi và bằng chứng sinh ra | D dòng 22–23; E §§5, 7 |
| NFR-03 | Giữ đúng bốn trường audit cho thành công và input lỗi theo D07–D08, UUID phiên giả lập, không payload thô. Thông báo lỗi và log cũng phải tránh lộ input. | Kiểm tra schema, trạng thái và dữ liệu bị cấm trong audit giả lập và thông báo lỗi | E §§7.2–7.3 A-06; G D07–D08; L |
| NFR-04 | Giữ interface phân loại ổn định, logic dễ đọc và review theo bảng quyết định, mô tả rõ chính sách D13 khi đánh giá dữ liệu thiếu. | Review interface và truy vết từ rule/yêu cầu đến triển khai | E §§7.1, 9; G D05; L |
| NFR-05 | Có unit tests cho normal, boundary, invalid, missing cùng phạm vi D09, D13. Chạy `pytest -q` đạt từ checkout sạch. Những kết quả chịu D01–D03 vẫn chờ xác nhận. | Bộ test được review, báo cáo chạy từ checkout sạch, ghi rõ phần pending | E §7.3 A-07–A-08; G D09; L |
| NFR-06 | GitHub Actions chạy test trên Pull Request. | Cấu hình workflow và liên kết lượt chạy PR có bước test thực tế | E §7.3 A-09; W |
| NFR-07 | Giải thích dễ hiểu, truy vết được và phản ánh đúng rule hoặc mức thiếu thông tin, không lộ dữ liệu lâm sàng thô hay hướng dẫn điều trị. | Review output đại diện theo contract và D13 | D dòng 49–55; E §7.3 A-05; G D06; L |
| NFR-08 | Có hướng dẫn cài/chạy/test tái lập, disclaimer chính xác trong README và hồ sơ tài liệu/bàn giao theo các mốc đề yêu cầu. | README và tài liệu yêu cầu, quyết định, kiểm thử, bảo mật/riêng tư, AI-use, đóng góp | E §§4–6, 7.3 A-11, 11 |

## 7. Tiêu chí nghiệm thu

Trạng thái mô tả bằng chứng hiện có tại mốc nguồn đã ghi. NOT IMPLEMENTED nghĩa là chưa có chức năng hoặc tài liệu yêu cầu. PARTIALLY AVAILABLE nghĩa là có hỗ trợ ban đầu nhưng thiếu nội dung hoặc bằng chứng nghiệm thu. PENDING CLARIFICATION nghĩa là có chi tiết contract đang chờ làm rõ. VERIFIED chỉ dùng khi đủ bằng chứng. Bản nháp này chưa đánh dấu AC nào VERIFIED.

| AC | Yêu cầu | Điều kiện nghiệm thu | Bằng chứng cần có | Nguồn | Trạng thái hiện tại |
|---|---|---|---|---|---|
| A-01 | Phân loại đúng contract | `classify()` thực thi contract và hết `NotImplementedError` của starter. | Review ánh xạ rule–code và kết quả test nghiệp vụ | E §7.3 A-01; D; C dòng 30–36 | NOT IMPLEMENTED |
| A-02 | Không hard-code theo ID fixture | Kết quả dựa trên trường đặc tả, độc lập với ID public fixture. | Review triển khai và ví dụ synthetic độc lập | E §7.3 A-02; C dòng 11–36 | NOT IMPLEMENTED — chưa có thuật toán phân loại để đánh giá |
| A-03 | Đủ các mức phân loại | Bao phủ các mức kết quả theo bảng. | Kiểm thử Tầng 1, Tầng 2 và `THEO_DOI` | E §7.3 A-03; D dòng 25–55 | NOT IMPLEMENTED |
| A-04 | Policy validation công bố và thực thi | Xử lý missing, sai kiểu, ngoài miền theo policy ở phần 3–4, gồm D13. Phần chịu D02–D03 phải được làm rõ trước khi chốt kỳ vọng. | Policy được review, triển khai và test tương ứng | E §7.3 A-04; D dòng 8–23, 45–47; L | NOT IMPLEMENTED, kèm PENDING CLARIFICATION cho D02–D03. D04/D13 đã được duyệt về hướng xử lý, chưa có implementation/test evidence. |
| A-05 | Giải thích truy vết được | `ly_do` gắn rule, không điều trị hoặc input thô. | Output được kiểm tra theo contract | E §7.3 A-05; D dòng 49–55 | NOT IMPLEMENTED |
| A-06 | Audit bốn trường an toàn | Chỉ bốn trường cho phép, không input lâm sàng thô. | Kiểm tra schema và riêng tư của audit synthetic | E §§7.2–7.3 A-06 | NOT IMPLEMENTED |
| A-07 | Unit tests đủ nhóm ca | Có normal, boundary, invalid và missing. | Bộ test nghiệp vụ được review và liên kết yêu cầu | E §7.3 A-07; T dòng 9–17 | PARTIALLY AVAILABLE — chỉ có test minh họa mong đợi `NotImplementedError`, chưa có bộ test nghiệp vụ đáp ứng A-07. |
| A-08 | Test đạt từ checkout sạch | `pytest -q` đạt trên bản checkout sạch với bộ test nghiệp vụ. | Lệnh, môi trường và kết quả chạy được ghi nhận | E §7.3 A-08; R dòng 16–21 | PARTIALLY AVAILABLE — có lệnh, chưa có bằng chứng clean-checkout test nghiệp vụ đạt. |
| A-09 | CI trên PR | GitHub Actions thực sự chạy test cho PR. | Liên kết PR run có bước test | E §7.3 A-09; W dòng 1–12 | PARTIALLY AVAILABLE — có cấu hình, còn thiếu bằng chứng PR run thực tế. |
| A-10 | Benchmark đúng yêu cầu | ≥ 1.000 lần sau warm-up, ghi máy đo, p50/p95, p95 < 100 ms. | Phương pháp và số liệu benchmark | E §7.3 A-10; R dòng 27 | NOT IMPLEMENTED — README mới nêu mục tiêu |
| A-11 | Disclaimer trong README | Có chính xác `educational/synthetic — not for clinical use`. | Kiểm tra README | E §7.3 A-11; R | NOT IMPLEMENTED |

Test mẫu hiện mong đợi `NotImplementedError`. Nếu test mẫu đạt, bằng chứng chỉ xác nhận trạng thái stub. D13 đã được Leader duyệt nhưng vẫn cần triển khai, test và human review trước nghiệm thu. [T dòng 9–17; L]

## 8. Truy vết yêu cầu

| ID yêu cầu | Rule hoặc AC liên quan | Kiểm chứng dự kiến ở mức yêu cầu |
|---|---|---|
| FR-01 | A-01, A-02 | Review interface, tính độc lập với fixture và kết quả hành vi. |
| FR-02 | R01-PV, A-01, A-03, A-07 | Kiểm tra các phép VÀ, hai nhánh HOẶC và áp dụng D13 mà giữ biểu thức gốc. |
| FR-03 | R02-PV, A-01, A-03, A-07 | Kiểm tra điều kiện hai trong bốn và kết hợp dị nguyên, gồm cách đếm TRUE/UNKNOWN theo D13. |
| FR-04 | R03-PV, A-01, A-03, A-07 | Kiểm tra ngoặc, phủ định đường hít và nhánh tuần hoàn với logic ba trạng thái. |
| FR-05 | R-SOC, A-01, A-03, A-07 | Kiểm tra nhóm tuổi, ranh giới nghiêm ngặt, hai nhánh người lớn và điều kiện Tầng 2. Không suy FALSE chỉ vì thiếu dữ liệu, giữ D02–D03 pending. |
| FR-06 | Ưu tiên tầng, `THEO_DOI`, A-01, A-03, A-07 | Kiểm tra kết luận khi rule TRUE/FALSE/UNKNOWN, ưu tiên sốc và giữ kết quả chịu D01–D03 ở trạng thái chờ. |
| FR-07 | A-04, A-07 | Review policy D04/D13 và phân biệt missing, null, invalid, khóa thừa, miền số học. |
| FR-08, NFR-07 | A-05 | Kiểm tra ba khóa, liên kết rule và cách diễn đạt thiếu thông tin, không dữ liệu thô. |
| FR-09, NFR-02–03 | A-06; E §5 | Kiểm tra đúng schema audit, dữ liệu giả lập và sự vắng mặt của dữ liệu bị cấm trong log/lỗi. |
| NFR-01 | A-10 | Review phương pháp và bằng chứng phép đo. |
| NFR-04 | A-01, A-02; E §9 | Review tính tương thích interface và ánh xạ rule/yêu cầu đến code. |
| NFR-05 | A-07, A-08 | Review phạm vi test D09/D13 và bằng chứng chạy từ checkout sạch. |
| NFR-06 | A-09 | Kiểm tra cấu hình và lượt test thực tế trên PR. |
| NFR-08 | A-11; E §§6, 11 | Kiểm tra disclaimer và hồ sơ bàn giao bắt buộc. |

Bảng này giữ mức truy vết yêu cầu. Test case và ma trận QA chi tiết do các phần việc M1-02/M1-03 cung cấp. [P §3]

## 9. Câu hỏi mở và giả định

**FACT.** Kiểm tra Issue #15 ngày 07/11/2026 chưa thấy bình luận phản hồi. D01–D03 giữ `PENDING TA CONFIRMATION`. [I]

| ID | Câu hỏi đang chờ | PENDING ASSUMPTION trong hướng dẫn nội bộ |
|---|---|---|
| D01 | Khi R02 và R03 cùng TRUE, không đạt Tầng 1, chọn một `rule_id` nào? | Tạm ưu tiên R02 trước R03 theo thứ tự bảng. Chưa được thầy/TA xác nhận. |
| D02 | Thiếu `tuoi` nhưng Tầng 2 khớp thì `THEO_DOI` hay `PHAN_VE`? | Tạm `THEO_DOI` theo đoạn nhắc thiếu tuổi. D13 không chốt trường hợp này. |
| D03 | HATT hiện tại null hoặc thiếu khóa, Tầng 2 khớp thì trả gì? Có cần phân biệt null và thiếu khóa? | Dự kiến `PHAN_VE` cho null được phép, trường hợp thiếu khóa còn chờ policy theo xác nhận TA. D13 không chốt kết quả. |

**D03 — trường hợp bổ sung cần làm rõ, `PENDING TA CONFIRMATION`.** Với người từ 18 tuổi trở lên, Tầng 2 chắc chắn TRUE, HATT hiện tại ≥ 90 mmHg nhưng thiếu HATT nền, chưa thể xác định nhánh giảm > 30% so với nền. Nhánh HATT tuyệt đối không thỏa chưa đủ để kết luận không có sốc khi nhánh tương đối chưa xác định. Kết quả cuối vẫn chờ TA xác nhận, chưa chốt `PHAN_VE` hoặc `THEO_DOI`. Đây là phần mở rộng câu hỏi D03 của TASK 02A.5, chưa được gửi bổ sung vào Issue #15.

Leader đã chốt cho phép boolean vắng mặt, miền validation số học và từ chối khóa thừa trong Revision 01. Các nội dung này thay thế phần chưa rõ tương ứng trong Revision 00. Chưa có phản hồi TA xác nhận D01–D03 hoặc D13 như một diễn giải chính thức. Khi phản hồi ảnh hưởng cách kết luận đã mô tả, cần báo Leader để đối chiếu trước khi cập nhật yêu cầu. [L; I]

Các chi tiết còn thuộc thiết kế/ADR gồm cách dùng `TypeError`/`ValueError`, truyền UUID phiên ngoài `PatientInput`, xử lý lỗi ghi audit, chuẩn hóa `Timestamp`/`Action_Type`/`Status`, phương pháp tính phân vị và phạm vi đo toàn luồng. D07–D10 đã được duyệt về định hướng, các chi tiết này chưa được tài liệu hóa đầy đủ.

Tên R03 trong bảng nói “dị nguyên đã biết” nhưng biểu thức dùng `co_di_nguyen_nghi_ngo`. FR-04 giữ nguyên biểu thức. Không bổ sung khóa để diễn giải lại tiêu đề. D13 là chính sách nội bộ mở rộng cách đánh giá thông tin thiếu, không được gán thành quy tắc giảng viên đã ban hành. Tại lần đối chiếu này chưa thấy mâu thuẫn trực tiếp với biểu thức trên input đầy đủ, nhưng việc tương thích với các diễn giải còn chờ TA vẫn cần được theo dõi. [D dòng 43; L; I]

## 10. Rủi ro, phụ thuộc và tài liệu tham chiếu

| Rủi ro | Phụ thuộc hoặc hoạt động review |
|---|---|
| Sai ngoặc, nhóm tuổi hoặc dấu so sánh | Đối chiếu FR-02–FR-06 với bảng đã khóa và review độc lập kỳ vọng biên. |
| Triển khai khác bảng quyết định | Giữ ánh xạ rule–yêu cầu và kiểm tra thay đổi theo nguồn đã chốt. |
| Đánh đồng UNKNOWN với False hoặc đổi invalid thành UNKNOWN | Review D13, validation và ranh giới giữa trạng thái nội bộ với output. |
| D13 vô tình chốt D02–D03 khi Tầng 2 TRUE | Giữ dấu pending ở FR-05–FR-07, A-04 và truy vết, đợi xác nhận TA. |
| Phản hồi làm rõ đến muộn | Theo dõi Issue #15, ghi rõ phần bị ảnh hưởng và cập nhật sau xác nhận. |
| Test thiếu hoặc nhầm test mẫu/cấu hình CI là bằng chứng nghiệm thu | Yêu cầu test nghiệp vụ, kết quả checkout sạch, PR run và benchmark thực tế theo AC. |
| Chậm phối hợp yêu cầu, thiết kế test và QA | Dùng ID yêu cầu để bàn giao phát hiện giữa M1-01, M1-02, M1-03. |
| Dùng đầu ra AI chưa kiểm chứng | Review theo nguồn và ghi công cụ, phạm vi, bằng chứng, quyết định giữ/sửa/loại, người chịu trách nhiệm trong hồ sơ AI-use. |

| Ký hiệu | Nguồn và phiên bản |
|---|---|
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung hiển thị v1.0.2 dù tên URL ghi v1.0.0, đối chiếu ngày 07/11/2026. Áp dụng §§4–7, 9, 11–12. |
| D | [Decision Table V1](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md), tag starter chính thức `bkt-2026-v1`. |
| G | [Project Guide](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/PROJECT_GUIDE.md), mốc nguồn tích hợp, đặc biệt §§3–5. |
| P | [Team Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/docs/TEAM_PLAN.md), mốc nguồn tích hợp, đặc biệt §3. |
| C | [Interface classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/rule_engine/classifier.py), mốc nguồn tích hợp. |
| T | [Test mẫu starter](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/tests/test_classifier.py), mốc nguồn tích hợp. |
| W | [Workflow GitHub Actions](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/.github/workflows/test.yml), mốc nguồn tích hợp. |
| R | [README starter](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/b65032f94ec3ce600df07d81b5df6b9b4bd203d1/README.md), mốc nguồn tích hợp. |
| I | [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15), kiểm tra ngày 07/11/2026. |
| L | Yêu cầu TASK 02A — REVISION 01 của Leader Huy Đức trong hội thoại ngày 07/11/2026, phê duyệt D13, chi tiết validation, tiếng Việt và cách ghi trạng thái AC. Chưa có URL repository cho nguồn phê duyệt này. |

Đề thi và Decision Table có thẩm quyền đối với yêu cầu bắt buộc. Tài liệu nhóm và yêu cầu Revision 01 ghi nhận quyết định nội bộ. Mọi xung đột ảnh hưởng hành vi phải báo Leader và hỏi giảng viên/TA khi cần.
