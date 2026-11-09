# TEAM PLAN — PHÂN CÔNG, BÀN GIAO & REVIEW

> **Nhóm 173820_n27 | Track A — Dr May Day**  
> Đồng bộ M1 Revision 04 trong TASK 02H. Phân công dưới đây ghi vai trò và kế hoạch review của nhóm. Kết quả từng phần được ghi theo bằng chứng bàn giao.
> Đọc [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) trước tài liệu này.

D01–D03 đã được giảng viên làm rõ. Ưu tiên R-SOC khi đủ điều kiện, sau đó chọn rule Tầng 2 đã thỏa theo R01 > R02 > R03. Thiếu tuổi → `THEO_DOI / null`. Có tuổi và đủ bằng chứng Tầng 2 thì giữ `PHAN_VE` khi thiếu HATT cần thiết để xác nhận sốc. Xem mục 5 của [Project Guide](PROJECT_GUIDE.md) và [phản hồi tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248).

Huy Đức phê duyệt **D13-E ngày 09/11/2026**. Boolean thiếu khóa hoặc `null` → UNKNOWN. Dữ liệu sai kiểu hoặc sai miền vẫn theo D04. Khi đã kiểm tra input và có tuổi, rule definite được xét trước rule chỉ possible. AllPV giữ mức phản vệ. Nếu Def rỗng và kết quả là `PHAN_VE`, chọn mã ưu tiên nhất trong Poss làm CANONICAL. `ly_do` phải giải thích đây là mã đại diện, nêu dữ liệu còn thiếu và ghi rõ rule riêng chưa được xác nhận. Mixed → `THEO_DOI / null` kèm lý do chưa đủ thông tin. R-SOC vẫn cần bằng chứng Tầng 2 và tụt HATT theo tuổi. D13-E là chính sách của nhóm trong phạm vi TA cho phép. [Requirements Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md), [ADR Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md).

## 1. Mục tiêu của cách phân công

Nhóm có ba người, sử dụng công cụ độc lập , khả năng lập trình và lịch làm việc khác nhau. Vì vậy, không chia việc chỉ theo số lượng file hoặc để AI làm hết rồi mới ghi tên người phụ trách.

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

### M1-01 — Huy Đức: Requirements & Scope

**Đầu ra hiện hành** gồm [`REQUIREMENTS.md`](../REQUIREMENTS.md) Revision 04 trong [Draft PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1). Bản theo SHA đã dùng để đối chiếu là [Requirements Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/a574ce20fbf307ad90f0d60064da394652462aea/REQUIREMENTS.md).

- Mô tả mục tiêu bài, giới hạn trong/ngoài phạm vi.
- Viết input/output contract chín trường/ba trường đúng bảng quyết định.
- Diễn giải R01–R03/R-SOC, thứ tự tầng, yêu cầu zero PII.
- Đối chiếu 11 acceptance criteria, phân biệt yêu cầu từ đề và quyết định của nhóm.
- Ghi D01–D03 **TA CONFIRMED**. D04–D10 giữ các quyết định Leader duyệt ở phần tương thích với phản hồi TA. D11–D12 giữ theo đề. D13-E đã được Leader phê duyệt ngày 09/11/2026.
- Dùng [phản hồi tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) để đối chiếu các ca thiếu dữ liệu và chồng lấp rule.

**Reviewer:** Hải kiểm tra logic rule; Việt Đức kiểm tra AC và điều kiện an toàn.  
**Đạt khi:** không sai contract, có nguồn, không thiếu AC, khớp Test Plan và có review.

### M1-02 — Rule Design & Test Cases

**Đầu ra hiện hành** nằm trong [Draft PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3). Hải là tác giả bản M1-02 gốc. Huy Đức sở hữu bản sửa TASK 02E, có Codex hỗ trợ. F01–F04 đã được xử lý ở mức thiết kế và dữ liệu test. PR có **175 ca thiết kế chính** và **81 ca toán logic nội bộ**. Xem [bàn giao theo SHA](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/HANDOFF.md) và [bằng chứng kiểm tra tĩnh](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/REMEDIATION_EVIDENCE.json).

**Phạm vi bộ ca thiết kế**

- Diễn giải chính xác từng điều kiện `AND/OR`, R01–R03 và R-SOC.
- Test các nhóm `SOC_PHAN_VE`, `PHAN_VE`, `THEO_DOI`.
- Test R02 với 0, 1, 2, 3, 4 hệ biểu hiện.
- Test R03 ở cả nhánh hô hấp và tuần hoàn, kể cả khi dị nguyên qua đường hít.
- Test overlap R02/R03; test ưu tiên R-SOC.
- Test tuổi `0`, `0.5`, `1`, `1.5`, `10.99`, `11`, `18`, huyết áp bằng ngưỡng, giảm đúng và trên 30%.
- Test dữ liệu thiếu, `null`, sai kiểu và trường dư. Expected của D01–D03 theo làm rõ của TA. Các ca D13-E bao phủ definite/possible, AllPV, Mixed và giải thích DIRECT/CANONICAL.
- Đề xuất hàm hỗ trợ **ít và rõ trách nhiệm** theo D05, giúp viết ADR.

**Không triển khai code `classify()` trong M1 nếu Huy chưa giao task viết code.**  
**Reviewer:** Huy kiểm tra expected độc lập theo Decision Table; Việt Đức kiểm tra ánh xạ AC.  
**Đạt khi:** test có input, expected, căn cứ; giải thích được ít nhất một ca của từng rule và một ca biên.

### M1-03 — Việt Đức: AC Traceability, QA & Audit/Security Review

**Đầu ra dự kiến** gồm QA Matrix A-01–A-11 → cách kiểm chứng/test ID/bằng chứng, QA checklist và phần audit, privacy, CI, benchmark, AI-use. QA Matrix và kết quả review độc lập cần được đối chiếu trước khi Leader nghiệm thu.

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

**Đầu ra hiện hành** là [ADR Rev04](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/7af011f3f95e21ac829a163ee4be36200c1e7d88/DECISIONS.md) trong [Draft PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2). Review chéo và chấp thuận M1 cuối cùng chưa được xác nhận.

| Người | Trách nhiệm |
|---|---|
| Huy | Tổng hợp D04–D10, làm rõ TA cho D01–D03 và D13-E đã duyệt, kèm lý do và đánh đổi |
| Hải | Kiểm tra kiến trúc hàm, logic rules, cách tách validation và classification |
| Việt Đức | Kiểm tra audit, UUID, bảo mật, test, CI và benchmark |
| Cả ba | Đọc chéo Requirements–ADR–Test Plan, không để một tài liệu mâu thuẫn tài liệu khác |

**Đạt khi:** cả ba đã đọc và phản hồi phần mình; Huy phê duyệt bản tổng hợp. TA duyệt **scope** ở Checkpoint 1, không thay nhóm phê duyệt toàn bộ kỹ thuật.

## 4. Các mốc bàn giao nội bộ đề xuất trước Checkpoint 1 (lịch sử)

| Mốc | Bàn giao cần có | Xử lý khi gặp khó khăn |
|---|---|---|
| **05/11** | Cả ba đọc `PROJECT_GUIDE.md` và `TEAM_PLAN.md`; Hải/Việt Đức nhắn xác nhận task | Hỏi trong Zalo nếu chưa hiểu |
| **06/11 — bản nháp đầu tiên** | Hải: rule design + ma trận test; Việt Đức: AC traceability + checklist; Huy: requirements khung | Gửi phần đã có + phần chưa làm + blocker, không im lặng |
| **07/11 — review/sửa** | Mỗi người sửa theo comment, gửi lại link bản nháp/PR | Huy cân nhắc thu hẹp hoặc chuyển giao task nếu có rủi ro |
| **08/11 — Checkpoint 1** | Requirements, AC, Test Plan, ADR đầu tiên nhất quán, đủ để trình TA | Không tuyên bố TA đã duyệt nếu chưa được phản hồi |

Bảng lưu lại các mốc quản lý nội bộ đã đề xuất trước Checkpoint 1. Hạn chính thức của Checkpoint 1 là cuối 08/11/2026.

## 5. Phân công định hướng M2–M4 (chưa phải lệnh làm ngay)

| Giai đoạn | Huy Đức | Hải | Việt Đức |
|---|---|---|---|
| **M2 · 09–15/11** | Review logic và PR, tích hợp, đối chiếu contract theo làm rõ D01–D03 và D13-E | Code `classify()` và các hàm logic/validation, test rule/boundary | Phần audit nhỏ và test audit, kiểm tra CI, smoke test |
| **M3 · 16–19/11** | Kiểm tra A-01–A-11, hoàn thiện tài liệu, review freeze/tag | Sửa lỗi core, mở rộng negative/boundary test | Chạy benchmark, security/privacy checklist, CI evidence, hỗ trợ TEST_REPORT và AI_USE |
| **M4 · 20/11** | Chuẩn bị PR nộp bài, điền `source-ref.json`, kiểm tra SHA/tag/CI | Đối chiếu source release, hỗ trợ sửa blocker | Rà schema nộp, tài liệu QA, evidence và contributions |
| **Viva · 21/11** | Giải thích kiến trúc, các quyết định và đánh đổi | Giải thích code/rule/test | Giải thích audit/CI/privacy/benchmark; **cả ba hiểu hệ thống tổng thể** |

### Bàn giao M2 từ thiết kế M1

**Đã có để đối chiếu** gồm [175 ca chính](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M1/TEST_CASES.csv), [81 ca logic nội bộ](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTERNAL_STATE_CASES.csv) và [kế hoạch integration có INT-021](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/blob/61b6b9ff2d0ef62ee1794d7b7b68eb74d814429e/docs/m1-hai/M2/INTEGRATION_TEST_PLAN.md). Đây là đầu vào cho triển khai và viết test. Chưa xác nhận thực thi classifier/helper, integration, CI nghiệp vụ, benchmark, peer QA hoặc nghiệm thu M1.

- **Hải** dự kiến triển khai validation và selector D13-E, chạy ca rule, biên và trạng thái nội bộ. Kiểm tra riêng definite thắng possible, AllPV, Mixed, ưu tiên sốc và các trường hợp thiếu tuổi/HATT. Review logic giải thích trong INT-021 cùng Việt Đức.
- **Việt Đức** đối chiếu QA Matrix A-01–A-11 với ID ca, test thực thi, nguồn bằng chứng và khoảng trống. Với INT-021, áp dụng `explanation_assertions` lên `ly_do` thực tế của DIRECT/CANONICAL/MIXED, kiểm tra cả mẫu phải khớp và mẫu sai phải bị loại. Kiểm tra gọi trực tiếp `classify(patient)`, validation, JSONL bốn trường, UUID/context theo phiên và việc dọn context, cô lập file test, đường lỗi audit/fail-closed và privacy ở output, audit, message và exception chaining.
- **Huy Đức** đối chiếu Requirements–ADR–Test Plan, review bằng chứng và quyết định tích hợp. Đường dẫn audit mặc định và cách xử lý lỗi nội bộ ngoài dự kiến vẫn theo trạng thái review riêng trong ADR.

Nếu kỹ năng thực tế khác với dự kiến, leader có thể điều chỉnh. Không gán công việc chưa thực hiện cho thành viên trong `CONTRIBUTIONS.md`.

## 6. Cách dùng AI riêng nhưng không làm lệch thiết kế

Cả nhóm dùng đề thi, Decision Table tại tag `bkt-2026-v1`, phản hồi TA cho D01–D03, Requirements/ADR Rev04 và bộ ca M1-02 ở mục 3. Guide và Plan tóm tắt cách áp dụng. D13-E là chính sách nhóm đã duyệt.

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
