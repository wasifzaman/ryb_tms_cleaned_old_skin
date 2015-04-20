import xlsxwriter
from datetime import datetime

def stringtime_to_decimal(string_time):
    (h, m, s) = string_time.split(':')
    return (int(h) * 3600 + int(m) * 60 + int(s)) / 3600

def exportreport(database, dest_path, sdate):
    if len(database.studentList) == 0: return

    sdates = [sdate]
    sdsplit = sdate.split('/')
    sdates.append(str(int(sdsplit[0])) + '/' + str(int(sdsplit[1])) + '/' + (sdsplit[2][2:] if len(sdsplit[2]) > 2 else sdsplit[2]))

    date = sdates[1].replace('/', '.')
    workbook = xlsxwriter.Workbook(dest_path + '/Teacher Report - ' + database.school + ' ' + date + '.xlsx')
    worksheet = workbook.add_worksheet()

    rows = []

    for student in database.studentList.values():
        for att in student.datapoints['attinfo'][1]:
            if att[0] in sdates:
                first_name = student.datapoints['firstName']
                last_name = student.datapoints['lastName']
                barcode_ = student.datapoints['bCode']
                rows.append([att[2], att[4], first_name, last_name, barcode_])

    #sorted
    row_indexed = [(att[0], att) for att in rows]
    row_indexed.sort()
    row_sorted = [index_[1] for index_ in row_indexed]

    #format
    tformat = workbook.add_format({'bold': True})
    tformat.set_bg_color('#C2FFAD')

    title_format = workbook.add_format({'bold': True})

    #to excel
    worksheet.set_column(0, 4, 14)
    worksheet.write(0, 0, 'RYB Teacher Attendance Report', title_format)
    worksheet.write(1, 0, 'Total check-ins: ' + str(len(row_sorted)), title_format)
    worksheet.write(2, 0, '日期: ' + str(sdates[0]), title_format)
    worksheet.write(4, 0, '到达时间', tformat) #check-in
    worksheet.write(4, 1, '注销时间', tformat) #check-out
    worksheet.write(4, 2, '名字', tformat) #first_name
    worksheet.write(4, 3, '姓', tformat) #last_name
    worksheet.write(4, 4, '条码号', tformat) #barcode

    r, c = 5, 0

    for row in row_sorted:
        worksheet.write(r, 0, '老师到达') #check-in
        if len(row[1]) != 0:
            worksheet.write(r, 1, '老师离开') #check-out
        worksheet.write(r, 2, row[2])
        worksheet.write(r, 3, row[3])
        worksheet.write(r, 4, row[4])
        r += 1

    return

def print_teacher_attendance(database, dest_path, start_date, end_date):
    if len(database.studentList) == 0: return

    rows = []

    for student in database.studentList.values():
        for att in student.datapoints['attinfo'][1]:
            date_ = datetime.strptime(att[0], '%m/%d/%Y')
            if date_.date() >= start_date.date() and date_.date() <= end_date.date():
                first_name = student.datapoints['firstName']
                last_name = student.datapoints['lastName']
                barcode_ = student.datapoints['bCode']
                rows.append((date_, att[2], att[4], first_name, last_name, barcode_))

    rows.sort()

    workbook = xlsxwriter.Workbook(dest_path + '/Teacher Report - ' + database.school + ' ' + \
                                    datetime.strftime(start_date, '%m.%d.%Y') + ' ' + \
                                    datetime.strftime(end_date, '%m.%d.%Y') + '.xlsx')
    worksheet = workbook.add_worksheet()

    #format
    tformat = workbook.add_format({'bold': True})
    tformat.set_bg_color('#C2FFAD')

    title_format = workbook.add_format({'bold': True})

    #to excel
    worksheet.set_column(0, 5, 13)
    worksheet.write(0, 0, 'RYB Teacher Attendance Report', title_format)
    worksheet.write(1, 0, 'Total check-ins: ' + str(len(rows)), title_format)
    worksheet.write(2, 0, 'From: ' + datetime.strftime(start_date, '%m/%d/%Y'), title_format)
    worksheet.write(3, 0, 'To: ' + datetime.strftime(end_date, '%m/%d/%Y'), title_format)
    worksheet.write(5, 0, 'Date', tformat)
    worksheet.write(5, 1, '到达时间', tformat) #check-in
    worksheet.write(5, 2, '注销时间', tformat) #check-out
    worksheet.write(5, 3, '名字', tformat) #first_name
    worksheet.write(5, 4, '姓', tformat) #last_name
    worksheet.write(5, 5, '条码号', tformat) #barcode

    r, c = 6, 0

    for row in rows:
        worksheet.write(r, 0, datetime.strftime(row[0], '%m/%d/%Y'))
        worksheet.write(r, 1, '老师到达') #check-in
        if len(row[2]) != 0:
            worksheet.write(r, 2, '老师离开') #check-out
        worksheet.write(r, 3, row[3])
        worksheet.write(r, 4, row[4])
        worksheet.write(r, 5, row[5])
        r += 1

def print_teacher_attendance_simple(database, dest_path, start_date, end_date):
    if len(database.studentList) == 0: return

    rows = []

    for student in database.studentList.values():
        for att in student.datapoints['attinfo'][1]:
            date_ = datetime.strptime(att[0], '%m/%d/%Y').date()
            if date_ >= start_date.date() and date_ <= end_date.date():
                first_name = student.datapoints['firstName']
                last_name = student.datapoints['lastName']
                barcode_ = student.datapoints['bCode']
                to_append = (first_name, last_name, barcode_)
                if to_append not in rows:
                    rows.append(to_append)

    rows.sort()

    workbook = xlsxwriter.Workbook(dest_path + '/Teacher Report - ' + database.school + ' ' + \
                                    datetime.strftime(start_date, '%m.%d.%Y') + ' ' + \
                                    datetime.strftime(end_date, '%m.%d.%Y') + '.xlsx')
    worksheet = workbook.add_worksheet()

    #format
    tformat = workbook.add_format({'bold': True})
    tformat.set_bg_color('#C2FFAD')

    title_format = workbook.add_format({'bold': True})

    #to excel
    worksheet.set_column(0, 4, 14)
    worksheet.write(0, 0, 'RYB Teacher Attendance Report (simple)', title_format)
    worksheet.write(1, 0, 'Total teachers: ' + str(len(rows)), title_format)
    worksheet.write(2, 0, 'From: ' + datetime.strftime(start_date, '%m/%d/%Y'), title_format)
    worksheet.write(3, 0, 'To: ' + datetime.strftime(end_date, '%m/%d/%Y'), title_format)
    worksheet.write(5, 0, '名字', tformat) #first_name
    worksheet.write(5, 1, '姓', tformat) #last_name
    worksheet.write(5, 2, '条码号', tformat) #barcode

    r, c = 6, 0

    for row in rows:
        worksheet.write(r, 0, row[0])
        worksheet.write(r, 1, row[1])
        worksheet.write(r, 2, row[2])
        r += 1

def print_pay_entries(database, dest_path, employee_id, pay_entries, pay_per_hour=0.00, max_hours=False):
    if len(database.studentList) == 0: return

    workbook = xlsxwriter.Workbook(dest_path + '.xlsx')
    worksheet = workbook.add_worksheet()

    info_headerformat = workbook.add_format({'bold': True, 'bg_color': '#C2FFAD', 'border': 1})
    info_headerformat.set_border_color = '#E0E0E0'

    timesheet_headerformat = workbook.add_format({'bold': True, 'bg_color': '#66FFCC', 'border': 1})
    timesheet_headerformat.set_border_color = '#E0E0E0'

    footer_format = workbook.add_format({'bold': True, 'bg_color': '#EBF5FF', 'border': 1})
    footer_format.set_border_color = '#E0E0E0'

    footer_format_2 = workbook.add_format({'bold': True, 'bg_color': '#FFAD5C', 'border': 1})
    footer_format_2.set_border_color = '#E0E0E0'

    hours_exceeded_format = workbook.add_format({'bold': True, 'bg_color': 'red', 'border': 1, 'font_color': 'yellow'})
    footer_format.set_border_color = '#E0E0E0'

    paid_alias = database.studentList[employee_id].datapoints['paid_entries']
    paid_alias = dict(list(paid_alias.items()) + list(pay_entries.items()))
    database.studentList[employee_id].datapoints['paid_entries'] = paid_alias
    database.studentList[employee_id].datapoints['last_payment'] = datetime.now().date()

    worksheet.write(0, 0, "发票号码:", info_headerformat)
    worksheet.write(0, 1, "", info_headerformat)
    worksheet.write(0, 2, "", info_headerformat)
    worksheet.write(0, 3, "今天日期", info_headerformat)
    worksheet.write(0, 4, datetime.strftime(datetime.now().date(), '%m/%d/%Y'), info_headerformat)
    
    worksheet.write(1, 0, "", info_headerformat)
    worksheet.write(1, 1, "", info_headerformat)
    worksheet.write(1, 2, "", info_headerformat)
    worksheet.write(1, 3, "", info_headerformat)
    worksheet.write(1, 4, "", info_headerformat)

    worksheet.write(2, 0, database.studentList[employee_id].datapoints['chineseName'], info_headerformat)
    worksheet.write(2, 1, database.studentList[employee_id].datapoints['firstName'], info_headerformat)
    worksheet.write(2, 2, database.studentList[employee_id].datapoints['lastName'], info_headerformat)
    worksheet.write(2, 3, "", info_headerformat)
    worksheet.write(2, 4, database.studentList[employee_id].datapoints['bCode'], info_headerformat)

    worksheet.write(3, 0, '日期', timesheet_headerformat)
    worksheet.write(3, 1, '工作开始时间', timesheet_headerformat)
    worksheet.write(3, 2, '工作结束时间', timesheet_headerformat)
    worksheet.write(3, 3, '支付小时', timesheet_headerformat)
    worksheet.write(3, 4, '工资', timesheet_headerformat)

    #column width
    worksheet.set_column(0, 0, 15)
    worksheet.set_column(1, 4, 14)

    #total hours
    total_time = 0
    total_salary = 0

    r = 4
    for entry in pay_entries.values():
        date = entry[0]
        checkin = datetime.strptime(date + ' ' + entry[2], '%m/%d/%Y %I:%M %p')
        checkout = datetime.strptime(date + ' ' + entry[4], '%m/%d/%Y %I:%M %p')
        time_clocked = checkout - checkin
        decimal_time = stringtime_to_decimal(str(time_clocked))
        total_time += decimal_time
        total_salary += float(decimal_time * pay_per_hour)
        #print()

        worksheet.write(r, 0, entry[0])
        worksheet.write(r, 1, entry[2])
        worksheet.write(r, 2, entry[4])
        worksheet.write(r, 3, str(time_clocked))
        worksheet.write(r, 4, str("%.2f" % float(decimal_time * pay_per_hour)))
        #worksheet.write(r, 4, )

        r += 1

    r += 1
    
    for row in range(r, r+8):
        for cell in range(0, 5):
            worksheet.write(row, cell, ' ', footer_format)

    school_translation = {'Flushing': '法拉盛学校',
                            'Chinatown': '唐人街学校',
                            'Brooklyn': '布鲁克林学校',
                            'Elmhurst': '艾姆赫斯特学校'}

    worksheet.write(r, 3, school_translation[database.school] + ':', footer_format)
    worksheet.write(r, 4, "%.2f" % total_salary, footer_format)
    r += 2
    worksheet.write(r, 3, "现金工资:", footer_format)
    r += 1
    worksheet.write(r, 3, "支票工资:", footer_format)
    r += 1
    worksheet.write(r, 3, "支票号码:", footer_format)
    r += 2
    worksheet.write(r, 3, "合计薪水:", footer_format)
    
    r += 3

    for row in range(r, r+2):
        for cell in range(0, 5):
            worksheet.write(row, cell, ' ', footer_format_2)

    worksheet.write(r, 3, "工资拿到日期:", footer_format_2)
    r += 1
    worksheet.write(r, 3, "老师签字:", footer_format_2)

    
    if max_hours and max_hours < total_time:
        r += 1

        for column in range(0, 5):
            worksheet.write(r, column, ' ', hours_exceeded_format)

        worksheet.write(r, 0, "Hours Exceeded:", hours_exceeded_format)
        worksheet.write(r, 1, str(total_time - max_hours), hours_exceeded_format)

    database.saveData()

    workbook.close()

    return True