import tkinter as tk
import numpy as np
import cv2
from tkinter import *
from tkinter import filedialog
import time
from threading import Timer

class MainWindow:
    
    def __init__(self, master):
        self.master = master
        self.framebutton = Frame(self.master,width=800, height=90,bg="black")
        self.framebutton.grid(row=0, sticky=W)
        self.framebutton.grid_propagate(False)
        ypad=30
        xpad=36
        self.flag = False
        self.filename = ""
        self.bupload = Button(self.framebutton, text="Upload", padx=20, pady=5, width=10, command=self.upload, bg="black", fg="white")
        self.bupload.bind("<Enter>",self.onEnterup)
        self.bupload.bind("<Leave>",self.onLeaveup)
        self.bupload.grid(row=0, column=0, padx=xpad, pady=ypad)
        
        self.bprocess = Button(self.framebutton, text="Process", padx=20, pady=5, width=10, command=self.threadprocess, bg="black", fg="white")
        self.bprocess.bind("<Enter>",self.onEnterpro)
        self.bprocess.bind("<Leave>",self.onLeavepro)
        self.bprocess.grid(row=0, column=1, padx=xpad, pady=ypad)
       
        self.breset = Button(self.framebutton, text="Reset", padx=20, pady=5, width=10, command=self.reset, bg="black", fg="white")
        self.breset.bind("<Enter>",self.onEnterre)
        self.breset.bind("<Leave>",self.onLeavere)
        self.breset.grid(row=0, column=2, padx=xpad, pady=ypad)
       
        self.bexit = Button(self.framebutton, text="Exit", padx=20, pady=5, width=10, command=exit, bg="black", fg="white")
        self.bexit.bind("<Enter>",self.onEnterxt)
        self.bexit.bind("<Leave>",self.onLeavext)
        self.bexit.grid(row=0, column=3, padx=xpad, pady=ypad)

        self.framelabel = Frame(self.master, width=800, height=90, bg="black")
        self.framelabel.grid(row=1,sticky=W)
        self.framelabel.grid_propagate(False)

        self.lfname = Label(self.framelabel, text="File name:", padx=20, pady=5, width=10, bg="black", fg="white")
        self.lfname.grid(row=0, column=0, padx=xpad, pady=ypad)

        self.lblfile = Label(self.framelabel, padx=20, pady=5, width=61, bg="gray", fg="white")
        self.lblfile.grid(row=0, column=1, padx=xpad, pady=ypad)

        self.lstatus = Label(self.master,anchor=W, bg="black", fg="white")
        self.lstatus.grid(row=2, columnspan=3)


    def upload(self):
        self.lstatus.configure(text="uploading file.....", anchor=W)
        self.filename =  filedialog.askopenfilename(initialdir = "/home/vishal/Desktop",title = "Select file",filetypes = (("all files","*.*"), ("jpeg files","*.jpg")))
        
        time.sleep(5)

        self.lblfile.configure(text=self.filename, anchor=W)
        self.lstatus.configure(text="file uploaded.....", anchor=W)

    def threadprocess(self):
        t = Timer(00,self.processn)
        t.start()

    def processn(self):
        if not self.filename:
            return
        self.lstatus.configure(text="processing video.....", anchor=W)
        time.sleep(5)
        self.cap1 = cv2.VideoCapture(self.filename)
        self.cap2 = cv2.VideoCapture(self.filename)
        cv2.namedWindow('Unprocessed video', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Processed video', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Unprocessed video', 40,30)
        cv2.moveWindow('Processed video', 1000,30)
        cv2.resizeWindow('Unprocessed video', 900,700)
        cv2.resizeWindow('Processed video', 900,700)
        self.flag = True
        while self.cap1.isOpened() & self.cap2.isOpened():
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            if ret1 == True & ret2 == True:
                cv2.imshow("Unprocessed video", frame1)
                cv2.imshow("Processed video", frame2)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()
        self.lstatus.configure(text="done.....", anchor=W)
        
    def reset(self):
        self.filename = ""
        self.lblfile.configure(text=self.filename,anchor=W)
        if self.flag:
            self.cap1.release()
            self.cap2.release()
            self.flag = False
        cv2.destroyAllWindows()

    def onEnterup(self, e):
        self.bupload['background']="white"
        self.bupload['fg']="black"

    def onLeaveup(self, e):
        self.bupload['background']="black"
        self.bupload['fg']="white"

    def onEnterpro(self, e):
        self.bprocess['background']="white"
        self.bprocess['fg']="black"

    def onLeavepro(self, e):
        self.bprocess['background']="black"
        self.bprocess['fg']="white"

    def onEnterre(self, e):
        self.breset['background']="white"
        self.breset['fg']="black"

    def onLeavere(self, e):
        self.breset['background']="black"
        self.breset['fg']="white"

    def onEnterxt(self, e):
        self.bexit['background']="white"
        self.bexit['fg']="black"

    def onLeavext(self, e):
        self.bexit['background']="black"
        self.bexit['fg']="white"


root = Tk()
root.geometry("800x200+550+800")
root.configure(bg="black")  
root.title("Traffic Rule Violation-Detection System")
M = MainWindow(root)
root.mainloop()