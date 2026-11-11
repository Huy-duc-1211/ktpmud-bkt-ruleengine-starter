# TEAM PLAN — PHÂN CÔNG, BÀN GIAO & REVIEW

> **Nhóm 173820_n27 | Track A — Dr May Day**  
> Trạng thái sau tích hợp M1. Phân công và tiêu chí review ghi theo vai trò, kết quả ghi theo bằng chứng.
> Đọc [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) trước tài liệu này.

Đối chiếu D01–D03 theo [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248). Chính sách D13-E do Leader phê duyệt ngày 09/11/2026. Dùng [Requirements](../REQUIREMENTS.md) và [ADR](../DECISIONS.md) hiện hành khi triển khai hoặc review.

## 1. Mục tiêu của cách phân công

Chia việc theo trách nhiệm và lịch làm việc của từng người. Ghi công cho người thực tế làm và kiểm chứng.

Mỗi task phải có **Owner** (người làm và chịu trách nhiệm), **Reviewer** (người kiểm chứng độc lập), **Đầu ra**, **Hạn bàn giao**, **Tiêu chí hoàn thành**. Leader chỉ đánh dấu hoàn thành khi đã xem bằng chứng thực tế.

**Không được nhầm:**
- Phê duyệt D04–D10 = thống nhất **cách thiết kế**; **không có nghĩa** code hoặc tài liệu đã hoàn thành.
- Phân công = quyết định **ai làm và ai kiểm tra**; **không được** coi lời hứa làm là bằng chứng đã làm.
- Codex báo *Done* = AI đã thực hiện yêu cầu của nó; **không phải** nhóm đã nghiệm thu.

## 2. Phân vai tổng thể

| Người | Vai trò chính | Chịu trách nhiệm xuyên suốt | Người review |
|---|---|---|---|
| **Huy Đức — SV1 (Leader)** | Requirements, quyết định thiết kế, tích hợp | Contract, phạm vi, quyết định Requirements/ADR, sở hữu bản sửa TASK 02E, theo dõi mốc, review cuối và tích hợp | Hải và Việt Đức review chéo; Huy tổng hợp quyết định cuối |
| **Hải — SV2 (Technical Owner)** | Logic phân loại & test kỹ thuật | Tác giả đóng góp M1-02 gốc. M2 dự kiến triển khai R01/R02/R03/R-SOC, validation và test biên/ca âm | Huy đối chiếu với Decision Table; Việt Đức kiểm tra AC/test coverage |
| **Việt Đức — SV3 (QA/Quality Owner)** | QA, audit, security, CI, benchmark | Đối chiếu QA Matrix A-01–A-11, kiểm chứng privacy, audit M2 có review, bằng chứng CI/benchmark | Huy review; Hải hỗ trợ phần code/test kỹ thuật |

**Phân công là trách nhiệm chính, không phải tách biệt kiến thức.** Cả ba phải hiểu luồng input → validation → rules → output/audit để trả lời vấn đáp ngẫu nhiên.

Không đưa họ tên đầy đủ, thông tin cá nhân hoặc thông tin đăng nhập vào repo công khai.

## 3. M1 (05–08/11) và trạng thái review hiện hành

[PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) đã tích hợp ngày 10/11/2026. GitHub ghi Leader self-review và approval từ `nvldvc`. Chưa có bằng chứng review kỹ thuật cuối của cả hai thành viên hoặc TA nghiệm thu phạm vi.
### M1-01 — Huy Đức: Requirements & Scope

**Đầu ra hiện hành:** [Requirements Revision 04](../REQUIREMENTS.md), đã tích hợp qua [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1).

- Mô tả mục tiêu bài, giới hạn trong/ngoài phạm vi.
- Viết input/output contract chín trường/ba trường đúng bảng quyết định.
- Diễn giải R01–R03/R-SOC, thứ tự tầng, yêu cầu zero PII.
- Đối chiếu 11 acceptance criteria, phân biệt yêu cầu từ đề và quyết định của nhóm.
- Ghi D01–D03 **TA CONFIRMED**. D04–D10 giữ các quyết định Leader duyệt ở phần tương thích với phản hồi TA. D11–D12 giữ theo đề. D13-E đã được Leader phê duyệt ngày 09/11/2026.
- Dùng [phản hồi tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) để đối chiếu các ca thiếu dữ liệu và chồng lấp rule.

**Reviewer:** Hải kiểm tra logic rule; Việt Đức kiểm tra AC và điều kiện an toàn.  
**Đạt khi:** không sai contract, có nguồn, không thiếu AC, khớp Test Plan và có review.

### M1-02 — Rule Design & Test Cases

**Đầu ra hiện hành:** [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3) đã tích hợp [gói M1-02](m1-hai/README.md), gồm 175 ca thiết kế chính và 81 ca logic nội bộ. Hải là tác giả bản gốc. Huy Đức phụ trách bản sửa TASK 02E với Codex hỗ trợ. F01–F04 được xử lý ở mức thiết kế và dữ liệu test. Xem [bàn giao](m1-hai/M1/HANDOFF.md) và [kiểm tra tĩnh](m1-hai/M1/REMEDIATION_EVIDENCE.json).

**Phạm vi bộ ca thiết kế**

- Diễn giải chính xác từng điều kiện `AND/OR`, R01–R03 và R-SOC.
- Test các nhóm `SOC_PHAN_VE`, `PHAN_VE`, `THEO_DOI`.
- Test R02 với 0, 1, 2, 3, 4 hệ biểu hiện.
- Test R03 ở cả nhánh hô hấp và tuần hoàn, kể cả khi dị nguyên qua đường hít.
- Test overlap R02/R03; test ưu tiên R-SOC.
- Test tuổi `0`, `0.5`, `1`, `1.5`, `10.99`, `11`, `18`, huyết áp bằng ngưỡng, giảm đúng và trên 30%.
- Test dữ liệu thiếu, `null`, sai kiểu và trường dư. Expected của D01–D03 theo làm rõ của TA. Các ca D13-E bao phủ definite/possible, AllPV, Mixed và giải thích DIRECT/CANONICAL.
- Đề xuất hàm hỗ trợ **ít và rõ trách nhiệm** theo D05, giúp viết ADR.

**Phạm vi bàn giao M1-02:** thiết kế và dữ liệu ca, trước triển khai `classify()` ở M2.

**Reviewer:** Huy kiểm tra expected độc lập theo Decision Table; Việt Đức kiểm tra ánh xạ AC.  
**Đạt khi:** test có input, expected, căn cứ; giải thích được ít nhất một ca của từng rule và một ca biên.

### M1-03 — Việt Đức: AC Traceability, QA & Audit/Security Review

**Bàn giao hiện hành:** [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) đã tích hợp [QA Matrix](m1-qa/QA_MATRIX.xlsx) với ánh xạ A-01–A-11 và bằng chứng dự kiến. Việt Đức là tác giả QA gốc. Huy Đức tiếp quản việc sửa và kiểm chứng thiết kế với công cụ AI hỗ trợ. Các mục thực thi vẫn `NOT RUN`.

- Dùng bộ ca M1-02 trong PR #3 để ánh xạ đủ **11 AC** và ghi rõ AC nào còn thiếu test hoặc bằng chứng.
- Không tự tuyên bố đã đạt A-08/A-09/A-10 trước khi chạy test/CI/benchmark thật.
- Đối chiếu yêu cầu audit **đúng bốn trường**: `Timestamp`, `User_UUID`, `Action_Type`, `Status`.
- Phân tích cách kiểm tra audit không chứa huyết áp, triệu chứng hay raw input.
- Đối chiếu quyết định D07–D08: audit writer riêng, JSON Lines, UUID synthetic theo phiên, có status khi input invalid.
- Kiểm tra `.github/workflows/test.yml` có chạy trên PR; lập checklist kiểm chứng CI thực tế giai đoạn sau.
- Chuẩn bị khung bằng chứng `AI_USE.md`, security/privacy và benchmark theo đề.

**Không tự viết lại clinical rule hoặc thiết kế database thật.**  
**Reviewer:** Huy kiểm tra tổng thể; Hải hỗ trợ test/code kỹ thuật.  
**Đạt khi:** 11/11 AC được liên kết tới test/bằng chứng dự kiến hoặc được đánh dấu GAP; checklist có thể dùng để nghiệm thu thực tế.

### M1-04 — Cả nhóm: ADR đầu tiên và review chéo

**Đầu ra hiện hành:** [ADR Revision 04](../DECISIONS.md), đã tích hợp qua [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2). Xem bằng chứng review ở đầu mục 3.

| Người | Trách nhiệm |
|---|---|
| Huy | Tổng hợp D04–D10, làm rõ TA cho D01–D03 và D13-E đã duyệt, kèm lý do và đánh đổi |
| Hải | Kiểm tra kiến trúc hàm, logic rules, cách tách validation và classification |
| Việt Đức | Kiểm tra audit, UUID, bảo mật, test, CI và benchmark |
| Cả ba | Đọc chéo Requirements–ADR–Test Plan, không để một tài liệu mâu thuẫn tài liệu khác |

**Đạt khi:** cả ba đã đọc và phản hồi phần mình; Huy phê duyệt bản tổng hợp. TA duyệt **scope** ở Checkpoint 1, không thay nhóm phê duyệt toàn bộ kỹ thuật.

## 4. Lịch sử M1 — các mốc nội bộ đề xuất trước Checkpoint 1

| Mốc | Bàn giao cần có | Xử lý khi gặp khó khăn |
|---|---|---|
| **05/11** | Cả ba đọc `PROJECT_GUIDE.md` và `TEAM_PLAN.md`; Hải/Việt Đức nhắn xác nhận task | Hỏi trong Zalo nếu chưa hiểu |
| **06/11 — bản nháp đầu tiên** | Hải: rule design + ma trận test; Việt Đức: AC traceability + checklist; Huy: requirements khung | Gửi phần đã có + phần chưa làm + blocker, không im lặng |
| **07/11 — review/sửa** | Mỗi người sửa theo comment, gửi lại link bản nháp/PR | Huy cân nhắc thu hẹp hoặc chuyển giao task nếu có rủi ro |
| **08/11 — Checkpoint 1** | Requirements, AC, Test Plan, ADR đầu tiên nhất quán, đủ để trình TA | Không tuyên bố TA đã duyệt nếu chưa được phản hồi |

Bảng lưu lại các mốc quản lý nội bộ đã đề xuất trước Checkpoint 1. Hạn chính thức của Checkpoint 1 là cuối 08/11/2026.

## 5. Phân công M2–M4 — DỰ KIẾN

| Mốc chính thức | Huy Đức | Hải | Việt Đức |
|---|---|---|---|
| **M2 · 09–15/11 · Build** | Review contract, PR và bằng chứng, tích hợp | Triển khai `classify()`, validation và chuyển ca rule/biên thành pytest | Triển khai audit, test audit, kiểm tra clean checkout cùng Hải và thu bằng chứng CI |
| **Checkpoint 2 · 15/11** | Điều phối demo nội bộ | Chuẩn bị phần classifier và test | Chuẩn bị phần audit và bằng chứng chạy |
| **M3 · 16–19/11 · Harden** | Đối chiếu A-01–A-11, review README, AI-use và contributions | Sửa lỗi core, mở rộng test âm/biên, hoàn thiện hướng dẫn kỹ thuật | Chạy benchmark, rà security/privacy và tổng hợp bằng chứng test/CI |
| **PC-2 · trước 11:30 ngày 18/11/2026.** Yêu cầu có một Draft PR nộp bài vào `fossbk-spec/ktpmud-project` với check `validate` xanh. [Erratum #28](https://github.com/fossbk-spec/ktpmud-project/issues/28) | Điều phối chuẩn bị Draft PR và theo dõi `validate` | Cung cấp SHA commit PC-2 trên fork code | Rà schema và kết quả `validate` |
| **Freeze · 23:59 ngày 19/11** | Chốt SHA và tag theo đề | Kiểm nguồn phát hành | Kiểm bằng chứng trên SHA chốt |
| **M4 · 20/11 · Submit** | Cập nhật `source-ref.json` và artifacts trên cùng nhánh, chuyển chính Draft PR từ PC-2 sang **Ready for review** và kiểm tra `validate` xanh | Đối chiếu source release, hỗ trợ blocker | Rà schema, hồ sơ QA và đóng góp |
| **Demo/Viva · 21/11** | Chuẩn bị demo và giải thích kiến trúc | Giải thích code, rule và test | Giải thích audit, CI, privacy và benchmark |

### Bàn giao M2 từ thiết kế M1

**Nguồn bàn giao:** [175 ca chính](m1-hai/M1/TEST_CASES.csv), [81 ca logic nội bộ](m1-hai/M2/INTERNAL_STATE_CASES.csv), [Test Plan](m1-hai/M1/TEST_PLAN.md), [Integration Test Plan có INT-021](m1-hai/M2/INTEGRATION_TEST_PLAN.md) và [QA Matrix](m1-qa/QA_MATRIX.xlsx). Đây là đầu vào thiết kế. Kết quả runtime, CI nghiệp vụ và benchmark cần được thu riêng.

- **Hải** dự kiến triển khai validation và selector D13-E, chạy ca rule, biên và trạng thái nội bộ. Kiểm tra riêng definite thắng possible, AllPV, Mixed, ưu tiên sốc và các trường hợp thiếu tuổi/HATT. Review logic giải thích trong INT-021 cùng Việt Đức.
- **Việt Đức** đối chiếu QA Matrix A-01–A-11 với ID ca, test thực thi, nguồn bằng chứng và khoảng trống. Với INT-021/CHK-058, áp dụng `explanation_assertions` lên `ly_do` thực tế của DIRECT/CANONICAL/MIXED. Kiểm tra cả mẫu phải khớp và mẫu sai phải bị loại, rồi đọc lại ý nghĩa và privacy cùng Hải. Ghi kết quả chạy và nguồn bằng chứng tách khỏi mapping thiết kế. Kiểm tra gọi trực tiếp `classify(patient)`, validation, JSONL bốn trường, UUID/context theo phiên và việc dọn context, cô lập file test, đường lỗi audit/fail-closed và privacy ở output, audit, message và exception chaining.
- **Huy Đức** đối chiếu Requirements–ADR–Test Plan, review bằng chứng và quyết định tích hợp. Đường dẫn audit mặc định và cách xử lý lỗi nội bộ ngoài dự kiến vẫn theo trạng thái review riêng trong ADR.

Nếu kỹ năng thực tế khác với dự kiến, leader có thể điều chỉnh. Không gán công việc chưa thực hiện cho thành viên trong `CONTRIBUTIONS.md`.

## 6. Cách dùng AI riêng nhưng không làm lệch thiết kế

Cả nhóm dùng đề thi, [Decision Table V1](decision-table.md), phản hồi Issue #15, [Requirements](../REQUIREMENTS.md), [ADR](../DECISIONS.md) và bộ ca M1-02 ở mục 3.

**Quy trình:**

1. Huy giao task có mã rõ (`M1-01`, `M1-02`, `M1-03`) và tiêu chí nghiệm thu.
2. Người làm đọc nguồn chung, giao **chính task được nhận** cho Codex riêng; không yêu cầu AI viết toàn bộ dự án.
3. Tự kiểm tra kết quả và ghi điều chưa chắc. Khi thay đổi file GitHub, dùng nhánh riêng từ `track-a-development`, ví dụ `docs/m1-tests-hai` hoặc `docs/m1-qa-viet-duc`. **Không push thẳng vào nhánh tích hợp**.
4. Gửi link PR/branch/tài liệu và báo cáo bàn giao theo mẫu ở mục 7.
5. Reviewer kiểm tra theo spec, để comment cụ thể; Owner sửa.
6. Huy mới quyết định merge. Không để Codex tự merge, tự phát hành release hay tự nộp PR cuối.

**Zalo để giao tiếp/nhắc hạn/báo blocker**. **GitHub để lưu nội dung có phiên bản, bằng chứng và lịch sử đóng góp**. Không gửi nhiều bản sửa trực tiếp qua Zalo rồi không rõ đâu là bản mới nhất.

## 7. Mẫu báo cáo bàn giao cho mọi task

```text
[TASK ID] M1-02
[OWNER] Hải
[LINK] <link file / branch / PR>
[ĐÃ LÀM] ...
[ĐÃ TỰ KIỂM TRA] Đối chiếu nguồn nào, kiểm tra ca nào...
[CHƯA RÕ / PENDING] ...
[TRẠNG THÁI] In progress / Ready for review / Blocked
[AI-USE] Codex hỗ trợ phần nào, người nào xác minh...
```

**Task chỉ được gọi “DONE” khi reviewer đã xác nhận.** Không ghi test pass, CI green, benchmark đạt nếu không có bằng chứng thực đo. Không ghi raw clinical data, PII hay secret vào báo cáo hoặc AI-use log.

## 8. Xử lý người làm chậm hoặc sản phẩm chưa đạt

- Báo khi phát sinh blocker hoặc có nguy cơ trễ mốc đang phụ trách.
- Nếu chất lượng chưa đạt, reviewer nêu lỗi cụ thể và Owner sửa; không lấy bản đầu do Codex tạo làm kết quả cuối.
- Nếu task có nguy cơ làm trễ Checkpoint, Huy có quyền chuyển giao **một phần công việc có phạm vi rõ**, cập nhật lại Owner/Reviewer.
- Ai thực tế viết, kiểm chứng, review thì ghi đúng vào bằng chứng đóng góp. Không gán công giả.
- Mỗi phần bàn giao phải đủ rõ để người khác tiếp nhận mà **không cần truy cập cuộc hội thoại Codex riêng**.

## 9. Chuẩn bị vấn đáp theo trách nhiệm

| Người | Phải giải thích được |
|---|---|
| Huy | Vì sao chọn D04–D10 và D13-E, ưu nhược điểm, tích hợp, trách nhiệm AI/human |
| Hải | `classify()`, R01/R02/R03/R-SOC, validation, test ranh giới |
| Việt Đức | Audit bốn trường, UUID synthetic, bảo mật, CI, p50/p95, bằng chứng nghiệm thu |
| **Cả nhóm** | Luồng tổng thể, vì sao test pass chưa đủ chứng minh đúng, D01–D03, cách kiểm chứng Codex |

**Không dùng AI khi vấn đáp trực tiếp.** Phải tự hiểu quyết định nhóm đã chốt, không học thuộc câu trả lời sai với code thực tế.
