# M1-02 — Thiết kế rule và kiểm thử

Hải là tác giả baseline M1-02; Huy Đức phụ trách bản sửa TASK 02E và các cập nhật với AI hỗ trợ. Gói M1-02 đã tích hợp qua [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3); merge tài liệu không chứng minh đã chạy test hoặc nghiệm thu.

## Bắt đầu đọc

1. [RULE_DESIGN.md](RULE_DESIGN.md): rule, ngưỡng, xử lý dữ liệu thiếu và cách chọn kết quả theo chính sách hiện hành.
2. [TEST_PLAN.md](TEST_PLAN.md): kế hoạch kiểm thử, các nhóm ca, expected và điều kiện kiểm `ly_do`.
3. [TEST_CASES.csv](TEST_CASES.csv): 175 ca thiết kế chính; trạng thái DRAFT_NOT_EXECUTED, chưa phải 175 test đã chạy. Gồm 157 ID/input baseline và 18 ca D13E bổ sung. TASK 02E giữ kết quả chính của baseline; sau Issue #31, bốn ca overlap đổi mã dự kiến nhưng giữ input và mức PHAN_VE.
4. [ISSUE15_SYNC.md](ISSUE15_SYNC.md): đối chiếu Issue #15 trong TASK 02E. Đây là ghi nhận lịch sử; chọn mã hiện hành xem hai file ở bước 1–2 và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002).
5. [HANDOFF.md](HANDOFF.md), [README_BAN_GIAO.md](README_BAN_GIAO.md), [REVIEW_NOTES.md](REVIEW_NOTES.md), [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md), [VALIDATION_REPORT.md](VALIDATION_REPORT.md) và [REMEDIATION_EVIDENCE.json](REMEDIATION_EVIDENCE.json): bàn giao, phát hiện, phản hồi và bằng chứng tĩnh TASK 02E/02Q; không thay thế bằng chứng thực thi theo chính sách mới.
6. [sources/README.md](sources/README.md): nguồn hiện hành và chỉ mục snapshots. Các bản trong sources dùng để truy vết lịch sử, không ghi đè nguồn hiện hành.

## Nguồn và việc cần kiểm chứng

Nguồn hiện hành: [Requirements](../../../REQUIREMENTS.md), [ADR](../../../DECISIONS.md), [Decision Table](../../decision-table.md), [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002).

Phản hồi Issue #31 xác nhận trực tiếp ví dụ MISS-009 và nêu quy tắc chung chọn mã; việc áp dụng cho ca R03 definite/R02 possible là quyết định nhóm. [Kế hoạch M2](../M2/README.md) và [QA Matrix](../../m1-qa/QA_MATRIX.xlsx) đã được cập nhật ở mức thiết kế để cùng mô tả chính sách này; Hải và Việt Đức cần review kỹ thuật. Không coi bản sửa thiết kế là test nghiệp vụ, CI, benchmark, peer review hay nghiệm thu đã đạt.
