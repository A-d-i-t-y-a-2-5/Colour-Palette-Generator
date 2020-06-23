#!/usr/bin/env python
# coding: utf-8


import PIL.Image
import requests
from cpgv1img import *
from tkinter import *
from tkinter.filedialog import askopenfilename

root = Tk()

root.geometry('300x125')
root.resizable(0, 0)
root.configure(bg = '#2C3436')
root.title('CPG')

Label(root, text = 'URL', bg = '#2C3436', fg = '#FFBD33').place(relx = 0, rely = 0)
i = Entry(root, relief = FLAT, bg = '#FFBD33', width=40)
i.place(relx = 1, rely = 0, anchor = NE)

Label(root, text = 'Cluster(s)', bg = '#2C3436', fg = '#FFBD33').place(relx = 0, rely = 0.25)
c = Entry(root, relief = FLAT, bg = '#FFBD33')
c.place(relx = 1, rely = 0.25, anchor = NE)

message = Label(root, bg = '#2C3436', fg = '#FFBD33')
message.place(relx = 0.5, rely = 0.55, anchor = CENTER)

def open_directory():
    files = [('JPEG Files', '*.jpg'), 
        ('PNG Files', '*.png')]
    
    filename = askopenfilename(title = "Select file", filetypes = files)
    cluster = c.get()
    if filename:
        if cluster:
            cluster = int(cluster)
        else:
            cluster = 6
        img = PIL.Image.open(filename)
        cpg = CPG(img, cluster)
#         message.config(text="Please wait")
        cpg.get_color()
        message.config(text="Success")
        
def open_url():
    url = i.get()
    cluster = c.get()
    if url:
        if cluster:
            cluster = int(cluster)
        else:
            cluster = 6
        try:
            img = PIL.Image.open(requests.get(url, stream=True).raw)
            cpg = CPG(img, cluster)
#             message.config(text="Please wait")
            cpg.get_color()
        except Exception:
            message.config(text=Exception)
    else:
        message.config(text="Please enter URL")
        
def clear():
    i.delete(0, END)
    c.delete(0, END)
    message.config(text = '')
        
buttonOpenD = Button(root, text="Open by Directory", command=lambda: open_directory()).place(rely = 0.75, anchor = W)
buttonOpenU = Button(root, text="Open by Image URL", command=lambda: open_url()).place(relx = 1, rely = 0.75, anchor = E)
buttonClr = Button(root, text = 'Clear', command = clear).place(relx = 0.5, rely = 0.90, anchor = CENTER)

root.mainloop()
