import sys, os
sys.path.append(os.path.abspath(os.pardir))
from dataHandler import *
from statistics import *


'''
	#year to year
	yty = {}

	for date in bydate:
		y = date.year
		if y in yty:
			yty[y] += len(bydate[date])
		else:
			yty[y] = len(bydate[date])


	#by check in time
	bycheckin = {}
	for date, checkin in bydate.items():
		for entry in checkin:
			bycheckin.setdefault(entry[1], []).append(entry)

	#age group of each check in
	agegroup = {}
	for date, checkin in bycheckin.items():
		for entry in checkin:
			age = d.studentList[entry[2]].datapoints['age']
			if age < 2 or age > 20: continue
			agegroup.setdefault(date, []).append(age)

	#for time, group in agegroup.items():
	#	print(time, mean(group), mode(group), pstdev(group))
		#group.sort()
		#print(group)


	#filter
	#year
	yearfilter = {}
	for date, checkin in bydate.items():
		for entry in checkin:
			yearfilter.setdefault(date.year, []).append(entry)

	monthfilter = {}
	for date, checkin in bydate.items():
		for entry in checkin:
			monthfilter.setdefault(date.month, []).append(entry)

	def return_agegroup(attendancelist, age):
		#test function for return_attribute_group
		agegroup = {}
		for date, checkin in attendancelist.items():
			for entry in checkin:
				student_age = d.studentList[entry[2]].datapoints['age']

				#filter age
				if student_age < 2 or student_age > 20: continue
				agegroup.setdefault(student_age, []).append(entry)

		return agegroup[age]

'''

#load database
k = keeper.Keeper('keeper.db')
d = StudentDB(file=k.files['cfilepath'], cfile=k.fname)

bydate = {}

timeslotsgood = {'09':'30 AM', '11':'00 AM', '01':'00 PM', '02':'30 PM', '04':'00 PM'}
closest = {9: '09', 11: '11', 1: '01', 2: '02', 4: '04'}


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
		p[1] = timeslotsgood[p[0]]
	except:
		p[0] = find_closest(p[0])
		p[1] = timeslotsgood[p[0]]
		#print(p[0])

	return ':'.join(p)





for student in d.studentList.values():
	for att in student.datapoints['attinfo'][1]:
		att[2] = fix_checkin(att[2])
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


print(bydate)
#by check in time
#bycheckin = {}
#for date, checkin in bydate.items():
#	for entry in checkin:
#		bycheckin.setdefault(entry[1], []).append(entry)




l = []
for k in bycheckin:
	p = []
	if ':' in k:
		p = k.split(':')
	elif ';' in k:
		p = k.split(';')

	if p == []: continue

	if ' ' in p[1]:
		p[1] = p[1].split(' ')[0]

	
	if len(p[0]) == 1:
		p[0] = '0' + p[0]

	try:
		p[1] = timeslotsgood[p[0]]
	except:
		p[0] = find_closest(p[0])
		p[1] = timeslotsgood[p[0]]
		#print(p[0])

	#if len(p[1]) == 3:
	#	p[1] = '0' + p[1][0]
	#elif len(p[1]) == 4:
	#	p[1] = p[1][:2]



	l.append(len(p[0]))
	l.append(len(p[1]))

	#print(p)


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
		p[1] = timeslotsgood[p[0]]
	except:
		p[0] = find_closest(p[0])
		p[1] = timeslotsgood[p[0]]
		#print(p[0])

	return p

#print(1 in l)