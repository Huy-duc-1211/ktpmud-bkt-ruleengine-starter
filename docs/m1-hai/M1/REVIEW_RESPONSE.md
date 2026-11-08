# F01–F04 và R01–R11 — bản sửa Leader-owned

Nguồn hiện hành: [Requirements Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md) (Q), [ADR Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md) (A), Decision Table (D) và [TA comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15). D13-E là **APPROVED BY LEAD — D13-E — 09/11/2026**, không phải canonical rule do TA định danh. Bản sửa TASK 02E do Leader Huy Đức sở hữu, AI hỗ trợ; chưa xác nhận Hải/Việt Đức peer review hoặc Leader nghiệm thu bản sửa.

Các trạng thái dưới mô tả repair/static evidence. Không tự đóng final acceptance, peer approval hoặc AC runtime. Xem [VALIDATION_REPORT](VALIDATION_REPORT.md) và [REMEDIATION_EVIDENCE.json](REMEDIATION_EVIDENCE.json).

## 1. F01–F04 — tiêu chí sửa cụ thể

| ID / severity | Evidence baseline | Exact repair / file | Acceptance condition cho Leader |
|---|---|---|---|
| F01 P1 | TEST_CASES MISS-012/TA15-DEPENDENT_INHALATION có approval blank; RULE_DESIGN/ISSUE15_SYNC gọi policy nhóm nhưng gate chưa đầy đủ | TEST_CASES đủ sáu approval/source và meaningful reason metadata; RULE_DESIGN/ISSUE15_SYNC/TEST_PLAN theo Q/A4 | Sáu input/level/ID giữ nguyên; policy tag đúng; MISS-009 R01/R02 U không bị đổi T; không current D13 awaiting |
| F02 P2 | HANDOFF §còn chờ yêu cầu Huy sync Q/A; sources README Q/A2 current | Current source Q4 a574ce20fbf307ad90f0d60064da394652462aea, A4 7af011f3f95e21ac829a163ee4be36200c1e7d88; sửa handoff/readmes/plans | Link pin đúng; snapshot historical hashes không đổi; không claim Hải/Việt Đức đã review |
| F03 P2 | Hai BOOL1 chỉ generic reason, không bắt S=False/confirmed-R01 | Expected.explanation_assertions cả ba canonical + Mixed/Direct cases, test semantics/forbidden examples | Controlled safe messages được chấp nhận, unsafe clinical fact/provenance bị reject; actual template runtime còn NOT EXECUTED |
| F04 P2 | Thiếu quantified selection/crossover, max64 và biên17.99 | 18 D13E cases + M2 property plan; tăng assertions ca cũ thay duplicate fixtures | Đủ ID/mục tiêu TEST_PLAN §7; independently derived expected match; 157 inputs/outputs cũ không regress |

Repair được ghi nhận ở mức thiết kế/data; Leader còn kiểm diff/evidence trước chấp nhận. Q/A4 chỉ approve policy D13-E, không chứng minh các file sửa đã được peer accept.

## 2. Tái đánh giá R01–R11

| ID | Vấn đề trước | Repair/evidence hiện tại | Trạng thái thực / còn lại |
|---|---|---|---|
| R01 | Sai/thiếu lớp lỗi, nullable cũ invalid | 36 invalid giữ 28 TypeError/8 ValueError; 3 fixture_ref an toàn; tám nullable INV và AUD-002 chuỗi đúng | Static oracle kiểm, runtime validation/audit NOT EXECUTED |
| R02 | Rule design/policy conflation | Formulas/ngưỡng giữ nguyên; D13-E definite-first/coverage/current approval đầy đủ | Repair applied; cần Leader review, helper implementation sau |
| R03 | Plan/source/status cũ | T15 và Q/A4 tách rõ, 175 DRAFT_NOT_EXECUTED, sáu approved oracles không pending | Repair applied; không biến TA requirement thành canonical convention |
| R04 | R02 bị R03/SOC che | Giữ R02/count assertions RULE-013/PAIR và CASE metadata; Def-vs-Poss thêm cho MISS-013/014/BOOL3 | Mathematical static checks; pure helper/public runtime tests riêng M2 |
| R05 | Audit/context integration thiếu | INT-001–021 chuẩn bị direct/UUID/reset/failures/privacy và D13 success/fallback | Plan adequate để review; không tính là actual integration PASS |
| R06 | Thiếu internal states/count | 81 rows giữ nguyên, recompute từng operator/count/allergen; TIER1_MATCH tách HATT evidence | Static math evidence, chưa gọi helper/Enum runtime |
| R07 | Source provenance | Q/A hiện hành Revision04, aliases Q2/A2/Q0 historical; không overwrite snapshots | F02 repaired; review references theo pinned commits |
| R08 | CON-004 assertion định dạng/nonmutation | Giữ before=deepcopy(patient), call, patient==before | Định dạng đã sửa ở baseline; nonmutation vẫn đề nghị riêng, không tự approve |
| R09 | Benchmark protocol thiếu | BENCH-001–006/phép đo chính giữ nguyên 100 warmup/N>=1000/nearest-rank/full audit I/O | Protocol design; benchmark NOT EXECUTED, QA evidence sau |
| R10 | NaN/Inf fixture unsafe/nonJSON | Registry +allowlist +deepcopy, ValueError; không eval/runner ngoài | Static construction/refs verified; actual loader not implemented |
| R11 | Handoff/evidence/traceability | Leader ownership rõ, report/evidence/main-index175, all relative links checked | Leader acceptance và Việt Đức QA/peer mapping còn chờ, không self-close |

Không tạo yêu cầu Hải/Việt Đức lập PR. Huy quản lý PR/merge riêng, task chỉ commit/push nhánh remediation sau static validation.
