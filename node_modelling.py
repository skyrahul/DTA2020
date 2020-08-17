from imports import *
from initialize import *
from dta import *

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