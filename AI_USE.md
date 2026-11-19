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

Hải tự ghi từng tác vụ AI thực tế khi làm Rule Engine, test, runner/CSV hoặc review. Nếu không dùng AI cho phần việc của mình, ghi rõ “SV2 không dùng AI cho phần việc riêng” và xác nhận. Không suy đoán tên model khi không biết. Mỗi dòng cần đủ sáu cột:

| Công cụ/model | Mục đích | Phạm vi file/module/commit | Kiểm chứng cụ thể | Giữ/sửa/loại đầu ra AI và lý do | Người review/chấp thuận |
|---|---|---|---|---|---|
| *SV2 điền sau khi tự đối chiếu; chưa có xác nhận* |  |  |  |  |  |

## SV3 — Việt Đức bổ sung hoặc xác nhận không dùng AI

Việt Đức tự ghi từng tác vụ AI thực tế khi làm QA Matrix, 175 file bằng chứng, review hoặc các phần khác đã thực hiện. Nếu không dùng AI cho phần việc của mình, ghi rõ “SV3 không dùng AI cho phần việc riêng” và xác nhận. Phân biệt phần Việt Đức thực hiện với phần Leader tiếp nhận; không ghi công cho việc chưa làm.

| Công cụ/model | Mục đích | Phạm vi file/module/commit | Kiểm chứng cụ thể | Giữ/sửa/loại đầu ra AI và lý do | Người review/chấp thuận |
|---|---|---|---|---|---|
| *SV3 điền sau khi tự đối chiếu; chưa có xác nhận* |  |  |  |  |  |

## Chốt bản nộp

Leader đối chiếu các dòng SV1–SV3 với file, commit, test và nhận xét thực tế; xóa dòng hướng dẫn/trống; cập nhật trạng thái quyết định và SHA cuối; rồi đồng bộ nội dung đã chốt sang `submissions/may_day_sprint_173820_n27/artifacts/AI_USE.md` trên cùng nhánh Draft PR #39. Không tự coi việc sửa file này là review hoặc chấp thuận của thành viên khác.
