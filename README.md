# KTPMUD Hack Marathon 2026 — Track A · Dr May Day

Nhóm `173820_n27` xây dựng mô-đun Python phân loại theo [Decision Table V1](docs/decision-table.md). Dự án chỉ dùng dữ liệu giả lập (synthetic).

## Trạng thái phát triển

- **M1:** Requirements, ADR, Rule Design, Test Plan, các ca thiết kế và QA Matrix đã tích hợp qua [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) ngày 10/11/2026.
- **M2:** `classify(patient)` đã chạy được. Hàm kiểm tra input, xét rule theo bảng quyết định rồi ghi audit JSONL. Bộ pytest có ca rule, ca ở ranh giới, dữ liệu thiếu và lỗi ghi audit.

## Cấu trúc repository

| Đường dẫn | Nội dung |
|---|---|
| [`rule_engine/classifier.py`](rule_engine/classifier.py) | Kiểu input/output, validation và logic phân loại |
| [`rule_engine/audit.py`](rule_engine/audit.py) | UUID phiên, đường dẫn và ghi audit JSONL |
| [`tests/`](tests/) | Kiểm thử nghiệp vụ, bảng logic, giải thích và audit |
| [`docs/m1-hai/`](docs/m1-hai/README.md) | Thiết kế rule, ca kiểm thử và kế hoạch kiểm chứng |
| [`docs/m1-qa/`](docs/m1-qa/) | QA Matrix và báo cáo audit thiết kế |
| [`.github/workflows/test.yml`](.github/workflows/test.yml) | Workflow pytest trên push và pull request |

## Cài đặt và kiểm thử

Dùng Python 3.12 như cấu hình CI. Từ thư mục gốc, tạo môi trường ảo bằng `python -m venv .venv`, rồi kích hoạt bằng `source .venv/bin/activate` trên bash hoặc `.\.venv\Scripts\Activate.ps1` trên PowerShell.

```text
python -m pip install -r requirements.txt
pytest -q
```

[`pytest.ini`](pytest.ini) áp dụng [erratum của starter](https://github.com/fossbk-spec/ktpmud-project/issues/16).

## Chạy thử với dữ liệu giả lập

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

Ví dụ trên trả `PHAN_VE / R01-PV`. Muốn chỉ định file audit, đặt `DR_MAY_DAY_AUDIT_PATH` thành đường dẫn tuyệt đối tới file JSONL ngoài repo. Nếu chưa đặt biến này, bản M2 ghi thử vào `~/.173820_n27/dr_may_day/runs/<run-id>/audit.jsonl`. Để dùng chung UUID giả lập cho nhiều lần gọi, đặt các lệnh gọi trong `with audit_session():` (import từ `rule_engine.audit`). Mỗi lần gọi ngoài phiên có UUID riêng.

Hàm ghi xong audit mới trả kết quả. Nếu input sai, hàm ghi `INVALID_INPUT` rồi báo `TypeError` hoặc `ValueError`. Nếu ghi audit thất bại, hàm báo `AuditError`. Các lần ghi vào cùng file diễn ra tuần tự.

Với INT-013, nhánh này thử ghi `INTERNAL_ERROR` khi logic phân loại gặp lỗi sau validation, rồi báo `RuntimeError` với thông báo chung. Nếu ghi bản ghi đó cũng lỗi, hàm báo `AuditError`. Bản ghi vẫn có bốn trường và không chứa input. Việt Đức và Huy Đức còn cần review cách xử lý này. [Ghi chú M2](docs/m1-hai/M2/README.md)

## Tài liệu tham chiếu

- [Decision Table](docs/decision-table.md), [Requirements](REQUIREMENTS.md), [ADR](DECISIONS.md).
- [Project Guide](docs/PROJECT_GUIDE.md), [Team Plan](docs/TEAM_PLAN.md).
- [Rule Design](docs/m1-hai/M1/RULE_DESIGN.md), [Test Plan](docs/m1-hai/M1/TEST_PLAN.md), [QA Matrix](docs/m1-qa/QA_MATRIX.xlsx).

## An toàn và giới hạn

educational/synthetic — not for clinical use

Chỉ dùng dữ liệu giả lập, không đưa dữ liệu bệnh nhân thật hoặc thông tin định danh vào input hay audit. Không tự đặt quy tắc hoặc ngưỡng ngoài Decision Table.
