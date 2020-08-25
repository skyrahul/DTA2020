from imports import *
from initialize import *

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