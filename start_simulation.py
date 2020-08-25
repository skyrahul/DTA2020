from imports import *
from initialize import *
from DTA import dynamic_traffic_assignment
from DFS import *

''' -------------------------------------------------------------------------------
----------------------------FUNCTION TO VISUALIZE SIMULATION ----------------------
-----------------------------------------------------------------------------------'''

# GUI related function
def visualize(i):
    global labelvis,edges,c, visual
    for k in labelvis:
        k.destroy()
        labelvis = []
    visual = i
    x = 1000/(edges[edge_pairs[i][0]][edge_pairs[i][1]][-1]+1)
    m = 683 - (len(AO[i])// 2) * x
    for j in range(0,len(AO[i])):
        val1 = int(AO[i][j] * 255/0.8881)
        val2,val3 = 0,0
        for a in range(4):
            val2 += density[i][a][j]
            val3 += flow[i][a][j]
        temp1 = int(val2)
        temp2 = int(val3)
        val2,val3 = min(255,int(val2/10)),min(255,int(val3/150))
        label = Label(c,text = round(AO[i][j],3),fg = 'yellow',bg ='black',borderwidth ='4',relief= RAISED)
        c.create_window(183+x//2+j*x,64,anchor='center',height ='30',width = x,window = label)
        labelvis.append(label)
        label = Label(c, text=temp1, fg='yellow', bg='black', borderwidth='4', relief=RAISED)
        c.create_window(183+x//2+ j * x, 264, anchor='center', height='30', width=x, window=label)
        labelvis.append(label)
        label = Label(c, text=temp2, fg='yellow', bg='black', borderwidth='4', relief=RAISED)
        c.create_window(183+x//2+ j * x, 464, anchor='center', height='30', width=x, window=label)
        labelvis.append(label)
        colorval1 = "#%02x%02x%02x" % (val1,val1,50)
        colorval2 = "#%02x%02x%02x" % (val2,val2,50)
        colorval3 = "#%02x%02x%02x" % (val3,val3,50)
        c.create_rectangle(183+j*x,84,183+(j+1)*x,184,fill = colorval1)
        c.create_rectangle(183 + j * x, 284, 183 + (j + 1) * x, 384, fill=colorval2)
        c.create_rectangle(183 + j * x, 484, 183 + (j + 1) * x, 584, fill=colorval3)
        
''' -------------------------------------------------------------------------------
----------------------------FUNCTION TO START SIMULATION --------------------------
-----------------------------------------------------------------------------------'''

# GUI related function
def flow_visual():
    global c
    alist = root.winfo_children()
    for item in alist:
        if (item.winfo_children()):
            alist.extend(item.winfo_children())
    for item in alist:
        item.destroy()
    c = Canvas(root,width = '1366', height = '768')

    for i in range(edge_count):
        x = 683 - (edge_count // 2) * 100 + 50
        button = Button(c, text='LINK ' + str(i + 1))
        button.configure(width=20, fg='orange', bg='black', borderwidth='4', relief=RAISED,
                         command=partial(visualize, i))
        c.create_window(x + i * 100, 634, anchor='center', height='30', width='100', window=button)

    label = Label(c, text='AREA OCCUPANCY', fg='blue', bg='black', borderwidth='4', relief=RAISED)
    c.create_window(700, 30, anchor='center', height='30', width=146, window=label)
    label = Label(c, text='DENSITY', fg='blue', bg='black', borderwidth='4', relief=RAISED)
    c.create_window(700, 230, anchor='center', height='30', width=146, window=label)
    label = Label(c, text='FLOW', fg='blue', bg='black', borderwidth='4', relief=RAISED)
    c.create_window(700, 430, anchor='center', height='30', width=146, window=label)
    c.pack()
    dynamic_traffic_assignment()



# Starting the simulation
def start_simulation():
    global param,OD_pairs,edges,edge_pairs,OD,demand_input,demand_data,msa_flow,destination_data
    for i in range(len(param)):
        for j in range(5):
            param[i][j] = param[i][j].get()    # Converting the gui object into its corresponding value

    for i in range(len(OD_pairs)):
        for j in range(2):
            OD_pairs[i][j] = OD_pairs[i][j].get()   # Converting the gui object into its corresponding value

    # GUI related
    alist = root.winfo_children()
    for item in alist:
        if(item.winfo_children()):
            alist.extend(item.winfo_children())
    for item in alist:
        item.destroy()

    # Updating the edge dictionary storing length width density and cell number corresponding to a particular link
    for i in range(len(param)):
        n1,n2,l,w,k = int(param[i][0]),int(param[i][1]),float(param[i][2]),float(param[i][3]),int(param[i][4])
        edges[n1][n2] = [l,w,k,int(math.ceil(l/0.225))]
        edge_pairs.append([n1,n2])
        incoming_links[n2].append(i)    #Adding i to the incoming links corresponding to node n2
        outgoing_links[n1].append(i)    #Adding i to the outgoing links corresponding to node n1

    for i in range(len(OD_pairs)):
        o,d = map(int,(OD_pairs[i][0],OD_pairs[i][1]))
        OD.append([o,d])

    for i in OD:
        demand_input[i[0]][i[1]] = [0, 0, 0, 0]

    # Opening the demand1.txt file that contains the class wise demand data for each O-D pair separated by space
    file = open('demand.txt', 'r')
    demand = file.readlines()
    for i in range(len(demand)):
        demand[i] = list(map(int,demand[i].split()))    #Storing the first line corresponding to demand1 file
    for i in range(len(OD)):
        for j in range(len(demand)):
            demand_data[tuple(OD[i])].append(demand[j][i * 4:(i + 1) * 4])  #Storing four values at a time and appending that to the corresponding O-D pair in demand_data dictionary

    for i in OD:
        for j in range(simtime):
            msa_flow[(i[0],i[1])].append([0,0,0,0]) #Initializing the msa flow

    for i in OD:
        destination_data[i[1]] = [0,0,0,0] #initializing the destination flow corresponding to each destination node that stores the flow coming out of the network at every destination node

    initialize()    #Calling the initialize function
    OD_dictionary()     #Calling the OD_dictionary function
    linkpath_calculation()  #Calling the link_path calculation function
    flow_visual()  # Calling the flow visualization method
