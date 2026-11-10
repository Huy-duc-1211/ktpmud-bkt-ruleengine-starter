# TASK 02N-C — Kiểm chứng Excel và nhật ký sửa

Bản vào `QA_MATRIX_M1_SELF_REVIEW_PATCHED.xlsx`, 43.195 byte, SHA-256 `453badfe2041e09481ab8e90db0a6589dd6eaa80fcafb395817afb17515d3079`. SHA nguồn kiểm lại sau khi ghi bản sao vẫn khớp. Bản ứng viên `QA_MATRIX_M1_CODEX_FINAL_CANDIDATE.xlsx`, 51.804 byte, SHA-256 `7a870f6fa36115ad2ef37969866816e90c47ce695995b9c7ddc3bb6efd344af7`.

## Tính lại và mở lại

Máy có Excel 16.0. Sandbox mặc định từ chối COM với 0x80070005. Phiên Excel COM riêng được mở qua quyền thực thi được cấp, tắt macro, events và cập nhật link. Chỉ mở bản sao. Áp 40 chỉnh sửa giá trị, gọi `CalculateFullRebuild`, kiểm CalculationState=0, lưu, đóng và mở lại chỉ đọc. Sau khi phát hiện AutoFilter tắt, bật bộ lọc trên bốn Table, gọi lại `CalculateFullRebuild`, lưu và mở lại. Không đặt điều kiện lọc. Đọc cache OOXML của file cuối qua openpyxl, đối chiếu Excel readback và đếm Python độc lập theo các tag AC. Không ghi cache bằng tay.

Cả 22 định nghĩa ở `AC_MATRIX!M2:N12` giữ nguyên. Với hàng `r=2…12`, dạng công thức chính xác là:

```text
M[r] = COUNTIF(QA_CASES!$B$2:$B$500,"*"&A[r]&"*")
N[r] = COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A[r]&"*")
```

Ký hiệu `[r]` chỉ vị trí hàng. Bảng dưới ghi từng định nghĩa, cache sau lưu và kết quả đếm độc lập. Cả 22 cache trước sửa là 0, trong đó M3 vốn có số đúng bằng 0. Tổng sau sửa là 97 lượt gắn QA và 81 lượt gắn checklist. Một dòng nhiều tag có thể đóng góp cho nhiều AC.

| AC/ô | M công thức | N công thức | Excel M/N | Cache M/N | Python M/N |
| --- | --- | --- | --- | --- | --- |
| A-01 M2/N2 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A2&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A2&"*")` | 8/8 | 8/8 | 8/8 |
| A-02 M3/N3 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A3&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A3&"*")` | 0/2 | 0/2 | 0/2 |
| A-03 M4/N4 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A4&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A4&"*")` | 21/6 | 21/6 | 21/6 |
| A-04 M5/N5 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A5&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A5&"*")` | 39/12 | 39/12 | 39/12 |
| A-05 M6/N6 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A6&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A6&"*")` | 9/3 | 9/3 | 9/3 |
| A-06 M7/N7 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A7&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A7&"*")` | 8/23 | 8/23 | 8/23 |
| A-07 M8/N8 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A8&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A8&"*")` | 8/8 | 8/8 | 8/8 |
| A-08 M9/N9 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A9&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A9&"*")` | 1/3 | 1/3 | 1/3 |
| A-09 M10/N10 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A10&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A10&"*")` | 1/2 | 1/2 | 1/2 |
| A-10 M11/N11 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A11&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A11&"*")` | 1/11 | 1/11 | 1/11 |
| A-11 M12/N12 | `=COUNTIF(QA_CASES!$B$2:$B$500,"*"&A12&"*")` | `=COUNTIF(QA_CHECKLIST!$B$2:$B$500,"*"&A12&"*")` | 1/3 | 1/3 | 1/3 |

## Hồi quy cấu trúc và ngữ nghĩa

| Sheet | ID | Table, AutoFilter sau sửa | Dropdown |
|---|---:|---|---|
| AC_MATRIX | 11 | ACTraceability A1:N12 | G2:G12, H2:H12 |
| QA_CASES | 64 | QACases A1:O65 | J2:J65, K2:K65 |
| QA_CHECKLIST | 60 | QAChecklist A1:L61 | H2:H61 |
| GAP_REVIEW | 15 | QAFindings A1:L16 | Giữ như bản vào |

Bốn `ListObject.ShowAutoFilter` chuyển false → true. `FilterMode` false trên cả bốn sheet sau khi mở lại, tức chưa áp tiêu chí. Mỗi AutoFilter ref trùng Table ref. TableStyleMedium2, freeze A2 và phạm vi validation giữ nguyên. So từng ô không thấy thay đổi ngoài 40 ô trong danh sách và cache. Không thêm, xóa hoặc đổi ID.

Font, căn lề và bảo vệ ô khớp. Excel chuẩn hóa XML border trống, fill nền/tint và làm tròn nhẹ 32 thông số hàng/cột khi lưu. Đây là thay đổi do Excel serialize, không phải thay kiểu hiển thị có chủ đích. Đã xem mẫu trước/sau của bốn sheet. Một số ô notes dài trong AC_MATRIX có chiều cao cố định từ bản vào và cần chọn ô để đọc trọn văn bản. Bản cuối giữ kích thước hiển thị đó.

Kiểm lại 21 JSON inline, 64 QA, 60 checklist, 175 fixture chính và 81 nội bộ, không có ID tham chiếu cụ thể mất, không sai mức/mã/lớp lỗi so với oracle. Các dòng fixture nhóm/thủ tục đã chỉnh được đối chiếu riêng với CSV và INT. 135 status thực thi còn NOT RUN, các evidence cells trống. Không phát hiện lỗi công thức. Nguồn URL theo đúng SHA/TA, đã kiểm Decision Table, Req/ADR, Plan, CSV chính, Internal State, INT, BENCH, registry và đề chính thức. [CSV](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv), [Internal CSV](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTERNAL_STATE_CASES.csv), [Integration Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md), [Đề chính thức](https://github.com/fossbk-spec/ktpmud-book/blob/gh-pages/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html).

## Nhật ký sửa đầy đủ

Ngoài 40 ô sau, thay đổi cấu trúc duy nhất có chủ đích là bật AutoFilter bốn Table nêu trên. NC-01 xử lý bằng Excel recalc, giữ 22 công thức. Không có sửa giá trị JSON inline, clinical rules, nguồn quy định, hay trạng thái thực thi.

| Finding | Ô | Trước | Sau |
| --- | --- | --- | --- |
| NC-02 | QA_CASES!E16 | MISS-007; MISS-015; MISS-016 | MISS-007 (EXACT G16); MISS-015/016 (VARIANT, mỗi fixture riêng). |
| NC-02 | QA_CASES!H16 | PHAN_VE / R01-PV, không raise/hạ mức. | PHAN_VE / R01-PV cho cả ba fixture. Không raise do nullable và không hạ mức. MISS-015/016 đổi trường thiếu nên phải chạy input riêng. |
| NC-02 | QA_CASES!E22 | CON-001; CON-002; CON-003 | CON-001/002/003 (contract); RULE-002 (cùng input CON-001); PEND-002/005 (CONTRAST thiếu tuổi/nền); INT-021 (attribution). |
| NC-02 | QA_CASES!G22 | RULE-002/PEND-002/PEND-005 output theo các input đã chuẩn bị. | Load từng ID pinned: CON-001/002/003 kiểm schema; RULE-002 cùng input CON-001; PEND-002/005 kiểm lý do thiếu tuổi/nền. INT-021 chạy riêng cho DIRECT/CANONICAL/MIXED. |
| NC-02 | QA_CASES!H22 | ly_do nonempty, diễn giải rule/missing đúng tình huống, không raw input/điều trị. | CON-001/RULE-002 PHAN_VE/R01-PV; CON-002/003 và PEND-002 THEO_DOI/null; PEND-005 PHAN_VE/R02-PV. Đúng 3 keys, ly_do không rỗng, nêu căn cứ/thiếu dữ liệu, không raw input, PII hoặc điều trị. Kiểm attribution và mẫu âm theo INT-021. |
| NC-02 | QA_CASES!N22 | Test Plan M1-02 hiện hành đã có tại PR #3; test code/runtime sẽ kiểm trong M2. | CON-002/003 kiểm contract, không dùng oracle thiếu tuổi/nền của PEND. M2 thu actual output và review ngữ nghĩa/privacy. |
| NC-03 | QA_CASES!G27 | Direct call không qua CLI hoặc wrapper. | INT-001: nạp RULE-002 từ CSV; gọi classify(patient) trực tiếp với path override hợp lệ và writer thật. Ghi delta audit và thứ tự hoàn tất so với return. |
| NC-03 | QA_CASES!G28 | Sink raise OSError synthetic khi append. | INT-006: nạp một fixture valid (RULE-002). Inject OSError riêng từng stage mkdir/open/write/flush/close với path/context cô lập. INT-008 kiểm append/write/close trước return ở đường thành công. |
| NC-03 | QA_CASES!G29 | tuoi=-1; audit sink raise OSError. | INT-007: thử riêng INV-002 (tuổi âm) và INV-003 (sai kiểu). Kết hợp mỗi input với lỗi từng stage audit mkdir/open/write/flush/close có thể inject, dùng file/context cô lập. |
| NC-03 | QA_CASES!H29 | G29 tuổi=-1 → validation ValueError; đồng thời audit sink raise OSError synthetic. Theo ADR, public ưu tiên lỗi audit an toàn, không trả classification, không khẳng định INVALID_INPUT record đã ghi; không rò raw input trong message, chain, traceback hoặc log. | Validation riêng cho ValueError (INV-002) hoặc TypeError (INV-003). Khi audit cũng lỗi, public ưu tiên lỗi audit an toàn. Không có classification, không giả định INVALID_INPUT đã ghi, không rò payload qua message/chain/traceback/log. |
| NC-03 | QA_CASES!G30 | Input marker synthetic đặc biệt; kiểm tra không xuất hiện trong audit/log/error. | Hai đường riêng: INT-015 gắn canary synthetic vào input invalid và thu audit/log/error; INT-021 dùng fixture valid DIRECT/CANONICAL/MIXED, thu actual ly_do, kiểm patterns và mẫu âm đã sửa cố ý. |
| NC-03 | QA_CASES!H30 | Dùng synthetic canary: không rò dữ liệu lâm sàng thô, PII/secrets vào audit JSONL, stdout/stderr, log, error message/chain/traceback hoặc actual ly_do. INT-021 áp positive/negative explanation assertions và cần review ngữ nghĩa/privacy. | INT-015 không rò canary/payload/PII/secret qua JSONL, stdout/stderr, log, message/chain/traceback. INT-021 actual ly_do đúng provenance và không lộ raw input/điều trị/giá trị UNKNOWN giả định; mẫu sai bị loại qua kiểm patterns + review ngữ nghĩa/privacy. |
| NC-04 | QA_CASES!H45 | PHAN_VE / R03-PV | PHAN_VE / R03-PV DIRECT. Helper R03=TRUE (definite), R02=UNKNOWN (possible). R02 có ưu tiên cao hơn nhưng không thay rule definite. |
| NC-04 | QA_CASES!H46 | PHAN_VE / R03-PV | PHAN_VE / R03-PV DIRECT. Helper R03=TRUE (definite), R02=UNKNOWN (possible). Null/missing da không đổi mức/mã. |
| NC-04 | QA_CASES!E59 | D13E-003 (exact); INT-020 | D13E-003 (EXACT SOC); RULE-020 (CONTRAST, low BP nhưng không phản vệ); INT-020. |
| NC-04 | QA_CASES!H59 | SOC_PHAN_VE / R-SOC; Tier1 coverage+HATT evidence; không suy SOC từ BP đơn độc. | D13E-003 SOC_PHAN_VE / R-SOC vì AllPV và tụt HATT. RULE-020 THEO_DOI / null, HYPOTENSION_EVIDENCE TRUE nhưng TIER1_MATCH FALSE. Kiểm hai input riêng. |
| NC-04 | QA_CASES!H60 | PHAN_VE / R01-PV CANONICAL; không hạ mức vì thiếu BP; ly_do nêu chưa đánh giá sốc. | PHAN_VE / R01-PV CANONICAL cho cả hai. ly_do nêu mã đại diện chưa xác nhận riêng, thiếu HATT nên chưa đánh giá sốc, không suy dữ kiện UNKNOWN. |
| NC-04 | QA_CASES!H61 | THEO_DOI / null, reason thiếu tuổi; override có hiệu lực trước shock/coverage. | THEO_DOI / null và reason thiếu tuổi sau validation. AllPV vẫn là assertion helper riêng. Public age override áp dụng dù bằng chứng phản vệ đủ. |
| NC-04 | QA_CASES!H62 | THEO_DOI / null MIXED; đủ 64 worlds, không khẳng định an toàn. | THEO_DOI / null MIXED; miền kiểm oracle có 64 khả năng, có cả dương và âm. ly_do nêu thiếu thông tin và không khẳng định an toàn. |
| NC-04 | QA_CASES!G65 | 015/016: adult25 BP110 nền missing/null. 017: age17.99 BP100 nền200. 018: age18 BP100 nền200. | 015: tuổi25 HATT110 nền null. 016: cùng input nhưng thiếu khóa nền. 017: tuổi17.99 HATT100 nền200. 018: tuổi18 HATT100 nền200. Nạp 4 CSV fixture riêng. |
| NC-04 | QA_CASES!H65 | 015/016 PHAN_VE/R01-PV CANONICAL; 017 PHAN_VE/R01-PV DIRECT; 018 SOC_PHAN_VE/R-SOC; tuổi 17.99 không làm tròn. | 015/016 PHAN_VE/R01-PV CANONICAL, ly_do nêu mã đại diện chưa xác nhận riêng và thiếu nền. 017 PHAN_VE/R01-PV DIRECT; 018 SOC_PHAN_VE/R-SOC. Không làm tròn 17.99. |
| NC-04 | QA_CHECKLIST!E55 | D13E-008/009; internal M2 property: 729 patterns T/F/U, worlds 1–64, permutation/idempotence; independent expected. | D13E-008/009; oracle độc lập kiểm 729 mẫu T/F/U, không gian 1–64 cách hoàn thiện, permutation/idempotence. Đối chiếu helper và public riêng. |
| NC-04 | QA_CHECKLIST!F55 | MIXED => THEO_DOI/null; 64 enumerations (age present), no unsafe claims. | THEO_DOI/null MIXED khi tuổi có. Oracle có 64 khả năng với cả dương/âm. Không ràng buộc thuật toán phải lặp 64 lần nếu kết quả tương đương. Không khẳng định an toàn. |
| NC-04 | QA_CHECKLIST!F57 | D13E-014: PHAN_VE/R01 DIRECT; rule definite không bị possible priority vượt; ly_do không canonical. | D13E-014: PHAN_VE/R01-PV DIRECT. MISS-013/014: PHAN_VE/R03-PV DIRECT, helper R03 TRUE và R02 UNKNOWN. R02 possible ưu tiên cao hơn không được vượt R03 definite. |
| NC-04 | QA_CHECKLIST!G58 | D13E-003–007; D13E-015–018; INT-020 | D13E-003–007; D13E-015–018; RULE-020 (CONTRAST); INT-020 |
| NC-05 | AC_MATRIX!D9 | Full pytest suite từ 157 public + 81 internal + INT khi triển khai; INT-012 (isolation) | Full pytest suite từ 175 ca chính + 81 internal riêng + INT khi triển khai; INT-012 (isolation) |
| NC-05 | AC_MATRIX!J8 | Không cộng 81 vào 157 như public classification cases; INT là test plan M2; M1 design review: Việt Đức QA; Hải technical peer; Huy acceptance. Execution M2/M3 NOT RUN; D13-E APPROVED BY LEAD 09/11/2026 (policy nhóm); TA §5 cho phép nhóm công bố policy, KHÔNG chỉ định canonical rule. | Giữ riêng 175 ca chính, 81 ca logic nội bộ và INT (kế hoạch M2). M1 design review: Việt Đức QA; Hải technical peer; Huy acceptance. Execution M2/M3 NOT RUN. D13-E APPROVED BY LEAD 09/11/2026. |
| NC-05 | QA_CHECKLIST!J4 | Hải cần cập nhật PEND-001–007. | PEND-001–007 đã có expected theo TA. M2 kiểm đúng output, rule priority và age/BP override. |
| NC-05 | QA_CHECKLIST!J5 | Cập nhật expected mới. | Expected D02/D03 đã có ở PEND-002–007 và TA15 numeric pairs. Chờ M2 đối chiếu runtime. |
| NC-06 | QA_CASES!I11 | TA §5; Requirements Rev04 §8.2 | TA §3–5; Requirements Rev04 §4.2/§8.1; INV-043; MISS-007 đối chứng. |
| NC-06 | QA_CASES!I14 | TA §2,5; Requirements Rev04 §8.2 | TA §2,5; Requirements Rev04 §3.1/§4.4/§8.1; INV-001. |
| NC-06 | QA_CASES!I15 | TA §5; Requirements Rev04 §8.2 | TA §5; Requirements Rev04 §3.2/§4.4/§8.1; D13-E. |
| NC-06 | QA_CASES!I23 | TA §5; Requirements Rev04 §8.2 | TA §2,5; Requirements Rev04 §3.1/§4.4/§8.1; INT-017. |
| NC-06 | QA_CHECKLIST!G7 | INV-002–043 (lọc 36 invalid thật); AUD-002 (bool chuỗi); INV-005/006/007 fixture_ref | 35 invalid thuộc INV-002–043 sau lọc exception_class; + AUD-002 = 36. INV-005/006/007 dùng fixture_ref. |
| NC-06 | GAP_REVIEW!L8 | (trống) | Workbook này: QACases A1:O65, QAChecklist A1:L61, dropdown QA_CASES J/K2:65 và QA_CHECKLIST H2:H61. Xem TASK_02N_C_EXCEL_VALIDATION.md. |
| NC-07 | QA_CASES!F13 | Tuổi/HATT an toàn; chỉ hô hấp TRUE, không đường hít. | Tuổi có, HATT không thỏa điều kiện tụt. Chỉ hô hấp TRUE trong bốn hệ và không qua đường hít. |
| NC-07 | QA_CASES!H25 | Keys = Timestamp,User_UUID,Action_Type,Status; không thêm payload; Parse record với 4 keys chính xác + Timestamp ISO8601 UTC, UUID synthetically valid, Action_Type CLASSIFY, Status SUCCESS\|INVALID_INPUT. | JSONL parse được, đúng 4 keys. Timestamp ISO 8601 UTC aware, UUID hợp lệ, Action_Type CLASSIFY. SUCCESS cho valid/nullable; INVALID_INPUT cho invalid thực nếu ghi thành công. Không raw payload. |
| NC-07 | QA_CASES!N25 | Parse record với 4 keys chính xác + Timestamp ISO8601 UTC, UUID synthetically valid, Action_Type CLASSIFY, Status SUCCESS\|INVALID_INPUT. Gate M2; path override hợp lệ trừ INT-010 default path cần peer review. | Đối chiếu QA-022/023 và INT-001/005/008. Gate M2 dùng path override hợp lệ. Default path INT-010 vẫn chờ review. |
| NC-07 | QA_CASES!F26 | Có context/session API đã review. | M2 có context/provider theo OPEN-01/02 và writer thật. Dùng context/file riêng để quan sát reset và UUID. |
| NC-07 | QA_CHECKLIST!J23 | Chờ PR thật. | Cần evidence CI nghiệp vụ trên PR và đúng SHA. Các Draft PR tài liệu hiện tại chưa cung cấp bằng chứng này. |
