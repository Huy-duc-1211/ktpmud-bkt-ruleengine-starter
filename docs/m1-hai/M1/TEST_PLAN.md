# M1-02 — Kế hoạch kiểm thử rule engine

**Phạm vi hiện tại là thiết kế/test case M1.** Các phần nhắc thực thi pytest/audit/benchmark là dự kiến cho giai đoạn sau; tài liệu chi tiết đã ở M2, chưa cần thực hiện khi review M1.

Nguồn hiện hành: [Requirements](../../../REQUIREMENTS.md) (Q), [ADR](../../../DECISIONS.md) (A), [Decision Table](../../decision-table.md) (D), [làm rõ Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15) và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002) (T31). Leader duyệt D13-E ngày 09/11/2026 và cập nhật cách chọn mã sau Issue #31. Hải là tác giả baseline; Huy Đức phụ trách TASK 02E và các bản sửa với AI hỗ trợ. Review kỹ thuật của các thành viên và kết quả thực thi cần bằng chứng riêng. Xem [sources](sources/README.md) cho các snapshot lịch sử.

**175 ca DRAFT_NOT_EXECUTED; 0 ca PENDING_TA_CONFIRMATION.** Static data/oracle checks không phải kết quả classifier.

## 1. Dữ liệu và expected

- Giữ 157 Test ID/input baseline và 18 D13E-001–018 bổ sung. Tại TASK 02E, mức/mã/lớp lỗi baseline được giữ; sau Issue #31, bốn ca MISS-013/014 và TA15-BOOL3-NULL/MISSING đổi mã dự kiến từ R03-PV sang R02-PV CANONICAL, giữ mức PHAN_VE. Có 18 nhóm Equivalence group (11 cũ+7 mới), null/missing cùng mức/mã. Cột Pending trống; Resolved decision ghi D01/D02/D03 cho bảy ID PEND đã được làm rõ. Prefix PEND/INV không phải trạng thái runtime.
- 36 ca invalid còn lại: **28 TypeError+8 ValueError** theo D04 không mâu thuẫn T15. Tám ca null trước kia bị coi invalid đã chuyển thành kiểm dữ liệu thiếu hợp lệ. AUD-002 dùng chuỗi boolean thay null để tiếp tục kiểm audit invalid.
- Expected TypeError/ValueError public có precondition audit INVALID_INPUT thành công; lỗi kép vẫn audit precedence, không đổi vì T15.
- Tuổi thiếu/null: THEO_DOI/null. Có tuổi và Tầng 2 đủ, thiếu HATT/nền cần thiết: PHAN_VE với mã rule và reason thiếu dữ liệu; không tự gán nền. Overlap chọn R01 > R02 > R03; có bằng chứng sốc luôn R-SOC.
- Boolean thiếu/null không gây exception vì nullable và không hạ mức khi đã đủ kết luận. Số/chuỗi khác null vẫn sai kiểu theo policy nhóm.
- Fixture encoding=json/fixture_ref và registry nonfinite giữ trong repo, không eval. [FIXTURE_CONTRACT.md](../M2/FIXTURE_CONTRACT.md)
- Internal assertions là notation helper, không field PatientInput/output/audit. HYPOTENSION có thể UNKNOWN; HYPOTENSION_EVIDENCE chỉ bằng chứng số đo, TIER1_MATCH kết hợp TIER2_COVERAGE với HYPOTENSION; không suy SOC từ HATT thấp đơn độc.

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

## 3. D13-E đã duyệt và explanation contract

**D13-E:** Leader duyệt chính sách ngày 09/11/2026; sau Issue #31, Leader cập nhật cách chọn mã theo Q/A hiện hành. Sáu ca MISS-009, TA15-BOOL1-NULL/MISSING, MISS-012 và TA15-DEPENDENT_INHALATION-NULL/MISSING giữ mức/mã. Issue #31 xác nhận trực tiếp MISS-009; các fixture overlap definite/possible là cách nhóm áp dụng quy tắc chọn mã.

C(p) là mọi True/False completion của boolean UNKNOWN, giữ known values; không fill patient hoặc numeric. Def là rule TRUE trong mọi completion; Poss là rule TRUE ở ít nhất một completion; AllPV là mọi completion khớp ít nhất một original rule; AnyPV là tồn tại completion positive. Có 1–64 completion.

1. Validation mọi trường theo D04; tuổi missing/null → THEO_DOI/null theo TA, nêu thiếu tuổi và chuyển sang audit.
2. Có tuổi: xác định Def, Poss, AllPV và AnyPV từ các completion. Nếu AllPV, phản vệ đã được chứng minh, kể cả khi Def rỗng.
3. AllPV và HYPOTENSION TRUE → SOC_PHAN_VE/R-SOC. HATT thấp đơn độc không đủ điều kiện sốc phản vệ.
4. AllPV nhưng chưa xác nhận sốc → PHAN_VE; chọn rule ưu tiên cao nhất trong Poss theo R01 > R02 > R03. Nếu rule được chọn thuộc Def, mã là DIRECT; nếu chưa chắc chắn thì là CANONICAL, kể cả khi rule ưu tiên thấp hơn đã chắc chắn. CANONICAL bắt buộc nêu mã đại diện, dữ liệu thiếu và chưa xác nhận rule riêng; không nói UNKNOWN=False đã được quan sát.
5. Mixed → THEO_DOI/null kèm lý do thiếu thông tin; không AnyPV → THEO_DOI/null với lý do không khớp. Không gọi Mixed là an toàn.

DIRECT và CANONICAL là nhãn nội bộ, không thêm khóa output hay status audit. Issue #31 nêu cách chọn mã ưu tiên trong các rule có thể thỏa và xác nhận trực tiếp MISS-009; việc dùng CANONICAL cho ca vừa có rule chắc chắn vừa có rule ưu tiên cao hơn có thể thỏa là cách nhóm áp dụng quyết định này. Mã đại diện không làm rule đó trở thành definite. Giữ Enum/Kleene/T-U, không ép UNKNOWN thành False; ly_do và negative assertions cần ngăn hiểu nhầm rule đại diện đã được xác nhận.

Expected.explanation_assertions là metadata harness, không key thứ tư của output. Trước khi so ClassificationResult chỉ assert đúng muc_do/rule_id/ly_do; không trả ly_do_contract, patterns hoặc attribution_kind ra public. required_patterns_all phải cùng khớp ly_do, forbidden_patterns_any không được khớp; không ép reason nguyên văn. Chúng bao phủ controlled template families tiếng Việt, không chứng minh mọi câu tự nhiên đều đúng; Việt Đức cần review semantics và privacy trên output thực.

Với mọi CANONICAL, ly_do phải nêu mã đại diện, dữ liệu thiếu và rule mang mã chưa được xác nhận riêng. Riêng MISS-009/TA15-BOOL1-* kiểm cả R01/R02 và kết luận phản vệ qua mọi khả năng; không nói S=True/False đã được quan sát. Với MISS-013/014 và TA15-BOOL3-NULL/MISSING, kiểm R02-PV là mã đại diện, thông tin hô hấp hoặc da/niêm mạc còn thiếu, và R02 chưa được xác nhận riêng; có thể nêu R03 đã chắc chắn. MIXED cần lý do thiếu thông tin, không nói “không phản vệ/an toàn” hay gán giá trị chưa biết. DIRECT phải nhắc đúng rule được chọn và không tự gọi canonical. Patterns là kiểm tra hỗ trợ, vẫn cần review semantics/privacy thực tế.

**Kiểm lời giải thích sau review:** Các mẫu trong CSV chỉ hỗ trợ kiểm tra những cách diễn đạt được kiểm soát, không xác nhận đầy đủ ý nghĩa câu tự nhiên. Phải có ca đối chứng đúng và sai: mã đại diện chưa xác nhận riêng, dữ liệu/trường còn thiếu, khẳng định mâu thuẫn và giá trị chưa biết bị gán là đã quan sát. Ca Mixed phải phân biệt “chưa đủ thông tin để kết luận không có phản vệ” với khẳng định đã loại trừ phản vệ. D13E-004/005 còn cần nêu thiếu HATT hiện tại; D13E-015/016 cần nêu thiếu HATT nền để đánh giá nhánh sốc liên quan. Kiểm riêng privacy, lời khuyên điều trị và ngữ nghĩa toàn câu trên output thực tế; không suy các nội dung này đã đạt chỉ vì regex khớp. Ví dụ một câu đủ từ khóa rồi thêm “Vì vậy, R02-PV đã thỏa” có thể vẫn lọt regex dù mâu thuẫn; cần có kiểm tra riêng cho toàn bộ mẫu output thực tế. Không bắt lời giải thích phải giống nguyên văn một câu ví dụ. Chưa có kết quả thực thi nghiệp vụ.

Với MISS-009, đối chứng hai cách giải thích cùng nêu R01 là mã đại diện chưa được xác nhận: câu có nêu thiếu thông tin dị nguyên nghi ngờ đạt điều kiện này; câu bỏ thông tin đó không đạt, kể cả khi khớp regex. Đây là ví dụ kiểm ngữ nghĩa, không bắt buộc dùng nguyên văn và chưa phải kết quả test.

RULE-020 giữ HYPOTENSION_EVIDENCE TRUE nhưng TIER1_MATCH FALSE; xem [INTERNAL_STATE_TEST_PLAN](../M2/INTERNAL_STATE_TEST_PLAN.md). Đây là tên assertion nội bộ, không API helper mới bắt buộc.

## 4. Đối chiếu tiêu chí nghiệm thu

| AC | Test/hoạt động | Trạng thái |
|---|---|---|
| A-01/A-03 | 175 main cases; definite/coverage, age/BP/shock và priority | Oracle thiết kế, chưa runtime |
| A-02 | CON-005 và review fixture independence | Implementation chưa kiểm; Test ID chỉ là harness metadata |
| A-04 | 36 invalid, nullable/missing, 18 cặp equivalence, sáu approved D13 cases | TASK 02E từng kiểm oracle tĩnh theo selector cũ; bản chọn mã cập nhật cần được kiểm lại, chưa runtime PASS |
| A-05 | CANONICAL/DIRECT/MIXED patterns và negative semantic assertions | Kiểm thiết kế bằng safe/unsafe examples, actual ly_do NOT EXECUTED |
| A-06 | AUD/INT, nullable SUCCESS và invalid INVALID_INPUT với precondition writer thành công | QA Matrix đã có mapping thiết kế; audit runtime và review mapping còn chờ |
| A-07 | 175+81 rows và INT plans | Không tính số dòng thành pytest pass |
| A-08/A-09 | Clean checkout/PR CI business suite | GAP runtime/CI, không yêu cầu có ở bản sửa M1 |
| A-10 | BENCH-001–006 protocol không đổi | Chưa đo full-path I/O latency |
| A-11 | Disclaimer README dự án | Requirements đã đối chiếu câu bắt buộc tại commit README 4482e4f; QA Matrix vẫn cần kiểm bằng chứng ở SHA nghiệm thu |

## 5. Review, ownership và phụ thuộc

TASK 02E do Leader sở hữu trên review/m1-02-leader-remediation từ SHA 768f196e6a9ec3b1142c44399ce8288f7cc2e87e, AI hỗ trợ. Không gán bản sửa cho Hải hoặc tuyên bố hai thành viên đã peer review. Nguồn Q/A Revision 04 đã xuất bản; không giao lại việc sửa Requirements/ADR. Snapshots cũ giữ lịch sử, không current oracle.

Default audit path còn PROPOSED — AWAITING PEER REVIEW; unexpected internal exception residual; CON-004 nonmutation vẫn là đề nghị kỹ thuật chưa được phê duyệt riêng. Approval D13-E không tự approve các mục đó. QA Matrix đã tích hợp qua PR #4; các mục chọn mã/ly_do đã cập nhật ở mức thiết kế theo policy sau Issue #31 và cần Việt Đức/Hải review. Không coi PR merge là runtime PASS hay peer review hoàn tất. Quyết định commit, push và merge thuộc Leader; AI không tự thực hiện.

## 6. Chỉ mục 175 ca trong CSV chung

157 Test ID/input gốc được giữ. Tại TASK 02E, mức/mã/lớp lỗi baseline được bảo toàn; sau Issue #31, bốn ca overlap đổi rule_id như mô tả ở §1. Prefix PEND/INV giữ lịch sử. Mọi ca DRAFT_NOT_EXECUTED.

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
| MISS-009 | Thiếu dị nguyên, da và hô hấp TRUE | PHAN_VE / R01-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-010 | R02 đủ hai hệ TRUE dù còn hệ UNKNOWN | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-011 | R02 T=0 U=1: chắc chắn không đủ hai hệ | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-012 | R02 T=1 U=1: chưa đủ kết luận | THEO_DOI / null | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-013 | R03 tuần hoàn TRUE, hô hấp UNKNOWN | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
| MISS-014 | Thiếu da nhưng R03 tuần hoàn đủ kết luận | PHAN_VE / R02-PV | A-01, A-03, A-07 | DRAFT_NOT_EXECUTED |
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
| TA15-BOOL1-NULL | dị nguyên nghi ngờ null — mọi khả năng dị nguyên đều dẫn đến phản vệ | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL1-MISSING | dị nguyên nghi ngờ thiếu khóa — mọi khả năng dị nguyên đều dẫn đến phản vệ | PHAN_VE / R01-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL2-NULL | dị nguyên đường hít null — tuần hoàn đã đủ R03 | PHAN_VE / R03-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL2-MISSING | dị nguyên đường hít thiếu khóa — tuần hoàn đã đủ R03 | PHAN_VE / R03-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL3-NULL | da niêm mạc null — tuần hoàn đã đủ R03 | PHAN_VE / R02-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
| TA15-BOOL3-MISSING | da niêm mạc thiếu khóa — tuần hoàn đã đủ R03 | PHAN_VE / R02-PV | A-01, A-03, A-04, A-07 | DRAFT_NOT_EXECUTED |
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
| D13E-001 | AllPV với bốn UNKNOWN, null | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-002 | AllPV với bốn UNKNOWN, thiếu khóa | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-003 | AllPV với bốn UNKNOWN và HATT thấp | SOC_PHAN_VE / R-SOC | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-004 | AllPV với HATT hiện tại null | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-005 | AllPV với HATT hiện tại thiếu khóa | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-006 | AllPV nhưng thiếu tuổi | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-007 | AllPV nhưng tuổi null | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-008 | Sáu UNKNOWN với tuổi có, 64 completions | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-009 | Sáu boolean thiếu khóa với tuổi có | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-010 | Mixed phụ thuộc S null | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-011 | Mixed phụ thuộc S thiếu khóa | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-012 | Mixed phụ thuộc đồng thời K và I null | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-013 | Mixed phụ thuộc đồng thời K và I thiếu khóa | THEO_DOI / null | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-014 | DIRECT R01 với ba UNKNOWN không liên quan | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-015 | AllPV adult thiếu nền null | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-016 | AllPV adult thiếu khóa nền | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-017 | 17.99 không áp nhánh giảm tương đối | PHAN_VE / R01-PV | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |
| D13E-018 | 18 áp nhánh giảm tương đối | SOC_PHAN_VE / R-SOC | A-01, A-03, A-04, A-05, A-07 | DRAFT_NOT_EXECUTED |

## 7. Ca bổ sung theo F04 và lý do không trùng mục tiêu

| Test ID | Gap cần phát hiện | Expected | Vì sao cần thêm |
|---|---|---|---|
| D13E-001 | AllPV với bốn UNKNOWN, null | PHAN_VE / R01-PV | F04: không chỉ enumerate S; 16 completions |
| D13E-002 | AllPV với bốn UNKNOWN, thiếu khóa | PHAN_VE / R01-PV | F04: null/missing tương đương khi nhiều UNKNOWN |
| D13E-003 | AllPV với bốn UNKNOWN và HATT thấp | SOC_PHAN_VE / R-SOC | F04: coverage positive kết hợp Tier1 |
| D13E-004 | AllPV với HATT hiện tại null | PHAN_VE / R01-PV | F04: không hạ AllPV vì thiếu BP |
| D13E-005 | AllPV với HATT hiện tại thiếu khóa | PHAN_VE / R01-PV | F04: BP null/missing tương đương |
| D13E-006 | AllPV nhưng thiếu tuổi | THEO_DOI / null | F04: age override trước coverage |
| D13E-007 | AllPV nhưng tuổi null | THEO_DOI / null | F04: age null/missing override tương đương |
| D13E-008 | Sáu UNKNOWN với tuổi có, 64 completions | THEO_DOI / null | F04: MISS-020 thiếu tuổi short-circuit, không kiểm max64 |
| D13E-009 | Sáu boolean thiếu khóa với tuổi có | THEO_DOI / null | F04: max64 missing/null tương đương |
| D13E-010 | Mixed phụ thuộc S null | THEO_DOI / null | F04: unknown allergen thật sự đổi có/không phản vệ |
| D13E-011 | Mixed phụ thuộc S thiếu khóa | THEO_DOI / null | F04: mixed S null/missing |
| D13E-012 | Mixed phụ thuộc đồng thời K và I null | THEO_DOI / null | F04: nhiều UNKNOWN có cả positive/negative worlds |
| D13E-013 | Mixed phụ thuộc đồng thời K và I thiếu khóa | THEO_DOI / null | F04: không promote chỉ từ một completion positive |
| D13E-014 | DIRECT R01 với ba UNKNOWN không liên quan | PHAN_VE / R01-PV | F04: DIRECT vì R01 là rule chắc chắn có ưu tiên cao nhất trong Poss; ba UNKNOWN không liên quan |
| D13E-015 | AllPV adult thiếu nền null | PHAN_VE / R01-PV | F04: coverage kết hợp adult baseline unavailable |
| D13E-016 | AllPV adult thiếu khóa nền | PHAN_VE / R01-PV | F04: baseline null/missing dưới coverage |
| D13E-017 | 17.99 không áp nhánh giảm tương đối | PHAN_VE / R01-PV | F04: phát hiện làm tròn 17.99 thành 18 |
| D13E-018 | 18 áp nhánh giảm tương đối | SOC_PHAN_VE / R-SOC | F04: cặp sát biên 18 với giảm >30% |

MISS-013/014 và TA15-BOOL3 có R03 definite, R02 possible: giữ input và helper; theo selector cập nhật chọn R02-PV CANONICAL, kiểm disclosure và không claim R02 đã chắc chắn. PEND-001 vẫn kiểm overlap R02/R03 cùng TRUE; RULE-020 kiểm low-BP-only. Hai ca D13E-017/018 dùng BP100/nền200 để phân biệt 17.99 và 18; chỉ so BP89/90 ở 17.99 sẽ không bắt lỗi làm tròn vì hai nhóm đều có ngưỡng tuyệt đối 90.

M2 cần property checks mọi 729 boolean states, mọi u từ 0..6 (1–64 completions), permutation enumeration/key-order, idempotence selection và null/missing symmetry; không sinh Expected bằng code classifier. Phép kiểm tĩnh 729 trạng thái/18 cấu hình numeric trong TASK 02E thuộc selector cũ, cần tính lại cho selector cập nhật; không phải kết quả runtime.
