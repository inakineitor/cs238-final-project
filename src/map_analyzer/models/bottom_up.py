from gerrychain import Graph
import networkx as nx

from .graph_generating_model import GraphGeneratingModel

from random import randint, random
import matplotlib.pyplot as plt
import numpy as np

class BottomUpModel(GraphGeneratingModel):
    def __init__(self, probability: float, num_pts: int):
        """
        Constructor for this model.

        Args:
            probability (float): prob of deleting an edge from Delaunay tesselation. 
        """
        self.p_delete = probability
        self.n = num_pts


    def generate_graph(n, m, k):
        og = nx.grid_graph([n, m])
        return random_flood_fill(og, k)

    def random_flood_fill(graph, num_floods):
        nodes = list(graph.nodes())
        boundary_nodes = set(graph.nodes_boundary())
        for _ in range(num_floods):
            start_node = random.choice(nodes)
            visited = set()
            to_visit = [start_node]
            while to_visit:
                current_node = to_visit.pop()
                if current_node not in visited and current_node not in boundary_nodes:
                    visited.add(current_node)
                    neighbors = list(graph.neighbors(current_node))
                    random.shuffle(neighbors)  
                    to_visit.extend(neighbors)
            for node in visited:
                graph.remove_node(node)
        return graph
    


'''
    def generate_graph(self, seed=None) -> Graph:
        
        n = 20 #grid size
        m = 20 #grid size
        k = 20 # number of possible steps
        ns = 500
        pt = True
        grid = nx.grid_graph([n,m])
        # grid_graph returns the n x m-dimensional grid graph
        unassigned = list(grid.nodes())
        rectangles = []
        cdict={}
        move = 0

        while unassigned:
            
            ll=unassigned[0]
            uboundary = [ll]
            rboundary = [ll]
            unassigned.remove(ll)
            cdict[ll]=move
            
            numr = 0
            numu = 0
            
            
            expands = randint(0,k)
                
            for i in range(expands):
                if random() < .5:
                    #move up
                    temp = 0 
                    for j in uboundary:
                        if (j[0],j[1]+1) in unassigned:
                            temp +=1
                    if temp == len(uboundary):
                        numu += 1
                    
                        for j in range(len(uboundary)):
                            
                            if uboundary[j] in rboundary:
                                rboundary.append((uboundary[j][0],uboundary[j][1]+1))
                            
                            #grid = nx.contracted_edge(grid, (ll, (uboundary[j][0],uboundary[j][1]+1)), self_loops=False)

                            unassigned.remove((uboundary[j][0],uboundary[j][1]+1))
                            cdict[(uboundary[j][0],uboundary[j][1]+1)] = move
                            uboundary[j] = (uboundary[j][0],uboundary[j][1]+1)
                            grid = nx.contracted_nodes(grid, ll, (uboundary[j][0],uboundary[j][1]), self_loops=False)
                            
                else:
                    #move right
                    temp = 0 
                    for j in rboundary:
                        if (j[0]+1,j[1]) in unassigned:
                            temp += 1
                    if temp == len(rboundary):
                        numr += 1
                    
                        for j in range(len(rboundary)):
                            if rboundary[j] in uboundary:
                                uboundary.append((rboundary[j][0]+1,rboundary[j][1]))
                            unassigned.remove((rboundary[j][0]+1,rboundary[j][1]))
                            cdict[(rboundary[j][0]+1,rboundary[j][1])] = move
                            rboundary[j] = (rboundary[j][0]+1,rboundary[j][1])
                                    
                            #grid = nx.contracted_edge(grid, (ll, (rboundary[j][0]+1,rboundary[j][1])), self_loops=False)
                            grid = nx.contracted_nodes(grid, ll, (rboundary[j][0],rboundary[j][1]), self_loops=False)

								
            rectangles.append([ll,(ll[0]+numr,ll[1]+numu)])
            move += 1
	


        slist = list(range(max(cdict.values())+1))
        np.random.shuffle(slist)


        reverse_cdict = {x:[[],[]] for x in range(max(cdict.values())+1)}
        grid2 = nx.grid_graph([n,m])

        for node in grid2.nodes():
            reverse_cdict[cdict[node]][0].append(node[0])
            reverse_cdict[cdict[node]][1].append(node[1])
    
        fig = plt.figure()


        nx.draw(grid2,pos= {x:x for x in grid2.nodes()},node_color=[slist[cdict[x]] for x in grid2.nodes()],cmap=plt.cm.jet,node_shape='s',node_size=ns,kwds = {'zorder':1})    

        nx.draw(grid,pos= {x:(np.mean(reverse_cdict[cdict[x]][0]),np.mean(reverse_cdict[cdict[x]][1])) for x in grid.nodes()},label=True,node_color=['w' for x in grid.nodes()],node_size=25,kwds = {'zorder':100})

        #nx.draw_networkx_edges(grid,pos= {x:(np.mean(reverse_cdict[cdict[x]][0]),np.mean(reverse_cdict[cdict[x]][1])) for x in grid.nodes()},kwds = {'zorder':100},width=10)

        for edge in grid.edges():
            plt.plot([np.mean(reverse_cdict[cdict[edge[0]]][0]),np.mean(reverse_cdict[cdict[edge[1]]][0])],[np.mean(reverse_cdict[cdict[edge[0]]][1]),np.mean(reverse_cdict[cdict[edge[1]]][1])],'w')



#fig.set_facecolor("lightpink")
        plt.title("Dual Graph")
        plt.show()

#print(max(cdict.values()))
#print(slist)
#print(cdict)


        corners = nx.Graph()


        for rect in rectangles:
            corners.add_node((rect[0][0]-.5,rect[0][1]-.5))
            corners.add_node((rect[1][0]+.5,rect[1][1]+.5))
            corners.add_node((rect[0][0]-.5,rect[1][1]+.5))
            corners.add_node((rect[1][0]+.5,rect[0][1]-.5))
    
            corners.add_edge((rect[0][0]-.5,rect[0][1]-.5),(rect[0][0]-.5,rect[1][1]+.5))
            corners.add_edge((rect[0][0]-.5,rect[0][1]-.5),(rect[1][0]+.5,rect[0][1]-.5))    
            corners.add_edge((rect[1][0]+.5,rect[1][1]+.5),(rect[0][0]-.5,rect[1][1]+.5))
            corners.add_edge((rect[1][0]+.5,rect[1][1]+.5),(rect[1][0]+.5,rect[0][1]-.5))    

        plt.figure()

        nx.draw(grid2,pos= {x:x for x in grid2.nodes()},node_color=[slist[cdict[x]] for x in grid2.nodes()],cmap=plt.cm.jet,node_shape='s',node_size=25)    

        nx.draw(corners, pos = {x:x for x in corners.nodes()}, node_color = ['k' for x in corners.nodes()], node_shape='s',node_size=25)

        for edge in corners.edges():
            plt.plot([edge[0][0],edge[1][0]],[edge[0][1],edge[1][1]],'k')


        plt.title("Corners")
        plt.show()

        fig = plt.figure()

        nx.draw(grid2,pos= {x:x for x in grid2.nodes()},node_color=[slist[cdict[x]] for x in grid2.nodes()],cmap=plt.cm.jet,node_shape='s',node_size=25)    

        nx.draw(corners, pos = {x:x for x in corners.nodes()}, node_color = ['k' for x in corners.nodes()], node_shape='s',node_size=25)


        #nx.draw_networkx_edges(grid,pos= {x:(np.mean(reverse_cdict[cdict[x]][0]),np.mean(reverse_cdict[cdict[x]][1])) for x in grid.nodes()},kwds = {'zorder':100},width=10)

        for edge in grid.edges():
            plt.plot([np.mean(reverse_cdict[cdict[edge[0]]][0]),np.mean(reverse_cdict[cdict[edge[1]]][0])],[np.mean(reverse_cdict[cdict[edge[0]]][1]),np.mean(reverse_cdict[cdict[edge[1]]][1])],'w')
    
        for edge in corners.edges():
            plt.plot([edge[0][0],edge[1][0]],[edge[0][1],edge[1][1]],'k')


        nx.draw(grid,pos= {x:(np.mean(reverse_cdict[cdict[x]][0]),np.mean(reverse_cdict[cdict[x]][1])) for x in grid.nodes()},node_color=['w' for x in grid.nodes()],node_size=25)

        plt.plot([],[],'k',label="Corners")
        plt.plot([],[],'w',label="Dual Graph")

        fig.set_facecolor("lightpink")
        plt.title("Overlays")
        plt.legend()
        plt.show()


        fig = plt.figure()

        nx.draw(grid2,pos= {x:x for x in grid2.nodes()},node_color=[slist[cdict[x]] for x in grid2.nodes()],cmap=plt.cm.jet,node_shape='s',node_size=ns)    

        nx.draw(corners, pos = {x:x for x in corners.nodes()}, node_color = ['k' for x in corners.nodes()], node_shape='s',node_size=25)


#nx.draw_networkx_edges(grid,pos= {x:(np.mean(reverse_cdict[cdict[x]][0]),np.mean(reverse_cdict[cdict[x]][1])) for x in grid.nodes()},kwds = {'zorder':100},width=10)

        for edge in grid.edges():
            plt.plot([np.mean(reverse_cdict[cdict[edge[0]]][0]),np.mean(reverse_cdict[cdict[edge[1]]][0])],[np.mean(reverse_cdict[cdict[edge[0]]][1]),np.mean(reverse_cdict[cdict[edge[1]]][1])],'w')
    
        for edge in corners.edges():
            plt.plot([edge[0][0],edge[1][0]],[edge[0][1],edge[1][1]],'k')


        nx.draw(grid,pos= {x:(np.mean(reverse_cdict[cdict[x]][0]),np.mean(reverse_cdict[cdict[x]][1])) for x in grid.nodes()},node_color=['w' for x in grid.nodes()],node_size=25)

        plt.plot([],[],'k',label="Corners")
        plt.plot([],[],'w',label="Dual Graph")

        fig.set_facecolor("lightpink")
        plt.title("Overlays")
        plt.legend()
#fig.savefig('./whatever.png', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.show()

        
        graph = nx.Graph(edges)

        # Return Graph 
        return graph



# -*- coding: utf-8 -*-
do an aggregate method where each knows its
 initial neighbos at each step try to grow the rectangle 
 upwatds or rightwards (or diagonal? - not for now). Rnadom number of growth attempts (0- k). 
 
 When a new collection of nodes is merged contract those edges after checking that it is permissible
 - need to know boundary nodes so you can check the individual +1 are still in the permissible dict
 
 Start with nxn array initialized to all zeros. Set the (0,0) entry  to 1 and check 
 '''
 




	

	