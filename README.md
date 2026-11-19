# KTPMUD Hack Marathon 2026 — Track A · Dr May Day

Nhóm `173820_n27` xây dựng Rule Engine Python theo [Decision Table V1](docs/decision-table.md). Hàm `classify(patient)` kiểm tra dữ liệu giả lập, xét rule, trả mức phân loại kèm lý do và ghi audit JSONL.

educational/synthetic — not for clinical use

## Cấu trúc repo code

Repo dùng vị trí `rule_engine/classifier.py` và `docs/decision-table.md` theo starter. Lệnh cài đặt và kiểm thử theo §7 của đề Track A. [Đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103) · [Starter](https://github.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/tree/bkt-2026-v1)

```text
.
├── README.md
├── REQUIREMENTS.md
├── DECISIONS.md
├── requirements.txt
├── pytest.ini
├── TEST_CASES.csv              # Input và expected theo mã ca
├── run_case.py                 # Chạy một ca và in kết quả thật
├── run_case.cmd                # Bấm đúp để chọn CSV và nhập mã ca
├── query_audit.py               # Đọc bản ghi audit và báo dòng lỗi
├── rule_engine/
│   ├── classifier.py          # Validation và logic phân loại
│   └── audit.py                # UUID phiên và ghi JSONL
├── tests/
│   ├── test_classifier.py
│   ├── test_audit.py
│   ├── conftest.py
│   └── fixtures/               # Bảng logic nội bộ và fixture NaN, Infinity
├── docs/
│   ├── decision-table.md
│   ├── design/
│   ├── testing/
│   ├── qa/
│   ├── reviews/
│   └── references/
├── progress/
└── .github/workflows/test.yml
```

## Cài đặt và kiểm thử

Dùng Python 3.12 như cấu hình CI. Chạy từ thư mục gốc của checkout vừa clone. Trên Bash, thay dòng kích hoạt PowerShell bằng `source .venv/bin/activate`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q
```

[`pytest.ini`](pytest.ini) áp dụng [erratum của starter](https://github.com/fossbk-spec/ktpmud-project/issues/16).

## Chạy thử với dữ liệu giả lập

Trên Windows, bấm đúp [`run_case.cmd`](run_case.cmd) rồi nhập `TEST_CASES.csv` hoặc đường dẫn đầy đủ tới file. Lệnh cũng nhận đường dẫn dán kèm tiền tố `cd `. Nếu file tồn tại, nhập mã ca như `MISS-009`. Sau mỗi kết quả, bạn có thể nhập tiếp mã khác trong cùng file. Gõ `END` rồi nhấn Enter để kết thúc. Nếu không tìm thấy file CSV, chương trình báo đường dẫn bị lỗi và dừng với mã thoát `1` trước khi hỏi mã ca. Cửa sổ chờ bạn nhấn thêm một phím trước khi đóng. File dùng Python trong `.venv` nếu có, hoặc chạy qua Python Launcher (`py`).

[Hướng dẫn tra mã ca và xuất CSV](runcase.md)

Trong CMD, mở thư mục gốc của repo và chạy `run_case.cmd MISS-009`. Trong PowerShell, dùng lệnh sau.

```powershell
.\.venv\Scripts\python.exe -X utf8 .\run_case.py MISS-009
```

Đổi `MISS-009` thành mã ca muốn xem. Lệnh tìm mã trong `TEST_CASES.csv`, lấy `Input` rồi in kết quả của `classify()`. Có thể thêm `--csv "đường-dẫn-tới-file.csv"` để dùng file ca giả lập khác. Nếu ca bị từ chối, lệnh in loại lỗi và thông báo. Dùng pytest khi cần tự động so kết quả với `Expected`.

Để lưu kết quả, nhập `/CSV` ở ô mã ca hoặc thêm `--export-csv ket_qua.csv` vào lệnh CMD hay PowerShell.

Để gọi hàm với input tự nhập, dùng Python như sau.

```python
from rule_engine.classifier import classify

print(classify({
    "tuoi": 15,
    "huyet_ap_tam_thu": 110,
    "co_di_nguyen_nghi_ngo": False,
    "co_ton_thuong_da_niem_mac": True,
    "co_trieu_chung_ho_hap": True,
}))
```

Ví dụ trên trả `PHAN_VE / R01-PV`. Muốn chỉ định file audit, đặt `DR_MAY_DAY_AUDIT_PATH` thành đường dẫn tuyệt đối tới file JSONL ngoài repo. Nếu chưa đặt biến này, chương trình ghi vào `~/.173820_n27/dr_may_day/runs/<run-id>/audit.jsonl`. Để dùng chung UUID giả lập cho nhiều lần gọi, đặt các lệnh gọi trong `with audit_session():` (import từ `rule_engine.audit`). Mỗi lần gọi ngoài phiên có UUID riêng.

Hàm ghi xong audit mới trả kết quả. Nếu input sai, hàm ghi `INVALID_INPUT` rồi báo `TypeError` hoặc `ValueError`. Nếu ghi audit thất bại, hàm báo `AuditError`. Các lần ghi vào cùng file diễn ra tuần tự.

Mỗi bản ghi kết thúc bằng `\n`. Trước khi ghi tiếp, chương trình xem byte cuối của file. Nếu file có nội dung và thiếu `\n`, chương trình thêm dấu phân cách để bản ghi mới nằm trên dòng riêng. Dữ liệu cũ, kể cả dòng bị ghi dở, vẫn nằm trong file.

Với INT-013, nếu validator hoặc logic phân loại bất ngờ gặp lỗi, hàm thử ghi `INTERNAL_ERROR` rồi báo `RuntimeError` với thông báo chung. Nếu bước audit thất bại, hàm báo `AuditError`. Bản ghi có bốn trường và không chứa input. Đây là chính sách nhóm, chưa có xác nhận riêng của thầy. [Ghi chú kiểm thử](docs/testing/README.md)

## Đọc audit

Dùng đường dẫn tới file cần đọc. Lệnh in các bản ghi hợp lệ ra màn hình và lưu báo cáo truy vấn vào một file riêng.

```powershell
.\.venv\Scripts\python.exe -X utf8 .\query_audit.py 'D:\audit\audit.jsonl' 2> "$env:TEMP\audit-query.log"
```

Ví dụ báo cáo: “Đọc được 12 bản ghi, bỏ qua 2 dòng lỗi, lỗi tại các dòng: 3, 8.” Số dòng tính từ 1. Các bản ghi hợp lệ sau dòng lỗi vẫn xuất hiện. Nếu bỏ phần `2>`, báo cáo hiện ngay trong cửa sổ lệnh. [Cách xử lý file ghi dở](DECISIONS.md#542-ghi-tiếp-khi-file-audit-đã-tồn-tại)

Một dòng có khóa JSON trùng cũng bị bỏ qua. Nếu gọi từ PowerShell, xem `$LASTEXITCODE` sau khi chạy.

| Mã thoát | Ý nghĩa |
|---|---|
| `0` | Đọc xong, không bỏ qua dòng nào. |
| `1` | Lỗi khi mở hoặc đọc file. |
| `2` | Tham số lệnh sai hoặc thiếu. |
| `3` | Đọc xong, có dòng bị bỏ qua. Các bản ghi hợp lệ vẫn được in ra. |

## Cấu trúc hồ sơ nộp bài

Theo §11.2, nhóm nộp PR trên `fossbk-spec/ktpmud-project`, dùng thư mục dưới đây. [Mẫu Track A](https://github.com/fossbk-spec/ktpmud-project/tree/main/submissions/_TEMPLATE_BKT_RULEENGINE) · [Bổ sung cho PC-2](https://github.com/fossbk-spec/ktpmud-project/issues/28)

```text
submissions/may_day_sprint_173820_n27/
├── submission.json
├── README.md
├── artifacts/
│   ├── REQUIREMENTS.md
│   ├── DECISIONS.md
│   ├── TEST_REPORT.md
│   ├── SECURITY_PRIVACY_CHECKLIST.md
│   ├── AI_USE.md
│   └── CONTRIBUTIONS.md
├── source-ref.json
└── slides/
```

Điền repo và commit starter, URL fork code, commit nộp, release tag và URL lần chạy CI thật vào `source-ref.json`. Báo cáo test có kết quả chạy từ checkout sạch và benchmark p50/p95 theo §7.3.

## Tài liệu tham chiếu

- [Decision Table](docs/decision-table.md), [Requirements](REQUIREMENTS.md), [ADR](DECISIONS.md).
- [Project Guide](docs/PROJECT_GUIDE.md), [Team Plan](docs/TEAM_PLAN.md).
- [Rule Design](docs/design/RULE_DESIGN.md), [Test Plan](docs/testing/TEST_PLAN.md), [QA Matrix](docs/qa/QA_MATRIX.xlsx) và [đối chiếu thực thi QA](docs/qa/EXECUTION_REVIEW.md).
- [Nhật ký AI đã tổng hợp trên PR #10](AI_USE.md); Leader đã đối chiếu nội dung ứng viên, còn xác nhận review cá nhân và đồng bộ vào artifact của Draft PR #39 theo SHA/tag cuối.

**Trạng thái trước Freeze (19/11):** PR #7 đã tích hợp code và pytest. [CI PR #10 trên ứng viên](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/actions/runs/44479428343) thành công trên Linux; lượt kiểm tra local đạt 490 test, ba test Windows bị skip. [Benchmark ứng viên](docs/testing/BENCHMARK_REPORT.md) lưu 1.000 mẫu full-path và công bố giới hạn `/tmp` tmpfs. QA Matrix đã được đối chiếu theo phạm vi ứng viên; các gate SHA cuối và peer review còn ghi `BLOCKED`. Hồ sơ PC-1/PC-2 trong `progress/PROGRESS.md` là ảnh chụp tại các mốc đã nộp; chỉ điền phần Freeze khi chốt SHA/tag thật. Artifact `AI_USE.md` trong PR #39 vẫn phải đồng bộ từ bản repo code.

## An toàn và giới hạn

Chỉ dùng dữ liệu giả lập, không đưa dữ liệu bệnh nhân thật hoặc thông tin định danh vào input hay audit. Không tự đặt quy tắc hoặc ngưỡng ngoài Decision Table.
