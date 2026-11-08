# Fixture NaN/Infinity — khai báo an toàn cho M2

Nguồn Q §3.1; A §5.1. INV-005/006/007 expected **ValueError vì tuổi không hữu hạn**, không phải TypeError. Mapping public áp dụng khi audit INVALID_INPUT thành công; lỗi kép theo OPEN-03.

| Test ID / fixture ID | Fixture encoding | Input cell |
|---|---|---|
| INV-005 | fixture_ref | {"fixture_ref":"INV-005"} |
| INV-006 | fixture_ref | {"fixture_ref":"INV-006"} |
| INV-007 | fixture_ref | {"fixture_ref":"INV-007"} |

Input ba ca trên là **descriptor của test harness**, không phải PatientInput để truyền trực tiếp vào classifier. 154 ca khác có Fixture encoding=json; giữ đúng kiểu và khóa thiếu trong ô Input.

Registry [fixtures/NONFINITE_INPUTS.json](fixtures/NONFINITE_INPUTS.json) có schema_version=1, base_patient synthetic đầy đủ và ba fixture chỉ override tuoi bằng token NAN/POSITIVE_INFINITY/NEGATIVE_INFINITY. Không chứa biểu thức Python, NaN không chuẩn JSON hoặc đường dẫn module/code.

## Hợp đồng dựng fixture ở pytest M2

1. csv.DictReader với utf-8-sig; json.loads từ chối duplicate keys và constants JSON không chuẩn.
2. Encoding=json: dùng JSON input, không ép kiểu/fill khóa thiếu.
3. Encoding=fixture_ref: descriptor chỉ có fixture_ref; Fixture ID tồn tại và trùng Test ID gốc, ví dụ INV-005. Từ chối schema/field/token ngoài allowlist.
4. Deep-copy base_patient; override đúng tuoi theo mapping hằng thư viện chuẩn dưới đây; không mutate registry giữa tests.
5. Assert kiểu float và tính chất toán học trước khi đưa vào validator/classify.

| Token | Hằng dựng trong pytest M2 | Assertion trước gọi |
|---|---|---|
| NAN | math.nan | math.isnan(value) |
| POSITIVE_INFINITY | math.inf | math.isinf(value) và value >0 |
| NEGATIVE_INFINITY | -math.inf | math.isinf(value) và value <0 |

Mapping là allowlist cố định, không diễn giải chuỗi thành chương trình. Không eval/exec, ast.literal_eval, dynamic import hoặc import runner bên ngoài repo. Không so NaN bằng == vì NaN != NaN.

Ở M1, tôi mới chuẩn bị dữ liệu và quy ước dựng fixture, chưa thêm loader hoặc pytest runtime. M2 triển khai fixture factory nhỏ trong suite repo theo hợp đồng trên; dữ liệu và cách dựng đã có trong repo, không phụ thuộc CSV_Test_Runner ngoài repo. Kiểm tra cấu trúc registry hiện tại không chứng minh runtime validation đã đạt.
