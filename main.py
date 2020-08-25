from edge_details import *
from imports import *
from initialize import *
from OD_details import *

''' ----------------------------------------------------------------------------------
Entire section below is related to the GUI development using tkinter library functions
 -------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    root = tkinter.Tk()         #GUI related
    root.geometry('1366x768')   #GUI related
    root.configure(background='powderblue')     #GUI related
    root.title('Dynamic Traffic Assignment Simulator')  #GUI related
    Label(root, text="DYNAMIC TRAFFIC ASSIGNMENT SIMULATOR", fg='orange', bg='black',
                  font=("Times New Roman", 20, "bold")).grid(row=0, columnspan=10, sticky='NSEW', ipady='10',
                                                             ipadx='380')      #GUI related

    Label(root, text=" ", bg='powderblue').grid(row=1, column=0, sticky='W')     #GUI related
    Label(root, text=" ", bg='powderblue').grid(row=2, column=0, sticky='W')     #GUI related
    Label(root, text="Enter the number of nodes").grid(row=3, column=0, sticky='NSEW')   #GUI related
    nodes = Entry(root)     #GUI related
    nodes.grid(row=3, column=1, sticky='W')     #GUI related

    # For code check purpose
    nodes = 4

    Label(root, text=" ", bg='powderblue').grid(row=4, column=0, sticky='W')     #GUI related
    Label(root, text=" ", bg='powderblue').grid(row=5, column=0, sticky='W')     #GUI related
    Label(root, text="Enter the number of links").grid(row=6, column=0, sticky='NSEW')     #GUI related
    links = Entry(root)     #GUI related
    links.grid(row=6, column=1, sticky='W')     #GUI related

    # For code check purpose
    

    Label(root, text=" ", bg='powderblue').grid(row=7, column=0, sticky='W')     #GUI related
    Label(root, text=" ", bg='powderblue').grid(row=8, column=0, sticky='W')     #GUI related
    Button(root, text="Enter the link details", fg='blue', bg='white', font=("Times New Roman", 10, "bold"),
                command=lambda: edge_details(links)).grid(row=9, column=0, sticky='E', ipadx='20')  #GUI related

    Label(root, text=" ", bg='powderblue').grid(row=10, column=0, sticky='W')    #GUI related
    Label(root, text=" ", bg='powderblue').grid(row=11, column=0, sticky='W')    #GUI related
    Label(root, text="Enter the number of O-D pairs").grid(row=12, column=0, sticky='NSEW')    #GUI related
    OD_ = Entry(root)    # GUI related
    OD_.grid(row=12, column=1, sticky='W')  #GUI related

    Label(root, text=" ", bg='powderblue').grid(row=13, column=0, sticky='W')    #GUI related
    Label(root, text=" ", bg='powderblue').grid(row=14, column=0, sticky='W')    #GUI related
    Button(root, text="Enter the O-D details", fg='blue', bg='white', font=("Times New Roman", 10, "bold"),command=lambda: OD_details(OD_, links,nodes)).grid(row=15, column=0, sticky='E', ipadx='20')
    root.mainloop()#GUI related

'''-------------------------------------------------------------------------------------------------------------
------------------------------------------------END OF THE PROJECT----------------------------------------------
----------------------------------------------------------------------------------------------------------------'''