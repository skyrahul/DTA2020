from imports import *
from initialize import *
from main import start_simulation

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
    nx.draw_networkx_edges(G,pos,edgelist= edges,edge_color='r')
    nx.draw_networkx_labels(G,pos,labels = node_label,font_size=16)
    nx.draw_networkx_edge_labels(G,pos,edge_labels= edge_label)
    sim = Button(root, text='Start Simulation', fg='blue', bg='white', font=("Times New Roman", 20, "bold"),command= start_simulation).grid(row= max(count + 2,17), column=1, pady='20')
    plt.show()