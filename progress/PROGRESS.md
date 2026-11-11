# PROGRESS — 173820_n27 — Track A

- **Starter:** `ktpmud-bkt-ruleengine-starter` · tag `bkt-2026-v1`
- **Fork:** https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter
- **Nhánh phát triển:** `track-a-development`
- **Track:** A — Dr May Day: Rule Engine Sprint
- **Phạm vi:** Rule Engine độc lập, dùng dữ liệu synthetic.
- **Mốc đối chiếu:** [`d0fc12f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/commit/d0fc12fe4846a38db5f92e83228222e68f7804c7) trên `track-a-development`. [Mẫu Progress Check](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_Progress_Check.html)

## PC-1 — 11/11/2026

### 1.1. Tiến độ theo acceptance criteria

| Mã | Trạng thái (Chưa / Đang / Xong) | Bằng chứng (commit / CI / file) | Ghi chú |
|---|---|---|---|
| A-01 | Chưa | [Classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/rule_engine/classifier.py#L30) | `classify()` còn raise `NotImplementedError`. Chưa có MVP phân loại theo contract. |
| A-02 | Chưa | [Classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/rule_engine/classifier.py#L30), [Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M1/TEST_PLAN.md) | Đã có kế hoạch kiểm tra bằng fixture độc lập. Cần classifier chạy được để xác minh kết quả dựa trên input. |
| A-03 | Đang | [Rule Design](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M1/RULE_DESIGN.md), [ca thiết kế](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M1/TEST_CASES.csv) | Đã thiết kế ca cho ba mức phân loại. Chưa có kết quả chạy nghiệp vụ. |
| A-04 | Đang | [Chính sách input](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/REQUIREMENTS.md#L42), [Làm rõ chung tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) | Đã công bố xử lý dữ liệu thiếu, sai kiểu và ngoài miền, gồm D13-E đã duyệt nội bộ. Chưa xác minh thực thi. |
| A-05 | Đang | [Output contract](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/REQUIREMENTS.md#L184), [kế hoạch INT-021](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md) | Đã thiết kế `ly_do` truy vết quy tắc, kiểm disclosure mã đại diện và tránh dữ liệu thô, lời khuyên điều trị. Chưa kiểm output thực tế. |
| A-06 | Đang | [Thiết kế audit](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/DECISIONS.md#L113), [QA Matrix](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-qa/QA_MATRIX.xlsx) | Đã thiết kế audit bốn trường và kiểm privacy. Chưa có bằng chứng audit writer chạy. |
| A-07 | Đang | [Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M1/TEST_PLAN.md), [81 ca logic nội bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M2/INTERNAL_STATE_CASES.csv), [test stub](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/tests/test_classifier.py#L9) | Có 175 ca thiết kế chính và 81 ca helper riêng. Cần chuyển thành pytest nghiệp vụ cho ca thường, biên, sai và thiếu dữ liệu. |
| A-08 | Đang | [pytest.ini tại commit `4482e4f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/pytest.ini), [test stub](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/tests/test_classifier.py#L9), [Erratum #16](https://github.com/fossbk-spec/ktpmud-project/issues/16) | Đã áp dụng cấu hình import. Diagnostic local trước đó có `1 passed` cho ca `NotImplementedError`. Chưa có bằng chứng pytest nghiệp vụ đạt từ clean checkout. |
| A-09 | Đang | [Workflow pytest](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/.github/workflows/test.yml) | Workflow có trigger PR. Chưa xác minh lượt chạy trên PR nội bộ với bộ test nghiệp vụ. |
| A-10 | Chưa | [Benchmark Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M2/BENCHMARK_PLAN.md) | Đã có protocol. Chưa có ≥1.000 lượt đo sau warm-up, số liệu p50/p95 và đối chiếu p95 < 100 ms. |
| A-11 | Xong | [README dòng 43 tại commit `4482e4f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/README.md#L43) | Đã đối chiếu nguyên văn `educational/synthetic — not for clinical use`. Bằng chứng áp dụng cho disclaimer của A-11. |

Hồ sơ thiết kế M1 đã được tích hợp qua [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4). Các ca trong [QA Matrix](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-qa/QA_MATRIX.xlsx) đang ở mức thiết kế, với trạng thái thực thi `NOT RUN`. A-11 đã có bằng chứng trực tiếp. Runtime, CI nghiệp vụ và benchmark còn chờ bằng chứng.

Hồ sơ Checkpoint 1 trên fork gồm [Requirements](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/REQUIREMENTS.md), [Acceptance criteria A-01–A-11](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/REQUIREMENTS.md#L231), [Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M1/TEST_PLAN.md) và [ADR](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/DECISIONS.md). Nhóm ghi nhận tài liệu đã có trên fork. Xác nhận nghiệm thu phạm vi của GV/TA cần được ghi riêng. [Erratum #25](https://github.com/fossbk-spec/ktpmud-project/issues/25)

### 1.2. Sửa đổi bắt buộc từ Checkpoint 1

| Mục | Trạng thái | Bằng chứng |
|---|---|---|
| Yêu cầu sửa riêng dạng ❗ của GV/TA | Chưa xác minh phản hồi riêng | Đã rà [Issue #17](https://github.com/fossbk-spec/ktpmud-project/issues/17), [Issue #25](https://github.com/fossbk-spec/ktpmud-project/issues/25) và các PR công khai tìm được. Nếu GV/TA gửi nhận xét riêng, Lead sẽ bổ sung đúng mục và bằng chứng xử lý. |
| D01–D03, hướng dẫn chung Track A | Đã đồng bộ trong thiết kế | [Làm rõ chung tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248), [Requirements](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/REQUIREMENTS.md), [ADR](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/DECISIONS.md) |
| D13-E, chính sách nhóm cho boolean thiếu/null | Đã duyệt nội bộ ở mức thiết kế | [Requirements §4.2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/REQUIREMENTS.md#L104), [ADR](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/DECISIONS.md), [Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M1/TEST_PLAN.md) |
| Cấu hình import pytest theo erratum chung Track A | Đã áp dụng | [Erratum #16](https://github.com/fossbk-spec/ktpmud-project/issues/16), [pytest.ini tại commit `4482e4f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/pytest.ini) |

Issue #15 làm rõ hành vi chung cho Track A. Phản hồi riêng về phạm vi Checkpoint 1 và các mục ❗ sẽ được ghi khi xác minh được.

### 1.3. Timeline dự kiến đến khi hoàn thành

Cấu hình import pytest đã có trên fork. Phân công dưới đây là dự kiến cho M2–M4. [pytest.ini tại commit `4482e4f`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/4482e4f61ee6e949705abbbda06b22480bbba8d6/pytest.ini)

| Việc | Vai trò phụ trách | Mốc | Ngày dự kiến |
|---|---|---|---|
| Triển khai `classify()`, validation, ưu tiên rule và D13-E | Dev, Lead review | M2 | 12–15/11 |
| Triển khai audit writer, UUID synthetic và xử lý lỗi | QA, Dev review | M2 | 13–15/11 |
| Chuyển ca thiết kế thành pytest, gồm ca thường, biên, sai và thiếu dữ liệu | Dev, QA review | M2 | 13–15/11 |
| Chạy pytest nghiệp vụ từ clean checkout và thu link CI trên PR nội bộ | Dev và QA, Lead rà bằng chứng | Checkpoint 2 · demo nội bộ | 15/11 |
| Chạy integration tests, kiểm audit/privacy và đo benchmark | QA và Dev | M3 | 16–19/11 |
| Hoàn thiện hồ sơ test, bảo mật, AI-use và đóng góp | Lead và QA | M3 | 16–19/11 |
| Mở Draft PR vào `fossbk-spec/ktpmud-project`, chỉ thêm `submissions/may_day_sprint_173820_n27/` và có check `validate` xanh. [Erratum #28](https://github.com/fossbk-spec/ktpmud-project/issues/28) | Lead, QA kiểm validate | PC-2 | Trước 11:30 ngày 18/11/2026 |
| Chốt commit, bằng chứng CI và tag dự kiến | Lead | Freeze | 23:59 ngày 19/11 |
| Cập nhật `source-ref.json` và artifacts trên cùng nhánh, chuyển chính Draft PR từ PC-2 sang **Ready for review** và kiểm `validate` xanh | Lead và QA | M4 | 20/11 |
| Chuẩn bị demo và vấn đáp cá nhân | Lead, Dev, QA | Demo/Viva | 21/11 |

### 1.4. Rủi ro / đang vướng

- **R1 — MVP:** Classifier còn stub. Ưu tiên luồng phân loại và validation trước demo nội bộ.
- **R2 — Test và CI:** Các ca nghiệp vụ còn ở mức thiết kế. Cần thu kết quả pytest từ clean checkout và link CI trên PR nội bộ.
- **R3 — Chính sách dữ liệu thiếu:** Cần kiểm D01–D03, definite-first, AllPV, Mixed và ưu tiên R-SOC trên runtime, cùng nội dung `ly_do`.
- **R4 — Quyết định mở:** INT-010 và INT-013 cần xử lý khi triển khai các đường audit liên quan. CON-004 vẫn là đề xuất kiểm tra input có bị sửa. [Integration Test Plan](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/d0fc12fe4846a38db5f92e83228222e68f7804c7/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md)
- **R5 — Review và tiến độ:** Chưa xác minh đủ vòng review kỹ thuật cuối của các vai trò. Cần xác nhận người nhận việc M2–M4 và theo dõi mốc Draft PR ngày 18/11.

### 1.5. Câu hỏi cho GV

- **Q1:** Khi thiếu một thông tin đầu vào, mọi khả năng còn lại đều cho kết luận phản vệ, nhưng không có một rule riêng nào chắc chắn đúng trong tất cả khả năng. Nhóm dự kiến giữ kết luận phản vệ và chọn một rule_id đại diện, đồng thời ghi rõ trong lý do rằng rule đó chưa được xác nhận riêng. Cách giải thích như vậy có phù hợp với yêu cầu của bài không ạ?
- **Q2:** Hồ sơ trên fork đã đủ để GV/TA xem xét phạm vi Checkpoint 1 chưa ạ? Nếu cần sửa, nhóm xin các mục ❗ cụ thể.

### 1.6. Phân công

| Alias / vai trò | Đầu việc chính | Commit/PR tiêu biểu |
|---|---|---|
| Lead | Đã phụ trách Requirements, ADR, bản sửa và tích hợp M1. Dự kiến điều phối và rà hồ sơ nộp. | [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2) và bản sửa tích hợp trong [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) |
| Dev | Đã đóng góp thiết kế rule và ca M1-02 ban đầu. Dự kiến triển khai classifier, validation và test kỹ thuật. | Bản nền M1-02 và lịch sử tích hợp tại [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) |
| QA | Đã đóng góp QA Matrix và checklist M1-03 ban đầu. Dự kiến phụ trách audit, privacy, CI và benchmark. | Bản nền QA và lịch sử tích hợp tại [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) |

Lead phụ trách các bản sửa M1-02 và M1-03 với công cụ AI hỗ trợ. Phân công tiếp theo được xác nhận theo tiến độ thực tế.

---

## PC-2 — 18/11/2026

*Chưa đến lượt cập nhật PC-2. Điền các mục dưới đây tại buổi PC-2 ngày 18/11/2026.*

### 2.1. Đối chiếu timeline PC-1

| Việc (theo bảng 1.3) | Kế hoạch | Thực tế | Lệch & lý do |
|---|---|---|---|
| Sẽ cập nhật 18/11 | — | — | — |

### 2.2. Tiến độ theo acceptance criteria (cập nhật toàn bộ bảng 1.1)

*Sẽ đánh giá lại đầy đủ A-01 đến A-11 tại PC-2, kèm bằng chứng thực thi.*

| Mã | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|
| A-01 đến A-11 | Chưa cập nhật PC-2 | — | — |

### 2.3. Sẵn sàng nộp bài (đề thi Mục 6)

| Deliverable | Có / Chưa | Đường dẫn |
|---|---|---|
| README.md (cài đặt / chạy / test) | — | — |
| REQUIREMENTS.md | — | — |
| DECISIONS.md / ADR | — | — |
| Test tự động + CI xanh | — | — |
| TEST_REPORT.md | — | — |
| SECURITY_PRIVACY_CHECKLIST.md | — | — |
| AI_USE.md | — | — |
| CONTRIBUTIONS.md | — | — |
| Slide / demo script ≤ 7 phút | — | — |
| Draft PR vào `ktpmud-project`, check `validate` xanh | — | — |

### 2.4. Việc còn lại đến Freeze (23:59 19/11)

| Việc | Vai trò phụ trách | Hạn |
|---|---|---|
| Sẽ cập nhật tại PC-2 | — | — |

### 2.5. Rủi ro / câu hỏi cho GV

- Sẽ cập nhật tại PC-2.

---

## Kết quả cuối — Freeze 19/11/2026

*Chưa đến lượt cập nhật Freeze.*

- **Tag dự kiến:** `bkt-2026-173820_n27-rc1`
- **SHA cuối:** Chưa chốt.
- **Trạng thái cuối từng mã AC:** Chưa đánh giá tại Freeze.
- **Những việc trong timeline chưa hoàn thành và lý do:** Sẽ cập nhật khi Freeze.
