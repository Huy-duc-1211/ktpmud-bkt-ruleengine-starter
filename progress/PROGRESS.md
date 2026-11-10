# PROGRESS — 173820_n27 — Track A

- **Starter:** `ktpmud-bkt-ruleengine-starter` · tag `bkt-2026-v1`
- **Fork:** https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter
- **Nhánh phát triển:** `track-a-development`
- **Track:** A — Dr May Day: Rule Engine Sprint
- **Phạm vi:** Rule Engine độc lập, dữ liệu synthetic, không tích hợp hệ thống production.

## PC-1 — 11/11/2026

### 1.1. Tiến độ theo acceptance criteria

| Mã | Trạng thái | Bằng chứng (commit / CI / file) | Ghi chú |
|---|---|---|---|
| A-01 | Chưa | `rule_engine/classifier.py` | `classify()` vẫn là stub `NotImplementedError`. Chưa có MVP chạy được. |
| A-02 | Chưa | `docs/m1-hai/M1/TEST_PLAN.md` | Đã thiết kế cách kiểm tra logic tổng quát, nhưng chưa triển khai classifier để xác minh không hard-code fixture. |
| A-03 | Đang | `docs/m1-hai/M1/RULE_DESIGN.md`, `TEST_CASES.csv` | Đã thiết kế các ca cho ba mức phân loại, chưa thực thi. |
| A-04 | Đang | `REQUIREMENTS.md`, `DECISIONS.md`, Issue #15 | Đã công bố chính sách xử lý input, missing/null và D13-E; chưa triển khai và kiểm thử runtime. |
| A-05 | Đang | `REQUIREMENTS.md`, `docs/m1-hai/M1/RULE_DESIGN.md` | Đã thiết kế `ly_do`, DIRECT/CANONICAL và giới hạn thông tin; chưa kiểm tra output thực tế. |
| A-06 | Đang | `DECISIONS.md`, `docs/m1-qa/` | Đã thiết kế audit bốn trường, privacy và test plan; chưa có bằng chứng audit writer chạy thực tế. |
| A-07 | Đang | `docs/m1-hai/M1/TEST_CASES.csv`, `docs/m1-hai/M2/INTERNAL_STATE_CASES.csv` | Có 175 ca thiết kế chính và 81 ca logic nội bộ. `tests/test_classifier.py` hiện vẫn là test stub; chưa chuyển thành bộ pytest nghiệp vụ. |
| A-08 | Chưa | `tests/test_classifier.py`, Issue #16 | Chưa xác minh `pytest -q` từ clean checkout; cần bổ sung `pytest.ini` và thay test stub. |
| A-09 | Đang | `.github/workflows/test.yml` | Có workflow trên push/PR nhưng chưa có bằng chứng CI chạy thành công với bộ test nghiệp vụ thực tế. |
| A-10 | Chưa | `docs/m1-hai/M2/BENCHMARK_PLAN.md` | Mới có phương pháp benchmark; chưa chạy ≥1.000 lần và chưa đo p50/p95. |
| A-11 | Chưa | `README.md` | README hiện còn mô tả starter; cần cập nhật hướng dẫn chạy và cảnh báo `educational/synthetic — not for clinical use`. |

**Tổng kết PC-1:** Đã tích hợp hồ sơ thiết kế M1, gồm Requirements, ADR, Rule Design, Test Plan và QA Matrix. Chưa có bằng chứng thực thi MVP, kiểm thử nghiệp vụ hoặc benchmark. Không đánh dấu các acceptance criteria là hoàn thành chỉ dựa trên tài liệu thiết kế.

**Bằng chứng tích hợp M1:**

- PR #1 — Requirements, Project Guide, Team Plan: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1
- PR #2 — Architecture Decisions: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2
- PR #3 — Rule Design & Test Plans: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3
- PR #4 — QA Matrix & Audit Documentation: https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4
- Commit tích hợp M1: `9bc4fc186415d7a13cd9d49692c50f3c945ddf7b`

### 1.2. Sửa đổi bắt buộc từ Checkpoint 1

| Mục | Trạng thái | Bằng chứng |
|---|---|---|
| Phản hồi riêng dạng ❗ từ GV/TA tại Checkpoint 1 | Chưa xác minh có phản hồi riêng | Sẽ cập nhật nếu GV/TA đưa ra yêu cầu sửa |
| D01–D03: Ưu tiên rule, thiếu tuổi, thiếu huyết áp | Đã đồng bộ ở mức thiết kế | Issue #15; `REQUIREMENTS.md`; `DECISIONS.md` |
| D13-E: Chính sách nội bộ cho boolean thiếu/null | Đã được Leader chấp thuận ở mức thiết kế | `REQUIREMENTS.md`; `DECISIONS.md`; bộ test cases |
| Sửa lỗi import pytest theo erratum | Chưa thực hiện | Issue #16 — cần bổ sung `pytest.ini` |

Issue #15 đã được áp dụng vào tài liệu thiết kế, không được coi là bằng chứng GV/TA đã nghiệm thu toàn bộ giải pháp.

### 1.3. Timeline dự kiến đến khi hoàn thành

| Việc | Vai trò phụ trách | Mốc | Ngày dự kiến |
|---|---|---|---|
| Bổ sung `pytest.ini`, hoàn thiện cấu trúc phát triển | Lead / Dev | M2 | 11/11 |
| Triển khai `classify()`, validation, rule precedence và D13-E | Dev; Lead review | M2 / CP2 | 12–15/11 |
| Triển khai audit writer, UUID synthetic và error handling | QA / Dev | M2 / CP2 | 13–15/11 |
| Chuyển test cases thành pytest; kiểm tra normal, boundary, invalid, missing | Dev / QA | M2 / CP2 | 13–15/11 |
| Chạy CI trên PR nội bộ, sửa lỗi và kiểm tra clean checkout | Dev / QA; Lead nghiệm thu | CP2 | 15/11 |
| Thực hiện integration tests, audit/privacy checks và benchmark | QA / Dev | M3 | 16–18/11 |
| Hoàn thiện README, TEST_REPORT, AI_USE và CONTRIBUTIONS | Lead / QA | M3 | 16–19/11 |
| Mở Draft PR nộp bài, kiểm tra `validate` xanh | Lead | PC-2 | Trước 11:30 ngày 18/11 |
| Chốt source, CI evidence và release tag | Lead | Freeze | Trước 23:59 ngày 19/11 |
| Cập nhật PR nộp bài và chuyển sang Ready for review | Lead | M4 | 20/11 |
| Chuẩn bị demo và vấn đáp cá nhân | Cả nhóm | Demo/Viva | 21/11 |

Phân công M2 là kế hoạch dự kiến; Leader có thể điều chỉnh theo tiến độ và phản hồi thực tế của thành viên.

### 1.4. Rủi ro / đang vướng

- **R1 — MVP chưa triển khai:** Code hiện còn starter stub, có nguy cơ ảnh hưởng tiến độ M2 nếu không ưu tiên thực hiện ngay.
- **R2 — Test và CI chưa được chứng minh:** Bộ test cases mới ở mức thiết kế, chưa có bằng chứng pytest nghiệp vụ đạt.
- **R3 — Tính nhất quán của chính sách:** Cần kiểm tra D01–D03 và D13-E trong runtime, đặc biệt missing/null, definite/possible, AllPV, Mixed và ưu tiên R-SOC.
- **R4 — Quyết định kỹ thuật còn mở:** INT-010, INT-013 và CON-004 cần được giải quyết trong triển khai M2.
- **R5 — Review và phối hợp:** Chưa có review của Dev (Hải) ở vòng nghiệm thu cuối M1; Leader đã quyết định tích hợp và ghi nhận ngoại lệ. Cần xác nhận lại tiến độ triển khai M2.
- **R6 — Thời gian:** Giai đoạn M2–M4 ngắn, cần ưu tiên MVP và bằng chứng kiểm thử hơn các tính năng ngoài phạm vi.

### 1.5. Câu hỏi cho GV

- **Q1:** Với các vấn đề thiết kế nội bộ chưa được quy định chi tiết, nhóm tiếp tục công bố lựa chọn trong ADR và kiểm thử nhất quán theo Issue #15. Nhóm sẽ hỏi bổ sung nếu phát sinh điểm có nguy cơ mâu thuẫn với Decision Table.
- **Q2:** Nhóm xin xác nhận các yêu cầu sửa bắt buộc cụ thể sau khi GV/TA kiểm tra scope Checkpoint 1, nếu có.

### 1.6. Phân công

| Alias / vai trò | Đầu việc chính | Commit/PR tiêu biểu |
|---|---|---|
| Lead | Requirements, ADR, tổng hợp phản hồi TA, rà soát và tích hợp M1; phụ trách nghiệm thu, tiến độ và hồ sơ nộp | PR #1, #2; remediation và tích hợp PR #3, #4 |
| Dev | Bản thiết kế rule và test cases M1-02 ban đầu; dự kiến triển khai classifier và test M2 | PR #3 (tài liệu nền tảng và bản sửa tích hợp) |
| QA | QA Matrix và checklist M1-03 ban đầu; dự kiến kiểm tra audit, privacy, CI và benchmark | PR #4 (tài liệu nền tảng và bản sửa tích hợp) |

Các bản sửa M1 do Lead tích hợp có sử dụng AI hỗ trợ. Lịch sử contribution và review sẽ được đối chiếu trước khi hoàn thiện `CONTRIBUTIONS.md`; không coi phê duyệt PR là bằng chứng đã chạy kiểm thử thực tế.

---

## PC-2 — 18/11/2026

*Phần này sẽ được cập nhật trong buổi PC-2 ngày 18/11. Giữ chung trong file PROGRESS.md hiện tại.*

### 2.1. Đối chiếu timeline PC-1

| Việc (theo bảng 1.3) | Kế hoạch | Thực tế | Lệch & lý do |
|---|---|---|---|
| Sẽ cập nhật 18/11 | — | — | — |

### 2.2. Tiến độ theo acceptance criteria

*Sẽ đánh giá lại đầy đủ A-01 đến A-11 tại PC-2, kèm bằng chứng thực thi.*

| Mã | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|
| A-01 đến A-11 | Chưa cập nhật PC-2 | — | — |

### 2.3. Sẵn sàng nộp bài

| Deliverable | Có / Chưa | Đường dẫn |
|---|---|---|
| README.md (cài đặt / chạy / test) | Chưa hoàn thiện | — |
| REQUIREMENTS.md | Có bản thiết kế | `REQUIREMENTS.md` |
| DECISIONS.md / ADR | Có bản thiết kế | `DECISIONS.md` |
| Test tự động + CI xanh | Chưa xác minh | — |
| TEST_REPORT.md | Chưa | — |
| SECURITY_PRIVACY_CHECKLIST.md | Chưa hoàn thiện | — |
| AI_USE.md | Chưa hoàn thiện | — |
| CONTRIBUTIONS.md | Chưa hoàn thiện | — |
| Slide / demo script ≤ 7 phút | Chưa | — |
| Draft PR vào `ktpmud-project`, check `validate` xanh | Chưa | Hạn PC-2: 18/11 |

### 2.4. Việc còn lại đến Freeze (23:59 19/11)

*Sẽ cập nhật tại PC-2 theo tình trạng thực tế.*

### 2.5. Rủi ro / câu hỏi cho GV

*Sẽ cập nhật tại PC-2.*

---

## Kết quả cuối — Freeze 19/11/2026

- **Tag dự kiến:** `bkt-2026-173820_n27-rc1`
- **SHA cuối:** Chưa chốt.
- **Trạng thái cuối từng mã AC:** Chưa đánh giá tại Freeze.
- **Những việc trong timeline chưa hoàn thành và lý do:** Sẽ cập nhật khi Freeze.
