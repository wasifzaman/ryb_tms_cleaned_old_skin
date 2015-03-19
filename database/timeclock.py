from datetime import datetime, date, time, timedelta


class timesheet:

	def __init__(self):
		self.sheet = []

	def clocktimein(self):
		currentitme = datetime.now()
		self.sheet.append(timeclock(currentitme, False, False))

	def clocktimeout(self):
		currentitme = datetime.now()
		if self.sheet[-1].checkin.date() != currentitme.date(): return False

		self.sheet[-1].checkout = currentitme

	def defineoutformat(self, dateformat, timeformat):
		self.dateformat = dateformat
		self.timeformat = timeformat

	def printtimesheet(self):
		outsheet = []
		for time in self.sheet:
			date = datetime.strftime(time.checkin, self.dateformat) if time.checkin != False else ''
			checkin = datetime.strftime(time.checkin, self.timeformat) if time.checkin != False else ''
			checkout = datetime.strftime(time.checkout, self.timeformat) if time.checkout != False else ''
			outsheet.append([date, checkin, checkout, time.scanmode])

		return outsheet


class timeclock:
	
	def __init__(self, checkin, checkout, scanmode):
		self.checkin = checkin
		self.checkout = checkout
		self.scanmode = scanmode
		self.checkinrounded = self.roundto(self.checkin)
		self.checkoutrounded = self.roundto(self.checkout)

	def roundto(self, checktime):
		if not checktime: return checktime
		print(checktime, checktime + timedelta(minutes=1))


	def printtime(self):
		return [self.checkin, self.checkout, self.scanmode]

	


'''
test = Timesheet()
test.clocktimein()
test.clocktimeout()

test.defineoutformat('%m/%d/%Y', '%I:%M %p')

for time in test.sheet:
	print(time.printtime())

printedsheet = test.printtimesheet()

for time in printedsheet:
	print(time)
#'''