# KTPMUD Hack Marathon 2026 — Track A · Dr May Day

Nhóm `173820_n27` xây dựng mô-đun Python phân loại theo [Decision Table V1](docs/decision-table.md). Dự án chỉ dùng dữ liệu giả lập (synthetic).

## Trạng thái phát triển

- **M1:** Requirements, ADR, Rule Design, Test Plan, các ca thiết kế và QA Matrix đã tích hợp qua [PR #1](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/1), [PR #2](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/2), [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4) ngày 10/11/2026.
- **M2:** `classify(patient)` vẫn raise `NotImplementedError`. Test hiện có kiểm tra stub. Chưa có bằng chứng pytest hoặc CI chạy đạt với bộ test nghiệp vụ, và chưa có kết quả benchmark.

## Cấu trúc repository

| Đường dẫn | Nội dung |
|---|---|
| [`rule_engine/classifier.py`](rule_engine/classifier.py) | Kiểu input/output và hàm khung `classify()` |
| [`tests/test_classifier.py`](tests/test_classifier.py) | Test minh họa của starter |
| [`docs/m1-hai/`](docs/m1-hai/README.md) | Thiết kế rule, ca kiểm thử và kế hoạch kiểm chứng |
| [`docs/m1-qa/`](docs/m1-qa/) | QA Matrix và báo cáo audit thiết kế |
| [`.github/workflows/test.yml`](.github/workflows/test.yml) | Workflow pytest trên push và pull request |

## Cài đặt và kiểm thử

Dùng Python 3.12 như cấu hình CI. Từ thư mục gốc, tạo môi trường ảo bằng `python -m venv .venv`, rồi kích hoạt bằng `source .venv/bin/activate` trên bash hoặc `.\.venv\Scripts\Activate.ps1` trên PowerShell.

```text
python -m pip install -r requirements.txt
pytest -q
```

[`pytest.ini`](pytest.ini) áp dụng [erratum của starter](https://github.com/fossbk-spec/ktpmud-project/issues/16). Kết quả test hiện tại chỉ phản ánh hành vi starter.

## Phạm vi chức năng

Kế hoạch gồm phân loại theo rule, validation input, kết quả có giải thích và audit trail bốn trường. Nhóm sẽ chuyển các ca thiết kế thành test tự động, kiểm tra trên CI và đo benchmark toàn luồng.

## Tài liệu tham chiếu

- [Decision Table](docs/decision-table.md), [Requirements](REQUIREMENTS.md), [ADR](DECISIONS.md).
- [Project Guide](docs/PROJECT_GUIDE.md), [Team Plan](docs/TEAM_PLAN.md).
- [Rule Design](docs/m1-hai/M1/RULE_DESIGN.md), [Test Plan](docs/m1-hai/M1/TEST_PLAN.md), [QA Matrix](docs/m1-qa/QA_MATRIX_M1_CODEX_FINAL_CANDIDATE.xlsx).

## An toàn và giới hạn

educational/synthetic — not for clinical use

Chỉ dùng dữ liệu giả lập, không đưa dữ liệu bệnh nhân thật hoặc thông tin định danh vào input hay audit. Không tự đặt quy tắc hoặc ngưỡng ngoài Decision Table.
