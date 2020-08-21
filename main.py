from edge_details import *;
from imports import *;
from initialize import *;


''' ------------------------------------------------------------------------------------------
Initializing all the parameters like density, AOnot, equi_speed, speed, flow and area occupancy
-----------------------------------------------------------------------------------------------'''

def initialize():
    global density,AOnot,equi_speed,speed,flow,AO,origin,destination,zipped
    zipped = list(zip(*OD))
    origin = zipped[0]
    destination = zipped[1]
    for i in edge_pairs:
        density.append([[0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        AOnot.append([[0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        equi_speed.append([[0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        speed.append([[0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        flow.append([[0 for j in range(edges[i[0]][i[1]][3] + 1)] for k in range(4)])
        AO.append([0 for j in range(edges[i[0]][i[1]][3] + 1)])


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

    flow_visual()  # Calling the flow visualization method

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
    file = open('demand1.txt', 'r')
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

'''-----------------------------------------------------
----------------NODE  MODELLING  FOR  NODES ------------
--------------------------------------------------------'''


demand_input = defaultdict(lambda: defaultdict(list))  # dictionary of dictionary to store the demand input for each O-D pair from the file
destination_data = defaultdict(list)    #To store the flow accumulating in all the destination nodes and going out of the network
demand_data = defaultdict(list)     #To store the class wise flow corresponding to
msa_flow = defaultdict(list)    #To store the previous flow alotted for calcualting the flow acording to msa algorithm

def node_modelling(t,n,vclass):

    global demand_input,destination_data #global variables so that update gets reflected in the original variables
    tfraction = defaultdict(list)  # Turning flow for node modelling
    space_coeff = defaultdict(list)  # Space coefficient for node modelling
    for i in range(1,node_count+1):  # Loop to allocate flow to the first cell of the origin nodes

        # For every O-D pair taking the demand_input according to the msa algorithm
        if i in origin:
            for j in destination:
                if([i,j] in OD):
                    for c in range(4): #Iterating for each class of vehicles
                        demand_input[i][j][c] += (1/n)*demand_data[(i,j)][t][c] + ((n-1)/n)*msa_flow[(i,j)][t][c] # MSA Algorithm

        for c in range(4):
            temp = travel_cost(i, c) #For every class of vehicles for a particular node function to return turning fraction
            for j in incoming_links[i]: #Iterating for each incoming link to the ith node
                x = edge_pairs[j]
                last_cell = flow[j][c][edges[x[0]][x[1]][3]] # Here last cell is the flow corresponding to the last cell
                for k in outgoing_links[i]: # For each outgoing link from the ith node multiplying the flow in the last cell of the incoming link to the turning fraction
                    tfraction[(j,k)].append(last_cell*temp[(j,k)]) # Appending the class wise turning flow corresponding to (j,k) link pair

            # If i is the origin taking one more virtual link into account and calculating the turning flow for that link also
            if i in origin:
                for k in outgoing_links[i]:
                    tot=0
                    for j in link_history[k]:
                        tot+=demand_input[i][j][c]
                    tfraction[('o',k)].append(tot*temp[('o',k)])  # o stand for origin

            # If i is the destination one more virtual link is taken into acount and turning fraction is calculated
            if i in destination:
                for j in incoming_links[i]:
                    x = edge_pairs[j]
                    last_cell = flow[j][c][edges[x[0]][x[1]][3]]
                    if i in link_history[j]:
                        tfraction[(j,'d')].append(last_cell * temp[(j,'d')]) # d stands for destination

        for c in range(4):
            for j in outgoing_links[i]:
                total = 0
                for k in incoming_links[i]:
                    total += tfraction[(k,j)][c]
                total+=tfraction[('o',j)][c] if(('o',j) in tfraction) else 0
                for k in incoming_links[i]:
                    if(total!=0):
                        space_coeff[(j,k)].append(tfraction[(k,j)][c]/total)
                    else:
                        space_coeff[(j,k)].append(1)
                if (total != 0):
                    space_coeff[(j,'o')].append(tfraction[('o', j)][c] / total)     # Calcualting the space coefficient
                else:
                    space_coeff[(j, 'o')].append(1)

            # If i is in destination calculating space coefficient for that virtual link also
            if i in destination:
                total=0
                for k in incoming_links[i]:
                    total += tfraction[(k, 'd')][c]
                for k in incoming_links[i]:
                    if (total != 0):
                        space_coeff[('d', k)].append(tfraction[(k, 'd')][c] / total)
                    else:
                        space_coeff[('d', k)].append(1 / 2)

        # For restricting the flow according to the AO critial based on the formula given by you
        max_flow = defaultdict(list)
        for c in range(4):
            for j in outgoing_links[i]:
                temp = 0
                if(AO[j][0]>=AO_critical[c]):
                    temp = density[j][c][0] * free_flow_speed[c] * math.exp((-1/b[c])*pow((AO[j][0]/AO_critical[c]),b[c]))
                else:
                    temp = density[j][c][0] * free_flow_speed[c] * math.exp((-1 / b[c]))
                max_flow[j].append(temp)

        # Assigning the flows
        for j in incoming_links[i]:
            for k in outgoing_links[i]:
                for c in range(4):
                    x = edge_pairs[j]
                    last_cell = flow[j][c][edges[x[0]][x[1]][3]]
                    first_cell = max_flow[k][c]
                    demand = tfraction[(j,k)][c]
                    supply = first_cell * space_coeff[(k,j)][c]
                    if(demand<supply):
                        flow[k][c][0] += demand
                        flow[j][c][edges[x[0]][x[1]][3]]-=demand
                    else:
                        flow[k][c][0] += supply
                        flow[j][c][edges[x[0]][x[1]][3]]-=supply

        # if i is origin flow needs to be alotted also according to the demand
        if i in origin:
            for k in outgoing_links[i]:
                for c in range(4):
                    first_cell = max_flow[k][c]
                    demand = tfraction[('o',k)][c]
                    supply = first_cell*space_coeff[(k,'o')][c]
                    if(demand<supply):
                        flow[k][c][0] += demand
                        for j in link_history[k]:
                            demand_input[i][j][c]-=demand/len(link_history[k])
                            msa_flow[(i,j)][t][c] = demand/len(link_history[k])
                    else:
                        flow[k][c][0] += supply//2
                        for j in link_history[k]:
                            demand_input[i][j][c] -= supply / len(link_history[k])
                            msa_flow[(i,j)][t][c] = supply / len(link_history[k])

        # If i is in destination flow needs to be removed from the network
        if i in destination:
            for k in incoming_links[i]:
                for c in range(4):  #supply will always be greater as destination is considered infinite capacity
                    demand = tfraction[('o',k)][c]
                    destination_data[i][c]+=demand
                    flow[k][c][edges[x[0]][x[1]][3]]-=demand

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
def dynamic_traffic_assignment():

    global density, AOnot, equi_speed, speed, flow, AO, average_speed, link_density, average_time, edge_cost, visual,row,sheet  #values are made global so that it can be updated inside the function
    for n in range(1, 5000):        # Number of iterations
        print("Iteration " + str(n) + " started")   #Printing the corresponding iteration
        li = 0  # link_index
        for i in edge_pairs:    #Iterating for each link in the network
            # Iterating for each cell in the corresponding link
            for x in range(edges[i[0]][i[1]][3] + 1):   # Here edges[i[0]][i[1]][3] gives the number of cells in the corresponding link
                density[li][0][x], density[li][1][x], density[li][2][x], density[li][3][x] = 100,40,200,20  # Allocating initial density to the cells
                # Calculating area_occupancy for all the cells belonging to a particular index
                AO[li][x] = (area[0] * density[li][0][x] + area[1] * density[li][1][x] + area[2] * density[li][2][x] + area[3] * density[li][3][x]) / edges[i[0]][i[1]][1]

                if (AO[li][x] < 0.0019):    #Checking if the area_occupancy is less than 0.0019 which is the lower bound
                    AO[li][x] = 0.0019
                if (AO[li][x] > AOmax[0]):  #Checking if the area occupancy is greater than 0.89 which is the upper bound
                    AO[li][x] = AOmax[0]

                # Calculating area occupancy excluding the area occupancy for a particular class of vehicle
                # Here edges[i[0]][i[1]][1] gives the corresponding width of the link
                AOnot[li][0][x] = (area[1] * density[li][1][x] + area[2] * density[li][2][x] + area[3] *density[li][3][x]) / edges[i[0]][i[1]][1]
                AOnot[li][1][x] = (area[0] * density[li][0][x] + area[2] * density[li][2][x] + area[3] *density[li][3][x]) / edges[i[0]][i[1]][1]
                AOnot[li][2][x] = (area[1] * density[li][1][x] + area[0] * density[li][0][x] + area[3] *density[li][3][x]) / edges[i[0]][i[1]][1]
                AOnot[li][3][x] = (area[1] * density[li][1][x] + area[2] * density[li][2][x] + area[0] *density[li][0][x]) / edges[i[0]][i[1]][1]

                for c in range(4): #Iterating for all the classes of vehicles
                    # Calculating the equilibrium speed according to the formula given
                    equi_speed[li][c][x] = min(free_flow_speed[c], max(3.0, (free_flow_speed[c] * (1.0 - math.exp(1.0 - math.exp(jam_density[c] * (AOmax[c] / AO[li][x] - 1.0)))))))
                    speed[li][c][x] = equi_speed[li][c][x] # Equating the speed to the quilibrium speed as the initial condition
                    flow[li][c][x] = density[li][c][x] * speed[li][c][x]    #Calculating the flow
            li += 1 #Updating the link_index that is the counter variable for repeating the same process for the next link

        current_density = [[0 for i in range(edges[i[0]][i[1]][3] + 1)] for j in range(4)] #This is to store the updated density based on the equation
        current_speed = [[0 for i in range(edges[i[0]][i[1]][3] + 1)] for j in range(4)]    #This is to store the updated speed based on the equation
        for t in range(1, simtime):     # Loop for iterating through the simulation time (180 in our case)
            li = 0  # Counter to iterate over each link
            for i in edge_pairs:    #Iterating through each link
                for vclass in range(4): #Iterating for each class of vehicle
                    if(t==1):   #For 1st time interval assigning some random flows to the origin nodes toward the outgoing links to avoid math errors
                        if i in origin:
                            for j in outgoing_links[i]:
                                flow[j][vclass][0] =  (1/n)*cla[c] + ((n-1)/n)*cla[c]
                    else:
                        node_modelling(t,n,vclass)  #Referring the node_modelling function and passing the time,iteration number and class of vehicle
                    speed[li][c][0] = free_flow_speed[c]
                    density[li][c][0] = flow[li][c][0]/speed[li][c][0]
                    equi_speed[li][c][0] = free_flow_speed[c]

                # ALL CODE BELOW THIS ARE THE SAME LOGIC AS YOUR CODE
                for c in range(4):
                    for x in range(1, edges[i[0]][i[1]][3]):
                        param1 = math.exp(jam_density[c] * (AOmax[c] / AO[li][x] - 1))
                        param2 = math.exp(1 - param1)
                        diffuk = -1 * (AOmax[c] * area[c] * jam_density[c] * free_flow_speed[c] * param1 * param2) / (edges[i[0]][i[1]][1] * pow(AO[li][x], 2))
                        diffuao = -1 * (AOmax[c] * jam_density[c] * free_flow_speed[c] * param1 * param2) / pow(AO[li][x], 2)
                        diffuaok = ((AOmax[c] ** 2) * area[c] * (jam_density[c] ** 2) * free_flow_speed[c] * param1 * param2)/(edges[i[0]][i[1]][1] * (AO[li][x] ** 4)) - ((AOmax[c] ** 2) * area[c] * (jam_density[c] ** 2) * free_flow_speed[c] * math.exp(jam_density[c] * (AOmax[c] / AO[li][x] - 1) * 2) * param2) / (edges[i[0]][i[1]][1] * (AO[li][x] ** 5)) + (AOmax[c] * area[c] * jam_density[c] * free_flow_speed[c] * param1 * param2 * 2) / (edges[i[0]][i[1]][1] * (AO[li][x] ** 3))
                        propagation_speed = min(speed[li][c][x], (speed[li][c][x] + diffuao + density[li][c][x] * (diffuk + diffuaok)))
                        current_density[c][x] = density[li][c][x] - (dt / 0.225) * (density[li][c][x] * speed[li][c][x + 1] - density[li][c][x - 1] * speed[li][c][x])
                        if (propagation_speed >= 0):
                            current_speed[c][x] = speed[li][c][x] - (dt / 0.225) * speed[li][c][x] * (
                                    speed[li][c][x] - speed[li][c][x - 1]) - (propagation_speed - speed[li][c][x]) * (diffuao * (
                                    AOnot[li][c][x] - AOnot[li][c][x - 1]) + diffuk * (density[li][c][x] - density[li][c][x - 1])) + (dt / relaxation_time[c]) * (
                                                          equi_speed[li][c][x] - speed[li][c][x])
                        else:
                            current_speed[c][x] = speed[li][c][x] - (dt / 0.225) * speed[li][c][x] * (
                                    speed[li][c][x + 1] - speed[li][c][x]) - (propagation_speed - speed[li][c][x]) * (diffuao * (
                                    AOnot[li][c][x + 1] - AOnot[li][c][x]) + diffuk * (density[li][c][x + 1] - density[li][c][x])) + (
                                                          dt / relaxation_time[c]) * (equi_speed[li][c][x] - speed[li][c][x])

                    for c in range(4):
                        for x in range(1, edges[i[0]][i[1]][3]):

                            density[li][c][x] = max(0, current_density[c][x])
                            if (current_speed[c][x] < 0):
                                speed[li][c][x] = equi_speed[li][c][x]
                            else:
                                speed[li][c][x] = min(free_flow_speed[c], max(1.0, current_speed[c][x]))
                            flow[li][c][x] = density[li][c][x] * speed[li][c][x]

                        density[li][c][edges[i[0]][i[1]][3]] = density[li][c][edges[i[0]][i[1]][3] - 1]
                        speed[li][c][edges[i[0]][i[1]][3]] = speed[li][c][edges[i[0]][i[1]][3] - 1]
                        flow[li][c][edges[i[0]][i[1]][3]] = density[li][c][edges[i[0]][i[1]][3]] *speed[li][c][edges[i[0]][i[1]][3]]
                    for x in range(1, edges[i[0]][i[1]][3] + 1):
                        AO[li][x] = (area[0] * density[li][0][x] + area[1] * density[li][1][x] + area[2] *density[li][2][x] + area[3] * density[li][3][x]) / edges[i[0]][i[1]][1]
                        AOnot[li][0][x] = min(AOmax[0] - area[0] * density[li][0][x] / edges[i[0]][i[1]][1], (area[1] * density[li][1][x] + area[2] * density[li][2][x] + area[3] *density[li][3][x]) / edges[i[0]][i[1]][1])
                        AOnot[li][1][x] = min(AOmax[0] - area[1] * density[li][1][x] / edges[i[0]][i[1]][1], (area[0] * density[li][0][x] + area[2] * density[li][2][x] + area[3] *density[li][3][x]) / edges[i[0]][i[1]][1])
                        AOnot[li][2][x] = min(AOmax[0] - area[2] * density[li][2][x] / edges[i[0]][i[1]][1], (area[1] * density[li][1][x] + area[0] * density[li][0][x] + area[3] *density[li][3][x]) / edges[i[0]][i[1]][1])
                        AOnot[li][3][x] = min(AOmax[0] - area[3] * density[li][3][x] / edges[i[0]][i[1]][1], (area[1] * density[li][1][x] + area[2] * density[li][2][x] + area[0] *density[li][0][x]) / edges[i[0]][i[1]][1])
                        if (AO[li][x] < 0.0019):
                            AO[li][x] = 0.0019
                            for c in range(4):
                                speed[li][c][x] = free_flow_speed[c]

                        if (AO[li][x] >= AOmax[0]):
                            for c in range(4):
                                speed[li][c][x] = 0
                            AO[li][x] = AOmax[0]

                        for c in range(4):
                            if (AO[li][x] >= AOmax[c]):
                                speed[li][c][x] = 0
                            if (AO[li][x] <= 0.0019):
                                speed[li][c][x], equi_speed[li][c][x], AO[li][x] = free_flow_speed[c], free_flow_speed[c], 0.0019
                            else:
                                equi_speed[li][c][x] = min(free_flow_speed[c], max(0.0, (free_flow_speed[c] * (1.0 - math.exp(1.0 - math.exp(jam_density[c] * (AOmax[c] / AO[li][x] - 1.0)))))))

                #Calculating the average_time for each of the links
                for c in range(4):
                    for x in range(1, edges[i[0]][i[1]][3]):
                        average_speed[li][t][c] += speed[li][c][x]
                        link_density[li][c] += density[li][c][x]
                    average_speed[li][t][c] = average_speed[li][t][c] / 8

                    # If average speed of the link is greater than 1 we calculate average time dividing the length by the average speed
                    if(average_speed[li][t][c]>1):
                        average_time[li][t][c] = edges[i[0]][i[1]][0] / average_speed[li][t][c]
                    # Else to avoid overflow error average time is set to infinity
                    else:
                        average_time[li][t][c] = sys.maxsize

                # FOR PRINTING THE DATA INTO EXCEL SHEET CURRENTLY ONLY FLOW IS GETTING PRINTED
                column = 1
                for j in range(1, edges[i[0]][i[1]][3]):
                    for c in range(4):
                        sheet.cell(row=row,column =column).value = flow[li][c][j]
                        column+=1
                    column+=1
                row+=1
                li+=1

            # FOR CALCULTING THE PATH COSTS (SUM OF COSTS OF ALL THE EDGES BELONGING TO THAT PATH)
            for i in link_paths:
                for c in range(4):
                    cost = 0
                    for j in range(len(link_paths[i])):
                        cost += average_time[link_paths[i][j]][t][c]
                    edge_cost[link_paths[i]].append(cost)
            visualize(visual) #GUI related
            root.update()   #GUI related
            time.sleep(0.2) #Time interval for every update of the GUI in seconds..can be adjusted for visualizing slower or faster
            wb.save('D:\\Node_practice\\result.xlsx')   #Saving the data to the excel file


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
    OD_.grid(row=12, column=1, sticky='W')  #GUI related

    lab1 = Label(root, text=" ", bg='powderblue').grid(row=13, column=0, sticky='W')    #GUI related
    lab2 = Label(root, text=" ", bg='powderblue').grid(row=14, column=0, sticky='W')    #GUI related
    bn = Button(root, text="Enter the O-D details", fg='blue', bg='white', font=("Times New Roman", 10, "bold"),command=lambda: OD_details(OD_, links)).grid(row=15, column=0, sticky='E', ipadx='20')
    root.mainloop()#GUI related

'''-------------------------------------------------------------------------------------------------------------
------------------------------------------------END OF THE PROJECT----------------------------------------------
----------------------------------------------------------------------------------------------------------------'''