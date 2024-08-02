# -*-coding = utf-8 -*-
# @Time : 2024/7/29 16:13
# @Author :skq
# @File : tst.py
# @Software: PyCharm
import base64
import ctypes
import os
import sys

import win32com.client

def firrs():
    Application = win32com.client.Dispatch("PowerPoint.Application")
    images_dir = './'
    Presentation = Application.Presentations.Open(r'D:\Code\KG2\erp.pptx')
    for i, slide in enumerate(Presentation.Slides):
        print(i, slide)
        slide: win32com.client.CDispatch
        print(type(slide))
        image_path = os.path.join(images_dir, f"slide_{i + 1}.jpg")
        slide.Export(image_path, "JPG")
    print('dasdasddas')


import os
import comtypes.client

def ppt_to_images(ppt_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize the PowerPoint application
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1

    # Open the presentation
    presentation = powerpoint.Presentations.Open(ppt_path)

    # Save each slide as an image
    for i, slide in enumerate(presentation.Slides):
        print(i,slide)
        image_path = os.path.join(output_folder, f"slide_{i + 1}.jpg")
        slide.Export(image_path, "JPG")

    # Close the presentation and quit PowerPoint
    presentation.Close()
    powerpoint.Quit()


import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False


if is_admin():
    result = subprocess.run(['runbat.exe'], capture_output=True, text=True)
    print(result.stdout)
else:
    # 以管理员权限重新运行程序
    print("Requesting admin privileges...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

