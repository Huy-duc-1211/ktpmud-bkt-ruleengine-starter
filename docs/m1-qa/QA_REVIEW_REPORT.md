# TASK 02N-C — Audit độc lập M1-03

> **Bối cảnh lịch sử:** Báo cáo ghi nhận TASK 02N-C trước Issue #31; selector, expected và kết quả kiểm tĩnh dưới đây phản ánh thời điểm đó. Xem [QA Matrix hiện hành](QA_MATRIX.xlsx), [Test Cases](../m1-hai/M1/TEST_CASES.csv) và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002) cho thiết kế đã cập nhật. Báo cáo cũ không phải bằng chứng chạy selector mới.

Nhóm 173820_n27, Track A. QA gốc do Việt Đức thực hiện. Bản sửa trước do Huy Đức với ChatGPT hỗ trợ. Audit này do Huy Đức với Codex hỗ trợ. Chưa xác lập review độc lập của thành viên.

**Phase A, ghi trước khi đọc workbook cũ và nhận xét ChatGPT.** Bản self-review đã cải thiện nhiều phần thiết kế. Cần sửa cache và các lệch giữa input, test ID, procedure và expected trước khi chuyển bản ứng viên cho Leader. Không thấy sai mức/mã/lớp lỗi trong 21 JSON inline đã đối chiếu. Có lỗi tại dòng dùng fixture và thủ tục, ngoài phạm vi phép kiểm 21 JSON.

File nguồn `QA_MATRIX_M1_SELF_REVIEW_PATCHED.xlsx` tại Downloads, **43.195 byte**, SHA-256 `453badfe2041e09481ab8e90db0a6589dd6eaa80fcafb395817afb17515d3079`. Đọc workbook ở chế độ phân tích và không lưu lại bản nguồn. PR #1/#2/#3 tại `f82ef67` / `7af011f` / `61b6b9f`, đều mở Draft, cùng base `b65032f`. Requirements pin `a574ce2`. Guide và Plan pin `f82ef67`. [Q], [A], [G], [P].

| Sheet | Excel Table và vùng dữ liệu | Kiểm tra |
|---|---|---|
| AC_MATRIX | ACTraceability A1:N12, 11 AC | G2:G12 và H2:H12 có validation; 22 COUNTIF wildcard, cache 22 ô bằng 0 |
| QA_CASES | QACases A1:O65, 64 ca | J2:J65 và K2:K65 có validation; có tag đa AC |
| QA_CHECKLIST | QAChecklist A1:L61, 60 dòng | H2:H61 có validation; checklist mới nằm trong Table |
| GAP_REVIEW | QAFindings A1:L16, 15 ID | L8 trống nguồn cấu trúc; các status là patched/review cần hoặc deferred |

Các sheet hiển thị và freeze hàng tiêu đề. Không có ID chính trùng hoặc mất. AC_MATRIX F, QA_CASES M, QA_CHECKLIST I trống evidence, phù hợp 135 status `NOT RUN`. Các nguồn lưu dạng URL text. Link bản sửa đúng pin Requirements, M1-02 và Issue #15. Không có phần đuôi ngoài Table như workbook ban đầu.

## Oracle và phạm vi kiểm

Áp bảng quyết định V1 và TA. Với dữ liệu synthetic đã qua D04, liệt kê các khả năng True/False của boolean thiếu/null, giữ nguyên trường đã biết. Tính R01 = ¬S ∧ K ∧ (H ∨ C), R02 = S ∧ (số hệ TRUE ≥2), R03 = S ∧ ((¬I ∧ H) ∨ C). Giao là Def, hợp là Poss, mọi khả năng dương là AllPV. Missing/null tuổi override sau validation. Với tuổi có, definite được chọn trước possible, và R-SOC cần cả phản vệ được chứng minh và bằng chứng HATT. CANONICAL dùng khi PHAN_VE, Def rỗng và AllPV. Mixed dùng THEO_DOI/null với lý do thiếu thông tin. Giữ phép so nghiêm ngặt cho HATT và `10×HATT < 7×nền`. Nhóm duyệt D13-E ngày 09/11/2026. [D], [T], [Q], [A].

Tính độc lập 175 fixture chính, kết quả **139 classification, 28 TypeError, 8 ValueError**, không sai khác mức/mã/lớp lỗi so với CSV. Đọc số JSON theo kiểu Python để không nhầm 90.0 với 90. Ba nonfinite dùng registry token, không eval. 81 internal được tính riêng, gồm AND 9, OR 9, NOT 3, count 15, count+allergen 45. Không gọi classifier hoặc pytest nghiệp vụ. [C], [U], [F], [IS].

Kiểm đủ 64 QA case. 21 JSON inline tính được, gồm 18 trùng ít nhất một fixture và ba own variant `QA-003/016/019`. Các ID fixture/plan dạng cụ thể trong cột E và checklist G phân giải được. Các nhóm `TA15-*`, internal 81 và hoạt động QA thuần được đối chiếu như nhóm. Kết quả dưới đây cho thấy vì sao cùng output vẫn có thể kiểm nhầm nhánh. [C], [Plan], [I], [B].

| Finding | Mức | Ô | Hiện trạng xác minh | Tái lập và sửa |
| --- | --- | --- | --- | --- |
| NC-01 | P2 | AC_MATRIX!M2:N12 | 22 cache bằng 0. Đếm độc lập theo tag cho kết quả khác ở 21/22 ô (M3 đúng 0). | Đọc data_only, sau đó đếm theo criterion wildcard của từng hàng. Giữ công thức và chạy CalculateFullRebuild. |
| NC-02 | P2 | QA_CASES!E16:H16,E22:H22 | QA-015 G16 khớp MISS-007. MISS-015/016 thay đổi field thiếu. QA-021 E22 liệt kê CON-001–003, G22 lại RULE-002/PEND-002/PEND-005. Mục đích từng nhóm và expected chưa tách rõ. | So từng field với CSV. CON-001 và RULE-002 cùng input, CON-002/003 kiểm contract khác PEND. Gắn EXACT/VARIANT/CONTRAST và từng điều kiện assert. |
| NC-03 | P2 | QA_CASES!G27:G30,H29:H30 | QA-026 chỉ ghi gọi trực tiếp, thiếu fixture cụ thể. QA-027 G chỉ inject append dù H yêu cầu từng stage. QA-028 G chỉ tuổi âm + OSError, N yêu cầu từng stage. QA-029 G chỉ nói audit/log/error dù H kiểm cả actual ly_do. | Dùng INT-001/006/007/008/015/021. Tách valid output có ly_do với invalid error không có output, thêm stage, loại input và proof không rò. |
| NC-04 | P2 | QA_CASES!H45:H46,H60,H62,G65:H65; QA_CHECKLIST!E55:F55,F57,G58 | Dòng AllPV thiếu HATT/nền cần nêu đủ canonical disclosure, và 015/016 bị đảo null/missing nếu đọc theo thứ tự ID. 64 là không gian logic, câu '64 enumerations' không nên bắt buộc cách thực thi. CHK-056 chỉ ghi expected của R01 direct, chưa ghi R03 definite thắng R02 possible cho MISS-013/014. RULE-020 mới nằm trong ghi chú. | Đọc raw D13E-015/016, tính Def/Poss của MISS-013/014 và TA15-BOOL3, tính RULE-020. Tách assertion helper khỏi public. Pin thiếu tuổi và không nâng low BP đơn độc. |
| NC-05 | P2 | AC_MATRIX!D9,J8; QA_CHECKLIST!J4:J5 | A-08 còn 157 public. CHK-003/004 nói PEND chờ cập nhật dù đã resolve. A-07 nhắc 157 trong dòng giải thích không cộng 81. | Đếm CSV 175 +81. So TA, ISSUE15_SYNC và PEND-001–007. Cập nhật baseline/chuyển gate về runtime. |
| NC-06 | P2 | QA_CASES!I11,I14:I15,I23; QA_CHECKLIST!G7; GAP_REVIEW!L8 | §8.2 Rev04 dành cho sáu oracle D13-E, không phải nguồn trực tiếp cho INV-043/001 và sáu INV nullable. CHK-006 ghi lọc 36 trong INV-002–043, thực tế chỉ 35, cộng AUD-002 mới 36. Ô nguồn F07 trống. | Mở Q §3.1/3.2/4.4/8.1–8.2, lọc exception_class theo prefix. Thay tham chiếu đúng, ghi nguồn Table tại workbook. |
| NC-07 | P3 | QA_CASES!F13,H25:N26; QA_CHECKLIST!J23 | Precondition 'an toàn' của QA-012 nói quá mức mà fixture chứng minh. Dòng audit ràng buộc status/UUID còn lẫn diễn đạt và CHK-022 ghi chờ PR thật dù đã có PR tài liệu. | Mở RULE-014/INT-001–005 và PR #1–3. Dùng 'không đủ tiêu chí tụt HATT', tách PR nghiệp vụ, gắn status tương ứng. |

## Theo từng QA case

Trong bảng, các giá trị sau dấu `@` là dòng CSV. Ký hiệu khác field dùng tên key từ input thật. Fixture không có JSON nội tuyến lấy nguyên dữ liệu pinned. Ca integration/evidence không có oracle phân loại riêng được đánh giá theo thủ tục và expected. [C], [I], [B].

| Ô QA | Oracle tĩnh | Fixture / chênh lệch | Kết luận thiết kế |
| --- | --- | --- | --- |
| QA-001 · QA_CASES!D2:O2 | PHAN_VE / R02-PV / DIRECT | PEND-001@79 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-002 · QA_CASES!D3:O3 | THEO_DOI / null / AGE_OVERRIDE | PEND-002@80 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-003 · QA_CASES!D4:O4 | THEO_DOI / null / AGE_OVERRIDE | INV-001@86 khác co_ton_thuong_da_niem_mac, co_trieu_chung_ho_hap · PEND-007@85 khác huyet_ap_tam_thu, tuoi | Own variant tuổi null + R01; INV-001/PEND-007 là đối chứng. |
| QA-004 · QA_CASES!D5:O5 | PHAN_VE / R01-PV / DIRECT | PEND-003@81 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-005 · QA_CASES!D6:O6 | PHAN_VE / R01-PV / DIRECT | PEND-004@82 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-006 · QA_CASES!D7:O7 | PHAN_VE / R02-PV / DIRECT | PEND-005@83 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-007 · QA_CASES!D8:O8 | PHAN_VE / R02-PV / DIRECT | PEND-006@84 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-008 · QA_CASES!D9:O9 | PHAN_VE / R01-PV / DIRECT | BP-022@51 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-009 · QA_CASES!D10:O10 | SOC_PHAN_VE / R-SOC / TIER1 | BP-025@54 exact · BP-026@55 khác huyet_ap_tam_thu_nen | BP-025 exact, BP-026 nền thiếu là đối chứng. |
| QA-010 · QA_CASES!D11:O11 | SOC_PHAN_VE / R-SOC / TIER1 | INV-043@128 exact · MISS-007@65 khác co_trieu_chung_tieu_hoa_nang, huyet_ap_tam_thu | INV-043 exact SOC, MISS-007 đối chứng PV. Sửa nguồn NC-06. |
| QA-011 · QA_CASES!D12:O12 | PHAN_VE / R02-PV / DIRECT | RULE-011@12 · RULE-012@13 · PEND-001@79 | RULE-011 exact theo dữ liệu mô tả. RULE-012 variant 3/4, PEND-001 overlap contrast. |
| QA-012 · QA_CASES!D13:O13 | PHAN_VE / R03-PV / DIRECT | RULE-014@21 exact | R03-only, loại cách gọi HATT an toàn. |
| QA-013 · QA_CASES!D14:O14 | THEO_DOI / null / AGE_OVERRIDE | INV-001@86 exact | Khớp fixture và expected. Giữ input/expected. |
| QA-014 · QA_CASES!D15:O15 | THEO_DOI / null / NO_RULE | INV-017@102 · INV-021@106 · INV-025@110 · INV-029@114 · INV-033@118 · INV-037@122 | Sáu fixture nullable riêng, không dùng chung JSON. |
| QA-015 · QA_CASES!D16:O16 | PHAN_VE / R01-PV / DIRECT | MISS-007@65 exact · MISS-015@73 khác co_trieu_chung_tieu_hoa_nang, co_trieu_chung_tuan_hoan · MISS-016@74 khác co_trieu_chung_ho_hap, co_trieu_chung_tieu_hoa_nang, co_trieu_chung_tuan_hoan | MISS-007 exact, MISS-015/016 biến thể. NC-02. |
| QA-016 · QA_CASES!D17:O17 | TypeError | INV-003@88 khác co_di_nguyen_nghi_ngo, tuoi · INV-004@89 khác co_di_nguyen_nghi_ngo, tuoi · INV-018@103 khác co_di_nguyen_nghi_ngo · INV-022@107 khác co_di_nguyen_nghi_ngo, di_nguyen_qua_duong_hit · INV-026@111 khác co_di_nguyen_nghi_ngo, co_ton_thuong_da_niem_mac · INV-030@115 khác co_di_nguyen_nghi_ngo, co_trieu_chung_ho_hap · INV-034@119 khác co_di_nguyen_nghi_ngo, co_trieu_chung_tuan_hoan · INV-038@123 khác co_di_nguyen_nghi_ngo, co_trieu_chung_tieu_hoa_nang | Own literal chuỗi None. Các INV trong E17 chỉ đối chứng khác loại/vị trí. |
| QA-017 · QA_CASES!D18:O18 | TypeError | INV-019@104 exact · INV-023@108 khác co_di_nguyen_nghi_ngo, di_nguyen_qua_duong_hit · INV-027@112 khác co_di_nguyen_nghi_ngo, co_ton_thuong_da_niem_mac · INV-031@116 khác co_di_nguyen_nghi_ngo, co_trieu_chung_ho_hap · INV-035@120 khác co_di_nguyen_nghi_ngo, co_trieu_chung_tuan_hoan · INV-039@124 khác co_di_nguyen_nghi_ngo, co_trieu_chung_tieu_hoa_nang | INV-019 exact, năm field khác chạy parameterized riêng. |
| QA-018 · QA_CASES!D19:O19 | ValueError | INV-002@87 exact · INV-005@90 khác tuoi · INV-006@91 khác tuoi · INV-007@92 khác tuoi | INV-002 exact. INV-005–007 fixture_ref riêng đều ValueError. |
| QA-019 · QA_CASES!D20:O20 | ValueError | INV-041@126 khác co_ton_thuong_da_niem_mac, co_trieu_chung_ho_hap, extra_marker, ngoai_allowlist | Own key lạ với R01 đủ. INV-041 đối chứng không R01. |
| QA-020 · QA_CASES!D21:O21 | PHAN_VE / R01-PV / CANONICAL | MISS-009@67 exact · MISS-012@70 khác co_di_nguyen_nghi_ngo, co_trieu_chung_ho_hap, co_trieu_chung_tieu_hoa_nang · INT-018 | MISS-009 exact, I=true và R01/R02/R03=U/U/F. MISS-012 riêng ở QA-056. |
| QA-021 · QA_CASES!D22:O22 | PHAN_VE / R01-PV / DIRECT · THEO_DOI / null / NO_RULE | CON-001@129 · CON-002@130 · CON-003@131 | Cần tách fixture schema và fixture nêu dữ liệu thiếu. NC-02. |
| QA-022 · QA_CASES!D23:O23 | THEO_DOI / null / AGE_OVERRIDE | INV-001@86 exact · TA15-AGE-NULL@137 khác co_ton_thuong_da_niem_mac, co_trieu_chung_ho_hap, huyet_ap_tam_thu · TA15-AGE-MISSING@138 khác co_ton_thuong_da_niem_mac, co_trieu_chung_ho_hap, huyet_ap_tam_thu, tuoi · AUD-002@135 khác co_di_nguyen_nghi_ngo, tuoi · INT-017 | INV-001 exact, CLASSIFY/SUCCESS với writer thành công; AUD-002 tách khỏi success. |
| QA-023 · QA_CASES!D24:O24 | ValueError | INV-002@87 exact · AUD-002@135 khác co_di_nguyen_nghi_ngo, tuoi · INV-003@88 khác tuoi · INV-041@126 khác extra_marker, tuoi · INT-005 | INV-002 exact ValueError, AUD-002 và INV-003 TypeError, INV-041 ValueError, tất cả writer thành công mới có INVALID_INPUT. |
| QA-024 · QA_CASES!D25:O25 | PHAN_VE / R01-PV / DIRECT · TypeError · THEO_DOI / null / NO_RULE | AUD-001@134 · AUD-002@135 · AUD-003@136 · INT-001 · INT-005 · INT-008 | Parse bốn field, UTC aware, UUID, CLASSIFY và status theo đường. NC-07. |
| QA-025 · QA_CASES!D26:O26 | THEO_DOI / null / NO_RULE | AUD-003@136 · INT-002 · INT-003 · INT-004 · INT-012 | Explicit/implicit/nested/reset ở INT-002/003/004/012. |
| QA-026 · QA_CASES!D27:O27 | Thủ tục/evidence | INT-001 | Direct RULE-002 qua override path, một record ghi xong trước return. NC-03. |
| QA-027 · QA_CASES!D28:O28 | Thủ tục/evidence | INT-006 · INT-008 | Fail closed mọi stage. G phải parameterize các stage. NC-03. |
| QA-028 · QA_CASES!D29:O29 | Thủ tục/evidence | INT-007 | Double failure, audit error an toàn ưu tiên. Cần input và stage chạy rõ. NC-03. |
| QA-029 · QA_CASES!D30:O30 | Thủ tục/evidence | INT-015 · INT-021 | Canary audit/error/chaining và actual ly_do cần hai đường riêng. NC-03. |
| QA-030 · QA_CASES!D31:O31 | Thủ tục/evidence | INT-012 | Clean checkout SHA/log/exit; chờ M2. |
| QA-031 · QA_CASES!D32:O32 | Thủ tục/evidence | Hoạt động QA | PR CI job đúng SHA và pytest nghiệp vụ; chờ M2. |
| QA-032 · QA_CASES!D33:O33 | Thủ tục/evidence | BENCH-001 · BENCH-002 · BENCH-003 · BENCH-004 · BENCH-005 · BENCH-006 | Benchmark full path có I/O, ≥1.000 mẫu, 100 warm-up, audit delta, raw timing và env; chờ M3. |
| QA-033 · QA_CASES!D34:O34 | Thủ tục/evidence | INT-016 | Kiểm disclaimer nguyên văn tại README root SHA nghiệm thu; chờ M2. |
| QA-034 · QA_CASES!D35:O35 | THEO_DOI / null / AGE_OVERRIDE | TA15-AGE-NULL@137 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-035 · QA_CASES!D36:O36 | THEO_DOI / null / AGE_OVERRIDE | TA15-AGE-MISSING@138 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-036 · QA_CASES!D37:O37 | PHAN_VE / R01-PV / DIRECT | TA15-CURRENT_BP-NULL@139 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-037 · QA_CASES!D38:O38 | PHAN_VE / R01-PV / DIRECT | TA15-CURRENT_BP-MISSING@140 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-038 · QA_CASES!D39:O39 | PHAN_VE / R02-PV / DIRECT | TA15-BASELINE_BP-NULL@141 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-039 · QA_CASES!D40:O40 | PHAN_VE / R02-PV / DIRECT | TA15-BASELINE_BP-MISSING@142 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-040 · QA_CASES!D41:O41 | PHAN_VE / R01-PV / CANONICAL | TA15-BOOL1-NULL@143 | BOOL1 null, canonical đúng, giữ disclosure. |
| QA-041 · QA_CASES!D42:O42 | PHAN_VE / R01-PV / CANONICAL | TA15-BOOL1-MISSING@144 | BOOL1 missing, canonical đúng, giữ disclosure. |
| QA-042 · QA_CASES!D43:O43 | PHAN_VE / R03-PV / DIRECT | TA15-BOOL2-NULL@145 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-043 · QA_CASES!D44:O44 | PHAN_VE / R03-PV / DIRECT | TA15-BOOL2-MISSING@146 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-044 · QA_CASES!D45:O45 | PHAN_VE / R03-PV / DIRECT | TA15-BOOL3-NULL@147 | R03 definite thắng R02 possible. Bổ sung helper assertion. |
| QA-045 · QA_CASES!D46:O46 | PHAN_VE / R03-PV / DIRECT | TA15-BOOL3-MISSING@148 | R03 definite thắng R02 possible. Bổ sung helper assertion. |
| QA-046 · QA_CASES!D47:O47 | PHAN_VE / R01-PV / DIRECT | TA15-BOOL4-NULL@149 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-047 · QA_CASES!D48:O48 | PHAN_VE / R01-PV / DIRECT | TA15-BOOL4-MISSING@150 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-048 · QA_CASES!D49:O49 | PHAN_VE / R01-PV / DIRECT | TA15-BOOL5-NULL@151 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-049 · QA_CASES!D50:O50 | PHAN_VE / R01-PV / DIRECT | TA15-BOOL5-MISSING@152 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-050 · QA_CASES!D51:O51 | PHAN_VE / R01-PV / DIRECT | TA15-BOOL6-NULL@153 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-051 · QA_CASES!D52:O52 | PHAN_VE / R01-PV / DIRECT | TA15-BOOL6-MISSING@154 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-052 · QA_CASES!D53:O53 | SOC_PHAN_VE / R-SOC / TIER1 | TA15-NO_DOWNGRADE_SHOCK-NULL@155 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-053 · QA_CASES!D54:O54 | SOC_PHAN_VE / R-SOC / TIER1 | TA15-NO_DOWNGRADE_SHOCK-MISSING@156 | Fixture TA15 đúng kiểu thiếu/null và mức/mã. Giữ phép so cặp và lý do theo tình huống. |
| QA-054 · QA_CASES!D55:O55 | THEO_DOI / null / MIXED | TA15-DEPENDENT_INHALATION-NULL@157 | Inhalation null Mixed, reason thiếu dữ liệu và cấm claim an toàn/observed unknown. |
| QA-055 · QA_CASES!D56:O56 | THEO_DOI / null / MIXED | TA15-DEPENDENT_INHALATION-MISSING@158 | Inhalation missing Mixed, reason thiếu dữ liệu và cấm claim an toàn/observed unknown. |
| QA-056 · QA_CASES!D57:O57 | THEO_DOI / null / MIXED | MISS-012@70 exact · INT-019 · INT-021 | MISS-012 exact. Một khả năng R02, một khả năng không có rule, U chỉ ở R02. |
| QA-057 · QA_CASES!D58:O58 | PHAN_VE / R01-PV / CANONICAL | D13E-001@159 · D13E-002@160 · INT-018 · INT-020 · INT-021 | D13E-001/002 AllPV, Def rỗng, 16 khả năng, canonical và equivalence. |
| QA-058 · QA_CASES!D59:O59 | SOC_PHAN_VE / R-SOC / TIER1 | D13E-003@161 · INT-020 | D13E-003 sốc khi AllPV + HATT đủ. RULE-020 đối chứng. |
| QA-059 · QA_CASES!D60:O60 | PHAN_VE / R01-PV / CANONICAL | D13E-004@162 · D13E-005@163 · INT-020 · INT-021 | D13E-004/005 current BP null/missing. Cần explicit canonical disclosure. |
| QA-060 · QA_CASES!D61:O61 | THEO_DOI / null / AGE_OVERRIDE | D13E-006@164 · D13E-007@165 · INT-020 | D13E-006/007 thiếu tuổi override public, helper coverage vẫn kiểm riêng. |
| QA-061 · QA_CASES!D62:O62 | THEO_DOI / null / MIXED | D13E-008@166 · D13E-009@167 · INT-019 · INT-021 | D13E-008/009 64 khả năng và Mixed. Không ràng buộc cách triển khai phải lặp 64 lần. |
| QA-062 · QA_CASES!D63:O63 | THEO_DOI / null / MIXED | D13E-010@168 · D13E-011@169 · D13E-012@170 · D13E-013@171 · INT-019 · INT-021 | D13E-010–013 hai cặp Mixed riêng. |
| QA-063 · QA_CASES!D64:O64 | PHAN_VE / R01-PV / DIRECT | D13E-014@172 · INT-021 | D13E-014 DIRECT R01 với ba UNKNOWN. Cần MISS-013/014 để thực sự thử cạnh tranh ưu tiên. |
| QA-064 · QA_CASES!D65:O65 | PHAN_VE / R01-PV / CANONICAL · PHAN_VE / R01-PV / DIRECT · SOC_PHAN_VE / R-SOC / TIER1 | D13E-015@173 · D13E-016@174 · D13E-017@175 · D13E-018@176 · INT-020 · INT-021 | 015 null, 016 missing; 017 17.99 direct, 018 18 shock. G đảo cách ghi thứ tự nền. NC-04. |

## A-01 đến A-11 và checklist

| AC | Độ phủ thiết kế và việc còn lại |
|---|---|
| A-01 | Signature, ba khóa, validation, selector, direct audit có nguồn. Cần nối procedure cụ thể ở QA-026 và test M2. |
| A-02 | Source review, ca mới và đảo key đã tách nonmutation. Chờ code và evidence. |
| A-03 | Có ba mức, priority, BP/tuổi, toàn bộ D13E và RULE-020. Bổ sung expected definite-first thực sự cạnh tranh trong CHK-056. |
| A-04 | Có nullable, D04, registry và sáu oracle. Sửa cách mô tả số invalid và quan hệ fixture. |
| A-05 | Có INT-021, regex và kiểm ngữ nghĩa. Sửa mâu thuẫn nhóm QA-021 và làm rõ ly_do ở biến thể missing BP. |
| A-06 | Có INT-001–021 trên các nhóm liên quan. Cần hoàn chỉnh procedure success/fault/canary và giữ hai điểm quyết định mở. |
| A-07 | 175 main và 81 internal riêng, đủ nhóm test. Chờ collection/runtime M2. |
| A-08 | Clone SHA, deps, pytest và log. Sửa 157 cũ ở D9 rồi giữ gate M2. |
| A-09 | Đúng gate PR run/step log/commit nghiệp vụ. Chưa có evidence chạy. |
| A-10 | BENCH-001–006 đủ protocol, timing thực, loại warm-up và không lọc lỗi. Chờ M3. |
| A-11 | Đúng chuỗi exact ở SHA nghiệm thu và INT-016, chờ README runtime. |

Đã đọc 60 checklist. CHK-001–007 bao contract, D04/D13 và explanation. CHK-008–017 là gate audit tổng quan. CHK-018–023 bao inventory, isolation, pytest và CI. CHK-024–029 là benchmark/README. CHK-030–046 lần lượt dẫn INT-001–017. CHK-047–052 dẫn BENCH-001–006, có kiểm 10/19 ms với vector 20 mẫu và index 499/949 cho N=1000. CHK-053–060 bao các nhóm D13E, review ngữ nghĩa, invalid audit và sign-off. Các dòng tổng quan và chi tiết nên trỏ cùng artifact khi trùng việc kiểm, không tính là hai lần chạy. [Plan], [I], [B].

Bốn điểm trọng tâm tính lại:
- `MISS-009` và TA15-BOOL1 null/missing có hai completion {R01} và {R02}. CANONICAL R01, helper U/U/F. `MISS-012` có tập rỗng và {R02}, MIXED. Hai ca TA15-DEPENDENT_INHALATION có {R03} hoặc rỗng, MIXED. [C], [S].
- `MISS-013/014` và TA15-BOOL3 có Def R03 và R02 possible. D13E-014 có Def=Poss={R01}. Ca R01 kiểm DIRECT nhưng riêng nó không thử rule possible ưu tiên cao hơn. [C].
- `RULE-020` có HATT evidence TRUE và TIER1_MATCH FALSE. D13E-003 cùng AllPV và tụt HATT trả R-SOC. 017/018 giữ tuổi 17.99 và 18 như CSV, không làm tròn. [C], [I].
- INT-021 kiểm actual ly_do. Với DIRECT nêu rule definite, CANONICAL nêu mã đại diện và chưa xác nhận riêng, MIXED nêu thiếu thông tin. Kiểm âm trên observed UNKNOWN, tuyên bố an toàn, raw clinical values và điều trị. Regex chỉ là một lớp. [Q], [C], [I].

Điểm chờ quyết định vẫn gồm default audit path INT-010, unexpected internal exception INT-013, CON-004 nonmutation và review/acceptance của nhóm. NOT RUN hợp lệ tại M1. Không xem đây là lỗi thiết kế chỉ vì chưa có runtime evidence.

[D]: https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md
[Q]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md
[A]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md
[G]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/f82ef67c7cf7f0ac5445bca17c80519af91339d8/docs/PROJECT_GUIDE.md
[P]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/f82ef67c7cf7f0ac5445bca17c80519af91339d8/docs/TEAM_PLAN.md
[C]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv
[U]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTERNAL_STATE_CASES.csv
[I]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md
[B]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/BENCHMARK_PLAN.md
[R]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/RULE_DESIGN.md
[Plan]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_PLAN.md
[S]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/ISSUE15_SYNC.md
[IS]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTERNAL_STATE_TEST_PLAN.md
[F]: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/fixtures/NONFINITE_INPUTS.json
[T]: https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248
[E]: https://github.com/fossbk-spec/ktpmud-book/blob/gh-pages/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html
