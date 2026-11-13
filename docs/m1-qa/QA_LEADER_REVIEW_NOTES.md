# TASK 02N-C — Quyết định cho Huy Đức

> **Bối cảnh lịch sử:** Ghi chú được lập trước PR #4 và trước cập nhật cách chọn mã sau Issue #31. Xem [QA Matrix hiện hành](QA_MATRIX.xlsx) và [Test Cases](../m1-hai/M1/TEST_CASES.csv); trạng thái review của các thành viên và runtime vẫn cần bằng chứng riêng.

**Kết luận kỹ thuật: bản ứng viên sẵn sàng để Huy xem xét nghiệm thu thiết kế và quyết định mở Draft PR #4.** Các sai lệch đã xác minh trong lượt audit được sửa trên bản sao. Chưa có quyết định nghiệm thu, peer review độc lập của thành viên hay xác minh runtime.

- **P0/P1 còn lại trong phạm vi audit:** chưa phát hiện. Sáu P1 của 02J đã được xử lý trong bản patched và hoàn thiện tại các điểm thiếu mapping/expected.
- **P2/P3 trong workbook:** đã xử lý các điểm tái lập được về nguồn, cache, filter, mapping, thủ tục và diễn đạt. AC_MATRIX còn một số notes dài cần mở ô để đọc đủ như bản vào. Không coi đó là lỗi thiết kế.
- **Trước PR #4:** Huy kiểm 40 ô sửa, bốn bộ lọc và 22 cache. Hải kiểm kỹ thuật các đường canonical, mixed, definite-first, RULE-020, fault-stage và INT-021. Ghi nhận vai trò Việt Đức là QA gốc, Huy là chủ bản sửa ChatGPT/Codex hỗ trợ. Huy quyết định design acceptance sau khi xem bằng chứng review và chọn thời điểm mở Draft PR.
- **Quyết định còn mở:** default audit path (INT-010), unexpected internal exception (INT-013), và nonmutation CON-004. Giữ test với path override hợp lệ và không nâng đề xuất thành policy. D13-E đã được Huy duyệt, giữ nguyên. [ADR Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md), [Integration Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md).
- **M2/M3:** test runtime classifier/helper và public audit, pytest clean checkout, CI nghiệp vụ, README root tại SHA nghiệm thu, rồi benchmark thật full path ở M3. Chỉ cập nhật status khi có evidence thực. [Requirements Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md), [Benchmark Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/BENCHMARK_PLAN.md).

Giữ nguyên PR #1/#2/#3. Chưa mở PR #4. Toàn bộ đầu ra nằm trong thư mục local. Đọc [audit độc lập](QA_REVIEW_REPORT.md), [đối chiếu ChatGPT](QA_REVIEW_COMPARISON.md) và [Excel validation cùng nhật ký sửa](QA_WORKBOOK_VALIDATION.md).
