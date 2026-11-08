# TASK 02E — Leader-owned remediation M1-02

Owner bản sửa: Huy Đức (Leader), AI hỗ trợ; ngày 09/11/2026. Baseline đóng góp Hải: docs/m1-tests-hai, SHA768f196e6a9ec3b1142c44399ce8288f7cc2e87e. Giữ lịch sử tác giả, không gán bản sửa/peer review cho Hải.

## 1. Nguồn và Git scope

Nhánh review/m1-02-leader-remediation tạo từ đúng baseline. Nhánh Hải/main/track-a-development/PR#1/PR#2 không bị sửa. Nguồn current [Q/A Revision04](sources/README.md); D13-E **APPROVED BY LEAD — D13-E — 09/11/2026**, risk canonical đã chấp nhận. Chỉ sửa docs/m1-hai, không runtime/test suite/CI/QA/Guide/Plan hoặc snapshots lịch sử. Không PR/merge trong TASK02E.

## 2. Nội dung cần Leader kiểm

- [RULE_DESIGN](RULE_DESIGN.md)/[ISSUE15_SYNC](ISSUE15_SYNC.md): exact approved D13-E, DIRECT/CANONICAL và HATT/Tier1 semantics.
- [TEST_CASES.csv](TEST_CASES.csv)/[TEST_PLAN](TEST_PLAN.md): 175 cases; giữ 157 ID/input và level/ID/exception cũ; thêm 18 focused cases, 18 equivalence groups; 36 invalid=28 TypeError+8 ValueError.
- [REVIEW_RESPONSE](REVIEW_RESPONSE.md)/[REVIEW_NOTES](REVIEW_NOTES.md): F01–F04/R01–R11 với acceptance conditions và giới hạn.
- [VALIDATION_REPORT](VALIDATION_REPORT.md)/[REMEDIATION_EVIDENCE.json](REMEDIATION_EVIDENCE.json): static oracle/logic/provenance/Git scope evidence; không engine test pass.
- [M2](../M2/README.md): 81 internal rows bất biến, plans INT/FIXTURE/BENCH và property coverage cần triển khai sau.

## 3. Sáu oracle policy đã chốt

MISS-009 và TA15-BOOL1-NULL/MISSING → PHAN_VE/R01-PV CANONICAL; ly_do MUST đại diện/chưa independently confirmed, không observed S=False. Helpers MISS-009 vẫn R01=U,R02=U,R03=F.

MISS-012 và TA15-DEPENDENT_INHALATION-NULL/MISSING → THEO_DOI/null MIXED, insufficient information, không khẳng định an toàn. Null/missing cùng mức/mã, không bắt reason nguyên văn hoặc UUID giống.

## 4. Evidence và những việc chưa làm

Static CSV/JSON parse, independent oracle và 81 mathematical rows được kiểm riêng, không gọi classify. 175 classifier cases, pytest/clean-checkout, actual helper/Enum tests, integration/audit/privacy/error paths, CI và benchmark đều NOT EXECUTED trong task này.

Chưa xác nhận Hải/Việt Đức peer review, QA Matrix mapping hoặc Huy final acceptance. Default audit path PROPOSED — AWAITING PEER REVIEW; unexpected internal exception residual; CON-004 nonmutation là đề nghị riêng. Các điểm này không được approval D13 giải quyết thay.

## 5. Checklist acceptance của Huy

- [ ] Đúng base/new branch/commit scope docs/m1-hai; nhánh nguồn và snapshots nguyên vẹn.
- [ ] Sáu approved policy cases đủ source/status và explanation positive/negative; không gán canonical là TA-defined.
- [ ] 157 input/ID/level/ID/exception cũ giữ nguyên, 18 new cases có gap độc lập.
- [ ] RULE-020 HATT evidence TRUE nhưng TIER1_MATCH FALSE; không ép helpers MISS-009 thành TRUE.
- [ ] 81 math rows và formulas/ngưỡng/benchmark protocol không đổi; đọc static evidence, không tính như runtime.
- [ ] Việt Đức map/review QA A-01–A-11, core/audit và explanation; Hải review technical handoff nếu có.
- [ ] Giữ unresolved không thuộc D13 và quyết định acceptance/PR/merge riêng.
