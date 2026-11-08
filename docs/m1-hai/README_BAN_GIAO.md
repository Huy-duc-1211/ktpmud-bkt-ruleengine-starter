# Bàn giao review M1-02 — Hải

Đọc theo thứ tự:
1. RULE_DESIGN.md: thiết kế luồng và đóng góp ADR.
2. TEST_PLAN.md: chiến lược, phạm vi và ánh xạ AC.
3. TEST_CASES.csv: 135 ca đã thiết kế, 7 ca pending TA; chưa chạy trên engine.
4. REVIEW_NOTES.md: nhận xét requirements và điểm cần quyết định.
5. HANDOFF.md: phạm vi bàn giao và ghi nhận AI-use của Hải.

sources/: bản nguồn để đối chiếu, không sửa các bản nguồn. Ký hiệu và phiên bản nguồn được ghi trong README.md.
VALIDATION_REPORT.md: kiểm tính nhất quán tài liệu, không phải test engine đạt.

Huy review logic/expected/ADR. Việt Đức review AC/QA/audit. Không khẳng định người nào đã review khi chưa có phản hồi.
Gói này không chứa phần triển khai classify(), web hoặc kết quả chạy classifier stub. Script chạy CSV được cung cấp riêng trong CSV_Test_Runner.zip.

educational/synthetic — not for clinical use
