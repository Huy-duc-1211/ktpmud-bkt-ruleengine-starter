# M1-02 — Kế hoạch test theo Issue #15

**Phạm vi hiện tại là thiết kế/test case M1.** Các phần nhắc thực thi pytest/audit/benchmark là dự kiến cho giai đoạn sau; tài liệu chi tiết đã ở M2, chưa cần thực hiện khi review M1.

Nguồn chính thức bổ sung T15 tại [ISSUE15_SYNC.md](ISSUE15_SYNC.md), ưu tiên hơn diễn giải mâu thuẫn trong Q/A Revision 02. Tôi đã review bộ test case M1 trước khi bàn giao. **157 ca trong CSV chung đều DRAFT_NOT_EXECUTED; 0 ca còn PENDING_TA_CONFIRMATION; chưa chạy engine nghiệp vụ.**

## 1. Dữ liệu và expected

- Giữ 135 ca gốc đầu file và gộp 22 ca T15 phía sau. Test ID đã trở về mã gốc RULE-/INV-/TA15-/D13-, không đổi input hoặc expected. Có 11 nhóm Equivalence group để tra các cặp null/missing. Cột Pending hiện trống; cột Resolved decision ghi D01/D02/D03 cho bảy ID PEND đã được làm rõ. Prefix PEND/INV không phải trạng thái runtime.
- 36 ca invalid còn lại: **28 TypeError+8 ValueError** theo D04 không mâu thuẫn T15. Tám ca null trước kia bị coi invalid đã chuyển thành kiểm dữ liệu thiếu hợp lệ. AUD-002 dùng chuỗi boolean thay null để tiếp tục kiểm audit invalid.
- Expected TypeError/ValueError public có precondition audit INVALID_INPUT thành công; lỗi kép vẫn audit precedence, không đổi vì T15.
- Tuổi thiếu/null: THEO_DOI/null. Có tuổi và Tầng 2 đủ, thiếu HATT/nền cần thiết: PHAN_VE với mã rule và reason thiếu dữ liệu; không tự gán nền. Overlap chọn R01 > R02 > R03; có bằng chứng sốc luôn R-SOC.
- Boolean thiếu/null không gây exception vì nullable và không hạ mức khi đã đủ kết luận. Số/chuỗi khác null vẫn sai kiểu theo policy nhóm.
- Fixture encoding=json/fixture_ref và registry nonfinite giữ trong repo, không eval. [FIXTURE_CONTRACT.md](../M2/FIXTURE_CONTRACT.md)
- Internal assertions là notation helper, không field PatientInput/output/audit. HYPOTENSION UNKNOWN diễn đạt thiếu thông tin, SHOCK_EVIDENCE FALSE là chưa chứng minh sốc; không khiến final output pending.

## 2. Các nhóm kiểm thử

| Lớp | Ca/kế hoạch | Oracle |
|---|---|---|
| Normal/boundary | RULE/PAIR/BP/CON | Rule/ngưỡng giữ nguyên; mã priority T15, reason an toàn |
| Invalid | INV còn exception và AUD-002 | TypeError sai kiểu, ValueError miền/khóa thừa; audit error precedence |
| Nullable/missing | MISS, tám INV chuyển mục tiêu, bảy PEND đã resolve | Không raise do null/missing; null và bỏ khóa cùng mức/mã; reason thiếu tuổi/HATT/nền đúng trường hợp |
| R02/D13 | Internal assertions +81 hàng INTERNAL_STATE_CASES.csv | Enum identity trước selection, count T/U và AND S; không nhìn output để suy helper đúng |
| Regression T15 | TEST_CASES.csv (nhóm Equivalence group), 22 ca/11 cặp | Ba trường số +sáu bool null/missing, không hạ sốc, fallback phụ thuộc missing và coverage S |
| Audit/context | AUD +INT kế hoạch | Direct call audit SUCCESS với nullable hợp lệ, UUID/session/reset, lỗi thật/failure stages/privacy/isolation |
| Benchmark | BENCH-001–006 | 100 warm-up, N>=1.000, nearest-rank/ns-ms, full-path audit I/O thật, chưa thực đo |

## 3. Policy nhóm còn chờ review

Giữ Enum UNKNOWN cho boolean thiếu/null và THEO_DOI khi kết luận thực sự phụ thuộc dữ liệu thiếu là policy nhóm, không phải T15 bắt buộc cách biểu diễn này. Khi thiếu S mà mọi completion đều phản vệ, không để mất kết luận chỉ vì từng rule riêng UNKNOWN. Đề xuất BOOL-COVERAGE bảo toàn mức; mã đại diện R01-PV ở MISS-009 và cặp TA15-BOOL1 được đánh dấu **PROPOSED FOR LEADER REVIEW** trong cột Policy review. Mã đại diện này vẫn cần Huy duyệt. [ISSUE15_SYNC §4]

## 4. Đối chiếu tiêu chí nghiệm thu

| AC | Test/hoạt động | Trạng thái |
|---|---|---|
| A-01/A-03 | 157 ca, priority/nullable T15, direct call | Thiết kế, chưa runtime |
| A-02 | CON-005 + source review fixture independence | Chưa review implementation |
| A-04 | 36 invalid, nullable/missing, bảy D01–D03 đã resolve và 22 regression | Contract thầy rõ; policy BOOL-COVERAGE riêng còn cần Leader review |
| A-05 | CON + reason_must_mention, không raw values/điều trị | Chưa output runtime |
| A-06 | AUD/INT, nullable hợp lệ -> SUCCESS | Chưa audit thật; QA Matrix chưa có |
| A-07 | 157 +81 hàng dữ liệu, plans INT | Số hàng không phải pytest pass |
| A-08/A-09 | Clean checkout/PR CI suite nghiệp vụ | GAP, chưa làm trong M1 này |
| A-10 | BENCH protocol giữ nguyên | Chưa có latency/I/O benchmark |
| A-11 | README runtime/disclaimer | Tài liệu M1 không thay bằng chứng README dự án |

## 5. Review và phạm vi

Tôi bàn giao phần tài liệu và test case M1 trên nhánh `docs/m1-tests-hai`, không tạo PR hoặc merge. Q/A Revision 02 được giữ làm nguồn lịch sử; việc đồng bộ Requirements/ADR thực hiện ở nhánh nguồn. Việt Đức chưa có QA Matrix nên phần đối chiếu QA còn chờ. Cơ chế default audit path, unexpected internal exception và mã đại diện BOOL-COVERAGE vẫn cần review theo trạng thái đã ghi.

## 6. Chỉ mục 157 ca trong CSV chung

Test ID dùng mã gốc. Tiền tố PEND/INV là lịch sử phân nhóm, không tự quyết định trạng thái hoặc expected hiện tại.

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
| MISS-009 | Thiếu dị nguyên, da và hô hấp TRUE | PHAN_VE / R01-PV [đề xuất mã nhóm] | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
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
| PEND-001 | R02 và R03 cùng TRUE, không sốc | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-002 | Thiếu tuổi nhưng R01 TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-003 | HATT null nhưng R01 TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-004 | Thiếu khóa HATT nhưng R01 TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-005 | Người lớn HATT 110, nền null | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-006 | Người lớn HATT 110, nền thiếu khóa | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| PEND-007 | Thiếu tuổi và HATT nhưng R01 TRUE | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| INV-001 | Tuổi null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-002 | Tuổi âm | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-003 | Tuổi chuỗi | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-004 | Tuổi bool | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-005 | Tuổi không hữu hạn: NaN | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-006 | Tuổi không hữu hạn: +Infinity | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-007 | Tuổi không hữu hạn: -Infinity | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-008 | huyet_ap_tam_thu là âm | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-009 | huyet_ap_tam_thu là float dù có phần lẻ 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-010 | huyet_ap_tam_thu là chuỗi | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-011 | huyet_ap_tam_thu là bool | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-012 | huyet_ap_tam_thu_nen là âm | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-013 | huyet_ap_tam_thu_nen là float dù có phần lẻ 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-014 | huyet_ap_tam_thu_nen là chuỗi | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-015 | huyet_ap_tam_thu_nen là bool | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-016 | HATT nền bằng 0, kể cả khi tuổi <18 | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-017 | co_di_nguyen_nghi_ngo là null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-018 | co_di_nguyen_nghi_ngo là số 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-019 | co_di_nguyen_nghi_ngo là số 1 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-020 | co_di_nguyen_nghi_ngo là chuỗi true | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-021 | di_nguyen_qua_duong_hit là null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-022 | di_nguyen_qua_duong_hit là số 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-023 | di_nguyen_qua_duong_hit là số 1 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-024 | di_nguyen_qua_duong_hit là chuỗi true | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-025 | co_ton_thuong_da_niem_mac là null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-026 | co_ton_thuong_da_niem_mac là số 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-027 | co_ton_thuong_da_niem_mac là số 1 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-028 | co_ton_thuong_da_niem_mac là chuỗi true | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-029 | co_trieu_chung_ho_hap là null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-030 | co_trieu_chung_ho_hap là số 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-031 | co_trieu_chung_ho_hap là số 1 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-032 | co_trieu_chung_ho_hap là chuỗi true | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-033 | co_trieu_chung_tuan_hoan là null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-034 | co_trieu_chung_tuan_hoan là số 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-035 | co_trieu_chung_tuan_hoan là số 1 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-036 | co_trieu_chung_tuan_hoan là chuỗi true | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-037 | co_trieu_chung_tieu_hoa_nang là null | THEO_DOI / null | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-038 | co_trieu_chung_tieu_hoa_nang là số 0 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-039 | co_trieu_chung_tieu_hoa_nang là số 1 | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-040 | co_trieu_chung_tieu_hoa_nang là chuỗi true | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-041 | Khóa ngoài allowlist với marker synthetic | ValueError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-042 | Thiếu boolean nhưng có khóa số sai kiểu | TypeError | A-04, A-07 | DRAFT_NOT_EXECUTED |
| INV-043 | Đủ rule sốc nhưng có boolean null | SOC_PHAN_VE / R-SOC | A-04, A-07 | DRAFT_NOT_EXECUTED |
| CON-001 | Output đúng ba khóa và reason an toàn | PHAN_VE / R01-PV | A-01, A-05, A-07 | DRAFT_NOT_EXECUTED |
| CON-002 | THEO_DOI có rule_id null | THEO_DOI / null | A-03, A-05 | DRAFT_NOT_EXECUTED |
| CON-003 | UNKNOWN không trở thành nhãn output thứ tư | THEO_DOI / null | A-01, A-04, A-05 | DRAFT_NOT_EXECUTED |
| CON-004 | Không sửa input của caller | PHAN_VE / R01-PV | A-01 | DRAFT_NOT_EXECUTED |
| CON-005 | Đảo thứ tự khóa không đổi kết quả phân loại | PHAN_VE / R01-PV | A-01, A-02 | DRAFT_NOT_EXECUTED |
| AUD-001 | Audit lần phân loại thành công | PHAN_VE / R01-PV | A-06 | DRAFT_NOT_EXECUTED |
| AUD-002 | Audit input sai kiểu boolean (chuỗi, không phải null) | TypeError | A-04, A-06 | DRAFT_NOT_EXECUTED |
| AUD-003 | Cùng phiên thao tác dùng cùng UUID synthetic | THEO_DOI / null | A-06 | DRAFT_NOT_EXECUTED |
| TA15-AGE-NULL | tuổi null — chưa có tuổi dù đủ phản vệ | THEO_DOI / null | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-AGE-MISSING | tuổi thiếu khóa — chưa có tuổi dù đủ phản vệ | THEO_DOI / null | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-CURRENT_BP-NULL | huyết áp hiện tại null — thiếu huyết áp vẫn giữ phản vệ | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-CURRENT_BP-MISSING | huyết áp hiện tại thiếu khóa — thiếu huyết áp vẫn giữ phản vệ | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BASELINE_BP-NULL | huyết áp nền null — người lớn thiếu nền vẫn giữ phản vệ | PHAN_VE / R02-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BASELINE_BP-MISSING | huyết áp nền thiếu khóa — người lớn thiếu nền vẫn giữ phản vệ | PHAN_VE / R02-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL1-NULL | dị nguyên nghi ngờ null — mọi khả năng dị nguyên đều dẫn đến phản vệ | PHAN_VE / R01-PV [đề xuất mã nhóm] | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL1-MISSING | dị nguyên nghi ngờ thiếu khóa — mọi khả năng dị nguyên đều dẫn đến phản vệ | PHAN_VE / R01-PV [đề xuất mã nhóm] | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL2-NULL | dị nguyên đường hít null — tuần hoàn đã đủ R03 | PHAN_VE / R03-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL2-MISSING | dị nguyên đường hít thiếu khóa — tuần hoàn đã đủ R03 | PHAN_VE / R03-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL3-NULL | da niêm mạc null — tuần hoàn đã đủ R03 | PHAN_VE / R03-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL3-MISSING | da niêm mạc thiếu khóa — tuần hoàn đã đủ R03 | PHAN_VE / R03-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL4-NULL | hô hấp null — da và tuần hoàn đã đủ R01 | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL4-MISSING | hô hấp thiếu khóa — da và tuần hoàn đã đủ R01 | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL5-NULL | tuần hoàn null — da và hô hấp đã đủ R01 | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL5-MISSING | tuần hoàn thiếu khóa — da và hô hấp đã đủ R01 | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL6-NULL | tiêu hóa nặng null — da và hô hấp đã đủ R01 | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL6-MISSING | tiêu hóa nặng thiếu khóa — da và hô hấp đã đủ R01 | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-NO_DOWNGRADE_SHOCK-NULL | tiêu hóa nặng null — không hạ mức sốc đã đủ bằng chứng | SOC_PHAN_VE / R-SOC | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-NO_DOWNGRADE_SHOCK-MISSING | tiêu hóa nặng thiếu khóa — không hạ mức sốc đã đủ bằng chứng | SOC_PHAN_VE / R-SOC | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-DEPENDENT_INHALATION-NULL | dị nguyên đường hít null — kết quả phụ thuộc đường hít chưa biết | THEO_DOI / null | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-DEPENDENT_INHALATION-MISSING | dị nguyên đường hít thiếu khóa — kết quả phụ thuộc đường hít chưa biết | THEO_DOI / null | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
