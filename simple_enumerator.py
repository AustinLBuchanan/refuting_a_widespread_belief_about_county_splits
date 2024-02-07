import networkx as nx
import time

districts = list()
num_districts = 0
num_search_nodes = 0

def pop_ok(P, L, U, k):
    for j in range(1,k+1):
        if L*j <= P and P <= U*j:
            return True
    return False


# G = input graph
# F = forbidden vertices
# S = subset of vertices that are fixed in the solution
# P = population of S
#
def enumerate_subroutine(G, F, S, P):
    
    global num_districts 
    global start_time
    global num_search_nodes
    
    num_search_nodes += 1
    
    if time.time() - G._start_time > G._time_limit:
        return
    
    # if population of S has grown too big, then we can exit
    if P > G._U * G._size:
        return
    
    # must grow the current subset S into a neighbor of S 
    #   that is still under consideration
    choices = { j for i in S for j in G.neighbors(i) if j not in F }
    
    if choices == set():
        if G._L * G._size <= P and P <= G._U * G._size: 
            # check that components of G-S have plausible populations
            VS = [ i for i in G.nodes if i not in S ]
            for comp in nx.connected_components( G.subgraph(VS) ):
                comp_pop = sum( G.nodes[i]['TOTPOP'] for i in comp )
                if not pop_ok(comp_pop, G._L, G._U, G._k):
                    return
            districts.append( S.copy() )
            num_districts += 1
            print(num_districts, num_search_nodes, round(time.time() - G._start_time, 2), S)
        return
    
    # greedy choice: pick max population vertex
    mpc = max( G.nodes[i]['TOTPOP'] for i in choices )
    v = [ i for i in choices if G.nodes[i]['TOTPOP']==mpc ][0]
            
    F.add(v)
    S.append(v) # add v
    enumerate_subroutine(G, F, S, P+G.nodes[v]['TOTPOP'])
    
    S.pop() # remove v
    enumerate_subroutine(G, F, S, P)
    F.remove(v)
    
    
def simple_enumerator(G):
    
    G._start_time = time.time()
    
    # apply the enumeration function
    F = { G._root }
    S = [ G._root ]
    P = G.nodes[G._root]['TOTPOP']

    print("Sol# Node# Time(s) district")
    enumerate_subroutine(G, F, S, P)

    print("---",round(time.time() - G._start_time, 2),"seconds to enumerate",len(districts),"districts using",num_search_nodes,"search nodes---")
    return districts
