from imports import *
from initialize import *
from dta import *
from node_modelling import *
''' ------------------------------------------------------------------------------------------
Initializing all the parameters like density, AOnot, equi_speed, speed, flow and area occupancy
-----------------------------------------------------------------------------------------------'''

def initialize():
    global density,AOnot,equi_speed,speed,flow,AO,origin,destination,zipped
    zipped = list(zip(*OD))
    origin = zipped[0]
    destination = zipped[1]
    for i in edge_pairs:
        density.append([[1.0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        AOnot.append([[0.0009 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        equi_speed.append([[1.0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        speed.append([[1.0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        flow.append([[1.0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        AO.append([0.00091 for j in range(edges[i[0]][i[1]][3] + 1)])


'''-------------------------------------------------------------------------
----------------FINDING THE PATHS(DEPTH FIRST SEARCH ALGORITHM)--------------
-----------------------------------------------------------------------------'''


def paths(u,v,visited,path):

    visited[u] = True
    path.append(u)
    total_path = path[:]
    if(u==v):
        all_paths.append(total_path)
    else:
        for i in edges[u].keys():
            if(visited[i]==False):
                paths(i,v,visited,path)
    path.pop()
    visited[u] = False

def OD_dictionary():

    global all_paths
    for i in range(1, node_count + 1):
        for j in range(1, node_count + 1):
            if (i != j and j in destination):
                visited = [False for i in range(0, node_count + 1)]
                path = []
                paths(i, j, visited, path)
                OD_dict[i][j] = all_paths
                all_paths = []

'''-----------------------------------------------------------
-----------------------LINK PATHS CALCULATION-----------------
--------------------------------------------------------------'''

def linkpath_calculation():

    global link_paths,OD_dict,link_history
    for i in OD_dict:
        for j in OD_dict[i]:
            OD_dict[i][j].append([1 / len(OD_dict[i]), 1 / len(OD_dict[i]), 1 / len(OD_dict[i]), 1 / len(OD_dict[i])])
    for i in OD_dict:
        for j in OD_dict[i]:
            index = 0
            for k in OD_dict[i][j]:
                res_list = []
                if (k == [0, 0, 0, 0]):
                    continue
                for f in range(0, len(k) - 1):
                    y = k[f:f + 2]
                    res_list.append([i for i, value in enumerate(edge_pairs) if value == y])
                for element in itertools.product(*res_list):
                    link_paths[tuple(k)] = element

    # Storing all the destination nodes that the vehicles in a particular link has to go in link history link
    for i in OD_dict:
        for j in OD_dict[i]:
            if([i,j] in OD):
                for k in range(len(OD_dict[i][j]) - 1):
                    path = OD_dict[i][j][k]
                    edge = link_paths[tuple(path)]
                    for m in edge:
                        if (j not in link_history[m]):
                            link_history[m].append(j)


''' ---------------------------------------------------------------------
---------------------CLASS   FOR   CAR  ANIMATION------------------------
-------------------------------------------------------------------------'''
#GUI related
class ImageButton(tkinter.Button):

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

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
    lab3 = Label(root, text="Length")
    lab3.grid(row=3, column=6, sticky='NSEW')
    lab4 = Label(root, text="Width")
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

''' -------------------------------------------------------------------------------
-------------------FUNCTION TO TAKE OD DETAILS FROM THE USER-----------------------
-----------------------------------------------------------------------------------'''
#GUI related
def OD_details(OD_,links):
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
        origin.grid(row=x+9+j, column=5, sticky='NSEW')
        destination = Entry(root)
        destination.grid(row=x+9+j, column=6, sticky='NSEW')
        OD_pairs.append([origin,destination])
        count = x+9+j
    edge_count = int(links.get())
    node_count = int(nodes.get())
    average_speed = [[[0 for i in range(4)] for j in range(simtime)] for k in range(edge_count)]
    link_density = [[0 for i in range(4)] for j in range(edge_count)]
    average_time = [[[0 for i in range(4)] for j in range(simtime)] for k in range(edge_count)]
    submit = Button(root, text='Generate Network', fg='blue', bg='white', font=("Times New Roman", 20, "bold"),command=lambda: generate_graph(param, count))
    if(flag==0):
        flag+=1
        submit.grid(row= max(count + 1,16), column=1, pady='50')

''' -------------------------------------------------------------------------------
-------------------FUNCTION TO GENERATE GRAPH BASED ON INPUT DATA------------------
-----------------------------------------------------------------------------------'''
#GUI related
def generate_graph(param,count):
    global node_count,edge_count
    G = nx.Graph()
    edges = []
    node = [i+1 for i in range(node_count)]
    start, end, length, width, density = zip(*param)
    for i in range(edge_count):
        edges.append([int(start[i].get()),int(end[i].get())])
    G.add_nodes_from(node)
    G.add_edges_from(edges)
    edge_label = defaultdict(int)
    node_label = defaultdict(int)
    for i in range(len(edges)):
        edge_label[tuple(edges[i])] = i+1
    for i in range(len(node)):
        node_label[i+1] = i+1
    pos = nx.random_layout(G)
    nx.draw_networkx_nodes(G,pos,nodelist = node)
    nx.draw_networkx_edges(G,pos,arrowstyle='>',arrowsize=25,edgelist= edges,edge_color='r')
    nx.draw_networkx_labels(G,pos,labels = node_label,font_size=16)
    nx.draw_networkx_edge_labels(G,pos,edge_labels= edge_label)
    sim = Button(root, text='Start Simulation', fg='blue', bg='white', font=("Times New Roman", 20, "bold"),command= start_simulation).grid(row= max(count + 2,17), column=1, pady='20')
    plt.show()

''' -------------------------------------------------------------------------------
----------------------------FUNCTION TO START SIMULATION --------------------------
-----------------------------------------------------------------------------------'''

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

    #GUI related
    lbl = ImageButton(root, text='Simulation In Progress.....', fg='orange', bg='black',font=("Times New Roman", 30, "bold"), compound=tkinter.TOP, command=flow_visual)
    lbl.pack(fill = 'both',expand ='YES')
    #lbl.load('D:\\Node_practice\\car.gif')

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
    print("check 0")   
    for i in range(len(OD)):
        for j in range(len(demand)):
            demand_data[tuple(OD[i])].append(demand[j][i * 4:(i + 1) * 4])  #Storing four values at a time and appending that to the corresponding O-D pair in demand_data dictionary
    print("check 1")
    for i in OD:
        for j in range(simtime):
            msa_flow[(i[0],i[1])].append([0,0,0,0]) #Initializing the msa flow

    for i in OD:
        destination_data[i[1]] = [0,0,0,0] #initializing the destination flow corresponding to each destination node that stores the flow coming out of the network at every destination node

    initialize()    #Calling the initialize function
    OD_dictionary()     #Calling the OD_dictionary function
    linkpath_calculation()  #Calling the link_path calculation function
    print("check 2")
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

''' -------------------------------------------------------------------------------
----------------------------INITIALIZATION OF GUI----------- ----------------------
-----------------------------------------------------------------------------------'''


'''-----------------------------------------------------
----------------INCOMING  FLOWS  INITIALIZATION---------
--------------------------------------------------------'''

'''for i in incoming_links:
    if(i in origin and i in destination):
        incoming_flows[i] = [0,0,0,0]*(len(incoming_links[i])+2)
    elif(i in origin or i in destination):
        incoming_flows[i] = [0,0,0,0]*(len(incoming_links[i])+1)
    else:
        incoming_flows[i] = [0,0,0,0]*(len(incoming_links[i]))'''


'''-----------------------------------------------------------
----------------DEMAND  INPUT (ASSUMED CONSTANT --------------
--------------------------------------------------------------'''

'''file = open("demand1.txt", "r")
demand_data = file.readlines()
temp=[]
for i in demand_data:
    i = i.replace('\t',' ')
    temp.append(list(map(int,i.split(' '))))
sum_OD = list(map(sum,zip(*temp)))
demand = defaultdict(list)
temp = 0
for i in OD:
    demand[tuple(i)] = sum_OD[temp*4:temp*4+4]'''






# Function to first calculate the travel cost and then the turning fraction based on all or nothing assignment
def travel_cost(i,c):

    temp = defaultdict(float)   # temporary defaultdict to store values
    turning_fraction = defaultdict(list)   # default dict to store the turning_fraction of the vehicles at a node
    for j in OD_dict[i]:
        minimum = sys.maxsize
        for k in range(len(OD_dict[i][j]) - 1):
            path = OD_dict[i][j][k]
            edge = link_paths[tuple(path)]
            temp[edge[0]] = edge_cost[edge][c]
            if(edge_cost[edge][c]<minimum):
                minimum = edge_cost[edge][c]

        for m in incoming_links[i]:
            if j in link_history[m]:
                for k in outgoing_links[i]:
                    if (temp[k] == minimum):
                        turning_fraction[(m, k)] = 1/len(link_history[m])
                    else:
                        turning_fraction[(m, k)] = 0
            else:
                for k in outgoing_links[i]:
                    turning_fraction[(m,k)] = 0

        if i in origin:
            if [i,j] in OD:
                for k in outgoing_links[i]:
                    if(temp[k]==minimum):
                        turning_fraction[('o',k)] = 1/2 #mfmd
                    else:
                        turning_fraction[('o',k)] = 0
            else:
                for k in outgoing_links[i]:
                    turning_fraction[('o',k)] = 0

        if i in destination:
            for m in incoming_links[i]:
                turning_fraction[(m,'d')] = 1/len(incoming_links[i])
    return turning_fraction


'''--------------------------------------------------------------------------
---------------------DYNAMIC  TRAFFIC  ASSIGNMENT----------------------------
-----------------------------------------------------------------------------'''
cla = [5000,2500,1000,500]
row=1


''' ----------------------------------------------------------------------------------
Entire section below is related to the GUI development using tkinter library functions
 -------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    root = tkinter.Tk()         #GUI related
    root.geometry('1366x768')   #GUI related
    root.configure(background='powderblue')     #GUI related
    root.title('Dynamic Traffic Assignment Simulator')  #GUI related
    title = Label(root, text="DYNAMIC TRAFFIC ASSIGNMENT SIMULATOR", fg='orange', bg='black',
                  font=("Times New Roman", 20, "bold")).grid(row=0, columnspan=10, sticky='NSEW', ipady='10',
                                                             ipadx='380')      #GUI related

    lab1 = Label(root, text=" ", bg='powderblue').grid(row=1, column=0, sticky='W')     #GUI related
    lab2 = Label(root, text=" ", bg='powderblue').grid(row=2, column=0, sticky='W')     #GUI related
    lab3 = Label(root, text="Enter the number of nodes").grid(row=3, column=0, sticky='NSEW')   #GUI related
    nodes = Entry(root)     #GUI related
    nodes.grid(row=3, column=1, sticky='W')     #GUI related

    lab1 = Label(root, text=" ", bg='powderblue').grid(row=4, column=0, sticky='W')     #GUI related
    lab2 = Label(root, text=" ", bg='powderblue').grid(row=5, column=0, sticky='W')     #GUI related
    bn = Label(root, text="Enter the number of links").grid(row=6, column=0, sticky='NSEW')     #GUI related
    links = Entry(root)     #GUI related
    links.grid(row=6, column=1, sticky='W')     #GUI related

    lab1 = Label(root, text=" ", bg='powderblue').grid(row=7, column=0, sticky='W')     #GUI related
    lab2 = Label(root, text=" ", bg='powderblue').grid(row=8, column=0, sticky='W')     #GUI related
    bn = Button(root, text="Enter the link details", fg='blue', bg='white', font=("Times New Roman", 10, "bold"),
                command=lambda: edge_details(links)).grid(row=9, column=0, sticky='E', ipadx='20')  #GUI related

    lab1 = Label(root, text=" ", bg='powderblue').grid(row=10, column=0, sticky='W')    #GUI related
    lab2 = Label(root, text=" ", bg='powderblue').grid(row=11, column=0, sticky='W')    #GUI related
    button = Label(root, text="Enter the number of O-D pairs").grid(row=12, column=0, sticky='NSEW')    #GUI related
    OD_ = Entry(root)    # GUI related
    OD_.grid(row=12, column=1, sticky='W')  #GUI relatedd

    lab1 = Label(root, text=" ", bg='powderblue').grid(row=13, column=0, sticky='W')    #GUI related
    lab2 = Label(root, text=" ", bg='powderblue').grid(row=14, column=0, sticky='W')    #GUI related
    bn = Button(root, text="Enter the O-D details", fg='blue', bg='white', font=("Times New Roman", 10, "bold"),command=lambda: OD_details(OD_, links)).grid(row=15, column=0, sticky='E', ipadx='20')
    root.mainloop()#GUI related

'''-------------------------------------------------------------------------------------------------------------
------------------------------------------------END OF THE PROJECT----------------------------------------------
----------------------------------------------------------------------------------------------------------------'''
