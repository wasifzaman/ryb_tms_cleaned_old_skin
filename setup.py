import sys, os, shutil
from cx_Freeze import setup, Executable
sys.path.append(os.path.abspath('windows'))
sys.path.append(os.path.abspath('widgets'))
sys.path.append(os.path.abspath('database'))
sys.path.append(os.path.abspath('miscellaneous'))
sys.path.append(os.path.abspath('messages windows'))

build_exe_options = {
                    'build_exe': 'build\\bin',
                    'create_shared_zip':False,
                    'silent': True
                    }

setup(name = "rybsms",
    version = "0.1",
    description = "RYB SMS",
    options = {"build_exe": build_exe_options},
    executables = [Executable("windows\\ryb_attendance.py",
    	targetName="RYB Teacher Attendance.exe",
    	base="Win32GUI",
    	icon = "images\\RYB_Attendance.ico")])

os.mkdir('build\\images')
os.mkdir('build\\temp')

for file_ in os.listdir('images'):
    shutil.copy('images\\' + file_, 'build\\images\\' + file_)
for file_ in os.listdir('temp'):
    shutil.copy('temp\\' + file_, 'build\\temp\\' + file_)
shutil.copy('config.ini', 'build\\config.ini')

print('\n\n****\nbuild successful\n****')