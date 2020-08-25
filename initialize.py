from imports import defaultdict

''' ---------------------------------------------------------------------
--------------------------------GLOBAL PARAMETERS------------------------
-------------------------------------------------------------------------'''

root = None # root tkinter element
classes = 4 # Number of classes of vehicles
node_count = 0   # Stores the number of nodes in the network
edge_count = 0  # Stores the number of links in the network
edges = defaultdict(lambda: defaultdict(list))   # Dictionary to store length,width,density and corresponding links
edge_pairs = []  # Edge pairs corresponding to the network
OD = []  # Stores the OD pairs corresponding to the network
param = [] # Stores the parameters input through the GUI, once the simulation starts no use
label = [] # Stores the labels of the GUI, once the simulation starts all label gets destroyed except visualization window
OD_pairs = [] # Input from the GUI related to OD pairs
labelvis = [] # Another list to store the labels of the GUI
label2 = []  # Another list to store the labels of the GUI
flag = 0 # To check if generate network button comes only once
incoming_links = defaultdict(list)  # Stores the incoming links corresponding to each node
outgoing_links = defaultdict(list)  # Stores the outgoing links corresponding to each node
incoming_flows = defaultdict(list)  # incoming flows to nodes
zipped = []     # Not of use
origin = []     # contains all the origins of O-D pairs
destination = []    # contains all the destinations of O-D pairs
OD_dict = defaultdict(lambda: defaultdict(list))    # O-D dict to store all paths from every node to every possible destination
all_paths = []  #temporary variable
b = [0.695,0.625,0.40,0.748]  # Parameter for calculation of flow_max in the first cell
area = [0.00000108,0.00000364,0.0000064,0.00001430] # area of each vehicle class
AO_critical = [0.59,0.5,0.5,0.23] # critical area occupancy for each class
AOmax = [0.89,0.83,0.83,0.5] # maximum area occupancy for each class
free_flow_speed = [45.0,42.0,52.0,47.0] # free_flow_speed for each class
jam_density = [0.89,0.78,0.74,0.5] # jam_density for each class
relaxation_time = [0.00057,0.0007,0.001,0.006] #Relaxation_time for each class
simtime = 180 # Simulation time in 10 seconds time interval  #have to increase
dt = 10/3600 # time element in hours
density,AOnot,equi_speed,speed,flow,AO = [],[],[],[],[],[]  #density, area occupancy excluding a particular vehicle class, equilibrium speed, normal speed, flow, Area_occupancy
average_speed = []  #average speed for each vehicle class,for each link,for every instant of time
link_density = [] # link density for each vehicle class for every link
average_time = [] #average time for each vehicle class,for each link,for every instant of time
edge_cost = defaultdict(list)   #Stores the travel time cost of each path
link_paths = defaultdict(list)  #Stores the edges corresponding to a particular path
link_history = defaultdict(list)    #Stores the destination nodes which a particular link vehicle is entitled to go
c = 0   #temporary variable
visual = 0  #temporary variable
demand_input = defaultdict(lambda: defaultdict(list))  # dictionary of dictionary to store the demand input for each O-D pair from the file
destination_data = defaultdict(list)    #To store the flow accumulating in all the destination nodes and going out of the network
demand_data = defaultdict(list)     #To store the class wise flow corresponding to
msa_flow = defaultdict(list)    #To store the previous flow alotted for calcualting the flow acording to msa algorithm


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