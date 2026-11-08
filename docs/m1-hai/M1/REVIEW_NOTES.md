# Ghi chú review sau Issue #15

[T15](https://github.com/fossbk-spec/ktpmud-project/issues/15#issuecomment-6722429248) là nguồn chính thức mới; [ISSUE15_SYNC](ISSUE15_SYNC.md) ghi cụ thể các phần thay Q/A Revision 02. Các source snapshot cũ giữ nguyên lịch sử.

## 1. D01–D03 đã được trả lời

R01>R02>R03 cho mã Tầng 2; Tầng 1 thắng. Tuổi thiếu/null -> THEO_DOI/null. Có tuổi/đủ phản vệ nhưng thiếu HATT hoặc nền cần thiết -> PHAN_VE/mã Tầng 2; không gán nền. Bảy ID PEND hiện có expected và clear Pending, không còn PENDING_TA_CONFIRMATION.

## 2. Các policy đã cập nhật

- Null tuổi không còn TypeError; numeric null và missing cùng không có dữ liệu.
- Null boolean không invalid và không gây exception; giữ Enum UNKNOWN như thiếu khóa trong policy nhóm, không chuyển toàn bộ unknown thành False trước khi kiểm bằng chứng.
- HYPOTENSION UNKNOWN không thể giữ final classification pending: chỉ bằng chứng TRUE mới làm thỏa sốc; có tuổi/đủ Tầng 2 thì PHAN_VE nếu chưa có bằng chứng sốc.
- Tám ca null chuyển từ invalid sang nullable/missing hợp lệ. Còn 36 invalid (28 TypeError+8 ValueError). AUD-002 dùng chuỗi để không coi null là invalid.
- Audit nullable hợp lệ là SUCCESS, không INVALID_INPUT. Audit failure/error precedence riêng vẫn giữ policy đã duyệt.

## 3. Đề xuất cần Huy review

T15 cho phép nhóm công bố policy khi kết luận thực sự phụ thuộc boolean thiếu. Giữ D13 UNKNOWN/THEO_DOI cho phần thực sự phụ thuộc; công bố rủi ro hạ mức khi thiếu dữ liệu. Riêng S xuất hiện ở cả nhánh phủ định và khẳng định: MISS-009 mọi completion phản vệ dù không rule riêng TRUE; không bỏ sót kết luận do mất tương quan.

Đề xuất BOOL-COVERAGE bảo toàn mức và chọn mã đại diện theo completion UNKNOWN=False chỉ khi mọi completion đều phản vệ nhưng mã khác nhau. MISS-009/cặp TA15-BOOL1 đánh dấu PROPOSED FOR LEADER REVIEW. Mức không được hạ; mã đại diện R01 là đề xuất nhóm, không thầy/Leader đã duyệt. [ISSUE15_SYNC §4]

## 4. Các quyết định giữ theo Requirements/ADR

Enum/toán tử, ContextVar/hai scope UUID, public orchestration, audit fields/lifecycle/fail-closed, isolation và benchmark 100 warm-up/nearest-rank giữ Q/A. Sai kiểu/miền không phải null và khóa lạ giữ D04 nhóm theo T15 §6. Không đổi clinical expressions/ngưỡng, không tự đặt cutoff mới.

Default path mechanism A §5.4.1 còn PROPOSED; unexpected internal exception còn residual review item. CON-004 đã sửa định dạng, không mutate input vẫn là đề nghị kỹ thuật chưa được phê duyệt riêng. T15 không phê duyệt thay các điểm này.

## 5. Trạng thái review và QA

Tôi đã review phần tài liệu và test case M1. Việt Đức chưa có QA Matrix; các ID INT/BENCH/TA15 được giữ để đối chiếu khi matrix có. Phần review chéo QA và phê duyệt policy BOOL-COVERAGE của Huy còn chờ. Chưa chạy test nghiệp vụ trên classifier và chưa nghiệm thu runtime.
