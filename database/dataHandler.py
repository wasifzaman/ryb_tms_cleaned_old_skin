import os
from datetime import datetime, time, timedelta
from Crypto.Cipher import AES
import configparser
import pickle
import xlrd
import shutil

import keeper
from student import StudentInfo

class StudentDB:

    def __init__(self, **kwargs):
        self.file = kwargs['file']
        self.pwfile = kwargs['pwfile']
        self.iv = b't\xd4\xbc\xee~\xa2\xc2\xc1\x14T\x91\xcfd\x95/\xfc'

        self.cell_format = {0: lambda y: y, 1: lambda y: str(y), 2: lambda y: int(y), 3: lambda y: (datetime.strptime('1/1/1900', "%m/%d/%Y") + timedelta(days=y-2)).strftime("%m/%d/%Y")}
        self.studentList = {}
        self.school = 'Flushing'
    
        if os.path.isfile(self.pwfile) and os.path.isfile(self.file):
            self.key = open(self.pwfile, 'rb').read()
            self.loadData()
        else:
            print('creating file')
            self.studentList = {}
            self.saveData()
            self.setLast()  
            #log this self.file + " file not found, new file was created"
    
    def addStudent(self, barcode, student):
        self.studentList[barcode] = student
        data_points = self.studentList[barcode].datapoints
        data_points['age'] = self.calcAge(data_points['dob'])
        self.last += 1
    
    def setLast(self):
        config = configparser.ConfigParser()
        config.read(os.path.abspath(os.pardir) + '\config.ini', encoding='utf-8')
        
        self.last = 0
        if len(self.studentList) != 0:
            self.last = int(sorted(self.studentList.keys())[-1][4:].replace('-', '')) + 1
        self.pre = config['SCHOOL_ABBERVIATIONS']['RYB']

    def formatCode(self):
        last_id = str(self.last)
        while len(last_id) < 6:
            last_id = '0' + last_id
        return self.pre + '-' + last_id[:3] + '-' + last_id[3:]

    def findTimeSlot(self, time):
        new_time = ''
        hour = time.hour
        minute = time.minute
        if minute <= 10:
            new_time = time - timedelta(minutes=time.minute)
        elif minute > 10 and minute <= 40:
            new_time = time + timedelta(minutes=-time.minute+30)
        elif minute > 40:
            new_time = time + timedelta(minutes=-time.minute+60)

        return datetime.strftime(new_time, '%I:%M %p')

    def calcAge(self, dob):
        return int((datetime.now() - datetime.strptime(dob, "%m/%d/%Y")).total_seconds() \
                / 60 / 60 / 24 / 365)

    def consecutive_checkin(self, student_id):
        return

    def reset_checkin(self, student_id, value):
        return

    def scanStudent(self, barcode):
        dt = datetime.now()
        timeslot = self.findTimeSlot(dt)
        time = '{:%I:%M %p}'.format(dt)
        date = '{:%m/%d/%Y}'.format(dt)

        data = [date, time, timeslot, '', '', self.school]

        data_points = self.studentList[barcode].datapoints
        data_points['attinfo'][1].append(data)

        #data_points['attinfo'] = list(data_points['attinfo'])
        #data_points['attinfo'][0] = ['Date', 'Check-In Time', 'Start Time', 'Check-Out Time', 'Confirm Time', 'School']

    def scanOutTeacher(self, barcode, confirmed_time):
        dt = datetime.now()

        timeslot = self.findTimeSlot(datetime.strptime(confirmed_time, '%I:%M %p'))
        time = '{:%I:%M %p}'.format(dt)

        data_points = self.studentList[barcode].datapoints
        data_points['attinfo'] = list(data_points['attinfo'])
        data_points['attinfo'][1][-1][3] = time
        data_points['attinfo'][1][-1][4] = timeslot
        #data_points['attinfo'][0] = ['Date', 'Check-In Time', 'Start Time', 'Check-Out Time', 'Confirm Time', 'School']

        self.studentList[barcode].timesheet.clocktimeout()

    def sort_attendance(self, barcode):
        attendance_table = self.studentList[barcode].datapoints['attinfo'][1]

        for row in attendance_table:
            row[0] = datetime.strptime(row[0], '%m/%d/%Y')

        attendance_table.sort()

        for row in attendance_table:
            row[0] = datetime.strftime(row[0], '%m/%d/%Y')

        self.saveData()

    def checkCode(self, barcode):
        return barcode in self.studentList

    def saveData(self):
        if not hasattr(self, 'key'):
            #log this print('creating key')
            self.key = b'=5<(M8R_P8CJx);^'
            file_ = open(self.pwfile, 'wb')
            file_.write(bytearray(self.key))
            file_.close()

        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        binary_string = pickle.dumps(self.studentList)
        encrypted = cipher.encrypt(binary_string)

        file_ = open(self.file, 'wb')
        file_.write(bytearray(encrypted))
        file_.close()

    def loadData(self):
        file_ = open(self.pwfile, 'rb')
        self.key = file_.read()
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)

        if os.path.exists(self.file):
            file_ = open(self.file, 'rb')
            #log this print('opened')
        else:
            self.saveData()
            file_ = open(self.file, 'rb')
            #log this print('created')
        
        decrypted = cipher.decrypt(file_.read())
        self.studentList = pickle.loads(decrypted)
        self.setLast()

    def format(self, ctype, value):
        if ctype != 0:
            return self.cell_format[ctype](value)
        
    def importxlsx(self, filename):
        config = configparser.ConfigParser()
        config.read(os.path.abspath(os.pardir) + '\config.ini', encoding='utf-8')
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)

        repr, headers = {}, [cell.value for cell in worksheet.row(0)]
        for header in headers:
            repr[headers.index(header)] = StudentInfo().datapont_aliases[header]

        unformatted_data = [worksheet.row(rx) for rx in range(1, worksheet.nrows)]
        student_info = [[self.cell_format[cell.ctype](cell.value) for cell in row] for row in unformatted_data]

        for info in student_info:
            new_student = StudentInfo()
            for data_point in info:
                new_student.datapoints[repr[info.index(data_point)]] = data_point

            if new_student.datapoints['bCode'][:3] in config['DEFAULT']['schools']:
                self.addStudent(new_student.datapoints['bCode'], new_student)

        self.saveData()

    def importtimexlsx(self, filename):
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)

        repr, headers = {}, [cell.value for cell in worksheet.row(0)][:4]
        for h in headers:
            repr[headers.index(h)] = StudentInfo().datapont_aliases[h]

        unformatted_data = [worksheet.row(rx) for rx in range(1, worksheet.nrows)]
        student_info = [[self.format(cell.ctype, cell.value) for cell in row] for row in unformatted_data]

        num_students_added, nt = 0, 0

        for info in student_info:
            student_id = info[0]
            time_data = info[4:]
            if student_id not in self.studentList: continue

            classes_awarded = info[3] if len(info[3]) != 0 else 0
            data_points = self.studentList[student_id].datapoints

            check_in_data = []
            for time_data_ in time_data:
                dt = time_data_.split(' ')
                time = dt[1]
                try:
                    date = datetime.strftime(datetime.strptime(dt[0], "%m/%d/%y"), "%m/%d/%Y")
                except ValueError:
                    date = dt[0]

                if len(dt) >= 4: check_in_data.append([date, dt[1] + ' ' + dt[2], dt[3], dt[4]])
                else: check_in_data.append([date, '', time])

            data_points['cAwarded'] = classes_awarded
            if classes_awarded.isdigit() and int(classes_awarded) > len(check_in_data):
                data_points['cRemaining'] = int(classes_awarded) - len(check_in_data)
            else:
                data_points['cRemaining'] = 0
            data_points['attinfo'][1] = check_in_data

            num_students_added += 1
            num_students_added += len(check_in_data)

        self.saveData()

        #return the amount of students and amount time data added
        return num_students_added, nt

    def exportdb(self, dest_path):
        shutil.copyfile(self.file, dest_path)

    def get_monthly_invoice(self, month, year):
        header = ['Date', 'Barcode', 'Chinese Name', 'First Name', 'Last Name', 'Check-in', 'Check-out', 'Hours worked']
        return_list = []
        return_teachers = {}
        gap = ['' for i in range(0, len(header))]
        
        attendance_list = []

        [return_list.append(list(gap)) for i in range(0, 6)]

        return_list[0][0] = 'Report date'
        return_list[0][1] = datetime.strftime(datetime.now(), '%m/%d/%Y')
        return_list[2][0] = 'Salary month'
        return_list[2][1] = datetime(1900, month, 1).strftime('%B')
        return_list[3][0] = 'Salary year'
        return_list[3][1] = year
        return_list[4][0] = 'School'
        return_list[4][1] = self.school

        return_list.append(header)

        for teacher_id, teacher in self.studentList.items():
            for attendance in teacher.datapoints['attinfo'][1]:
                date = datetime.strptime(attendance[0], '%m/%d/%Y')
                if date.month != month or date.year != year:
                    continue

                attendance_ = [
                    attendance[0],
                    teacher.datapoints['bCode'],
                    teacher.datapoints['chineseName'],
                    teacher.datapoints['firstName'],
                    teacher.datapoints['lastName'],
                    attendance[2] if len(attendance[2]) > 0 else 'X',
                    attendance[4] if len(attendance[4]) > 0 else 'X'
                ]

                if teacher_id not in return_teachers: return_teachers[teacher_id] = {}
                return_teachers[teacher_id][teacher.datapoints['attinfo'][1].index(attendance) + 1] = attendance[:5]
                
                if len(attendance[2]) > 0 and len(attendance[4]) > 0:
                    check_in = datetime.strptime(attendance[0] + ' ' + attendance[2], '%m/%d/%Y %I:%M %p')
                    check_out = datetime.strptime(attendance[0] + ' ' + attendance[4], '%m/%d/%Y %I:%M %p')
                    hours_worked = (check_out - check_in).seconds / 3600
                    attendance_.append((check_out - check_in).seconds / 3600)
                else:
                    attendance_.append('')

                attendance_list.append(attendance_)

        attendance_list.sort()

        for i in range(0, len(attendance_list)):
            current_day = datetime.strptime(attendance_list[i][0], '%m/%d/%Y')
            previous_day = datetime.strptime(attendance_list[i - 1][0], '%m/%d/%Y')
            if i != 0 and (current_day - previous_day).days > 1:
                return_list.append(list(gap))
            return_list.append(attendance_list[i])

        return return_list, return_teachers

    def search_attendance(self, barcode, date):
        if barcode not in self.studentList:
            return 'no teacher'

        attendance_table = self.studentList[barcode].datapoints['attinfo']
        for attendance in attendance_table[1]:
            if attendance[0] == date:
                return attendance_table[0], attendance
        return False