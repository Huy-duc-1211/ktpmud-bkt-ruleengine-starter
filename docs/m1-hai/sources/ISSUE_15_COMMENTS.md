# Issue #15 — Snapshot bình luận đã đọc

Ngày kiểm tra: 08/11/2026. Snapshot chỉ chứa các bình luận tool trả về, không tự nhận là phản hồi TA. Danh sách đã đọc có 1 bình luận, của Huy-duc-1211; chưa thấy bình luận TA.

## Bình luận: Huy-duc-1211

Nguồn: https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6719840642

Thưa thầy/TA,

Nhóm `173820_n27` xin phép bổ sung một trường hợp liên quan đến **câu hỏi D03 về dữ liệu huyết áp** trong Issue #15.

Theo Decision Table V1, với người từ 18 tuổi trở lên đã thỏa ít nhất một rule phản vệ ở Tầng 2, điều kiện huyết áp để xác định R-SOC là:

- HATT hiện tại < 90 mmHg; **HOẶC**
- HATT hiện tại giảm > 30% so với HATT nền.

**Ví dụ sử dụng dữ liệu synthetic:**

- `tuoi = 25`.
- Tầng 2 chắc chắn thỏa R02-PV.
- `huyet_ap_tam_thu = 110`.
- `huyet_ap_tam_thu_nen = null` hoặc khóa này không được cung cấp.

Trong tình huống này, nhánh HATT < 90 không thỏa, nhưng nhóm chưa đủ dữ liệu để đánh giá nhánh giảm > 30%.

Để minh họa:

- Nếu HATT nền là 140, mức giảm là `(140-110)/140 ≈ 21,43%`, không đạt >30%.
- Nếu HATT nền là 160, mức giảm là `(160-110)/160 = 31,25%`, đạt >30%.

Hai giá trị huyết áp nền chỉ là giả định để giải thích câu hỏi; chương trình không tự suy đoán hoặc bổ sung các giá trị đó.

Nhóm xin thầy/TA xác nhận:

1. Trường hợp này nên trả `PHAN_VE` vì chưa xác nhận được R-SOC, hay `THEO_DOI` vì chưa thể đánh giá đầy đủ điều kiện sốc? Khi chọn kết quả, `rule_id` và `ly_do` cần thể hiện như thế nào?
2. Với cả HATT hiện tại và HATT nền, giá trị `null` và thiếu hẳn khóa có cần được xử lý khác nhau không ạ?
3. Nếu Decision Table chưa quy định chi tiết các trường hợp này, nhóm có được công bố chính sách xử lý nội bộ trong `REQUIREMENTS.md`/`DECISIONS.md` và kiểm thử nhất quán hay cần chờ một quy định chung ạ?

Nhóm giữ nguyên ngưỡng HATT <90 và mức giảm >30%, chưa tự chốt expected output cho D03.

Nhóm em cảm ơn thầy/TA ạ.
