##Giới thiệu 
Đây là một dự án cá nhân được viết bằng ngôn ngữ Python3.
Tên chương trình: Quản lý nhân viên
Tên Tiếng Anh: Employee Management
Dự án thể hiện một số kỹ thuật trong lập trình Python:
- Lập trình hướng đối tượng (OOP)
- Làm việc với các định dạng dữ liệu: xml, json
và các kiểu dữ liệu: dictionary, list
- Crawl dữ liệu từ flat file và website 
- Làm việc với module trong standard library của Python như:
-- urllib.request
-- xml.etree.ElementTree
-- sys

##Tổng quan chương trình

Chương trình giải quyết 2 yêu cầu chính:
- Quản lý thông tin nhân viên
- Quản lý tiền lương nhân viên

###Quản lý thông tin nhân viên
Thông tin nhân viên bao gồm:
>Mã nhân viên
Mã bộ phận
Chức vụ
Họ và tên
Lương theo ngày
Số ngày làm việc
Hệ số hiệu quả
Thưởng
Số ngày đi muộn
>

###Quản lý tiền lương nhân viên
Các thành phần tính lương nhân viên bao gồm:
>- Mức lương trả theo ngày
>- Số ngày làm việc
>- Số ngày đi muộn
>- Hệ số hiệu quả
>- Thưởng
>- Đóng bảo hiểm
>- Thuế thu nhập cá nhân
>**>>** Kết quả cho ra **Lương thực nhận** của mỗi nhân viên

##Các tính năng của chương trình
>**Menu:**
>**1.** Hiển thị danh sách nhân viên
>**2.** Hiển thị danh sách bộ phận
>**3.** Thêm nhân viên mới
>**4.** Xóa nhân viên theo ID
>**5.** Xóa bộ phận theo ID
>**6.** Hiển thị bảng lương
>**7.** Chỉnh sửa nhân viên
>**8.** Thoát

##Hướng dẫn sử dụng chương trình
Có 4 file được đóng gói với nhau:
_departments.json_: lưu trữ thông tin phòng ban
_employees.json_: lưu trữ thông tin nhân viên
_income.json_: lưu trữ thông tin lương thực nhận của nhân viên.
_main.py_: file source code chương trình

Tải tất cả 4 file về chung 1 folder rồi chạy main.py trên 1 IDE hay 1 Code editor.

*Note: Chương trình khi load thông tin sẽ lấy dữ liệu từ các file .json ở trên.
Riêng thông tin về tính thuế thu nhập và phạt đi muộn được lấy từ website.
Phạt đi muộn: https://bit.ly/3VtWiOL
Tính thuế thu nhập: https://bit.ly/3IhJM1Q 
