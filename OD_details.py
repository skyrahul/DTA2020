from imports import *
from initialize import *
from generateGraph import generate_graph

''' -------------------------------------------------------------------------------
-------------------FUNCTION TO TAKE OD DETAILS FROM THE USER-----------------------
-----------------------------------------------------------------------------------'''
#GUI related
def OD_details(OD_,links,nodes):
    count = 0
    global param,OD_pairs,label2,flag,node_count,edge_count,average_speed,link_density,average_time
    x = int(links.get())
    for i in OD_pairs:
        for j in i:
            j.destroy()
        for k in label2:
            k.destroy()
    lab1 = Label(root, text="ORIGIN")
    lab1.grid(row=x+8, column=5, sticky='NSEW')
    lab2 = Label(root, text="DESTINATION")
    lab2.grid(row=x+8, column=6, sticky='NSEW')
    label2 = [lab1,lab2]
    for j in range(int(OD_.get())):
        lab = Label(root, text = 'OD Pair '+str(j+1))
        lab.grid(row = x+9+j,column = 4,sticky = 'NSEW')
        label2.append(lab)
        origin = Entry(root)
        origin.grid(row = x+9+j, column = 5, sticky = 'NSEW')
        destination = Entry(root)
        destination.grid(row = x+9+j, column = 6, sticky = 'NSEW')
        OD_pairs.append([origin,destination])
        count = x+9+j
    edge_count = int(links.get())
    node_count = int(nodes.get())
    average_speed = [[[0 for i in range(classes)] for j in range(simtime)] for k in range(edge_count)]
    link_density = [[0 for i in range(classes)] for j in range(edge_count)]
    average_time = [[[0 for i in range(classes)] for j in range(simtime)] for k in range(edge_count)]
    submit = Button(root, text='Generate Network', fg='blue', bg='white', font=("Times New Roman", 20, "bold"),command=lambda: generate_graph(param, count))
    if(flag==0):
        flag+=1
        submit.grid(row= max(count + 1,16), column=1, pady='50')