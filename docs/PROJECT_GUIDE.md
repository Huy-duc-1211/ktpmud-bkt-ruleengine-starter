# PROJECT GUIDE — ĐỌC TRƯỚC KHI NHẬN VIỆC

> **Nhóm 173820_n27 | Hack Marathon 2026 | Track A — Dr May Day**  
> Hướng dẫn nội bộ sau tích hợp M1. Đề thi và bảng quyết định là nguồn bắt buộc của Track A.

## 1. Bắt đầu từ đâu? (10–15 phút)

1. Đọc toàn bộ mục 2–6 của file này để hiểu bài thi, những việc đã làm và những quyết định đã chốt.
2. Mở **đề chính thức** và **`docs/decision-table.md`** (link mục 2). Đây là nguồn có thẩm quyền; nếu có mâu thuẫn, dừng lại và hỏi leader.
3. Đọc [Requirements](../REQUIREMENTS.md) và [ADR](../DECISIONS.md) để đối chiếu contract và quyết định thiết kế. Xem bàn giao M2 ở mục 5 của [Team Plan](TEAM_PLAN.md).
4. Xác nhận nhận việc trong nhóm Zalo. Không để Codex tự quyết định những điểm nhóm đã khóa.

## 2. Bài thi và nguồn chính thức

**Bài thi:** Hoàn thiện một **Rule Engine Python** phân loại dữ liệu giả lập theo bảng quyết định đã được giảng viên cung cấp. Bài **không yêu cầu** xây website, machine learning, hệ thống bệnh viện, database thật hoặc kết nối sản phẩm Dr May Day đang vận hành.

**Triết lý chấm:** Phân tích và thiết kế quan trọng hơn độ nhiều tính năng, nhưng vẫn **bắt buộc có MVP chạy được, unit tests và CI**.

| Hạng mục | Điểm |
|---|---:|
| Phân tích yêu cầu, phạm vi, acceptance criteria | 14 |
| Kiến trúc và quyết định thiết kế | 18 |
| MVP chạy được | 12 |
| Test và CI | 13 |
| Bảo mật, riêng tư, giới hạn AI/dữ liệu | 8 |
| Maintainability và handoff | 5 |
| Demo/vấn đáp cá nhân | 10 |
| Track A: đúng bảng quyết định | 10 |
| Track A: giải thích và audit | 5 |
| Track A: benchmark | 5 |
| **Tổng** | **100** |

Điều kiện giới hạn điểm theo đề: không có MVP chạy được → tối đa 49; không có test tự động hoặc CI → tối đa 59; thiếu `AI_USE.md` sau hạn bổ sung → tối đa 70. Thành viên không giải thích được công việc của mình có thể bị điều chỉnh điểm cá nhân.

**Nguồn cần mở:**

- [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html) (URL ghi v1.0.0, nội dung đã đối chiếu hiển thị v1.0.2).
- [Decision Table V1](decision-table.md) — nguồn công thức và ngưỡng.
- [Repo starter gốc](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter), **tag `bkt-2026-v1`** tại `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469`.
- [Repo phát triển của nhóm](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter), nhánh `track-a-development`.
- [Repo chuẩn bị nộp của nhóm](https://github.com/Huy-duc-1211/ktpmud-project); **không viết code phân loại ở repo này**.
- [Repo đích nộp bài của thầy](https://github.com/fossbk-spec/ktpmud-project).
- [phản hồi chính thức tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) (D01–D03 và cách xử lý dữ liệu thiếu).
- [Phản hồi Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31#issuecomment-6796604002) về chọn mã đại diện khi thiếu khóa boolean.
- [Erratum pytest của starter (Issue #16)](https://github.com/fossbk-spec/ktpmud-project/issues/16).
- Nguồn nhóm hiện hành: [Requirements](../REQUIREMENTS.md), [ADR](../DECISIONS.md), [Rule Design và Test Plan](m1-hai/M1/README.md), [QA Matrix](m1-qa/QA_MATRIX.xlsx).
- [Mẫu hồ sơ Track A](https://github.com/fossbk-spec/ktpmud-project/tree/main/submissions/_TEMPLATE_BKT_RULEENGINE).

**Định danh:** Lớp `173820`, nhóm `27`, mã dự kiến `173820_n27`; slug Track A `may_day_sprint`. Nhóm cần xác nhận mã từ đồ án chính có dùng chung cho Hack Marathon hay không.

**Hai repository có vai trò khác nhau:** Fork starter để phát triển và test chương trình; fork `ktpmud-project` để chuẩn bị hồ sơ cuối cùng, sau đó PR vào repo đích của thầy. Không tạo bài nộp hoặc release khi chưa được leader phê duyệt.

## 3. Logic nghiệp vụ cần hiểu

### 3.1. Input có 9 tên trường được phép

| Trường | Kiểu theo tài liệu | Ý nghĩa |
|---|---|---|
| `tuoi` | `float` (năm) | **Cho phép số lẻ**, ví dụ `0.5` = 6 tháng; tuổi 0 thuộc bảng |
| `huyet_ap_tam_thu` | `int` hoặc `null` | Huyết áp tâm thu; `null` khi không đo được |
| `huyet_ap_tam_thu_nen` | `int` hoặc `null` | Huyết áp nền để xét giảm >30% ở người lớn |
| `co_di_nguyen_nghi_ngo` | `bool` | Có dị nguyên nghi ngờ |
| `di_nguyen_qua_duong_hit` | `bool` | Dị nguyên qua đường hít |
| `co_ton_thuong_da_niem_mac` | `bool` | Tổn thương da/niêm mạc |
| `co_trieu_chung_ho_hap` | `bool` | Triệu chứng hô hấp |
| `co_trieu_chung_tuan_hoan` | `bool` | Triệu chứng tuần hoàn |
| `co_trieu_chung_tieu_hoa_nang` | `bool` | Triệu chứng tiêu hóa nặng |

Bảng trên ghi kiểu trong Data Dictionary. Theo D04, tuổi có giá trị nhận `int` hoặc `float` hữu hạn ≥0, loại `bool`. HATT hiện tại có giá trị phải là `int` ≥0, HATT nền có giá trị phải là `int` >0, cả hai loại `bool`. Quy tắc với khóa thiếu và `null` nằm ở mục 5.

Chỉ sử dụng **dữ liệu synthetic**; không đưa tên, MSSV, số điện thoại, CCCD hay thông tin định danh vào `PatientInput`.

### 3.2. Các rule (phải xem công thức gốc khi làm)

- **R01:** Không có dị nguyên nghi ngờ **và** tổn thương da/niêm mạc **và** (hô hấp **hoặc** tuần hoàn).
- **R02:** Có dị nguyên nghi ngờ **và** ít nhất **2/4** hệ da/niêm mạc, hô hấp, tuần hoàn, tiêu hóa nặng.
- **R03:** Có dị nguyên nghi ngờ **và** ((**không** qua đường hít **và** có triệu chứng hô hấp) **hoặc** có triệu chứng tuần hoàn).
- **R-SOC:** Đã thỏa ít nhất một trong ba rule phản vệ **và** có tụt huyết áp theo tuổi:

| Độ tuổi | Điều kiện huyết áp tâm thu (HATT) |
|---|---|
| 0 ≤ tuổi < 1 | HATT < 70 |
| 1 ≤ tuổi < 11 | HATT < 70 + 2 × tuổi |
| 11 ≤ tuổi < 18 | HATT < 90 |
| Tuổi ≥ 18 | HATT < 90 **hoặc** giảm **>30%** so với nền |

Dấu `<` và `>` là **nghiêm ngặt**. Đúng bằng ngưỡng **không đạt** điều kiện đó. HATT thấp đơn độc không đủ kết luận sốc.

### 3.3. Output và giải thích

Đầu ra có **3 khóa**: `muc_do`, `rule_id`, `ly_do`.

```json
{"muc_do":"PHAN_VE","rule_id":"R01-PV","ly_do":"Đáp ứng kịch bản R01 theo bảng quyết định."}
```

- `muc_do`: `SOC_PHAN_VE`, `PHAN_VE`, `THEO_DOI`.
- `rule_id`: `R-SOC`, `R01-PV`, `R02-PV`, `R03-PV`, `null`.
- Với `PHAN_VE`, chọn rule ưu tiên cao nhất trong các rule có thể thỏa. Nếu rule được chọn chắc chắn đúng, mã là DIRECT; nếu chưa chắc chắn, mã là CANONICAL, kể cả khi rule ưu tiên thấp hơn đã chắc chắn. Với CANONICAL, `ly_do` nêu mã đại diện, dữ liệu thiếu và rule mang mã chưa được xác nhận riêng.
- `ly_do` giải thích ngắn gọn căn cứ phân loại và thông tin còn thiếu khi liên quan. Tránh dữ liệu lâm sàng thô và lời khuyên điều trị. Ví dụ JSON trên minh họa DIRECT.
- `THEO_DOI` nghĩa là **chưa đủ điều kiện kết luận theo bảng**, không đồng nghĩa “an toàn”.

### 3.4. Thuật ngữ tối thiểu

| Từ | Giải thích |
|---|---|
| Contract | Quy ước bắt buộc về input/output, kiểu dữ liệu và hành vi |
| Acceptance Criteria (AC) | Điều kiện có thể kiểm chứng để nghiệm thu |
| Unit test / pytest | Bài kiểm tra một hành vi với input và expected output |
| Boundary test | Test tại ranh giới tuổi/huyết áp và các dấu `<`, `>` |
| CI | GitHub Actions tự chạy test khi có push/PR |
| Audit trail | Nhật ký thao tác, chỉ bốn trường cho phép |
| ADR | Ghi quyết định: vấn đề, phương án, lý do, đánh đổi |
| PR (Pull Request) | Đề nghị gộp thay đổi, cần người khác review |
| p50/p95 | Phân vị thời gian xử lý; bài thi yêu cầu ≥1.000 lượt sau warm-up và p95 < 100 ms |

## 4. Đến nay nhóm đã làm được gì?

| Nội dung | Trạng thái sau tích hợp M1 |
|---|---|
| Tích hợp | [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) đã merge vào `track-a-development` ngày 10/11/2026. Mốc tích hợp [`9bc4fc1`](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/commit/9bc4fc186415d7a13cd9d49692c50f3c945ddf7b). |
| M1-01 / M1-04 | [Requirements](../REQUIREMENTS.md) và [ADR](../DECISIONS.md) đã tích hợp. D01–D03 được giảng viên làm rõ. Leader phê duyệt chính sách nhóm D13-E ngày 09/11/2026. |
| M1-02 | [Rule Design](m1-hai/M1/RULE_DESIGN.md), [Test Plan](m1-hai/M1/TEST_PLAN.md), [175 ca thiết kế chính](m1-hai/M1/TEST_CASES.csv) và [81 ca logic nội bộ](m1-hai/M2/INTERNAL_STATE_CASES.csv). Hải đóng góp bản gốc, Huy Đức phụ trách bản sửa TASK 02E với Codex hỗ trợ. |
| M1-03 | [QA Matrix](m1-qa/QA_MATRIX.xlsx) và báo cáo audit thiết kế gồm 11 AC, 64 ca QA, 60 mục checklist và 15 phát hiện. Các mục thực thi vẫn `NOT RUN`. |
| Review và nghiệm thu | GitHub ghi Leader self-review và approval từ `nvldvc` trên bốn PR. Chưa thấy bằng chứng review kỹ thuật cuối của cả hai thành viên hoặc TA nghiệm thu phạm vi. |

[Classifier](../rule_engine/classifier.py) vẫn raise `NotImplementedError`. [Test hiện có](../tests/test_classifier.py) chỉ kiểm tra stub. [Workflow CI](../.github/workflows/test.yml) đã cấu hình, chưa có bằng chứng bộ test nghiệp vụ chạy đạt trên CI. Chưa có kết quả benchmark. Hồ sơ tích hợp là đầu ra phân tích và thiết kế M1.

## 5. Các quyết định đã thống nhất và đang chờ

### D04–D10: leader đã phê duyệt định hướng

| ID | Quyết định |
|---|---|
| **D04** | Validation nghiêm ngặt, không ép kiểu ngầm. Tuổi là số hữu hạn **≥0, có thể là số lẻ**; không coi `True/False` là số. Kiểm tra toàn bộ input trước phân loại. Sai kiểu thật sự dùng `TypeError`. Sai miền hoặc khóa lạ dùng `ValueError`. Missing/null được xử lý theo TA và D13-E. |
| **D05** | Giữ `classify(patient)`; tách vài hàm theo trách nhiệm, **kiến trúc tối giản**, không làm rối logic. |
| **D06** | `ly_do` dựa trên mẫu tất định theo kết quả và nguồn gán mã DIRECT/CANONICAL. Nêu thiếu tuổi/HATT/nền khi liên quan. Tránh LLM, dữ liệu thô và lời khuyên điều trị. |
| **D07** | Tách audit writer; dùng JSON Lines cho bài thi; UUID giả lập theo **phiên người thao tác** nằm ngoài `PatientInput`; hỗ trợ thay cách lưu sau này nhưng **không tích hợp production**. |
| **D08** | Audit cả xử lý thành công và input lỗi, chỉ ghi trạng thái tổng quát; không log payload hoặc exception chứa dữ liệu đầu vào. |
| **D09** | Test normal, boundary, invalid, missing, overlap, output, audit. **Test tuổi số lẻ** vì đề quy định. |
| **D10** | Benchmark `classify()` toàn luồng và phép đo phụ logic thuần; ≥1.000 lượt sau warm-up; báo p50/p95 và máy đo. |

**D11–D12 là ràng buộc từ đề:** Không tự thêm clinical rules/ngưỡng; input chỉ chín trường, output ba trường, audit đúng `Timestamp, User_UUID, Action_Type, Status`; zero PII/PHI/secret.

### D01–D03 đã được giảng viên làm rõ

| ID | Hướng dẫn hiện hành |
|---|---|
| **D01** | Nếu đủ Tầng 1, ưu tiên `SOC_PHAN_VE / R-SOC`. Khi nhiều rule Tầng 2 cùng thỏa và chưa đủ Tầng 1, chọn một mã theo R01-PV > R02-PV > R03-PV. R02 và R03 cùng thỏa thì chọn R02-PV. |
| **D02** | Tuổi thiếu khóa hoặc `null` → `THEO_DOI / null` kể cả khi bằng chứng Tầng 2 đã đủ. `ly_do` nêu thiếu tuổi để chọn ngưỡng. |
| **D03** | Có tuổi và đủ bằng chứng Tầng 2 thì giữ `PHAN_VE` với mã Tầng 2 phù hợp khi HATT hiện tại thiếu/`null` hoặc người ≥18 tuổi có HATT ≥90 mmHg nhưng thiếu/`null` HATT nền. Nêu số đo nào còn thiếu, tránh suy hoặc gán nền mặc định. Người ≥18 tuổi có HATT <90 mmHg vẫn đủ bằng chứng cho nhánh tuyệt đối khi Tầng 2 đã được chứng minh. |

Thiếu khóa và `null` tương đương về `muc_do` và `rule_id` đối với tuổi, HATT hiện tại và HATT nền. Với boolean thiếu/`null`, TA yêu cầu không lỗi chỉ vì thiếu dữ liệu và giữ mức đã đủ bằng chứng. Xem [phản hồi chính thức tại Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248).

### D13-E đã được Leader phê duyệt ngày 09/11/2026

D13-E là chính sách nội bộ đã công bố theo phạm vi TA cho phép. Issue #31 làm rõ thứ tự chọn mã đại diện khi thiếu khóa; cách nhóm áp dụng cho overlap definite/possible do Leader quyết định. Xem [Requirements](../REQUIREMENTS.md) và [ADR](../DECISIONS.md).

- Boolean thiếu khóa hoặc `null` → UNKNOWN nội bộ. Boolean có giá trị phải đúng kiểu. Áp dụng D04 cho dữ liệu không hợp lệ và giữ Enum/Kleene, cách đếm T/U của R02. Không ép UNKNOWN thành False.
- Giữ dữ liệu đã biết khi xét mọi cách gán True/False cho boolean UNKNOWN. **Def** là tập rule đúng trong mọi khả năng. **Poss** là tập rule đúng trong ít nhất một khả năng. **AllPV** nghĩa là mỗi khả năng đều khớp ít nhất một rule Tầng 2.
- Khi AllPV và chưa xác nhận sốc, chọn rule ưu tiên cao nhất trong **Poss** theo R01 > R02 > R03. Rule được chọn thuộc Def là DIRECT; nếu chưa chắc chắn là CANONICAL, kể cả khi rule ưu tiên thấp hơn đã chắc chắn. Giải thích mã đại diện như mục 3.3.
- Bằng chứng phản vệ từ Def hoặc AllPV kết hợp bằng chứng tụt HATT theo bảng và tuổi đã biết → `SOC_PHAN_VE / R-SOC`. Ưu tiên kiểm tra tuổi theo D02 và xử lý HATT thiếu theo D03.
- **Mixed**, tức có cả khả năng khớp và không khớp Tầng 2 → `THEO_DOI / null` với lý do chưa đủ thông tin. Nếu mọi khả năng đều không khớp, dùng cùng mức/mã với lý do không khớp rule.

Các lựa chọn về validation số, ContextVar/UUID, fail-closed, thứ tự lỗi kép và protocol benchmark đã có trong ADR Rev04. Cơ chế đường dẫn audit mặc định vẫn là đề xuất chờ review. Xử lý lỗi nội bộ ngoài dự kiến vẫn là mục cần review riêng.

## 6. A-01 đến A-11: cần làm gì để đạt?

| Mã | Điều kiện |
|---|---|
| A-01 | `classify()` chạy đúng contract, hết `NotImplementedError` |
| A-02 | Không hard-code theo fixture ID |
| A-03 | Bao phủ mọi mức phân loại |
| A-04 | Chính sách thiếu/sai kiểu/ngoài miền rõ và được thực thi |
| A-05 | `ly_do` truy vết được rule, không khuyên điều trị |
| A-06 | Audit đúng bốn trường, không raw clinical input |
| A-07 | Unit tests normal/boundary/invalid/missing |
| A-08 | `pytest -q` đạt từ clean checkout |
| A-09 | CI chạy test trên PR |
| A-10 | ≥1.000 lượt sau warm-up; p50/p95; p95 <100 ms; ghi máy đo |
| A-11 | README ghi `educational/synthetic — not for clinical use` |

## 7. Milestone chính thức

| Mốc | Ngày | Đầu ra |
|---|---|---|
| M0 | 04/11 | Chọn track, nhóm, tag/commit — phần kỹ thuật đã hoàn thành |
| M1 | 05–08/11 | Requirements, AC, Test Plan, ADR đầu tiên |
| **Checkpoint 1** | **Cuối 08/11** | TA duyệt phạm vi, không duyệt thay mọi thiết kế |
| M2 | 09–15/11 | Vertical slice chạy được, public tests đạt |
| **Checkpoint 2** | **Cuối 15/11** | Demo nội bộ 5 phút |
| M3 | 16–19/11 | Test, CI, audit, security/privacy, tài liệu bàn giao |
| **Freeze** | **23:59 ngày 19/11** | SHA cuối + tag `bkt-2026-173820_n27-rc1` |
| M4 | **20/11** | PR nộp bài, CI xanh |
| Demo/Viva | **21/11** | Demo tối đa 7 phút; vấn đáp tối đa 8 phút |

Mốc nội bộ cho từng người ghi tại `TEAM_PLAN.md`, **không thay thế** mốc chính thức.

## 8. Hồ sơ cuối kỳ và nguyên tắc làm việc

Bộ hồ sơ gồm code/test/CI, `README.md`, `REQUIREMENTS.md`, `DECISIONS.md`/ADR, `TEST_REPORT.md`, `SECURITY_PRIVACY_CHECKLIST.md`, `AI_USE.md`, `CONTRIBUTIONS.md`, benchmark, slide/demo và PR theo thư mục `submissions/may_day_sprint_173820_n27/`. `source-ref.json` phải liên kết đúng starter, SHA, fork, final commit, release tag và CI run URL.

**Không được làm:** Dùng dữ liệu thật, kết nối production/Railway/CSDL thật, commit token/`.env`/secret, tìm hidden tests, để AI tự merge/release, dùng AI trong buổi vấn đáp.

**Mỗi người có thể dùng Codex riêng**, nhưng phải dùng cùng nguồn đặc tả, cùng quyết định đã chốt, cùng task. AI giúp soạn/lập trình, **không tự xác nhận đúng**. Người phụ trách phải tự đọc, kiểm tra, giải thích và bàn giao bằng chứng. Ghi hoạt động AI vào `AI_USE.md` theo công cụ, mục đích, file/commit, kiểm chứng, quyết định giữ/sửa/loại và người review.

## 9. Tự kiểm tra trước khi nhận việc

Mỗi thành viên cần trả lời được:
1. Vì sao Track A chỉ cần Rule Engine Python, không cần website hay ML?
2. R01, R02 và R03 khác nhau chỗ nào; khi nào mới là R-SOC?
3. Vì sao `tuoi=0.5` hợp lệ và HATT **bằng** ngưỡng không thỏa điều kiện `<`?
4. Vì sao nếu test stub chạy đạt thì vẫn chưa chứng minh code đúng nghiệp vụ?
5. Audit có những trường nào? Vì sao UUID không thuộc input bệnh nhân?
6. D01–D03 đã được giảng viên làm rõ thế nào? Khi nào D13-E dùng mã CANONICAL và phải giải thích điều gì?
7. Phải làm gì khi Codex tạo ra nội dung khác Decision Table?

**Việc ngay sau khi đọc:** mở `TEAM_PLAN.md`, xác nhận vai trò và task trên Zalo. Nếu chưa hiểu, hỏi trước khi làm.
