import geopandas as gpd

# function to draw single districts/county_clusters/multi_districts
#
def draw_single_district( filepath, filename, G, district, zoom=False ):
    
    df = gpd.read_file( filepath + filename )
    node_with_this_geoid = { G.nodes[i]['GEOID20'] : i for i in G.nodes }
    assignment = [ -1 for i in G.nodes ]

    if zoom:
        picked = { i : None for i in G.nodes }
    else:
        picked = { i : False for i in G.nodes }
    
    for i in district:
        picked[i] = True

    for u in range(G.number_of_nodes()):
        geoid = df['GEOID20'][u]
        i = node_with_this_geoid[geoid]
        assignment[u] = picked[i]

    df['assignment'] = assignment
    my_fig = df.plot(column='assignment').get_figure()
    return 

# function to draw plan
#
def draw_plan( filepath, filename, G, plan ):
    
    df = gpd.read_file( filepath + filename )
    assignment = [ -1 for i in G.nodes ]
    labeling = { i : j for j in range(len(plan)) for i in plan[j] }
    node_with_this_geoid = { G.nodes[i]['GEOID20'] : i for i in G.nodes }

    for u in range(G.number_of_nodes()):
        geoid = df['GEOID20'][u]
        i = node_with_this_geoid[geoid]
        assignment[u] = labeling[i]

    df['assignment'] = assignment
    my_fig = df.plot(column='assignment').get_figure()
    return 
