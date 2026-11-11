# M1-02 — Bản sửa Leader-owned sau approval D13-E

Nguồn hiện hành: [Requirements](../../../REQUIREMENTS.md) (Q), [ADR](../../../DECISIONS.md) (A), [Decision Table](../../decision-table.md) (D) và [phản hồi Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (T15). D13-E là **APPROVED BY LEAD — D13-E — 09/11/2026**. CANONICAL là quy ước của nhóm. Hải đóng góp bản gốc, Huy Đức phụ trách TASK 02E với AI hỗ trợ. Gói đã tích hợp qua [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3).

1. [ISSUE15_SYNC](ISSUE15_SYNC.md): TA và sáu approved policy oracles.
2. [RULE_DESIGN](RULE_DESIGN.md): formulas/ngưỡng giữ nguyên, D13-E selection/provenance.
3. [TEST_PLAN](TEST_PLAN.md) và [TEST_CASES.csv](TEST_CASES.csv): 175 ca thiết kế chính, gồm 157 ca baseline được bảo toàn ID, input và kết quả chính (mức phân loại và mã quy tắc, hoặc lớp lỗi dự kiến) cùng 18 ca hồi quy bổ sung. TASK 02E cập nhật nhãn phê duyệt và điều kiện kiểm tra `ly_do` ở một số ca baseline. Các ca này chưa được thực thi bằng pytest nghiệp vụ.
4. [REVIEW_NOTES](REVIEW_NOTES.md), [REVIEW_RESPONSE](REVIEW_RESPONSE.md): F01–F04 và R01–R11, không tự xác nhận final acceptance.
5. [HANDOFF](HANDOFF.md), [VALIDATION_REPORT](VALIDATION_REPORT.md), [sources](sources/README.md).

Xem [kế hoạch M2/M3](../M2/README.md) cho 81 ca logic nội bộ, integration, fixture và benchmark. Trạng thái thiết kế và bằng chứng thực thi được theo dõi riêng trong [QA Matrix](../../m1-qa/QA_MATRIX_M1_CODEX_FINAL_CANDIDATE.xlsx).
