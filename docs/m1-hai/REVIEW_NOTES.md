# M1 — Nhận xét đối chiếu requirements và thiết kế


## 1. Các điểm khớp đã đối chiếu trong tài liệu

- Biểu thức FR-02/03/04 khớp R01/02/03 trong Decision Table V1, giữ đúng ngoặc và khóa dị nguyên nghi ngờ.
- Bốn nhóm tuổi, dấu < và >, điều kiện kết hợp phản vệ với tụt HATT khớp bảng.
- Output ba khóa và giới hạn ly_do phù hợp nguồn.
- Requirements tách rõ D13 nội bộ với D01–D03 pending; không mặc định missing=False.

Đây là đối chiếu tài liệu, không phải xác nhận chương trình chạy đúng. Khả năng tương thích của policy missing với diễn giải TA vẫn chưa được xác nhận.

## 2. Điểm phải xử lý trước khi khóa expected/triển khai liên quan

| ID | Nguồn | Nhận xét | Hướng xử lý đề xuất | Người quyết định |
|---|---|---|---|---|
| RV-01 | Q §9; I | D01–D03 chưa có kết luận TA trong comments đã đọc | Giữ 7 ca PEND; Huy theo dõi issue. Không chọn mặc định R02 hoặc PHAN_VE rồi gắn là contract chính thức | Huy / TA |
| RV-02 | Q §§3.1,9 | Đã khóa từ chối invalid nhưng chưa chốt lớp exception/API lỗi | Huy ghi ADR lớp lỗi, giá trị thông báo an toàn; Hải bổ sung assert cụ thể sau duyệt | Huy, Hải |
| RV-03 | Q §§4.2,9 | D13 là policy nội bộ; cần xác nhận cách chọn một rule chắc chắn TRUE khi rule khác UNKNOWN | Đưa các ca MISS liên quan ra review; không biến UNKNOWN thành FALSE, không thêm nhãn output | Huy, Hải |
| RV-04 | Q §9; D07–D08 | Truyền UUID phiên, chuẩn hóa status/timestamp, xử lý audit sink lỗi chưa khóa | Việt Đức đề xuất giao diện sink/context ngoài PatientInput, Huy duyệt; Hải phối hợp test | Việt Đức / Huy |
| RV-05 | Q §3; C TypedDict | Root input không phải dict chưa có policy exception cụ thể | Đề xuất ADR kiểm root mapping/dict trước field validation; chưa đưa expected exception chính xác vào ma trận | Hải / Huy |

## 3. Cập nhật quản lý tài liệu nên báo Huy

**RV-06 — Q §9 đang ghi câu hỏi D03 bổ sung “chưa được gửi”.** Khi kiểm tra Issue #15 ngày 08/11/2026, đã thấy bình luận bổ sung của Huy: https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6719840642. Vì vậy đề xuất đổi ghi nhận sang “đã gửi bổ sung, đang chờ xác nhận”. Không nhầm bình luận của Huy là phản hồi TA.

**RV-07 — bằng chứng hiện trạng.** classifier.py còn raise NotImplementedError, test mẫu đòi exception này, workflow đã khai báo push/pull_request. Các file này không chứng minh A-08/A-09 đã đạt nghiệp vụ.

## 4. Không phải lỗi requirements

- HATT thấp đơn độc không phải sốc theo contract.
- HATT bằng 90 ở người lớn vẫn có thể thỏa giảm >30% so với nền: cần kiểm cả OR.
- Ngưỡng 91.98 ở tuổi 10.99 không cho phép truyền HATT float trái kiểu dữ liệu.
- Khi b<90 ở người lớn, thiếu nền không cản xác nhận sốc nếu Tầng 2 đã TRUE.
- THEO_DOI không khẳng định an toàn; UNKNOWN không phải nhãn output mới.

## 5. Reviewer

| Reviewer | Phạm vi | Nhận xét / quyết định | Ngày / link bằng chứng |
|---|---|---|---|
| Huy | Biểu thức, expected, pending, ADR | Chưa xác nhận | Chưa có |
| Việt Đức | AC, QA, audit và evidence gaps | Chưa xác nhận | Chưa có |
