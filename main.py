import xml.etree.ElementTree as ET
import urllib.request
import json
import sys

#1. Tạo các class cần thiết
class Employees:
    def __init__(self, employee_id, employee_name, employee_position, employee_bonus, department_id, salary_base, 
    working_days, working_performance, late_coming_days):
        self.employee_id = employee_id                  # Mã nhân viên
        self.employee_name = employee_name              # Họ tên nhân viên
        self.employee_position = employee_position      # Chức vụ (NV/QL)
        self.employee_bonus = employee_bonus            # Thưởng nhân viên
        self.department_id = department_id              # Mã bộ phận
        self.salary_base = salary_base                  # Lương theo ngày cơ bản
        self.working_days = working_days                # Số ngày làm việc
        self.working_performance = working_performance  # Hệ số hiệu quả
        self.late_coming_days = late_coming_days        # Số ngày đi muộn

class Manager(Employees):
    def __init__(self, employee_id, employee_name, employee_position, employee_bonus, department_id, salary_base, 
    working_days, working_performance, late_coming_days):
        super().__init__(employee_id, employee_name, employee_position, employee_bonus, department_id, salary_base, 
        working_days, working_performance, late_coming_days)

class Departments:
    def __init__(self, department_id, department_bonus):
        self.department_id = department_id              # Mã bộ phận
        self.department_bonus = department_bonus        # Thưởng bộ phận

# Global Variable
employee_id = ''
employee_name = ''
employee_position = ''
employee_bonus = int()
department_id = ''
salary_base = int()
working_days = int()
working_performance = float() #hệ số hiệu quả
late_coming_days = int()
department_bonus = int()

employee_info = Employees(employee_id, employee_name, employee_position, employee_bonus, department_id, salary_base, 
    working_days, working_performance, late_coming_days)

department_info = Departments(department_id, department_bonus)

# Đọc các file dữ liệu
EMPLOYEE_FILE = 'employees.json'
DEPARTMENT_FILE = 'departments.json'
INCOME_FILE = 'income.json'

    # Hàm đọc file employees.json
def Employees_Read():
    with open(EMPLOYEE_FILE, encoding="utf-8") as f:
        return json.load(f)

    # Hàm đọc file departments.json
def Departments_Read():
    with open(DEPARTMENT_FILE, encoding="utf-8") as f:
        return json.load(f)

    # Hàm đọc file income.json
def Income_Read():
    with open(INCOME_FILE, encoding="utf-8") as f:
        return json.load(f)

employees_file = Employees_Read()
departments_file = Departments_Read()
income_file = Income_Read()


#2. Viết hàm để trích xuất dữ liệu

    #2.1. Lấy dữ liệu phạt đi muộn
def PunishLateComing():
    url_late_coming = urllib.request.urlopen('https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Flate_coming.json?alt=media&token=55246ee9-44fa-4642-aca2-dde101d705de').read()
    late_coming = json.loads(url_late_coming)

    min_late_list = []
    max_late_list = []
    value_late_list = []

    for i in late_coming:
        try:
            max_late_list.append(i['max'])
        except KeyError:
            continue
    for i in late_coming:
        min_late_list.append(i['min'])
        value_late_list.append(i['value'])
    
    # Từ số ngày đi muộn tính Số tiền phạt đi muộn
    if min_late_list[0] < int(employee_info.late_coming_days) < max_late_list[0]:           # từ 1-3 buổi phạt 20k/buổi
        punish_late_coming = value_late_list[0] * int(employee_info.late_coming_days)
    elif min_late_list[1] <= int(employee_info.late_coming_days) < max_late_list[1]:        # từ 3-6 buổi phạt 30k/buổi
        punish_late_coming = value_late_list[1] * int(employee_info.late_coming_days)
    else:
        punish_late_coming = value_late_list[2] * int(employee_info.late_coming_days)       # từ 6 buổi trở lên phạt 50k/buổi
    return punish_late_coming

    #2.2. Lấy dữ liệu thuế thu nhập
def IncomeTaxData():
    url_tax = urllib.request.urlopen('https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Ftax.xml?alt=media&token=f7a6f73d-9e6d-4807-bb14-efc6875442c7')
    tax = ET.parse(url_tax)
    tax_root = tax.getroot()

    min_tax = []
    max_tax = []
    values_tax = []

    for i in tax_root.findall('tax'):
        try:
            max_salary = int(i.find('max').text) * 1000000      # Chuyển thành đơn vị lương hàng triệu
            for k in [max_salary]:
                max_tax.append(k)
        except AttributeError:
            continue
    for i in tax_root.findall('tax'):
        min_salary = int(i.find('min').text) * 1000000          # Chuyển thành đơn vị lương hàng triệu    
        for k in [min_salary]:
            min_tax.append(k)
        tax_value = (int(i.find('value').text) / 100)           # Chuyển số nguyên thành % tính thuế
        for k in [tax_value]:
            values_tax.append(k)
    return sorted(set(min_tax)), max_tax, values_tax


#3. Viết hàm tính lương nhân viên

    #3.1. Tính thu nhập trước thuế (income_before_tax)
def IncomeBeforeTax():
    dep_bonus = 0

    for i in departments_file:
        if employee_info.department_id == i['department_id']:
            dep_bonus += i['department_bonus']

        # tổng thu nhập chưa thưởng = (salary_base * working_days) * working_performance
    income_before_bonus = (int(employee_info.salary_base) * int(employee_info.working_days)) * float(employee_info.working_performance)

        # tổng thu nhập  = tổng thu nhập chưa thưởng + bonus + thưởng bộ phận - phạt đi muộn
    if employee_info.employee_position == 'QL':
        total_income = (income_before_bonus + int(employee_info.employee_bonus) + dep_bonus + (dep_bonus * 0.1)) - PunishLateComing()
    else:
        total_income = (income_before_bonus + int(employee_info.employee_bonus) + dep_bonus) - PunishLateComing()

        # Nhân viên sẽ cần trích ra 10.5% thu nhập để đóng bảo hiểm:
    income_before_tax = total_income * 0.895     
    return income_before_tax

    #3.2. Thuế thu nhập phải nộp (income_tax)
def IncomeTax():

    # income_before_tax = IncomeBeforeTax()
    income_tax = 0
    income_tax_lst = IncomeTaxData()
    min_tax = [i for i in income_tax_lst[0]]
    max_tax = [i for i in income_tax_lst[1]]
    values_tax = [i for i in income_tax_lst[2]]
    # for i in IncomeBeforeTax():
    if min_tax[0] <= IncomeBeforeTax() < max_tax[0]:            # từ 0 - dưới 5 triệu nộp 5% thuế
        income_tax = values_tax[0] * IncomeBeforeTax()
    elif min_tax[1] <= IncomeBeforeTax() < max_tax[1]:          # từ 5 - dưới 10 triệu nộp 10% thuế
        income_tax = values_tax[1] * IncomeBeforeTax()
    elif min_tax[2] <= IncomeBeforeTax() < max_tax[2]:          # từ 10 - dưới 18 triệu nộp 15% thuế
        income_tax = values_tax[2] * IncomeBeforeTax()
    elif min_tax[3] <= IncomeBeforeTax() < max_tax[3]:          # từ 18 - dưới 32 triệu nộp 20% thuế
        income_tax = values_tax[3] * IncomeBeforeTax()
    elif min_tax[4] <= IncomeBeforeTax() < max_tax[4]:          # từ 32 - dưới 52 triệu nộp 25% thuế
        income_tax = values_tax[4] * IncomeBeforeTax()
    elif min_tax[5] <= IncomeBeforeTax() < max_tax[5]:          # từ 52 - dưới 80 triệu nộp 30% thuế
        income_tax = values_tax[5] * IncomeBeforeTax()
    elif min_tax[6] <= IncomeBeforeTax():                       # từ 80 triệu nộp 35% thuế
        income_tax = values_tax[6] * IncomeBeforeTax()
    return income_tax

    #3.3. Tính thu nhập sau thuế (Lương nhân viên thực nhận)
def IncomeAfterTax():  
    income_after_tax = IncomeBeforeTax() - IncomeTax()
    return int(income_after_tax)


#4. Lưu dữ liệu nhân viên xuống file
def Employees_Save(employees, departments, income):
    # Lưu thông tin nhân viên
    with open(EMPLOYEE_FILE, 'w', encoding="utf-8") as emp_save_f:
        json.dump(employees, emp_save_f, ensure_ascii=False, indent=4)

    # Lưu thông tin bộ phận
    with open(DEPARTMENT_FILE, 'w', encoding='utf-8') as dep_save_f:
        json.dump(departments, dep_save_f, ensure_ascii=False, indent=4)   

    # Lưu thông tin thu nhập
    with open(INCOME_FILE, 'w', encoding='utf-8') as income_save_f:
        json.dump(income, income_save_f, ensure_ascii=False, indent=4)


#5. Tạo menu khởi động chương trình

    # Menu hiển thị lựa chọn
MENU_SHOW = """Nhập số tương ứng
1. Hiển thị danh sách nhân viên
2. Hiển thị danh sách bộ phận
3. Thêm nhân viên mới
4. Xóa nhân viên theo ID
5. Xóa bộ phận theo ID
6. Hiển thị bảng lương
7. Chỉnh sửa nhân viên
8. Thoát
Lựa chọn của bạn: """

    # Kiểm tra file tồn tại hay chưa nếu tồn tại rồi thì không tạo chưa tồn tại thì tạo
def init():
    try:
        with open(EMPLOYEE_FILE, 'x') as f:
            json.dump([], f, ensure_ascii=False)
        with open(DEPARTMENT_FILE, 'x') as f:
            json.dump([], f, ensure_ascii=False)
        with open(INCOME_FILE, 'x') as f:
            json.dump([], f, ensure_ascii=False)
    except FileExistsError:
        pass
    
    # Tạo Menu
def Menu():
    init()
    OPERATIONS = [0, Show_Employees_List, Show_Departments_List, Add_New_Employee, 
    Remove_Employee, Remove_Department, Show_Salary, Modify_Employee, Quit]

    while True:
        selection = int(input(MENU_SHOW).strip())
        if selection in range(len(OPERATIONS)):
            OPERATIONS[selection]()
        else:
            print("Sự lựa chọn không hợp lệ")

    #5.1. Hàm hiển thị danh sách nhân viên
def Show_Employees_List():
    print('====== Thông tin nhân viên ======')
    for i in employees_file:
        print(f"Mã nhân viên: {i['employee_id']}")
        print(f"Mã bộ phận: {i['department_id']}")
        print(f"Chức vụ: {i['position']}")
        print(f"Họ và tên: {i['name']}")
        print(f"Lương theo ngày: {format(i['salary'], ',')}/ngày")
        print(f"Số ngày làm việc: {i['working_day']}")
        print(f"Hệ số hiệu quả: {i['working_perform']}")
        print(f"Thưởng: {format(i['bonus'],',')}")
        print(f"Số ngày đi muộn: {i['late_day']}")
        print('===================================')

    #5.2. Hàm hiển thị danh sách bộ phận
def Show_Departments_List():

    if departments_file:
        """
        departments_lst: list of dicts
        department:
            dep_id: string
            dep_bonus: string
        """
        formatter = """------ BỘ PHẬN {} -------
Mã bộ phận: {}
Thưởng bộ phận: {}
-------------------------"""
        for counter, dep_dict in enumerate(departments_file, start=1):
            dep_id, dep_bonus = dep_dict.values()
            print(formatter.format(counter, dep_id, format(int(dep_bonus),',')))
    else:
        print("Danh sách bộ phận trống")

    #5.3. Hàm thêm nhân viên mới
def Add_New_Employee():

        #Nhập mã nhân viên
    emp_ids = [i["employee_id"] for i in employees_file]
    employee_info.employee_id = input('Nhập mã nhân viên: ').upper()
    emp1 = (len(employee_info.employee_id) == 0)    # ĐK ko bỏ trống 
    emp2 = employee_info.employee_id in emp_ids     # ĐK ko trùng mã nhân viên
    while emp1 or emp2:
        if emp1:
            print('Bạn không được bỏ trống thông tin này')
            employee_info.employee_id = input('Nhập mã nhân viên: ').upper()
        emp1 = (len(employee_info.employee_id) == 0)    # ĐK ko bỏ trống 
        emp2 = employee_info.employee_id in emp_ids     # ĐK ko trùng mã nhân viên 
        if emp2:
            print('Mã nhân viên đã tồn tại')
            employee_info.employee_id = input('Nhập mã nhân viên: ').upper()
        emp1 = (len(employee_info.employee_id) == 0)    # ĐK ko bỏ trống 
        emp2 = employee_info.employee_id in emp_ids     # ĐK ko trùng mã nhân viên               

        #Nhập mã bộ phận
    dep_ids = [dep["department_id"] for dep in departments_file]
    employee_info.department_id = input('Nhập mã bộ phận: ').upper()
    dep1 = (len(employee_info.department_id) == 0)
    dep2 = employee_info.department_id not in dep_ids
    while dep1 or dep2:
        if dep1:
            print('Bạn không được bỏ trống thông tin này')
            employee_info.department_id = input('Nhập mã bộ phận: ').upper()
            dep1 = (len(employee_info.department_id) == 0)
        if dep2:
            print('Mã bộ phận chưa tồn tại, tạo mới....')    
            dep_bonus = input('Nhập thưởng bộ phận: ')    
            dep_bonus1 = (len(dep_bonus) == 0)
            while dep_bonus1:
                if dep_bonus1:
                    print('Bạn không được bỏ trống thông tin này')
                    dep_bonus = input('Nhập thưởng bộ phận: ')
                dep_bonus1 = (len(dep_bonus) == 0)
                try:
                    dep_bonus2 = ((int(dep_bonus)+0 < 0))
                    while dep_bonus2:
                        if dep_bonus2:
                            print('Bạn phải nhập một số dương')
                            dep_bonus = input('Nhập thưởng bộ phận: ')
                        dep_bonus2 = ((int(dep_bonus)+0 < 0))
                except ValueError:
                    continue
            print('Đã tạo bộ phận mới')
            break

        #Nhập chức vụ
    employee_info.employee_position = input('Nhập chức vụ (NV / QL): ').upper()
    pos1 = (len(employee_info.employee_position) == 0)     
    while pos1:
        if pos1:
            print('Bạn không được bỏ trống thông tin này')
        employee_info.employee_position = input('Nhập chức vụ (NV / QL): ').upper()
        pos1 = (len(employee_info.employee_position) == 0)

        #Nhập họ tên
    employee_info.employee_name = input('Nhập họ tên nhân viên: ')
    name1 = (len(employee_info.employee_name) == 0)         
    while name1:
        if name1:
            print('Bạn không được bỏ trống thông tin này')
            employee_info.employee_name = input('Nhập họ tên nhân viên: ')
        name1 = (len(employee_info.employee_name) == 0)

        #Nhập lương theo ngày
    employee_info.salary_base = input('Nhập lương cơ bản: ')
    salary1 = (len(str(employee_info.salary_base)) == 0)
    while salary1:
        if salary1:
            print('Bạn không được bỏ trống thông tin này')
            employee_info.salary_base = input('Nhập lương cơ bản: ')
        salary1 = (len(str(employee_info.salary_base)) == 0)
        try:
            salary2 = ((int(employee_info.salary_base) + 0) < 0)    # ĐK nhập số dương
            while salary2:
                if salary2:
                    print('Bạn phải nhập một số dương')
                    employee_info.salary_base = input('Nhập lương cơ bản: ')
                salary2 = ((int(employee_info.salary_base) + 0) < 0)
        except ValueError:
            continue

        #Nhập số ngày làm việc
    employee_info.working_days = int(input('Nhập số ngày làm việc: '))
    working_day1 = (len(str(employee_info.working_days)) == 0)
    while working_day1:
        if working_day1:
            print('Bạn không được bỏ trống thông tin này')
        employee_info.working_days = int(input('Nhập số ngày làm việc: '))
        working_day1 = (len(str(employee_info.working_days)) == 0)
        try:
            working_day2 = ((employee_info.working_days+0) < 0)
            while working_day2:
                if working_day2:
                    print('Bạn phải nhập một số dương')
                employee_info.working_days = int(input('Nhập số ngày làm việc: '))
                working_day2 = ((employee_info.working_days)+0 < 0)
        except ValueError:
            continue

        # Nhập hệ số hiệu quả
    employee_info.working_performance = float(input('Nhập hệ số hiệu quả: '))
    working_performance1 = (len(str(employee_info.working_performance)) == 0)
    while working_performance1:
        if working_performance1:
            print('Bạn không được bỏ trống thông tin này')
        employee_info.working_performance = float(input('Nhập hệ số hiệu quả: '))
        working_performance1 = (len(str(employee_info.working_performance)) == 0)
        try:
            working_performance2 = ((employee_info.working_performance+0) < 0)
            while working_performance2:
                if working_performance2:
                    print('Bạn phải nhập một số dương')
                    employee_info.working_performance = float(input('Nhập hệ số hiệu quả: '))
                working_performance2 = ((employee_info.working_performance+0) < 0)
        except ValueError:
            continue

        # Nhập thưởng
    employee_info.employee_bonus = int(input('Nhập thưởng: '))
    bonus1 = (len(str(employee_info.employee_bonus)) == 0)
    while bonus1:
        if bonus1:
            print('Bạn không được bỏ trống thông tin này')
        employee_info.employee_bonus = int(input('Nhập thưởng: '))
        bonus1 = (len(str(employee_info.employee_bonus)) == 0)
        try:
            bonus2 = ((employee_info.employee_bonus+0) < 0)
            while bonus2:
                if bonus2:
                    print('Bạn phải nhập một số dương')
                employee_info.employee_bonus = int(input('Nhập thưởng: '))
                bonus2 = ((employee_info.employee_bonus+0) < 0)
        except ValueError:
            continue  

        # Nhập số ngày đi muộn
    employee_info.late_coming_days = int(input('Nhập số ngày đi muộn: '))
    late_day1 = (len(str(employee_info.late_coming_days)) == 0)
    while late_day1:
        if late_day1:
            print('Bạn không được bỏ trống thông tin này')
        employee_info.late_coming_days = int(input('Nhập số ngày đi muộn: '))
        late_day1 = (len(str(employee_info.late_coming_days)) == 0)
        try:
            late_day2 = ((employee_info.late_coming_days+0) < 0)
            while late_day2:
                if late_day2:
                    print('Bạn phải nhập một số dương')
                employee_info.late_coming_days = int(input('Nhập số ngày đi muộn: '))
                late_day2 = ((employee_info.late_coming_days+0) < 0)
        except ValueError:
            continue

    employees_file.append({
        "employee_id": employee_info.employee_id,
        "department_id": employee_info.department_id,
        "position": employee_info.employee_position,
        "name": employee_info.employee_name,
        "salary": int(employee_info.salary_base),
        "working_day": employee_info.working_days,
        'working_perform': employee_info.working_performance,
        'bonus': int(employee_info.employee_bonus),
        'late_day': employee_info.late_coming_days
    })
    try: 
        departments_file.append({
            "department_id": employee_info.department_id,
            "department_bonus": dep_bonus
        })
    except UnboundLocalError:
        pass

    income_file.append({
            "employee_id": employee_info.employee_id,
            "income_after_tax": IncomeAfterTax()
        })

    # Lưu dữ liệu vừa nhập vào các file: employees.json; departments.json; income.json
    Employees_Save(employees_file, departments_file, income_file)    

    #5.4. Xóa nhân viên theo ID
def Remove_Employee():
    del_emp_id = str(input('Nhập mã nhân viên muốn xóa: ')).upper()
    emp_id_lst = [i['employee_id'] for i in employees_file]
    
    if len(del_emp_id) == 0:
        print('Bạn không được bỏ trống thông tin này')
    elif del_emp_id not in emp_id_lst:
        print('Mã nhân viên không tồn tại')
    elif del_emp_id in emp_id_lst:             # Loại trừ nhân viên và lưu dữ liệu mới vào file employees.json và income.json
        new_employees_data = [i for i in employees_file if i['employee_id'] not in del_emp_id]
        new_income_data = [i for i in income_file if i['employee_id'] not in del_emp_id]
        Employees_Save(new_employees_data, Departments_Read(), new_income_data)
        print('Đã xóa nhân viên thành công!')

    #5.5. Xóa bộ phận theo ID
def Remove_Department():
    del_dep_id = str(input('Nhập mã bộ phận muốn xóa: ')).upper()
    dep_id_lst = [i['department_id'] for i in employees_file]     # Danh sách các bộ phận có trong file employees.json
    dep_lst = [i['department_id'] for i in departments_file]      # Danh sách các bộ phận có trong file departments.json
    if len(del_dep_id) == 0:
        print('Bạn không được bỏ trống thông tin này')
    elif del_dep_id in dep_id_lst:                                # Nếu bộ phận có trong file employees.json => "Ko thể xóa bộ phận"
        print('Bạn không thể xóa bộ phận đang có nhân viên')
    elif del_dep_id not in dep_id_lst:                            # Nếu bộ phận ko có trong file employees.json
        if del_dep_id not in dep_lst:                               # Nếu bộ phận ko có trong file departments.json => "Bộ phận ko tồn tại"
            print('Bộ phận không tồn tại')
        else:                                                       # Nếu bộ phận có trong file departments.json => Loại trừ bộ phận và lưu dữ liệu mới
            new_departments_data = [i for i in departments_file if i['department_id'] not in del_dep_id]    
            Employees_Save(Employees_Read(), new_departments_data)                                          
            print('Đã xóa bộ phận thành công!')

    #5.6. Hiển thị bảng lương
def Show_Salary():
    if income_file:
        """
        income_lst: list of dicts
        income:
            emp_id: string
            income_after_tax: string
        """
        formatter = """------ BẢNG LƯƠNG NHÂN VIÊN {} -------
Mã nhân viên: {}
Thu nhập thực nhận: {}
-------------------------"""
        for counter, income_dict in enumerate(income_file, start=1):
            emp_id, income_after_tax = income_dict.values()
            print(formatter.format(counter, emp_id, format(int(income_after_tax),',')))
    else:
        print("Danh sách bảng lương trống")

    #5.7. Chỉnh sửa nhân viên
def Modify_Employee():
    employee_info.employee_id = input('Nhập mã nhân viên: ').upper()
    for emp_data in employees_file:
        if emp_data['employee_id'] == employee_info.employee_id:
            print('Nhập thông tin cần chỉnh sửa')

            # Nhập chức vụ
            employee_info.employee_position = input('Nhập chức vụ (NV / QL): ').upper()
            if len(employee_info.employee_position) == 0:
                employee_info.employee_position = emp_data['position']

            # Nhập họ tên nhân viên
            employee_info.employee_name = input('Nhập họ tên nhân viên: ')
            if len(employee_info.employee_name) == 0:
                employee_info.employee_name = emp_data['name']

            # Nhập lương cơ bản
            employee_info.salary_base = input('Nhập lương cơ bản: ')
            while True:
                if (len(employee_info.salary_base) == 0):
                    employee_info.salary_base = emp_data['salary']
                elif int(employee_info.salary_base) < 0:
                    print('Bạn cần nhập đúng định dạng')
                    employee_info.salary_base = input('Nhập lương cơ bản: ')
                break
                
            # Nhập số ngày làm việc
            employee_info.working_days = input('Nhập số ngày làm việc: ')
            while True:
                if (len(employee_info.working_days) == 0):
                    employee_info.working_days = emp_data['working_day']
                elif int(employee_info.working_days) < 0:
                    print('Bạn cần nhập đúng định dạng')
                    employee_info.working_days = input('Nhập số ngày làm việc: ')
                break

            # Nhập hệ số hiệu quả
            employee_info.working_performance = input('Nhập hệ số hiệu quả: ')
            while True:
                if (len(employee_info.working_performance) == 0):
                    employee_info.working_performance = emp_data['working_perform']
                elif float(employee_info.working_performance) < 0:
                        print('Bạn cần nhập đúng định dạng')
                        employee_info.working_performance = input('Nhập hệ số hiệu quả: ')
                break

            # Nhập thưởng
            employee_info.employee_bonus = input('Nhập thưởng: ')
            while True:
                if len(employee_info.employee_bonus) == 0:
                    employee_info.employee_bonus = emp_data['bonus']
                elif int(employee_info.employee_bonus) < 0:
                    print('Bạn cần nhập đúng định dạng')
                    employee_info.employee_bonus = input('Nhập thưởng: ')
                break

            # Nhập số ngày đi muộn
            employee_info.late_coming_days = input('Nhập số ngày đi muộn: ')
            while True:
                if len(employee_info.late_coming_days) == 0:
                    employee_info.late_coming_days = emp_data['late_day']
                elif int(employee_info.late_coming_days) < 0:
                        print('Bạn cần nhập đúng định dạng')
                        employee_info.late_coming_days = input('Nhập số ngày đi muộn: ')
                break

            # Cập nhật thông tin vừa nhập vào file employees.json
            emp_data.update({
                "position": employee_info.employee_position,
                "name": employee_info.employee_name,
                "salary": int(employee_info.salary_base),
                "working_day": employee_info.working_days,
                'working_perform': employee_info.working_performance,
                'bonus': int(employee_info.employee_bonus),
                'late_day': employee_info.late_coming_days
                })
                
            # Show update
            print('====== Thông tin mới cập nhật ======')
            print(f"Mã nhân viên: {emp_data['employee_id']}")
            print(f"Chức vụ: {emp_data['position']}")
            print(f"Họ và tên: {emp_data['name']}")
            print(f"Lương theo ngày: {format(emp_data['salary'],',')}/ngày")
            print(f"Số ngày làm việc: {emp_data['working_day']}")
            print(f"Hệ số hiệu quả: {emp_data['working_perform']}")
            print(f"Thưởng: {format(emp_data['bonus'],',')}")
            print(f"Số ngày đi muộn: {emp_data['late_day']}")
            print('===================================')
            # Cập nhật thông tin vừa nhập vào file income.json
            income_data = [k for k in income_file if k['employee_id'] == employee_info.employee_id]
            income_data[0].update({
                    "income_after_tax": IncomeAfterTax()
                    })    

            # Lưu thông tin vừa cập nhật
            Employees_Save(employees_file, Departments_Read(), income_file)
        else:
            print('Mã nhân viên ko tồn tại')
        break
        
    #5.8. Thoát
def Quit():
    sys.exit(0)


Menu()

