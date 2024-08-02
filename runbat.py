# -*-coding = utf-8 -*-
# @Time : 2024/7/31 16:27
# @Author :skq
# @File : runbat.py
# @Software: PyCharm
import os
import subprocess
path = os.getcwd()
bat_file1 = os.path.join(path,'./install_audio.bat')
bat_file2 = os.path.join(path,'./install_splitter.bat')
bat_file3 = os.path.join(path,'./install_video.bat')

def run_bat(filepath):
    command = f'cmd /c "start "" "{filepath}""'
    p = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    print(p.returncode) # is 0 if success

def write_file(num):
    try:
        with open("./.regLAV.txt", 'w') as f:
            f.write('regsiter:'+str(num))
            return True
    except:
        return False

def run():
    run_bat(bat_file1)
    write_file(1)
    run_bat(bat_file2)
    write_file(2)
    run_bat(bat_file3)
    write_file(3)

import ctypes, sys

def readtxt():
    if not os.path.isfile(r'./.regLAV.txt'):
        return False
    else:
        with open("./.regLAV.txt", 'r') as f:
            a = f.readline()
            a = a.replace('\n','').replace('regsiter:','')
            print(a)
            if a == '3' or a==3:
                return True
            else:
                return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_admin():
    if not readtxt():
        if is_admin():
            run()
        # 主程序写在这里
        else:
            # 以管理员权限重新运行程序
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


run_admin()