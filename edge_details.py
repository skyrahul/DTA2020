from imports import *;
from initialize import *;

''' -------------------------------------------------------------------------------
-------------------FUNCTION TO TAKE EDGE DETAILS FROM THE USER---------------------
-----------------------------------------------------------------------------------'''
# GUI related
def edge_details(links):
    global param,label
    if(len(param)!=0):
        for i in param:
            for j in i:
                j.destroy()
        for i in label:
            i.destroy()
        label = []
        param = []
    lab1 = Label(root, text="Start Node")
    lab1.grid(row=3, column=4, sticky='NSEW')
    lab2 = Label(root, text="End Node")
    lab2.grid(row=3, column=5, sticky='NSEW')
    lab3 = Label(root, text="Length (km)")
    lab3.grid(row=3, column=6, sticky='NSEW')
    lab4 = Label(root, text="Width (m)")
    lab4.grid(row=3, column=7, sticky='NSEW')
    lab5 = Label(root, text="Density")
    lab5.grid(row=3, column=8, sticky='NSEW')
    label = [lab1,lab2,lab3,lab4,lab5]
    for j in range(int(links.get())):
        lab = Label(root, text='Link ' + str(j + 1))
        lab.grid(row=j+4, column=3, sticky='NSEW')
        label.append(lab)
        n1 = Entry(root)
        n1.grid(row=j + 4, column=4, sticky='NSEW')
        n2 = Entry(root)
        n2.grid(row=j + 4, column=5, sticky='NSEW')
        l = Entry(root)
        l.grid(row=j+4, column=6, sticky='NSEW')
        w = Entry(root)
        w.grid(row=j + 4, column=7, sticky='NSEW')
        d = Entry(root)
        d.grid(row=j + 4, column=8, sticky='NSEW')
        param.append([n1,n2,l,w,d])