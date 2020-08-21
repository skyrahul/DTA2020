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


