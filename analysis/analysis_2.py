import sys, os
sys.path.append(os.path.abspath(os.pardir))
from dataHandler import *
from statistics import *


#load database
k = keeper.Keeper('keeper.db')
d = StudentDB(file=k.files['cfilepath'], cfile=k.fname)


for student in d.studentList.values():
	try:
		student.datapoints['cTaken'] = student.datapoints['cAwarded'] - student.datapoints['cRemaining']
	except:
		student.datapoints['cTaken'] = 0


#timeslot sorter
timeslotsodd = {'9:30': '09:30', '1:00': '01:00', '2:30': '02:30', '4:00': '04:00'}
timeslotsgood = ['09:30', '11:00', '01:00', '02:30', '04:00']

timeslotsgoodfull = {'09':'30 AM', '11':'00 AM', '01':'00 PM', '02':'30 PM', '04':'00 PM'}
closest = {9: '09', 11: '11', 1: '01', 2: '02', 4: '04'}


bydate = {}
byweek = {}


#find closest hour
def find_closest(t):
	i = int(t)
	closeness = 9
	for k in closest:
		if abs(i-closeness) < abs(i-k):
			closeness = k

	return closest[closeness]

	
def fix_checkin(t):
	p = []
	if ':' in t:
		p = t.split(':')
	elif ';' in t:
		p = t.split(';')

	if p == []: return

	if ' ' in p[1]:
		p[1] = p[1].split(' ')[0]

	
	if len(p[0]) == 1:
		p[0] = '0' + p[0]

	try:
		p[1] = timeslotsgoodfull[p[0]]
	except:
		p[0] = find_closest(p[0])
		p[1] = timeslotsgoodfull[p[0]]
		#print(p[0])

	return ':'.join(p)


def fix_database_checkin(db):
	for student in db.studentList.values():
		for att in student.datapoints['attinfo'][1]:
			if len(att[0]) < 10: continue
			
			if att[2] == None: continue
			att[2] = fix_checkin(att[2])
	
	db.saveData()


#fix_database_checkin(d)


l = 0
for student in d.studentList.values():
	for att in student.datapoints['attinfo'][1]:
		if len(att[0]) < 10: continue
		dtformat = datetime.strptime(att[0], '%m/%d/%Y')
		cintime = att[2]
		

		#eliminate odd timeslots
		#if cintime[:4] in timeslotsodd:
		#	cintime = timeslotsodd[cintime[:4]]
		#elif cintime[:5] in timeslotsgood:
		#	cintime = cintime[:5]
		#else:
		#	continue
		
		
		bydate.setdefault(dtformat, []).append([dtformat, cintime, student.datapoints['bCode']])


for student in d.studentList.values():
	for att in student.datapoints['attinfo'][1]:
		if len(att[0]) < 10: continue
		dtformat = datetime.strptime(att[0], '%m/%d/%Y')
		week = dtformat.isocalendar()[1]
		cintime = att[2]

		byweek.setdefault(week, []).append([dtformat, cintime, student.datapoints['bCode']])


def return_bd(filteredlist):
	#internal
	#return student list bydate
	bd = {}
	for date in filteredlist:
		bd.setdefault(date[0], []).append(date)

	return bd


def return_year(attendancelist, year):
	#return_year(dict, int) -> dict
	#takes input of list filtered by date and year and
	#returns an outpot of list filtered by date
	yfilter = {}
	for date, checkin in attendancelist.items():
		for entry in checkin:
			yfilter.setdefault(date.year, []).append(entry)
	
	y = yfilter[year]
	return return_bd(y)


def return_month(attendancelist, month):
	#return_month(dict, int) -> dict
	#takes input of list filtered by date and month and
	#returns an outpot of list filtered by date
	mfilter = {}
	for date, checkin in attendancelist.items():
		for entry in checkin:
			mfilter.setdefault(date.month, []).append(entry)

	m = mfilter[month]
	bd = {}
	return return_bd(m)


def return_week(attendancelist, week):
	wfilter = {}

	for date, checkin in attendancelist.items():
		for entry in checkin:
			wfilter.setdefault(date.isocalendar()[1], []).append(entry)

	w = wfilter[week]
	return return_bd(w)


def return_year_month(attendancelist, year, month):
	#return_year_month(dict, int, int) -> dict
	#takes input of list filtered by date, year and month and
	#returns an outpot of list filtered by date
	return return_month(return_year(attendancelist, year), month)


def return_check_in(attendancelist, time):
	#return_check_in(dict, str) -> dict
	#takes an input of list filtered by date and string which is a time slot and
	#returns an output of list filtered by date matching the time slot
	bycheckin = {}
	for date, checkin in attendancelist.items():
		for entry in checkin:
			bycheckin.setdefault(entry[1], []).append(entry)

	t = bycheckin[time]
	return return_bd(t)


def return_attendance(attendancelist):
	total = 0
	for day in attendancelist.values():
		total += len(day)

	return total


def return_attribute_group(attendancelist, attribute, sign='==', option=False):
	#return_attribute_group(dict, str, value_type) -> list
	#takes input of list filtered by date, string and a value type (int, float, str) and
	#returns an output a dictionary of students matching the value of the attribute
	#where the keys are the attribute values and the values are all the classes they attended
	attribute_group = {}
	for date, checkin in attendancelist.items():
		for entry in checkin:
			student_attrib = d.studentList[entry[2]].datapoints[attribute]
			if option:
				if sign == '==' and option != student_attrib: continue
				elif sign == '<=' and option <= student_attrib: continue
				elif sign == '>=' and option >= student_attrib: continue
			attribute_group.setdefault(student_attrib, []).append(entry)

	return attribute_group


def return_studentlist(attendancelist):
	#return_studentlist(dict) -> dict
	#takes input of list filtered by date and returns an output
	#of dictionary where the keys are students and values are their corresponding attendance
	studentlist = {}
	for date, entry in attendancelist.items():
			for checkin in entry:
				studentlist.setdefault(checkin[2], []).append(checkin)

	return studentlist


def return_studentlist_filtered(attendancelist, attribute, sign='==', value=False):
	#return_studentlist(dict) -> dict
	#takes input of list filtered by date and returns an output
	#of dictionary where the keys are students and values are their corresponding attendance
	if not value: return
	studentlist = {}
	for date, entry in attendancelist.items():
			for checkin in entry:
				studentlist.setdefault(checkin[2], []).append(checkin)

	studentlist_fileterd = {}
	for s in studentlist:
		if sign == '<=':
			if d.studentList[s].datapoints[attribute] <= value: studentlist_fileterd[s] = studentlist[s]
			continue
		elif sign == '>=':
			if d.studentList[s].datapoints[attribute] >= value: studentlist_fileterd[s] = studentlist[s]
			continue
		elif sign == '==':
			if d.studentList[s].datapoints[attribute] == value: studentlist_fileterd[s] = studentlist[s]
			continue

	return studentlist_fileterd


def return_attribute(studentlist, attribute):
	#obsolete
	return {s: d.studentList[s].datapoints[attribute] for s in studentlist}


def return_attribute_list(attendancelist, attribute):
	#return_attribute_list(dict, str) -> list
	#takes input of dictionary and string filtered by date and
	#returns an output of list which contains data but without
	#the corresponding student of each attribute
	return [d.studentList[s].datapoints[attribute] for s in return_studentlist(attendancelist)]


def return_bydate_filtered(attendancelist, attribute, sign, value):
	alist = []
	slist = return_attribute_group(attendancelist, attribute, sign, value)

	for value in slist.values():
		alist += value

	return return_bd(alist)


all_entries = bydate

'''

	v2014_6 = return_year_month(all_entries, 2014, 6)
	v2014_6_11 = return_check_in(v2014_6, '11:00 AM')
	v2014_6_11_7 = return_studentlist(return_attribute_group(v2014_6_11, 'age'))


	for i in range(3, 115):
		try:
			slist = return_studentlist(return_attribute_group(all_entries, 'age', i))
			if len(slist) == 0: continue

			gen = return_attribute_group(slist, 'gender')
			if 'M' in gen:
				m = len(gen['M'])
			if 'F' in gen:
				f = len(gen['F'])
		except:
			continue

	m = len(return_studentlist(return_attribute_group(all_entries, 'gender', 'M')))
	f = len(return_studentlist(return_attribute_group(all_entries, 'gender', 'F')))
	#print(m, f)

	all_classes = return_attribute_list(all_entries, 'cAwarded')
	all_classes_taken = [d.studentList[s].datapoints['cTaken'] for s in return_studentlist(all_entries)]


	print('........................')
	print('......All Classes.......')

	print('Total: ', len(all_classes))
	print('Mean: ', mean(all_classes))
	print('Mode: ', mode(all_classes))
	print('Median: ', median(all_classes))
	print('STDev: ', stdev(all_classes))
	print('Sample STDev: ', mean(all_classes)/stdev(all_classes))

	print('.................................')
	print('........All Classes Taken........')

	print('Mean: ', mean(all_classes_taken))
	print('Mode: ', mode(all_classes_taken))
	print('Median: ', median(all_classes_taken))
	print('STDev: ', stdev(all_classes_taken))
	print('Sample STDev: ', mean(all_classes_taken)/stdev(all_classes_taken))

'''

'''
total = {}

for i in range(2009, 2015):
	for j in range(1, 13):
		try:
			total_classes = return_year_month(all_entries, i, j)
			total_students = return_studentlist(total_classes)
			total_males = return_studentlist_filtered(total_classes, 'gender', value='M')
			total_females = return_studentlist_filtered(total_classes, 'gender', value='F')
			
			total_students_filtered = return_studentlist_filtered(total_classes, 'cAwarded', '<=', 15)
			total_students_filtered_greater = return_studentlist_filtered(total_classes, 'cAwarded', '>=', 16)

			total_this_month = 0
			for c in total_classes.values():
				total_this_month += len(c)
			
			print(j, '/', i, '/', total_this_month, '/', len(total_students_filtered), '/', len(total_students_filtered_greater), '/', len(total_students), '/', len(total_males), '/', len(total_females))
		except:
			continue
	print('\n')

'''

'''
	for i in range(3, 115):
		try:
			slist = return_studentlist_filtered(all_entries, 'age', value=i)
			if len(slist) == 0: continue

			gen = return_attribute_group(slist, 'gender')
			if 'M' in gen:
				m = len(gen['M'])
			if 'F' in gen:
				f = len(gen['F'])
		except:
			continue

	m = len(return_studentlist_filtered(all_entries, 'gender', value='M'))
	f = len(return_studentlist_filtered(all_entries, 'gender', value='F'))
	print(m, f)
'''

all_classes = return_attribute_list(all_entries, 'cAwarded')
all_classes_taken = [d.studentList[s].datapoints['cTaken'] for s in return_studentlist(all_entries)]


def mymode(l):
	mo = {}
	for i in l:
		if i in mo:
			mo[i] += 1
		else:
			mo[i] = 1

	max_mo = False
	for i in mo:
		if not max_mo:
			max_mo = i
			continue
		if mo[i] >= mo[max_mo]:
			max_mo = i

	return max_mo 

'''
	print('Total: ', len(all_classes), '\n')
	print('........................')
	print('......All Classes.......')

	mode2 = [m for m in all_classes if m != mode(all_classes)]
	mode3 = [m for m in mode2 if m != mode(mode2)]
	mode4 = [m for m in mode3 if m != mode(mode3)]
	mode5 = [m for m in mode4 if m != mode(mode4)]
	mode5.sort()
	mode2all_classes = [m for m in all_classes_taken if m != mode(all_classes_taken)]
	mode3all_classes = [m for m in mode2all_classes if m != mode(mode2all_classes)]
	mode4all_classes = [m for m in mode3all_classes if m != mymode(mode3all_classes)]
	mode5all_classes = [m for m in mode4all_classes if m != mode(mode4all_classes)]
	#mode5all_classes.sort()

	print('Mean: ', mean(all_classes))
	print('Mode: ', mode(all_classes))
	print('Mode 2:', mode(mode2))
	print('Mode 3:', mode(mode3))
	print('Mode 4:', mode(mode4))
	print('Mode 5:', mymode(mode5))
	print('Median: ', median(all_classes))
	print('STDev: ', stdev(all_classes))
	print('Sample STDev: ', mean(all_classes)/stdev(all_classes))

	print('.................................')
	print('........All Classes Taken........')

	print('Mean: ', mean(all_classes_taken))
	print('Mode: ', mode(all_classes_taken))
	print('Mode 2:', mode(mode2all_classes))
	print('Mode 3:', mymode(mode3all_classes))
	print('Mode 4:', mode(mode4all_classes))
	print('Mode 5:', mymode(mode5all_classes))
	print('Median: ', median(all_classes_taken))
	print('STDev: ', stdev(all_classes_taken))
	print('Sample STDev: ', mean(all_classes_taken)/stdev(all_classes_taken))
'''

'''
year_2014 = return_year(all_entries, 2012)
week5 = return_week(year_2014, 5)
sort_gender = return_bydate_filtered(week5, 'gender', '==', 'M')
sort_age = return_bydate_filtered(sort_gender, 'age', '>=', 15)
sort_classes = return_bydate_filtered(sort_age, 'cAwarded', '==', 60)


s_list = return_studentlist(sort_classes)

show_classes = return_attribute_list(s_list, 'cAwarded')

'''

'''
yw = {}
yw_gender = {}

for year in range(2011, 2015):

	try:
		y = return_year(all_entries, year)

		#print(year, ' ', return_attendance(y))

		for w in range(1, 53):
			try:
				week_filtered = return_week(y, w)
				sort_gender_m = return_bydate_filtered(week_filtered, 'gender', '==', 'M')
				sort_gender_f = return_bydate_filtered(week_filtered, 'gender', '==', 'F')
				yw.setdefault(year, []).append([w, return_attendance(week_filtered)])
				yw_gender.setdefault(year, []).append([w, len(return_studentlist(sort_gender_m)), len(return_studentlist(sort_gender_f))])
			except:
				continue


		#for w in range(1, 53):
		#	try:
		#		print(year, w, return_week())
		#	except:
		#		continue

	except:
		continue


workbook = xlsxwriter.Workbook('analysis_by_week.xlsx')
worksheet = workbook.add_worksheet()

r = 0
for year, value in yw_gender.items():
	worksheet.write(r, 0, year)
	for week in value:
		ratio = week[1] / (week[1] + week[2])
		#try:
		worksheet.write(r, week[0], ratio)
		#except:
		#	continue
	r += 1

workbook.close()

'''


print('Total: ', len(all_classes), '\n')
print('........................')
print('......All Classes.......')

mode2 = [m for m in all_classes if m != mode(all_classes)]
mode3 = [m for m in mode2 if m != mode(mode2)]
mode4 = [m for m in mode3 if m != mode(mode3)]
mode5 = [m for m in mode4 if m != mode(mode4)]
mode5.sort()
mode2all_classes = [m for m in all_classes_taken if m != mode(all_classes_taken)]
mode3all_classes = [m for m in mode2all_classes if m != mode(mode2all_classes)]
mode4all_classes = [m for m in mode3all_classes if m != mymode(mode3all_classes)]
mode5all_classes = [m for m in mode4all_classes if m != mode(mode4all_classes)]
#mode5all_classes.sort()

print('Mean: ', mean(all_classes))
print('Mode: ', mode(all_classes))
print('Mode 2:', mode(mode2))
print('Mode 3:', mode(mode3))
print('Mode 4:', mode(mode4))
print('Mode 5:', mymode(mode5))
print('Median: ', median(all_classes))
print('STDev: ', stdev(all_classes))
print('Sample STDev: ', mean(all_classes)/stdev(all_classes))

print('.................................')
print('........All Classes Taken........')

print('Mean: ', mean(all_classes_taken))
print('Mode: ', mode(all_classes_taken))
print('Mode 2:', mode(mode2all_classes))
print('Mode 3:', mymode(mode3all_classes))
print('Mode 4:', mode(mode4all_classes))
print('Mode 5:', mymode(mode5all_classes))
print('Median: ', median(all_classes_taken))
print('STDev: ', stdev(all_classes_taken))
print('Sample STDev: ', mean(all_classes_taken)/stdev(all_classes_taken))
