# Tài liệu dự án

Gói M1-02 đã tích hợp qua [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3). Hải là tác giả baseline `768f196e6a9ec3b1142c44399ce8288f7cc2e87e` trên `docs/m1-tests-hai`. Huy Đức phụ trách bản sửa TASK 02E với AI hỗ trợ. Xem [nguồn và lịch sử](references/README.md).

- [Rule Design](design/RULE_DESIGN.md), [Test Plan](testing/TEST_PLAN.md) và [Test Cases](../TEST_CASES.csv): 175 ca thiết kế chính. TASK 02E giữ ID, input và kết quả chính (mức phân loại và mã quy tắc, hoặc lớp lỗi dự kiến) của 157 ca baseline, đồng thời cập nhật nhãn phê duyệt và điều kiện kiểm tra `ly_do` ở một số ca. Bộ ca có thêm 18 ca tập trung vào D13-E.
- [Kiểm thử](testing/README.md): 81 ca logic nội bộ, kiểm thử tích hợp, fixture và benchmark.
- [QA Matrix](qa/QA_MATRIX.xlsx) và [ghi chú review](qa/README.md).

D13-E được Leader phê duyệt ngày 09/11/2026. Mã CANONICAL là quy ước của nhóm. Xem [thiết kế](design/README.md) và [ADR hiện hành](../DECISIONS.md).
