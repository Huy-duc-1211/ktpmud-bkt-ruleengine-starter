# M1-02 — Kế hoạch và chỉ mục test

**135 ca được thiết kế; 0 ca chạy trên engine**

## 1. Cách đọc và sử dụng

- CSV chứa đủ Test ID—Scenario—Input—Expected—AC—Nguồn—Trạng thái; các ô Input/Expected chứa JSON khi biểu diễn được bằng JSON chuẩn.
- Mỗi input JSON được mở rộng từ BASE_INPUT rồi lưu đầy đủ, trừ đúng các khóa bị bỏ ở ca missing. Không cần đoán các trường còn lại.
- Ba ca NaN/Infinity dùng biểu thức Python vì JSON chuẩn không hỗ trợ; BASE_INPUT được định nghĩa tại mục 2 bên dưới. Không eval chuỗi tự động.
- Expected classification khóa hai giá trị muc_do/rule_id và hợp đồng ly_do; không cố định nguyên văn mẫu lý do chưa được nhóm duyệt.
- Expected invalid chỉ khóa hành vi từ chối có kiểm soát. Lớp exception chính xác vẫn PENDING_ADR.
- Ca pending có thông báo chưa chốt output trong cột Expected và mã quyết định trong cột Pending. Cột Known assertions chỉ ghi phần chắc chắn, không đủ nghiệm thu cả ca.
- Trước M2: Huy review expected, Việt Đức map AC, Hải sửa và lưu lịch sử review. Không đánh dấu PASS từ việc đọc bảng.

## 2. Dữ liệu nền

```json
{
  "tuoi": 15,
  "huyet_ap_tam_thu": 110,
  "huyet_ap_tam_thu_nen": null,
  "co_di_nguyen_nghi_ngo": false,
  "di_nguyen_qua_duong_hit": false,
  "co_ton_thuong_da_niem_mac": false,
  "co_trieu_chung_ho_hap": false,
  "co_trieu_chung_tuan_hoan": false,
  "co_trieu_chung_tieu_hoa_nang": false
}
```

Tuổi 15 giúp tách nhiều ca rule khỏi câu hỏi thiếu HATT nền ở người lớn. HATT 110 không thấp theo nhóm này. Mỗi ca sốc vẫn kiểm chứng điều kiện Tầng 2. Chỉ dùng huyết áp nền giả lập khi trường hợp yêu cầu.

## 3. Chiến lược test

1. Normal: từng rule dương tính và trường hợp không khớp; R02 đủ 0–4 hệ và cả sáu cặp.
2. Boundary: nhóm tuổi 0/0.5/1/1.5/10.99/11/18; HATT dưới/bằng/trên ngưỡng nếu giá trị bằng là int; giảm dưới/đúng/trên 30%.
3. Negative/invalid: tuổi null/âm/chuỗi/bool/không hữu hạn; số đo sai kiểu/miền; từng boolean null/0/1/chuỗi; khóa dư và lỗi vẫn hiện diện khi rule khác đã TRUE.
4. Missing: thiếu từng boolean, minh họa AND/OR và đếm T/U; không chốt D02–D03.
5. Overlap/priority: R02/R03 đồng thời, và R-SOC thắng khi đã đủ điều kiện.
6. Output/audit: đúng schema, reason truy vết, không raw input; QA chuẩn bị sink/context khi M2 triển khai.

Ở tuổi 10.99, ngưỡng là 91.98; không dùng HATT=91.98 để kiểm “bằng” vì input HATT phải int. Hai ca 91/92 kiểm hai phía, còn tuổi 1.5 có ngưỡng int 73 để kiểm đúng bằng ở tuổi lẻ.

## 4. Truy vết AC

| AC | Ca/hoạt động liên quan | Trạng thái bằng chứng |
|---|---|---|
| A-01 | RULE/PAIR/BP/MISS/CON; review interface | Đã thiết kế ca, engine chưa triển khai |
| A-02 | CON đảo thứ tự khóa và review code không dùng fixture ID | Kế hoạch; behavioral test đơn lẻ không chứng minh toàn bộ |
| A-03 | RULE có đủ ba nhãn; BP ưu tiên sốc | Kế hoạch, chưa chạy |
| A-04 | INV/MISS/PEND, D04/D13 | Có ca; D01–D03/lớp exception còn treo |
| A-05 | CON và assertions ly_do ở ca classification | Có điều kiện kiểm; chưa chạy |
| A-06 | AUD, INV liên quan audit | QA cần thiết kế sink/context, chưa chạy |
| A-07 | Toàn ma trận normal/boundary/invalid/missing | Chưa có pytest nghiệp vụ |
| A-08 | QA chạy pytest -q từ clean checkout sau M2 | GAP — không thể xác nhận ở M1 |
| A-09 | QA kiểm PR run thật, không chỉ workflow có sẵn | GAP — chưa có bằng chứng run |
| A-10 | QA benchmark >=1000 sau warm-up, p50/p95/máy đo | GAP — chưa có phép đo |
| A-11 | Huy/QA bổ sung và kiểm disclaimer README dự án | GAP — bản tài liệu offline không thay README dự án |

## 5. Thống kê và các điểm chờ

- DRAFT_NOT_EXECUTED: 128 ca.
- PENDING_TA_CONFIRMATION: 7 ca.
- Hải xác nhận đã review và chỉnh sửa bản bàn giao; chờ Huy và Việt Đức review chéo. Các ca chưa chạy trên engine; không mặc định skipped/xfail là đã đạt AC.
- Ca D01 có thể kiểm riêng muc_do=PHAN_VE nhưng chưa khóa rule_id. Ca D02/D03 giữ output cuối chưa xác định.
- Ca theo D13/validation có nguồn Q là quyết định nội bộ, không gắn nhãn “thầy đã xác nhận”.

## 6. Chỉ mục (input đầy đủ ở CSV)

| Test ID | Scenario | Expected tóm tắt | AC | Trạng thái |
|---|---|---|---|---|
| RULE-001 | Không hệ biểu hiện, không dị nguyên | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-002 | R01: da và hô hấp | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-003 | R01: da và tuần hoàn | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-004 | R01: cả hai nhánh OR cùng TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-005 | R01 thiếu da | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-006 | R01 chỉ có da | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-007 | R01 không được dùng tiêu hóa thay hô hấp/tuần hoàn | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-008 | Không dị nguyên: tuần hoàn đơn độc | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-009 | R02 có 0/4 hệ | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-010 | R02 có 1/4 hệ, chỉ tiêu hóa | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-011 | R02 có 2/4 hệ, da và tiêu hóa | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-012 | R02 có 3/4 hệ, không tuần hoàn, qua đường hít | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-013 | R02 có 4/4 hệ, đủ điều kiện sốc | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PAIR-001 | R02 từng cặp 2/4: co_ton_thuong_da_niem_mac + co_trieu_chung_ho_hap | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PAIR-002 | R02 từng cặp 2/4: co_ton_thuong_da_niem_mac + co_trieu_chung_tuan_hoan | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PAIR-003 | R02 từng cặp 2/4: co_ton_thuong_da_niem_mac + co_trieu_chung_tieu_hoa_nang | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PAIR-004 | R02 từng cặp 2/4: co_trieu_chung_ho_hap + co_trieu_chung_tuan_hoan | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PAIR-005 | R02 từng cặp 2/4: co_trieu_chung_ho_hap + co_trieu_chung_tieu_hoa_nang | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PAIR-006 | R02 từng cặp 2/4: co_trieu_chung_tuan_hoan + co_trieu_chung_tieu_hoa_nang | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-014 | R03 hô hấp đơn độc, không qua đường hít | PHAN_VE / R03-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-015 | R03 hô hấp đơn độc bị chặn bởi đường hít | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-016 | R03 tuần hoàn đơn độc, qua đường hít | PHAN_VE / R03-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-017 | R03 tuần hoàn đơn độc, không qua đường hít | PHAN_VE / R03-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-018 | Có dị nguyên nhưng da đơn độc | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-019 | R02 vẫn khớp dù đường hít chặn R03 | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-020 | HATT thấp nhưng không có phản vệ | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-021 | R01 và HATT thấp | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| RULE-022 | R03 đơn độc và HATT thấp | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-001 | Tuổi 0; HATT 69; ngưỡng 70 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-002 | Tuổi 0; HATT 70; ngưỡng 70 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-003 | Tuổi 0; HATT 71; ngưỡng 70 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-004 | Tuổi 0.5; HATT 69; ngưỡng 70 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-005 | Tuổi 0.5; HATT 70; ngưỡng 70 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-006 | Tuổi 0.5; HATT 71; ngưỡng 70 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-007 | Tuổi 1; HATT 71; ngưỡng 72 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-008 | Tuổi 1; HATT 72; ngưỡng 72 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-009 | Tuổi 1; HATT 73; ngưỡng 72 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-010 | Tuổi 1.5; HATT 72; ngưỡng 73 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-011 | Tuổi 1.5; HATT 73; ngưỡng 73 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-012 | Tuổi 1.5; HATT 74; ngưỡng 73 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-013 | Tuổi 10.99; HATT 91; ngưỡng 91.98 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-014 | Tuổi 10.99; HATT 92; ngưỡng 91.98 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-015 | Tuổi 11; HATT 89; ngưỡng 90 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-016 | Tuổi 11; HATT 90; ngưỡng 90 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-017 | Tuổi 11; HATT 91; ngưỡng 90 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-018 | Tuổi 18; HATT 89; ngưỡng 90 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-019 | Tuổi 18; HATT 90; ngưỡng 90 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-020 | Tuổi 18; HATT 91; ngưỡng 90 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-021 | Người lớn nền 200; HATT 141 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-022 | Người lớn nền 200; HATT 140 | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-023 | Người lớn nền 200; HATT 139 | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-024 | HATT bằng 90 nhưng nhánh giảm tương đối vẫn TRUE | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-025 | Người lớn HATT <90, nền null | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-026 | Người lớn HATT <90, thiếu khóa nền | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-027 | Tuổi dưới 18: giảm tương đối không phải tiêu chí | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-028 | HATT 0 hợp lệ theo miền validation của nhóm | SOC_PHAN_VE / R-SOC | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| BP-029 | Nền 1 hợp lệ, không tự đặt giới hạn y khoa | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-001 | Thiếu boolean co_di_nguyen_nghi_ngo, không có rule chắc chắn TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-002 | Thiếu boolean di_nguyen_qua_duong_hit, không có rule chắc chắn TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-003 | Thiếu boolean co_ton_thuong_da_niem_mac, không có rule chắc chắn TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-004 | Thiếu boolean co_trieu_chung_ho_hap, không có rule chắc chắn TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-005 | Thiếu boolean co_trieu_chung_tuan_hoan, không có rule chắc chắn TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-006 | Thiếu boolean co_trieu_chung_tieu_hoa_nang, không có rule chắc chắn TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-007 | Thiếu tiêu hóa nhưng R01 đã chắc chắn TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-008 | Thiếu đường hít nhưng tuần hoàn xác nhận R03 | PHAN_VE / R03-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-009 | Thiếu dị nguyên, da và hô hấp TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-010 | R02 đủ hai hệ TRUE dù còn hệ UNKNOWN | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-011 | R02 T=0 U=1: chắc chắn không đủ hai hệ | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-012 | R02 T=1 U=1: chưa đủ kết luận | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-013 | R03 tuần hoàn TRUE, hô hấp UNKNOWN | PHAN_VE / R03-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-014 | Thiếu da nhưng R03 tuần hoàn đủ kết luận | PHAN_VE / R03-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-015 | Thiếu tuần hoàn, R01 hô hấp vẫn TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-016 | Thiếu hô hấp, R01 tuần hoàn vẫn TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-017 | Thiếu tuổi nhưng Tầng 2 chắc chắn FALSE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-018 | HATT null nhưng Tầng 2 chắc chắn FALSE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-019 | Thiếu HATT nhưng Tầng 2 chắc chắn FALSE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-020 | Input rỗng: tất cả dữ kiện còn thiếu | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-001 | R02 và R03 cùng TRUE, không sốc | PENDING D01 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| PEND-002 | Thiếu tuổi nhưng R01 TRUE | PENDING D02 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| PEND-003 | HATT null nhưng R01 TRUE | PENDING D03 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| PEND-004 | Thiếu khóa HATT nhưng R01 TRUE | PENDING D03 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| PEND-005 | Người lớn HATT 110, nền null | PENDING D03 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| PEND-006 | Người lớn HATT 110, nền thiếu khóa | PENDING D03 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| PEND-007 | Thiếu tuổi và HATT nhưng R01 TRUE | PENDING D02/D03 | A-01, A-03, A-07 | PENDING_TA_CONFIRMATION |
| INV-001 | Tuổi null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-002 | Tuổi âm | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-003 | Tuổi chuỗi | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-004 | Tuổi bool | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-005 | Tuổi không hữu hạn: NaN | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-006 | Tuổi không hữu hạn: +Infinity | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-007 | Tuổi không hữu hạn: -Infinity | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-008 | huyet_ap_tam_thu là âm | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-009 | huyet_ap_tam_thu là float dù có phần lẻ 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-010 | huyet_ap_tam_thu là chuỗi | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-011 | huyet_ap_tam_thu là bool | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-012 | huyet_ap_tam_thu_nen là âm | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-013 | huyet_ap_tam_thu_nen là float dù có phần lẻ 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-014 | huyet_ap_tam_thu_nen là chuỗi | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-015 | huyet_ap_tam_thu_nen là bool | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-016 | HATT nền bằng 0, kể cả khi tuổi <18 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-017 | co_di_nguyen_nghi_ngo là null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-018 | co_di_nguyen_nghi_ngo là số 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-019 | co_di_nguyen_nghi_ngo là số 1 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-020 | co_di_nguyen_nghi_ngo là chuỗi true | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-021 | di_nguyen_qua_duong_hit là null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-022 | di_nguyen_qua_duong_hit là số 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-023 | di_nguyen_qua_duong_hit là số 1 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-024 | di_nguyen_qua_duong_hit là chuỗi true | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-025 | co_ton_thuong_da_niem_mac là null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-026 | co_ton_thuong_da_niem_mac là số 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-027 | co_ton_thuong_da_niem_mac là số 1 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-028 | co_ton_thuong_da_niem_mac là chuỗi true | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-029 | co_trieu_chung_ho_hap là null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-030 | co_trieu_chung_ho_hap là số 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-031 | co_trieu_chung_ho_hap là số 1 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-032 | co_trieu_chung_ho_hap là chuỗi true | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-033 | co_trieu_chung_tuan_hoan là null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-034 | co_trieu_chung_tuan_hoan là số 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-035 | co_trieu_chung_tuan_hoan là số 1 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-036 | co_trieu_chung_tuan_hoan là chuỗi true | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-037 | co_trieu_chung_tieu_hoa_nang là null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-038 | co_trieu_chung_tieu_hoa_nang là số 0 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-039 | co_trieu_chung_tieu_hoa_nang là số 1 | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-040 | co_trieu_chung_tieu_hoa_nang là chuỗi true | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-041 | Khóa ngoài allowlist với marker synthetic | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-042 | Thiếu boolean nhưng có khóa số sai kiểu | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-043 | Đủ rule sốc nhưng có boolean null | Lỗi validation (lớp exception chờ ADR) | A-04, A-07 | DRAFT_NOT_EXECUTED |
| CON-001 | Output đúng ba khóa và reason an toàn | PHAN_VE / R01-PV | A-01, A-05, A-07 | DRAFT_NOT_EXECUTED |
| CON-002 | THEO_DOI có rule_id null | THEO_DOI / null | A-03, A-05 | DRAFT_NOT_EXECUTED |
| CON-003 | UNKNOWN không trở thành nhãn output thứ tư | THEO_DOI / null | A-01, A-04, A-05 | DRAFT_NOT_EXECUTED |
| CON-004 | Không sửa input của caller | PHAN_VE / R01-PV | A-01 | DRAFT_NOT_EXECUTED |
| CON-005 | Đảo thứ tự khóa không đổi kết quả phân loại | PHAN_VE / R01-PV | A-01, A-02 | DRAFT_NOT_EXECUTED |
| AUD-001 | Audit lần phân loại thành công | PHAN_VE / R01-PV | A-06 | DRAFT_NOT_EXECUTED |
| AUD-002 | Audit input invalid | Lỗi validation (lớp exception chờ ADR) | A-04, A-06 | DRAFT_NOT_EXECUTED |
| AUD-003 | Cùng phiên thao tác dùng cùng UUID synthetic | THEO_DOI / null | A-06 | DRAFT_NOT_EXECUTED |
