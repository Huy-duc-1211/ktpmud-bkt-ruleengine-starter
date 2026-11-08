# R02/D13 và selection theo Issue #15

Nguồn: D và [T15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248); Q/A Enum/toán tử vẫn áp dụng khi không mâu thuẫn T15. Chưa có helper/runtime được triển khai.

## 1. Hai lớp assertion

Pure helper assert Enum identity trước lựa chọn output; public integration assert mức/mã/reason/audit. Internal assertions trong CSV là notation test, không schema mới. Không assert truthiness, không dùng public output để chứng minh R02 đúng. Tên helper/điểm quan sát tối giản chốt ở M2; không mở public debug API hay log raw input.

## 2. Bảng logic và cách kiểm R02 riêng

INTERNAL_STATE_CASES.csv giữ 81 hàng: 9 AND+9 OR+3 NOT, 15 cặp T/U khả thi, 45 kết hợp count với S. Rule R02=AND(S,count). Enum logic không đổi vì raw boolean null được ánh xạ UNKNOWN như missing.

RULE-009–013 kiểm 0–4 hệ; sáu PAIR assert count/R02 TRUE kể cả R03 hoặc R-SOC đã che. RULE-014/016/017 assert R02 FALSE nhưng R03 TRUE; MISS-010/011/012 assert R02 TRUE/FALSE/UNKNOWN tương ứng T/U. MISS-013/014 giữ R02 UNKNOWN trong khi R03 TRUE.

## 3. Raw nullable và quyết định HATT

True/False -> Enum TRUE/FALSE; missing/null bool -> UNKNOWN trong policy nhóm; số/chuỗi không bool -> TypeError. Không dùng các ca boolean null làm expected exception. Tám ca INV đã đổi oracle nullable, AUD-002 đổi fixture sang chuỗi.

HYPOTENSION UNKNOWN là diagnostic thiếu thông tin, không bằng chứng sốc. SHOCK_EVIDENCE chỉ TRUE khi HYPOTENSION TRUE, còn FALSE/UNKNOWN cho FALSE ở bước chứng minh sốc. Không kết luận dữ liệu đo bình thường và không giữ public pending:

- PEND-002/007 thiếu tuổi -> THEO_DOI/null, dù có đủ phản vệ.
- PEND-003/004 thiếu HATT, có tuổi/R01 đủ -> PHAN_VE/R01-PV.
- PEND-005/006 nền thiếu, b>=90 -> PHAN_VE/R02-PV; nhánh tương đối chưa đánh giá được không làm thỏa sốc.
- Người lớn b<90 vẫn có bằng chứng sốc dù nền thiếu nếu phản vệ đủ. Không cần bịa nền.
- PEND-001 R02/R03 TRUE, không sốc -> PHAN_VE/R02-PV đúng thứ tự thầy chốt.

## 4. Coverage khi S xuất hiện cả hai nhánh

Không chỉ OR kết quả Enum của từng rule rồi hạ THEO_DOI: MISS-009 có R01/R02 UNKNOWN nhưng mọi completion S=True/False đều phản vệ. Thêm test coverage các rule gốc và tách policy chọn mã đại diện: [ISSUE15_SYNC §4](../M1/ISSUE15_SYNC.md). Bảo toàn mức, mã nhóm đề xuất còn Leader review, không gán là thầy chỉ định R01 trong mọi input thiếu S.

CSV chung TEST_CASES.csv có 157 ca; 22 dòng có Equivalence group là 11 cặp null-vs-missing đã gộp. Các cặp so cùng muc_do/rule_id và không raise do nullable; hai record không bắt buộc cùng UUID. Cặp no-downgrade-shock phải giữ SOC_PHAN_VE/R-SOC; cặp phụ thuộc đường hít giữ THEO_DOI theo D13 nhóm, nêu rõ rủi ro bỏ sót khi chưa biết I.

## 5. Kết quả cần ghi khi triển khai M2

Khi triển khai M2, cần ghi test ID, tên test/helper, kết quả chạy và người review. Kiểm đủ 81 ca logic, assertion riêng của từng case, coverage S, nullable và thứ tự chọn rule. Chỉ đánh dấu AC VERIFIED khi có kết quả chạy tương ứng.
