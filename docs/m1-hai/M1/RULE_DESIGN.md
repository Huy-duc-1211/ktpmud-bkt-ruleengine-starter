# M1-02 — Thiết kế rule theo Issue #15

Nguồn T15: [comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248); [các thay đổi chi tiết](ISSUE15_SYNC.md), [danh mục nguồn](sources/README.md). T15 là làm rõ chính thức dùng chung Track A, ưu tiên hơn phần diễn giải mâu thuẫn của Requirements/ADR Revision 02. Tôi cập nhật thiết kế theo phản hồi này. Các đề xuất riêng của nhóm vẫn được ghi rõ để Huy review; phần runtime chưa triển khai.

## 1. Đầu vào, đầu ra và validation

Giữ classify(patient), chín tên khóa PatientInput và ba khóa kết quả muc_do/rule_id/ly_do. Context UUID/path không nằm trong PatientInput. TypedDict skeleton cần được đồng bộ nullable khi M2 triển khai, chưa sửa code trong lượt tài liệu.

| Dữ liệu | Chính sách hiện hành |
|---|---|
| tuoi thiếu/null | Không có dữ liệu; không TypeError do null. Selector trả THEO_DOI/null, reason thiếu tuổi. [T15 §§2,5] |
| HATT hiện tại/nền thiếu/null | Không có dữ liệu; không số đo mặc định; dùng bằng chứng sẵn có theo T15 §§3–5 |
| Boolean thiếu/null | Không gây exception vì thiếu/null; D13 ánh xạ UNKNOWN theo policy nhóm, bảo toàn mức đã đủ chứng minh. [T15 §5] |
| tuoi có giá trị khác null | Giữ policy nhóm int/float hữu hạn >=0, loại bool; sai kiểu TypeError, âm/NaN/Infinity ValueError |
| HATT hiện tại có số | Giữ int >=0, loại bool/float/chuỗi; sai kiểu TypeError, số âm ValueError |
| HATT nền có số | Giữ int >0, loại bool/float/chuỗi; sai kiểu TypeError, <=0 ValueError |
| Boolean khác null nhưng không bool | Giữ TypeError cho số/chuỗi; không ép kiểu |
| Khóa ngoài allowlist | Giữ ValueError |

Những miền số không phải null là policy nhóm Q/A mà T15 §6 cho phép công bố, không phải ngưỡng chẩn đoán. Kiểm mọi trường có mặt trước lựa chọn output; trường sai kiểu khác vẫn có thể lỗi dù một field thiếu/null được phép. Public invalid mapping áp dụng khi audit INVALID_INPUT thành công; lỗi kép vẫn ưu tiên lỗi audit. Hiện có **36 ca invalid: 28 TypeError+8 ValueError**; tám ca null trước kia bị coi invalid đã được sửa.

## 2. Biểu thức và ngưỡng không đổi

S=co_di_nguyen_nghi_ngo; I=di_nguyen_qua_duong_hit; K=co_ton_thuong_da_niem_mac; H=co_trieu_chung_ho_hap; C=co_trieu_chung_tuan_hoan; G=co_trieu_chung_tieu_hoa_nang.

- R01 = NOT S AND K AND (H OR C).
- R02 = S AND ít nhất 2 TRUE trong K/H/C/G.
- R03 = S AND ((NOT I AND H) OR C).
- P = R01 OR R02 OR R03. R-SOC cần phản vệ và bằng chứng tụt HATT theo tuổi.

| Tuổi | Tiêu chí HATT |
|---|---|
| 0 <= a <1 | b <70 |
| 1 <= a <11 | b <70+2*a |
| 11 <= a <18 | b <90 |
| a >=18 | b <90 OR giảm >30% so với nền |

Dấu < và > nghiêm ngặt, đúng 30% không đạt; không làm tròn tuổi. R03 giữ biểu thức khóa dị nguyên nghi ngờ, đường hít chỉ chặn hô hấp R03. Không thêm clinical rule/threshold. [D; T15 §§1,4]

## 3. Cách chọn kết quả theo D01–D03

1. Sau validation, tuổi thiếu/null -> THEO_DOI/null và reason thiếu tuổi, kể cả biểu hiện đủ rule hoặc HATT rất thấp. [T15 §2]
2. Có tuổi, phản vệ đủ kết luận và có bằng chứng tụt HATT -> SOC_PHAN_VE/R-SOC. [T15 §1]
3. Có tuổi, đủ phản vệ nhưng chưa có bằng chứng sốc (gồm thiếu/null HATT hoặc người lớn b>=90 thiếu/null nền) -> PHAN_VE. Không lấy UNKNOWN của điều kiện huyết áp làm lý do trì hoãn output. [T15 §§3–4]
4. Không sốc và có nhiều rule Tầng 2 TRUE: chọn đúng một mã theo R01-PV > R02-PV > R03-PV. Reason có thể nhắc rule đồng thời, không raw clinical data. [T15 §1]
5. Không đủ rule và không có kết luận bất biến theo policy dữ liệu thiếu: THEO_DOI, reason chưa đủ thông tin; không nói an toàn.

Null/missing của mỗi trường số phải cùng muc_do/rule_id; không nhất thiết cùng reason nguyên văn hoặc UUID. Nhánh giảm tương đối không đánh giá được vì thiếu nền coi là không thỏa ở bước chọn bằng chứng sốc, không gán baseline mặc định. [T15 §§4–5]

## 4. D13 — phân biệt thông tin và quyết định

Giữ Enum TRUE/FALSE/UNKNOWN và phép toán tường minh; không dùng if state hoặc Python truthiness của Enum. Null boolean nay như missing -> UNKNOWN theo policy nhóm, không còn TypeError. Toán tử không thay đổi:

| A | B | AND | OR |
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

NOT TRUE=FALSE; NOT FALSE=TRUE; NOT UNKNOWN=UNKNOWN. R02 T>=2 -> count TRUE; T+U<2 -> FALSE; còn lại UNKNOWN; sau đó AND S. R02 helper/count phải assert riêng trước priority để R03 không che lỗi.

HYPOTENSION UNKNOWN có thể ghi nhận thông tin huyết áp chưa đủ; SHOCK_EVIDENCE chỉ TRUE khi đã có bằng chứng, UNKNOWN thông tin cho SHOCK_EVIDENCE FALSE. Đây là “chưa chứng minh sốc”, không khẳng định huyết áp bình thường. Public selector phải áp dụng kết quả T15 §§2–4, không giữ pending D02/D03. [ISSUE15_SYNC §3]

Khi kết luận thực sự phụ thuộc boolean chưa biết, giữ policy nhóm D13 trả THEO_DOI với reason. Khi mọi completion đều đủ phản vệ dù không một rule riêng TRUE (S xuất hiện cả NOT S và S), thêm kiểm tra coverage để không hạ mức. **Cách chọn mã đại diện ở MISS-009 là đề xuất BOOL-COVERAGE còn chờ Huy review**. Tôi đề xuất cách chọn mã này; phần phê duyệt vẫn chờ Huy. Chi tiết và rủi ro tại [ISSUE15_SYNC.md](ISSUE15_SYNC.md). Enum semantics không đổi, không thêm output field/rule y khoa.

## 5. Luồng xử lý của classify() và helper

```text
Context/provider UUID + writer path ngoài PatientInput
  -> validate giá trị có mặt (cho phép null/missing theo T15)
  -> tuổi không có dữ liệu: chuẩn bị THEO_DOI/null, reason thiếu tuổi
  -> có tuổi: rule helpers Enum + coverage policy
     -> đủ phản vệ và SHOCK_EVIDENCE TRUE: SOC_PHAN_VE/R-SOC
     -> đủ phản vệ, chưa chứng minh sốc: PHAN_VE/mã rule theo policy đã nêu
     -> chưa đủ kết luận: THEO_DOI/null, reason thiếu thông tin
  -> audit CLASSIFY/SUCCESS hoàn tất rồi mới trả kết quả
Invalid khác: audit CLASSIFY/INVALID_INPUT rồi raise TypeError/ValueError
Audit lỗi: lỗi audit an toàn, không trả thành công
finally: reset/khôi phục ContextVar token
```

Giữ classify(patient) là entry point điều phối kể cả direct call; validation, R01/R02/R03, HATT/priority/explanation có helper tối thiểu và rule tách I/O. Tên/số helper là chi tiết M2, không framework/DB/plugin system. Pure helper được kiểm độc lập, không log dữ liệu thô hoặc thêm debug vào output.

## 6. Context, audit và xử lý lỗi

ContextVar token ngoài input: explicit session chung UUID trong scope; không session tạo UUID tạm mới từng call, reset trong finally kể cả exception. Không nhầm context mới độc lập với copy_context kế thừa. [A OPEN-01/02]

JSONL chỉ Timestamp ISO 8601 UTC, User_UUID synthetic hợp lệ, Action_Type CLASSIFY, Status SUCCESS hoặc INVALID_INPUT. Public output hợp lệ do null/missing phải audit SUCCESS; không ghi INVALID_INPUT chỉ vì null. Invalid khác + audit thành công raise đúng D04; lỗi audit, kể cả lỗi kép, ưu tiên lỗi audit an toàn. Không raw payload/message/chaining nhạy cảm, không thêm status/field.

Writer path ngoài input, độc lập cwd, runtime log ngoài repo, ownership/file riêng, V1 tuần tự. Mỗi record open append/write/close trước khi báo hoàn tất; lỗi open/write/flush/close được nhận biết, không retry vô hạn hoặc cam kết fsync/durability. Không mặc định ghi chung file concurrent-safe.

Default path mechanism A §5.4.1 còn PROPOSED; unexpected internal exception còn residual item. T15 không phê duyệt thay hai điểm này. [INTEGRATION_TEST_PLAN.md](../M2/INTEGRATION_TEST_PLAN.md) có kế hoạch kiểm và cập nhật nullable.

## 7. Test, benchmark và bàn giao

- CSV chung 157 ca (135 gốc +22 T15); Test ID trở về mã gốc để khớp các tài liệu review. Bảy PEND đã resolve; PEND/INV chỉ là mã lịch sử.
- 81 hàng logic/count/allergen không đổi phép toán, 22 regression/null-vs-missing đã gộp trong CSV chung và kiểm coverage tại [INTERNAL_STATE_TEST_PLAN.md](../M2/INTERNAL_STATE_TEST_PLAN.md).
- Nonfinite giữ fixture_ref/allowlist, ValueError tuổi không hữu hạn; không eval/runner ngoài repo.
- D10 không đổi: perf_counter_ns, 100 warm-up ngoài N>=1.000, nearest-rank p50/p95, full-path có audit I/O thật; chưa có số đo. [BENCHMARK_PLAN.md](../M2/BENCHMARK_PLAN.md)
- Việt Đức chưa có QA Matrix. Tôi giữ các ID INT/BENCH để đối chiếu khi matrix có; phần này chưa hoàn tất review chéo. Runtime, CI và benchmark chưa thực hiện.
