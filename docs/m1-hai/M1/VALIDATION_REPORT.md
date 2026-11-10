# TASK 02E — Kiểm chứng tĩnh remediation

Owner: Huy Đức/AI hỗ trợ — 09/11/2026. Nhánh review/m1-02-leader-remediation, base768f196e6a9ec3b1142c44399ce8288f7cc2e87e. Đây là báo cáo static design/data checks; Leader chưa final acceptance.

## 1. Nguồn và cách kiểm

Theo [sources](sources/README.md): D+T15, Q Revision04 a574ce20fbf307ad90f0d60064da394652462aea và A Revision04 7af011f3f95e21ac829a163ee4be36200c1e7d88. Oracle scratch độc lập từ các biểu thức official +D13-E, không lấy Expected của CSV làm định nghĩa luật hoặc import runtime nhóm. Dữ liệu fixture_ref dựng bằng allowlist math và deepcopy; không eval.

Trong workspace Leader có script kiểm ở work/reviews/task-02e/verify_remediation.py (ngoài tracked project); [REMEDIATION_EVIDENCE.json](REMEDIATION_EVIDENCE.json) lưu summary và per-case static status để review. Công thức và coverage được mô tả đủ trong RULE_DESIGN/TEST_PLAN, không phụ thuộc script ngoài repo để chạy classifier. Runtime fixture factory còn là việc M2.

## 2. Những gì kiểm và điều kiện PASS

| Check | Evidence/điều kiện |
|---|---|
| CSV/JSON | 175 unique IDs; đủ header/ô; Input/Expected/Internal assertions parse strict; regex metadata compile; three fixture refs allowlisted |
| Preservation | 157 original ID/Input và mức/mã/lớp lỗi không đổi so base; chỉ metadata/assertions được tăng |
| Oracle | Independent bit-world rules/quantifiers +approved D13-E tính từng output/exception và existing internal assertions |
| Validation | 36 invalid thật=28 TypeError+8 ValueError; unrelated invalid không bị bỏ; numeric/bool strict; no coercion |
| Six cases | Current approval/source, exact expected, canonical vs mixed, meaningful explanation assertions |
| Logic | Recompute 81 rows độc lập, đủ 9/9/3/15/45; file 81 rows không đổi byte |
| Coverage | 18 added IDs có mục tiêu; 18 null/missing groups pair-equal; property enumeration729 states và representative numeric conditions |
| Evidence semantics | RULE-020 HYPOTENSION_EVIDENCE TRUE/TIER1_MATCH FALSE; MISS-009 helpers UNKNOWN/UNKNOWN/FALSE; Def thắng Poss |
| Explanation design | Safe controlled messages pass patterns; deliberately unsafe/provenance messages fail. Không claim đã kiểm actual engine reason hoặc mọi câu ngôn ngữ tự nhiên |
| Provenance/scope | Q/A4 current, source snapshots unchanged; only allowed docs/data changes; no Guide/Plan/runtime/CI/QA changes |
| Documentation | Markdown/UTF-8/relative links/index/schema-note đúng; no unsupported runtime/CI/benchmark success claims |

Kết quả kiểm tĩnh ngày 09/11/2026: 175 main cases (139 classification +36 invalid), 81 math rows, 18 equivalence groups và 30 explanation profiles (9 canonical) khớp oracle; 157 ID/input/level/ID/exception gốc được bảo toàn. Mô hình độc lập đã duyệt 729 trạng thái boolean với 18 cấu hình numeric, tổng 13.122 lượt đối chiếu mô hình; discrepancies rỗng. Chi tiết per-case trong REMEDIATION_EVIDENCE.json. PASS chỉ nghĩa các điều kiện tĩnh được kiểm đạt, không phải classifier đã chạy hoặc AC được VERIFIED.

## 3. NOT EXECUTED và review còn lại

Classifier business tests: NOT EXECUTED. Actual Enum/helper tests: NOT EXECUTED. Public audit/context/error-path/privacy tests: NOT EXECUTED. Clean-checkout pytest/PR CI: NOT EXECUTED. Full-path audit benchmark: NOT EXECUTED. Không AC nào được nâng VERIFIED.

Peer review/QA Matrix mapping và Leader acceptance chưa được xác nhận. Default path/internal exception/CON-004 ngoài approval D13 giữ đúng trạng thái riêng. Validation không cho phép AI merge hoặc tự xác nhận M1 đạt.

## 4. Lịch sử

Baseline 768f196 từng báo26/26 structural checks bằng local script không kèm repository. Đó là báo cáo của lần publish trước, không được dùng làm proof oracle hiện tại. TASK02E bổ sung kiểm độc lập và portable summary; không sửa snapshots hoặc giả rằng runtime đã chạy.
