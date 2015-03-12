class StudentInfo:

    def __init__(self):
        self.datapoints = {
            "lastName": '', "firstName": '', "chineseName": '',
            "schoolLoc": '', "bCode": '', "sid": '',
            "dob": '01/01/1900', "age": 0, "parentName": '',
            "hPhone": '', "cPhone": '', "cPhone2": '', "pup": '',
            "addr": '', "state": '', "city": '', "zip": '',
            "wkdwknd": '',
            "tpd": '01/01/1900', "tpa": 0, "tpo": 0, "tp": 0,
            "email": '',
            "sType": '',
            "cAwarded": 0, "cRemaining": 0,
            "findSchool": '',
            "notes": '',
            "attinfo": [['Date', 'Check-In Time', 'Start Time', 'Check-Out Time', 'Confirm Time', 'School'], []],
            "portr": '',
            "ctime": '', "expire": '', "cp": "N",
            "paid_entries": {},
            "last_payment": False,
            "inrow": 0,
            "pay_per_hour": 0.00
            }

        self.datapont_aliases = {
            "Last Name": "lastName", "First Name": "firstName", "Chinese Name": "chineseName",
            "School Location": "schoolLoc", "Barcode": "bCode",
            "Student Number": "sid",
            "Date of Birth": "dob", "Age": "age", "Gender": "gender",
            "Parent Name": "parentName", "Home Phone": "hPhone",
            "Cell Phone": "cPhone", "Cell Phone 2": "cPhone2",
            "Pick Up Person": "pup",
            "Address": "addr", "State": "state", "City": "city", "Zip": "zip",
            "Weekday/Weekend": "wkdwknd",
            "Payment Date": "tpd", "Payment Method": "Payment Method: ",
            "Payment Amount": "tpa", "Payment Owed": "tpo",
            "Email": "email",
            "Service Type": "sType",
            "Classes Awarded": "cAwarded", "Classes Remaining": "cRemaining",
            "How did you hear about the school?": "findSchool",
            "Notes": "notes",
            "Already Paid": "tp",
            "Card Printed": "cp",
            "Notes": 'notes'
            }

        self.ordered_datapoints = ['bCode', 'sid', 'firstName', 'lastName', 'chineseName', 'parentName', 'pup', 'gender', 'dob', 'addr', 'state', 'city',\
            'zip', 'cPhone', 'cPhone2', 'hPhone', 'tpd', 'tpa', 'email', 'findSchool', 'cp', 'notes']
        self.reverse_datapoint_aliases = {value:key for key, value in self.datapont_aliases.items()}
        self.ordered_datapoints_aliases = [self.reverse_datapoint_aliases[key] for key in self.ordered_datapoints]