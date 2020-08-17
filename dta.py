from imports import *
from initialize import *

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
                                flow[j][vclass][0] =  (1/n)*cla[vclass] + ((n-1)/n)*cla[vclass]
                    else:
                        node_modelling(t,n,vclass)  #Referring the node_modelling function and passing the time,iteration number and class of vehicle
                    speed[li][c][0] = free_flow_speed[c]
                    density[li][c][0] = flow[li][c][0]/speed[li][c][0]
                    equi_speed[li][c][0] = free_flow_speed[c]

                # ALL CODE BELOW THIS ARE THE SAME LOGIC AS YOUR CODE
                for c in range(4):
                    for x in range(1, edges[i[0]][i[1]][3]+1):
                        param1 = math.exp(jam_density[c] * (AOmax[c] / AO[li][x] - 1))
                        param2 = math.exp(1 - param1)
                        diffuk = -1 * (AOmax[c] * area[c] * jam_density[c] * free_flow_speed[c] * param1 * param2) / (edges[i[0]][i[1]][1] * pow(AO[li][x], 2))
                        diffuao = -1 * (AOmax[c] * jam_density[c] * free_flow_speed[c] * param1 * param2) / pow(AO[li][x], 2)
                        uao[c][x] = diffuao
                        diffuaok = ((AOmax[c] ** 2) * area[c] * (jam_density[c] ** 2) * free_flow_speed[c] * param1 * param2)/(edges[i[0]][i[1]][1] * (AO[li][x] ** 4)) - ((AOmax[c] ** 2) * area[c] * (jam_density[c] ** 2) * free_flow_speed[c] * math.exp(jam_density[c] * (AOmax[c] / AO[li][x] - 1) * 2) * param2) / (edges[i[0]][i[1]][1] * (AO[li][x] ** 5)) + (AOmax[c] * area[c] * jam_density[c] * free_flow_speed[c] * param1 * param2 * 2) / (edges[i[0]][i[1]][1] * (AO[li][x] ** 3))
                        propagation_speed = min(speed[li][c][x], (speed[li][c][x] + diffuao + density[li][c][x] * (diffuk + diffuaok)))
                        current_density[c][x] = density[li][c][x] - (dt / 0.225) * (density[li][c][x] * speed[li][c][x + 1] - density[li][c][x - 1] * speed[li][c][x])
                        if(x==edges[i[0]][i[1]][3]):
                            current_density[c][x] = density[li][c][x] - (dt / 0.225) * (flow[li][c][edges[x[0]][x[1]][3]] - density[li][c][x - 1] * speed[li][c][x])
                        if(x==1):
                            current_density[c][x] = density[li][c][x] - (dt / 0.225) * (density[li][c][x] * speed[li][c][x + 1] - flow[li][c][0])
                        
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
                    for x in range(1, edges[i[0]][i[1]][3]+1):

                        density[li][c][x] = max(0, current_density[c][x])
                        if (current_speed[c][x] < 0):
                            speed[li][c][x] = equi_speed[li][c][x]
                        else:
                            speed[li][c][x] = min(free_flow_speed[c], max(1.0, current_speed[c][x]))
                        
                        kcr[li][c][x]=max(0.0,-1.0*speed[li][c][x]*edges[i[0]][i[1]][1]/(area[c]*uao[c][x]))                       
                       
                        flow[li][c][x] = max(density[li][c][x] * speed[li][c][x], kcr[li][c][x]*speed[li][c][x])

                    #density[li][c][edges[i[0]][i[1]][3]] = density[li][c][edges[i[0]][i[1]][3] - 1]
                    #speed[li][c][edges[i[0]][i[1]][3]] = speed[li][c][edges[i[0]][i[1]][3] - 1]
                    #flow[li][c][edges[i[0]][i[1]][3]] = density[li][c][edges[i[0]][i[1]][3]] *speed[li][c][edges[i[0]][i[1]][3]]
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
                    average_speed[li][t][c] = average_speed[li][t][c] / edges[i[0]][i[1]][3]

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
            wb.save('G:\\result.xlsx')   #Saving the data to the excel file
