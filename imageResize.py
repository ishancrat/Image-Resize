import cv2
import os
import math
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

img_path = filedialog.askopenfilename(
    title = "select the image",
    filetypes = [("Image files","*.jpg *.jpeg *.png")]
)
if img_path:
    print("selected path : ", img_path)
else:
    print("no file selected")

temp_path = filedialog.asksaveasfilename(
    title = "save image as",
    defaultextension = ".jpeg",
    filetypes = [("PNG","*.png"),
                 ("JPEG","*.jpeg")]
)

if temp_path:
    print("save image path : ",temp_path)
else:
    print("no save path selected")
    
img = cv2.imread(img_path)


def img_size_on_disk(filepath):
    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes/1024
    return size_kb

choice = int(input("Choose action: [1] Downscale   [2] Upscale  :  "))


if (choice == 1):
    target = int(input("Enter max target size (in KB) :  "))
    fsize = img_size_on_disk(img_path)
    if (fsize < target):
        print("can't downscale, aborting")
    else:
        quality_factor = int((target * 100) / fsize);
        while(4):
            cv2.imwrite(temp_path,img,[cv2.IMWRITE_JPEG_QUALITY, quality_factor]);
            temp_size = img_size_on_disk(temp_path)
            if(temp_size > target):
                quality_factor -= 5
            elif (temp_size < (target - 20)): #maintains range of 50kb from max value
                quality_factor += 5;
            else:
                print("image saved successfully")
                break

elif (choice == 2):
    target = int(input("Enter min target size (in KB) :  "))
    fsize = img_size_on_disk(img_path)
    if (fsize > target):
        print("can't upscale, aborting")
    else:
        scale_factor = math.sqrt((float(target))/(float(fsize)));
        while(4):
            upscaled_img = cv2.resize(img, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(temp_path,upscaled_img);
            temp_size = img_size_on_disk(temp_path)
            if(temp_size < target):
                scale_factor += 0.1
            elif (temp_size > (target + 20)): #maintains range of 50kb from min value
                scale_factor -= 0.05;
            else:
                print("image saved successfully")
                break

else:
    print("invalid choice")
                
