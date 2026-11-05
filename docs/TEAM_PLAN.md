# TEAM PLAN — PHÂN CÔNG, BÀN GIAO & REVIEW

> **Nhóm 173820_n27 | Track A — Dr May Day**  
> Bản dự thảo v0.1, 05/11/2026. **Chưa đăng lên GitHub.**  
> **Huy Đức đã đồng ý hướng chia việc; Hải và Việt Đức chưa xác nhận nhận việc.**  
> Đọc [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) trước tài liệu này.

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
| **Huy Đức — SV1 (Leader)** | Requirements, quyết định thiết kế, tích hợp | Contract, phạm vi, thống nhất D01–D12, quản lý deadline, chốt tài liệu/PR cuối | Hải và Việt Đức review chéo; Huy tổng hợp quyết định cuối |
| **Hải — SV2 (Technical Owner)** | Logic phân loại & test kỹ thuật | Thiết kế rồi triển khai R01/R02/R03/R-SOC, validation, boundary/negative tests | Huy đối chiếu với Decision Table; Việt Đức kiểm tra AC/test coverage |
| **Việt Đức — SV3 (QA/Quality Owner)** | QA, audit, security, CI, benchmark | Đối chiếu A-01–A-11, kiểm chứng không rò dữ liệu, triển khai audit nhỏ ở M2 có review, bằng chứng CI/benchmark | Huy review; Hải hỗ trợ phần code/test kỹ thuật |

**Phân công là trách nhiệm chính, không phải tách biệt kiến thức.** Cả ba phải hiểu luồng input → validation → rules → output/audit để trả lời vấn đáp ngẫu nhiên.

Không đưa họ tên đầy đủ, thông tin cá nhân hoặc thông tin đăng nhập vào repo công khai.

## 3. M1: công việc ngay trước Checkpoint 1 (05–08/11)

### M1-01 — Huy Đức: Requirements & Scope

**Đầu ra dự kiến:** bản nháp `REQUIREMENTS.md` (file chính thức chỉ tạo khi TASK 02 được giao).

- Mô tả mục tiêu bài, giới hạn trong/ngoài phạm vi.
- Viết input/output contract chín trường/ba trường đúng bảng quyết định.
- Diễn giải R01–R03/R-SOC, thứ tự tầng, yêu cầu zero PII.
- Đối chiếu 11 acceptance criteria, phân biệt yêu cầu từ đề và quyết định của nhóm.
- Ghi D01–D03 **PENDING TA CONFIRMATION**, D04–D10 **APPROVED BY LEAD**, D11–D12 **SPECIFIED**.
- Theo dõi [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15) và cập nhật nếu thầy trả lời.

**Reviewer:** Hải kiểm tra logic rule; Việt Đức kiểm tra AC và điều kiện an toàn.  
**Đạt khi:** không sai contract, có nguồn, không thiếu AC, khớp Test Plan và có review.

### M1-02 — Hải: Rule Design & Test Cases

**Đầu ra dự kiến:** sơ đồ/diễn giải luồng `classify()` tối giản; danh sách test cases có **Test ID — Scenario — Input — Expected — AC — Nguồn — Trạng thái**.

- Diễn giải chính xác từng điều kiện `AND/OR`, R01–R03 và R-SOC.
- Test các nhóm `SOC_PHAN_VE`, `PHAN_VE`, `THEO_DOI`.
- Test R02 với 0, 1, 2, 3, 4 hệ biểu hiện.
- Test R03 ở cả nhánh hô hấp và tuần hoàn, kể cả khi dị nguyên qua đường hít.
- Test overlap R02/R03; test ưu tiên R-SOC.
- Test tuổi `0`, `0.5`, `1`, `1.5`, `10.99`, `11`, `18`, huyết áp bằng ngưỡng, giảm đúng và trên 30%.
- Test dữ liệu thiếu, `null`, sai kiểu và trường dư. Các ca chịu ảnh hưởng D01–D03 phải ghi **PENDING**, không tự chốt expected.
- Đề xuất hàm hỗ trợ **ít và rõ trách nhiệm** theo D05, giúp viết ADR.

**Không triển khai code `classify()` trong M1 nếu Huy chưa giao task viết code.**  
**Reviewer:** Huy kiểm tra expected độc lập theo Decision Table; Việt Đức kiểm tra ánh xạ AC.  
**Đạt khi:** test có input, expected, căn cứ; giải thích được ít nhất một ca của từng rule và một ca biên.

### M1-03 — Việt Đức: AC Traceability, QA & Audit/Security Review

**Đầu ra dự kiến:** bảng A-01–A-11 → cách kiểm chứng/test ID/bằng chứng; QA checklist; đóng góp thiết kế audit, privacy, CI, benchmark và AI-use.

- Dùng danh sách test của Hải để map đủ **11 AC**; chỉ ra AC nào **chưa có test/bằng chứng**.
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

**Đầu ra dự kiến:** `DECISIONS.md` / ADR đầu tiên.

| Người | Trách nhiệm |
|---|---|
| Huy | Tổng hợp D04–D10 đã duyệt, các lý do và đánh đổi; giữ D01–D03 pending |
| Hải | Kiểm tra kiến trúc hàm, logic rules, cách tách validation và classification |
| Việt Đức | Kiểm tra audit, UUID, bảo mật, test, CI và benchmark |
| Cả ba | Đọc chéo Requirements–ADR–Test Plan, không để một tài liệu mâu thuẫn tài liệu khác |

**Đạt khi:** cả ba đã đọc và phản hồi phần mình; Huy phê duyệt bản tổng hợp. TA duyệt **scope** ở Checkpoint 1, không thay nhóm phê duyệt toàn bộ kỹ thuật.

## 4. Các mốc bàn giao nội bộ (đề xuất)

| Mốc | Bàn giao cần có | Xử lý khi gặp khó khăn |
|---|---|---|
| **05/11** | Cả ba đọc `PROJECT_GUIDE.md` và `TEAM_PLAN.md`; Hải/Việt Đức nhắn xác nhận task | Hỏi trong Zalo nếu chưa hiểu |
| **06/11 — bản nháp đầu tiên** | Hải: rule design + ma trận test; Việt Đức: AC traceability + checklist; Huy: requirements khung | Gửi phần đã có + phần chưa làm + blocker, không im lặng |
| **07/11 — review/sửa** | Mỗi người sửa theo comment, gửi lại link bản nháp/PR | Huy cân nhắc thu hẹp hoặc chuyển giao task nếu có rủi ro |
| **08/11 — Checkpoint 1** | Requirements, AC, Test Plan, ADR đầu tiên nhất quán, đủ để trình TA | Không tuyên bố TA đã duyệt nếu chưa được phản hồi |

Đây là **mốc quản lý nội bộ**, có thể điều chỉnh theo thống nhất của nhóm trên Zalo. **Hạn chính thức:** cuối 08/11/2026.

## 5. Phân công định hướng M2–M4 (chưa phải lệnh làm ngay)

| Giai đoạn | Huy Đức | Hải | Việt Đức |
|---|---|---|---|
| **M2 · 09–15/11** | Review logic và PR, tích hợp, đối chiếu contract, xử lý D01–D03 theo phản hồi | Code `classify()` và các hàm logic/validation, test rule/boundary | Phần audit nhỏ và test audit, kiểm tra CI, smoke test |
| **M3 · 16–19/11** | Kiểm tra A-01–A-11, hoàn thiện tài liệu, review freeze/tag | Sửa lỗi core, mở rộng negative/boundary test | Chạy benchmark, security/privacy checklist, CI evidence, hỗ trợ TEST_REPORT và AI_USE |
| **M4 · 20/11** | Chuẩn bị PR nộp bài, điền `source-ref.json`, kiểm tra SHA/tag/CI | Đối chiếu source release, hỗ trợ sửa blocker | Rà schema nộp, tài liệu QA, evidence và contributions |
| **Viva · 21/11** | Giải thích kiến trúc, các quyết định và đánh đổi | Giải thích code/rule/test | Giải thích audit/CI/privacy/benchmark; **cả ba hiểu hệ thống tổng thể** |

Nếu kỹ năng thực tế khác với dự kiến, leader có thể điều chỉnh. Không gán công việc chưa thực hiện cho thành viên trong `CONTRIBUTIONS.md`.

## 6. Cách dùng AI riêng nhưng không làm lệch thiết kế

**Một nguồn chung:** đề thi + Decision Table đúng tag + `PROJECT_GUIDE.md` + `TEAM_PLAN.md` + D04–D10 đã duyệt + D01–D03 pending.

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

- **Không chờ đến 08/11 mới nói không làm kịp**: báo khi phát sinh blocker hoặc có nguy cơ trễ.
- Nếu chất lượng chưa đạt, reviewer nêu lỗi cụ thể và Owner sửa; không lấy bản đầu do Codex tạo làm kết quả cuối.
- Nếu task có nguy cơ làm trễ Checkpoint, Huy có quyền chuyển giao **một phần công việc có phạm vi rõ**, cập nhật lại Owner/Reviewer.
- Ai thực tế viết, kiểm chứng, review thì ghi đúng vào bằng chứng đóng góp. Không gán công giả.
- Mỗi phần bàn giao phải đủ rõ để người khác tiếp nhận mà **không cần truy cập cuộc hội thoại Codex riêng**.

## 9. Chuẩn bị vấn đáp theo trách nhiệm

| Người | Phải giải thích được |
|---|---|
| Huy | Vì sao chọn D04–D10, ưu nhược điểm, tích hợp, trách nhiệm AI/human |
| Hải | `classify()`, R01/R02/R03/R-SOC, validation, test ranh giới |
| Việt Đức | Audit bốn trường, UUID synthetic, bảo mật, CI, p50/p95, bằng chứng nghiệm thu |
| **Cả nhóm** | Luồng tổng thể, vì sao test pass chưa đủ chứng minh đúng, D01–D03, cách kiểm chứng Codex |

**Không dùng AI khi vấn đáp trực tiếp.** Phải tự hiểu quyết định nhóm đã chốt, không học thuộc câu trả lời sai với code thực tế.
