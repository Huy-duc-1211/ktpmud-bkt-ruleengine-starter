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

*Bản chuẩn bị ngày 17/11, đối chiếu repo code tại commit `925cea676f4962f9318e7dc35aad6017d4f80bd3`; cần kiểm tra lại trước khi xác nhận PC-2.*

### 2.1. Đối chiếu timeline PC-1

| Việc theo PC-1 | Kế hoạch | Thực tế tại mốc chuẩn bị | Lệch & lý do |
|---|---|---|---|
| Classifier, validation và audit | M2, 12–15/11 | Đã tích hợp qua [PR #7](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/7). | Merge ngày 17/11; nghiệm thu cuối còn tiếp tục. |
| Pytest và CI | Dự kiến trước 15/11 | CI sau merge đạt 490 test, 3 test Windows bỏ qua: [run](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44111237320). | CI đã được bật và chạy ngày 17/11; chưa xác minh demo nội bộ ngày 15/11. |
| Audit/privacy và benchmark | M3, 16–19/11 | Đã kiểm tra audit ở phạm vi test; có [benchmark sơ bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/docs/testing/BENCHMARK_REPORT.md). | Cần hoàn thiện báo cáo và kiểm tra trên SHA freeze. |
| Hồ sơ, Draft PR nộp bài | Trước 11:30 18/11 | Đã mở [Draft PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39); check validate xanh tại commit `3869272`. | Tiếp tục cập nhật hồ sơ và kiểm tra validate trước khi xác nhận. |

### 2.2. Tiến độ theo acceptance criteria

| Mã | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|
| A-01 | Đang | [Classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/rule_engine/classifier.py), [CI](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44111237320) | Đã có triển khai và test; còn review contract và SHA cuối. |
| A-02 | Đang | [Classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/rule_engine/classifier.py) | Đã đọc source; cần bổ sung kiểm tra synthetic độc lập. |
| A-03 | Đang | [Test classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/tests/test_classifier.py), [CI](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44111237320) | Có ca cho ba mức; cần hoàn tất mapping và review. |
| A-04 | Đang | [Test classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/tests/test_classifier.py), [Requirements](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/REQUIREMENTS.md) | Có policy và test missing/null/invalid; còn đối chiếu SHA cuối. |
| A-05 | Đang | [Test ly_do](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/tests/test_classifier.py) | Đã review ca thiết kế và giữ cách giải thích; còn đối chiếu nghiệm thu. |
| A-06 | Đang | [Test audit](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/tests/test_audit.py), [CI](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44111237320) | Có test schema, lỗi và privacy; không suy rộng sang mọi môi trường. |
| A-07 | Đang | [Test classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/tests/test_classifier.py), [test audit](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/tests/test_audit.py) | Có test nghiệp vụ; còn hoàn thiện mapping QA. |
| A-08 | Đang | [CI sau merge](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44111237320) | CI đạt 490 test, 3 test Windows bỏ qua; clean checkout độc lập trước đó tại 0d00584 đạt 483. Cần chạy lại SHA cuối. |
| A-09 | Xong | [CI PR #7](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44106490534) | Workflow PR chạy test thành công; cần xác minh lại SHA freeze. |
| A-10 | Đang | [Benchmark sơ bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/docs/testing/BENCHMARK_REPORT.md) | Có số đo sơ bộ; cần lưu mẫu và đối chiếu SHA freeze. |
| A-11 | Xong | [README](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/README.md) | Có disclaimer bắt buộc; kiểm lại SHA freeze. |

### 2.3. Sẵn sàng nộp bài

| Deliverable | Có / Chưa | Đường dẫn / ghi chú |
|---|---|---|
| README.md | Có | [README](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/README.md) |
| REQUIREMENTS.md | Có | [Requirements](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/REQUIREMENTS.md) |
| DECISIONS.md / ADR | Có | [Decisions](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/925cea676f4962f9318e7dc35aad6017d4f80bd3/DECISIONS.md) |
| Test tự động + CI xanh | Có | [CI PR #7](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44106490534); 3 test Windows bỏ qua trên Linux. |
| TEST_REPORT.md | Có bản nháp | [TEST_REPORT.md](https://github.com/Huy-duc-1211/ktpmud-project/blob/38692726cd971b568f04cf10a4ee82ceac9c9079/submissions/may_day_sprint_173820_n27/artifacts/TEST_REPORT.md); cần hoàn thiện trước Freeze. |
| SECURITY_PRIVACY_CHECKLIST.md | Có bản nháp | [SECURITY_PRIVACY_CHECKLIST.md](https://github.com/Huy-duc-1211/ktpmud-project/blob/38692726cd971b568f04cf10a4ee82ceac9c9079/submissions/may_day_sprint_173820_n27/artifacts/SECURITY_PRIVACY_CHECKLIST.md); cần hoàn thiện trước Freeze. |
| AI_USE.md | Có bản nháp | [AI_USE.md](https://github.com/Huy-duc-1211/ktpmud-project/blob/38692726cd971b568f04cf10a4ee82ceac9c9079/submissions/may_day_sprint_173820_n27/artifacts/AI_USE.md); cần hoàn thiện trước Freeze. |
| CONTRIBUTIONS.md | Có bản nháp | [CONTRIBUTIONS.md](https://github.com/Huy-duc-1211/ktpmud-project/blob/38692726cd971b568f04cf10a4ee82ceac9c9079/submissions/may_day_sprint_173820_n27/artifacts/CONTRIBUTIONS.md); cần hoàn thiện trước Freeze. |
| Slide / demo script ≤ 7 phút | Có bản nháp | [Kịch bản demo](https://github.com/Huy-duc-1211/ktpmud-project/blob/38692726cd971b568f04cf10a4ee82ceac9c9079/submissions/may_day_sprint_173820_n27/slides/DEMO_SCRIPT.md); cần nhóm chạy thử. |
| Draft PR nộp bài + validate xanh | Có | [Draft PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39); validate xanh tại commit `3869272`. |

### 2.4. Việc còn lại đến Freeze

| Việc | Vai trò phụ trách | Hạn dự kiến |
|---|---|---|
| Cập nhật hồ sơ và kiểm lại validate trên Draft PR | Lead | Trước 11:30 18/11 |
| Hoàn thiện QA/AC, CI và bằng chứng báo cáo | Lead, Dev hỗ trợ | 19/11 |
| Benchmark lại/đối chiếu trên SHA freeze; lưu mẫu và môi trường | Lead, Dev review | 19/11 |
| Hoàn thiện test report, privacy, AI use, contributions | Lead, các thành viên đối chiếu | 19/11 |
| Chốt SHA, tag, chuẩn bị demo | Lead và nhóm | 23:59 19/11 |

### 2.5. Rủi ro

- Ba test riêng cho Windows chưa chạy trong CI Linux; cần xác minh trên Windows.
- Benchmark và hồ sơ nộp chưa nghiệm thu trên SHA freeze; kiểm tra lại validate sau mỗi lần cập nhật PR.

---

## Kết quả cuối — Freeze 19/11/2026

- **Tag đã tạo:** [`bkt-2026-173820_n27-rc1`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/tree/bkt-2026-173820_n27-rc1), trỏ tới đúng SHA bên dưới.
- **SHA code/hồ sơ đã freeze:** [`7af8d47fd410b96dcdb4b7caccd48580ce07cf4a`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/commit/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a) — commit merge PR #10 trên `track-a-development`. Tag giữ snapshot này; commit cập nhật phần báo cáo Freeze sau khi tạo tag không làm đổi SHA đã gắn tag.
- **CI trên đúng SHA:** [run 44525947180](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44525947180) `success`; bộ pytest có **490 passed, 3 skipped** trên Linux. Ba test Windows chỉ được skip, chưa có bằng chứng chạy trên Windows.
- **Hồ sơ nộp:** [Draft PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39) đã cập nhật `source-ref.json` đến SHA và CI này; [`validate` tại commit `8a71a8d`](https://github.com/fossbk-spec/ktpmud-project/actions/runs/44527053887) xanh. Trạng thái Ready for review và nghiệm thu GV/TA là các bước riêng.

### Trạng thái cuối từng acceptance criterion

Đây là **tự đánh giá của nhóm trên snapshot đã gắn tag**, không phải kết luận nghiệm thu của GV/TA. `Xong` được dùng khi có triển khai và bằng chứng tương ứng; giới hạn của môi trường thử được ghi bên dưới.

| AC | Trạng thái | Bằng chứng tại SHA freeze và phạm vi |
|---|---|---|
| A-01 | Xong | [Classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/rule_engine/classifier.py) có `classify(patient)` trả contract ba khóa; [CI](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44525947180) chạy test nghiệp vụ. |
| A-02 | Xong | [Đối chiếu QA](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/docs/qa/EXECUTION_REVIEW.md) có input synthetic ngoài CSV và đảo thứ tự khóa, cùng kết quả giữ nguyên theo input. |
| A-03 | Xong | [Test classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/tests/test_classifier.py) kiểm `THEO_DOI`, `PHAN_VE`, `SOC_PHAN_VE` và thứ tự rule. |
| A-04 | Xong | [Requirements](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/REQUIREMENTS.md), [test classifier](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/tests/test_classifier.py) kiểm missing/null, sai kiểu, sai miền và khóa lạ theo chính sách nhóm. |
| A-05 | Xong | [Test lời giải thích](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/tests/test_classifier.py) gồm kiểm ý nghĩa `ly_do` và đối chứng sai; [đối chiếu QA](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/docs/qa/EXECUTION_REVIEW.md). |
| A-06 | Xong | [Audit writer](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/rule_engine/audit.py) và [61 test audit](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/tests/test_audit.py) kiểm schema bốn trường, lỗi và privacy trên dữ liệu synthetic. |
| A-07 | Xong | [175 ca input/expected](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/TEST_CASES.csv), [81 ca helper](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/tests/fixtures/INTERNAL_STATE_CASES.csv) được pytest dùng; 175 snapshot output QA chỉ là bằng chứng truy vết, không tự thành 175 test độc lập. |
| A-08 | Xong | [CI đúng SHA](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44525947180) checkout và chạy pytest: 490 passed, 3 skipped trên Linux. |
| A-09 | Xong | [Workflow](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/.github/workflows/test.yml) và [run sau merge](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44525947180) `success`. |
| A-10 | Xong trong môi trường đo | [Benchmark report](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/docs/testing/BENCHMARK_REPORT.md) có hai lượt 100 warm-up + 1.000 mẫu, p95 lần lượt **0.301703 ms** và **0.349306 ms**; cả hai dưới 100 ms trên `/tmp` tmpfs. Kết quả không đại diện I/O ổ vật lý và không có `fsync`. |
| A-11 | Xong | [README tại SHA freeze](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/README.md) có nguyên văn `educational/synthetic — not for clinical use`. |

### Việc chưa hoàn thành hoặc chưa có bằng chứng

- Demo nội bộ dự kiến 15/11 trong PC-1: chưa xác minh có diễn ra đúng ngày; không hồi tố thành đã hoàn thành.
- Ba test launcher riêng cho Windows chưa chạy trong CI Linux. Kịch bản demo đã có trên PR nộp, nhưng chưa có biên bản nhóm chạy thử.
- [QA Matrix tại tag](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af8d47fd410b96dcdb4b7caccd48580ce07cf4a/docs/qa/QA_MATRIX.xlsx) là snapshot rà trước tag: 11 AC PASS trên ứng viên, 63/64 QA case và 55/60 checklist PASS. `QA-033` và `CHK-029/045` đang ghi BLOCKED vì lúc điền workbook chưa có permalink SHA cuối; hiện đã có tag nhưng chưa sửa hồi tố snapshot. `CHK-039/042/060` chờ bằng chứng review kỹ thuật cá nhân và đối chiếu mapping. Không biến nội dung AI-use hoặc Leader tự review thành xác nhận của từng thành viên.
- [Draft PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39) cần chuyển **Ready for review ngày 20/11** và kiểm `validate` vẫn xanh sau cập nhật cuối. Việc GV/TA nghiệm thu phạm vi/kết quả chưa được ghi nhận.

Bảng PC-1 và PC-2 phía trên giữ nguyên trạng thái tại thời điểm báo cáo; phần Freeze này là cập nhật sau khi tag được tạo.
