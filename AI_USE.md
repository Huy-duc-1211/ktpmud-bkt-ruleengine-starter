# Nhật ký sử dụng AI — bản làm việc trước Freeze

Đây là bản nhóm cùng rà trên PR #10 của repo code. Trước khi nộp cuối, Leader đối chiếu nội dung và đồng bộ vào [`artifacts/AI_USE.md` của Draft PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39). File ở repo code không thay thế artifact trong PR nộp bài.

Theo §5.3 của [đề chính thức](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103), ghi công cụ/model và phiên bản nếu biết, tác vụ, phạm vi file/module/commit, kiểm chứng, quyết định của nhóm và mã thành viên chấp thuận. `SV1` là Huy Đức (Lead), `SV2` là Hải, `SV3` là Việt Đức; attribution chi tiết xem [hồ sơ đóng góp tại PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39). Không đưa prompt riêng tư, secret, input thật hoặc thông tin định danh vào nhật ký.

## SV1 — phần Leader đang rà

Các dòng dưới dựa trên bản chuẩn bị PC-2. Tên công cụ đã biết được ghi để đúng yêu cầu của đề; phiên bản cụ thể của từng lượt chưa đối chiếu. Phần quyết định của Leader cần kiểm tra lại với artifact cuối trước khi chuyển PR #39 sang Ready.

| Công cụ/model | Mục đích | Phạm vi | Kiểm chứng | Quyết định của nhóm và lý do | Người chịu trách nhiệm |
|---|---|---|---|---|---|
| ChatGPT; phiên bản từng lượt chưa xác minh | Giải thích đề, trao đổi yêu cầu và hỗ trợ soạn/sửa tài liệu, câu hỏi về dữ liệu thiếu. | [REQUIREMENTS.md](REQUIREMENTS.md), [DECISIONS.md](DECISIONS.md), các câu hỏi Issue #15/#31. | Đối chiếu [Decision Table](docs/decision-table.md), [Issue #15](https://github.com/fossbk-spec/ktpmud-project/issues/15) và [Issue #31](https://github.com/fossbk-spec/ktpmud-project/issues/31); Lead đọc và sửa. | Giữ các phần phù hợp nguồn, sửa cách diễn đạt và quyết định chính sách nội bộ; AI không thay cho xác nhận của thầy. | SV1; còn rà bản nộp cuối. |
| Codex; phiên bản từng lượt chưa xác minh | Rà soát/sửa tài liệu M1-02, QA và liên kết. | [PR #3](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/3), [PR #4](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/4), các commit đồng bộ tài liệu. | Đối chiếu CSV, workbook, nguồn chính thức và báo cáo kiểm tra tĩnh; giữ attribution Hải/Việt Đức cho bản gốc. | Giữ bản sửa đã đối chiếu, sửa nhãn trạng thái và đường dẫn; approval tài liệu không tự chứng minh test runtime. | SV1; còn rà bản nộp cuối. |
| ChatGPT/Codex; phiên bản từng lượt chưa xác minh | Phân tích quyết định audit, review tài liệu, hỗ trợ kiểm thử và benchmark. | [PR #6](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/6), [PR #7](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/7), [benchmark ứng viên](docs/testing/BENCHMARK_REPORT.md). | Đối chiếu source, test/CI và số đo theo từng SHA; [1.000 mẫu ứng viên](docs/testing/benchmark_4be_timings.json) có giới hạn môi trường ghi rõ. | Giữ quyết định được Leader chốt trong ADR; chỉ báo kết quả test/đo trong phạm vi đã kiểm, chưa coi là nghiệm thu trên SHA/tag Freeze. | SV1; còn rà bản nộp cuối. |
| Codex; phiên bản từng lượt chưa xác minh | Hỗ trợ tổng hợp hồ sơ PC-2 và đối chiếu tài liệu trước Freeze. | [Draft PR #39](https://github.com/fossbk-spec/ktpmud-project/pull/39), [PR #10](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/pull/10). | So template, đề, các PR nội bộ, link CI và báo cáo benchmark; Leader kiểm từng bản sửa. | Bản PC-2 được dùng làm nền; các mục còn thiếu và nguồn Freeze phải được rà lại trước khi quyết định giữ trong bản nộp cuối. | SV1; còn rà bản nộp cuối. |

## SV2 — Hải bổ sung hoặc xác nhận không dùng AI

Dùng OpenAI Codex để hỗ trợ phần Rule Engine, test, audit và runner trong phạm vi công việc đã trao đổi. Codex trực tiếp, viết và sửa code, chạy kiểm tra, soạn tài liệu theo yêu cầu và logic của tôi.

| Công cụ/model | Mục đích | Phạm vi file/module/commit | Kiểm chứng cụ thể | Giữ/sửa/loại đầu ra AI và lý do | Người review/chấp thuận |
|---|---|---|---|---|---|
| OpenAI Codex, model 6.1 Sol high | Triển khai classifier, validation, theo logic của tôi | [classifier.py](rule_engine/classifier.py). | Codex đối chiếu Decision Table, Requirements, ADR và chạy pytest với các ca thiết kế, ca biên và trạng thái nội bộ. | Giữ phần triển khai phù hợp contract. Sửa tiếp theo quyết định của nhóm về AllPV, Mixed, ưu tiên rule và lời giải thích để code khớp đặc tả hiện hành. | SV2 phụ trách kiểm tra kết quả
| OpenAI Codex, model 6.1 Sol high | Viết test classifier và bổ sung đối chứng cho lời giải thích sai. | [test_classifier.py](tests/test_classifier.py), các commit `ecb6eed`, [b6d544d](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/commit/b6d544d). | Chạy các test phân loại và test đối chứng cho Mixed tự mâu thuẫn, thiếu ý cần nêu hoặc có lời khuyên điều trị. | Giữ kiểm tra ý nghĩa và các ca đối chứng để chấp nhận câu khác chữ nhưng đủ ý, đồng thời phát hiện câu sai. | SV2 phụ trách.|
| OpenAI Codex, model 6.1 Sol high | Tái hiện và sửa lỗi audit/privacy, xử lý lỗi validator và writer. | [audit.py](rule_engine/audit.py), [classifier.py](rule_engine/classifier.py), [test_audit.py](tests/test_audit.py), các commit `69e0b8c`, [eaca642](https://github.com/Huy-duc-1211/ktpmud-bkt-ruleengine-starter/commit/eaca642). | Dùng dữ liệu synthetic và mô phỏng lỗi để kiểm tra thông báo, traceback, nội dung audit và trường hợp lỗi nội bộ xảy ra cùng lỗi ghi audit. | Sửa cách công khai lỗi để tránh lộ input. Giữ TypeError/ValueError cho input sai, ghi INTERNAL_ERROR theo quyết định nhóm và ưu tiên AuditError an toàn khi ghi audit thất bại. | SV2 phụ trách phần sửa theo trao đổi. |
| OpenAI Codex, model 6.1 Sol high | Xử lý audit ghi dở dang và truy vấn file có dòng hỏng. | [audit.py](rule_engine/audit.py), [query_audit.py](query_audit.py), [test_audit.py](tests/test_audit.py), các commit `eaca642`, `b6d544d`. | Bổ sung test dòng lỗi, khóa JSON trùng và mã thoát khi đọc một phần. | Giữ hướng kiểm soát newline khi ghi. Khi đọc, bỏ qua dòng lỗi, báo số bản ghi đọc được và số/vị trí dòng bỏ qua. Sửa mã thoát thành `3` khi có dòng bị bỏ qua để phản ánh tình trạng đọc một phần. | SV2 phụ trách logic code. |
| OpenAI Codex, model 6.1 Sol high | Sắp xếp repo theo chức năng và đồng bộ tài liệu sau PR #6. | [README.md](README.md), `docs/`, `tests/fixtures/`, các commit `6a2af32`, `bc08910`. | Codex đối chiếu đường dẫn, dữ liệu ca thử và tài liệu của Leader sau PR #6. | Giữ cấu trúc một project chung theo yêu cầu của tôi, chuyển TEST_CASES.csv về gốc repo.| SV2 phụ trách kiểm tra, chấp thuận. |

## SV3 — Việt Đức bổ sung hoặc xác nhận không dùng AI

Việt Đức tự ghi từng tác vụ AI thực tế khi làm QA Matrix, 175 file bằng chứng, review hoặc các phần khác đã thực hiện. Nếu không dùng AI cho phần việc của mình, ghi rõ “SV3 không dùng AI cho phần việc riêng” và xác nhận. Phân biệt phần Việt Đức thực hiện với phần Leader tiếp nhận; không ghi công cho việc chưa làm.

| Công cụ/model | Mục đích | Phạm vi file/module/commit | Kiểm chứng cụ thể | Giữ/sửa/loại đầu ra AI và lý do | Người review/chấp thuận |
|---|---|---|---|---|---|
| *SV3 điền sau khi tự đối chiếu; chưa có xác nhận* |  |  |  |  |  |

## Chốt bản nộp

Leader đối chiếu các dòng SV1–SV3 với file, commit, test và nhận xét thực tế; xóa dòng hướng dẫn/trống; cập nhật trạng thái quyết định và SHA cuối; rồi đồng bộ nội dung đã chốt sang `submissions/may_day_sprint_173820_n27/artifacts/AI_USE.md` trên cùng nhánh Draft PR #39. Không tự coi việc sửa file này là review hoặc chấp thuận của thành viên khác.
