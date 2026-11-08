# M1-02 — Thiết kế logic và test case của Hải

Hải xác nhận đã review và chỉnh sửa bộ tài liệu trước khi bàn giao lên nhánh `docs/m1-tests-hai`. Huy Đức review logic/expected/ADR, Việt Đức review AC/QA. Chưa ghi nhận nghiệm thu của hai reviewer này.

## Nội dung

- [Thiết kế luồng phân loại](RULE_DESIGN.md).
- [Kế hoạch và chỉ mục test](TEST_PLAN.md).
- [Ma trận 135 ca test](TEST_CASES.csv): 128 ca chưa chạy, 7 ca pending TA.
- [Nhận xét requirements](REVIEW_NOTES.md).
- [Báo cáo bàn giao và AI-use](HANDOFF.md).
- [Kiểm tra tính nhất quán của bản bàn giao](VALIDATION_REPORT.md).
- [Hướng dẫn đọc bộ bàn giao](README_BAN_GIAO.md).

Đây là tài liệu M1, chưa triển khai `classify()` hoặc pytest nghiệp vụ. Kiểm tra cấu trúc tài liệu không chứng minh đạt các AC runtime/CI/benchmark.

## Ký hiệu và mốc nguồn dùng để review

Các snapshot được giữ nguyên trong `sources/` để truy vết bản đã đọc. Chúng không thay thế tài liệu hiện hành của nhánh tích hợp hoặc các cập nhật mới hơn của Huy.

| Ký hiệu | Nguồn |
|---|---|
| D | [Decision Table V1](sources/docs/decision-table.md), trùng blob chính thức `95c2bbd43be8e80c8c7ecb938761a273d062c17e` tại tag `bkt-2026-v1` |
| Q | [Requirements đã dùng đối chiếu](sources/REQUIREMENTS.md), commit `673aaef3c320475196366103289c7c174e2d3b54` của nhánh `docs/m1-requirements-huy` |
| P | [Team Plan đã đọc](sources/docs/TEAM_PLAN.md), cùng mốc nguồn Q |
| G | [Project Guide đã đọc](sources/docs/PROJECT_GUIDE.md), cùng mốc nguồn Q |
| I | [Bình luận Issue #15 đã đọc](sources/ISSUE_15_COMMENTS.md), snapshot ngày 08/11/2026 |
| C | Interface `rule_engine/classifier.py` tại mốc tích hợp `b65032f94ec3ce600df07d81b5df6b9b4bd203d1` |
| E | [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html), nội dung đã đọc hiển thị v1.0.2 |

Expected của D01–D03 tiếp tục được ghi pending trong bản bàn giao này. Khi có quyết định mới, nhóm cần đối chiếu và cập nhật riêng, không tự suy đoán kết quả.

educational/synthetic — not for clinical use
