# PROJECT GUIDE — ĐỌC TRƯỚC KHI NHẬN VIỆC

> **Nhóm 173820_n27 | Hack Marathon 2026 | Track A — Dr May Day**  
> Bản dự thảo v0.1, ngày 05/11/2026. Dành cho Huy Đức, Hải và Việt Đức.  
> **Đây là tài liệu bàn giao nội bộ**, không thay thế đề thi hay bảng quyết định chính thức. Leader đã duyệt bản đưa lên GitHub; cập nhật đồng bộ D13 ngày 07/11/2026 đang chờ nhóm review.

## 1. Bắt đầu từ đâu? (10–15 phút)

1. Đọc toàn bộ mục 2–6 của file này để hiểu bài thi, những việc đã làm và những quyết định đã chốt.
2. Mở **đề chính thức** và **`docs/decision-table.md`** (link mục 2). Đây là nguồn có thẩm quyền; nếu có mâu thuẫn, dừng lại và hỏi leader.
3. Đọc [`REQUIREMENTS.md`](../REQUIREMENTS.md), tài liệu requirements hiện hành để Hải và Việt Đức đối chiếu, và [`TEAM_PLAN.md`](TEAM_PLAN.md) để biết mình phụ trách task nào, đầu ra cần bàn giao và ai review.
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
- [Decision Table — nguồn duy nhất về rule](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/blob/bkt-2026-v1/docs/decision-table.md).
- [Repo starter gốc](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter), **tag `bkt-2026-v1`**.
- [Repo phát triển của nhóm](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter), nhánh `track-a-development`.
- [Repo chuẩn bị nộp của nhóm](https://github.com/Huy-duc-1211/ktpmud-project); **không viết code phân loại ở repo này**.
- [Repo đích nộp bài của thầy](https://github.com/fossbk-spec/ktpmud-project).
- [Issue #15 — nhóm hỏi thầy](https://github.com/fossbk-spec/ktpmud-project/issues/15).
- [Mẫu hồ sơ Track A](https://github.com/fossbk-spec/ktpmud-project/tree/main/submissions/_TEMPLATE_BKT_RULEENGINE).

**Định danh:** Lớp `173820`, nhóm `27`, mã dự kiến `173820_n27`; slug Track A `may_day_sprint`. Nhóm cần xác nhận mã từ đồ án chính có dùng chung cho Hack Marathon hay không.

**Hai repository có vai trò khác nhau:** Fork starter để phát triển và test chương trình; fork `ktpmud-project` để chuẩn bị hồ sơ cuối cùng, sau đó PR vào repo đích của thầy. Không tạo bài nộp hoặc release khi chưa được leader phê duyệt.

## 3. Logic nghiệp vụ cần hiểu

### 3.1. Input có đúng 9 trường

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
- `ly_do`: chuỗi ngắn, giải thích rule đã kích hoạt; không có raw clinical input hay lời khuyên điều trị.
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

| Nội dung | Trạng thái cập nhật ngày 07/11/2026 |
|---|---|
| Chọn Track A và lập nhóm 3 người | **Xong** |
| Fork hai repo, tạo nhánh `track-a-development` | **Xong** |
| Đối chiếu tag/commit khởi đầu | **Xong**: `1c0a5b11fe8ea2b8a3126665cfe13ff551ad3469` |
| TASK 01 — Codex đọc starter và viết báo cáo phân tích | **Xong**, đã được leader và AI reviewer rà soát |
| Đăng Issue #15 hỏi D01–D03 | **Đã gửi; chưa có phản hồi tại thời điểm cập nhật** |
| Chốt định hướng thiết kế D04–D10 | **Leader đã đồng ý**, thành viên khác cần đọc và hiểu |
| D13 — đánh giá input một phần | **Leader đã phê duyệt**, xem yêu cầu hiện hành trong `REQUIREMENTS.md` |
| Thống nhất hướng phân vai | **Leader đồng ý**, chờ Hải và Việt Đức nhận task |
| `REQUIREMENTS.md` | **Đã có bản nháp hiện hành**, bổ sung D03 và đồng bộ D13 để nhóm review Checkpoint 1 |
| `DECISIONS.md`, Test Plan chính thức | Tiếp tục theo phần việc được giao, chưa có bằng chứng hoàn thành trong đợt đồng bộ này |
| `classify()` nghiệp vụ, audit, benchmark, test đầy đủ | **Chưa viết** |
| CI xanh với test nghiệp vụ; freeze, release, PR nộp | **Chưa thực hiện** |

**Cảnh báo:** `tests/test_classifier.py` trong starter đang kiểm tra `NotImplementedError`, không phải kiểm tra phân loại thật. Có workflow CI **không có nghĩa** đã đáp ứng A-08/A-09.

## 5. Các quyết định đã thống nhất và đang chờ

### D04–D10: leader đã phê duyệt định hướng

| ID | Quyết định |
|---|---|
| **D04** | Validation nghiêm ngặt, không ép kiểu ngầm. Tuổi là số hữu hạn **≥0, có thể là số lẻ**; không coi `True/False` là số. Input sai kiểu xử lý lỗi rõ ràng. Dữ liệu thiếu theo chính sách D02–D03 khi được làm rõ. |
| **D05** | Giữ `classify(patient)`; tách vài hàm theo trách nhiệm, **kiến trúc tối giản**, không làm rối logic. |
| **D06** | `ly_do` dựa trên mẫu giải thích gắn rule, không dùng LLM, không đưa dữ liệu thô hoặc khuyên điều trị. |
| **D07** | Tách audit writer; dùng JSON Lines cho bài thi; UUID giả lập theo **phiên người thao tác** nằm ngoài `PatientInput`; hỗ trợ thay cách lưu sau này nhưng **không tích hợp production**. |
| **D08** | Audit cả xử lý thành công và input lỗi, chỉ ghi trạng thái tổng quát; không log payload hoặc exception chứa dữ liệu đầu vào. |
| **D09** | Test normal, boundary, invalid, missing, overlap, output, audit. **Test tuổi số lẻ** vì đề quy định. |
| **D10** | Benchmark `classify()` toàn luồng và phép đo phụ logic thuần; ≥1.000 lượt sau warm-up; báo p50/p95 và máy đo. |

**D11–D12 là ràng buộc từ đề:** Không tự thêm clinical rules/ngưỡng; input chỉ chín trường, output ba trường, audit đúng `Timestamp, User_UUID, Action_Type, Status`; zero PII/PHI/secret.

### D13: Leader đã phê duyệt logic ba trạng thái

Với sáu trường boolean, thiếu khóa → UNKNOWN nội bộ; có khóa với null → invalid. Không biến UNKNOWN thành False hoặc đổi dữ liệu sai thành UNKNOWN. Khi tuổi/HATT còn thiếu, không tự kết luận không có sốc. D01–D03 vẫn `PENDING TA CONFIRMATION`, gồm trường hợp bổ sung D03 về người ≥18 tuổi, HATT hiện tại ≥90 mmHg nhưng thiếu HATT nền để xét giảm >30%. [`REQUIREMENTS.md`](../REQUIREMENTS.md) là tài liệu requirements hiện hành để Hải và Việt Đức đối chiếu chi tiết.

**Chi tiết còn cần thiết kế trong ADR:** miền giá trị số đo không được thầy định nghĩa đầy đủ; cách truyền UUID theo phiên mà không đổi contract; chính sách xử lý lỗi lưu audit; cách thống kê benchmark. Không tự thêm ngưỡng y khoa mới.

### D01–D03: còn chờ TA qua Issue #15

| ID | Câu hỏi | Phương án dự phòng **chưa được xác nhận** |
|---|---|---|
| **D01** | Nếu R02 và R03 cùng đúng, chọn `rule_id` nào? | Tạm ưu tiên R02 trước R03 theo thứ tự bảng |
| **D02** | Thiếu `tuoi` nhưng R01/R02/R03 đúng thì phân loại gì? | Tạm `THEO_DOI` theo đoạn đặc tả nhắc thiếu tuổi |
| **D03** | HATT `null`/thiếu nhưng thỏa phản vệ thì sao? | Với `null` hợp lệ, dự kiến `PHAN_VE`; thiếu hẳn khóa còn phải có policy |

**Không tự viết expected output chắc chắn cho ba ca mơ hồ.** Ghi `PENDING TA CONFIRMATION` trong bản nháp, cập nhật sau phản hồi của thầy.

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
4. Vì sao test stub đang pass không chứng minh code đã đúng?
5. Audit có những trường nào? Vì sao UUID không thuộc input bệnh nhân?
6. D01–D03 đang chờ gì, D04–D10 đã được ai duyệt?
7. Phải làm gì khi Codex tạo ra nội dung khác Decision Table?

**Việc ngay sau khi đọc:** mở `TEAM_PLAN.md`, xác nhận vai trò và task trên Zalo. Nếu chưa hiểu, hỏi trước khi làm.
