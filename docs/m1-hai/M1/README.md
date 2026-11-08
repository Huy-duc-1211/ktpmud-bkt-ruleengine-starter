# M1-02 — Bản sửa Leader-owned sau approval D13-E

Nguồn hiện hành: [Requirements Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md) (Q), [ADR Revision 04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md) (A), Decision Table (D) và [TA comment 6722429248](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15). D13-E là **APPROVED BY LEAD — D13-E — 09/11/2026**, không phải canonical rule do TA định danh. Bản sửa TASK 02E do Leader Huy Đức sở hữu, AI hỗ trợ; chưa xác nhận Hải/Việt Đức peer review hoặc Leader nghiệm thu bản sửa.

1. [ISSUE15_SYNC](ISSUE15_SYNC.md): TA và sáu approved policy oracles.
2. [RULE_DESIGN](RULE_DESIGN.md): formulas/ngưỡng giữ nguyên, D13-E selection/provenance.
3. [TEST_PLAN](TEST_PLAN.md) và [TEST_CASES.csv](TEST_CASES.csv): 175 ca, giữ 157 input/ID gốc, thêm 18 focused regressions.
4. [REVIEW_NOTES](REVIEW_NOTES.md), [REVIEW_RESPONSE](REVIEW_RESPONSE.md): F01–F04 và R01–R11, không tự xác nhận final acceptance.
5. [HANDOFF](HANDOFF.md), [VALIDATION_REPORT](VALIDATION_REPORT.md), [sources](sources/README.md).

M1 review cần đọc kế hoạch [M2](../M2/README.md) cho 81 internal rows, integration/fixture/benchmark; đó là design dependency, không đòi code/runtime ở M1. Mọi classifier test, CI và benchmark NOT EXECUTED. D13 policy đã approved; bản sửa, QA/peer review và nghiệm thu vẫn do người kiểm soát.
