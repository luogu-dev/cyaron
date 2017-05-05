#!/usr/bin/env python

from cyaron import *

"""Generate the data for a graph problem."""

_n = ati([0, 7, 50]) # The number of vertexs
_m = ati([0, 11, 100]) # The number of edges

for i in range(1, 3):
    test_data = IO(file_prefix="heat", data_id=i) # Open an IO object for each pair of test data

    n = _n[i] # The n for this data
    m = _m[i] # The m for this data
    s = randint(1, n) # 
    t = randint(1, n) # 
    test_data.input_writeln(n, m, s, t) # Write n,m,s,t to the input file

    graph = Graph.graph(n, m, weight_limit=5) # Generate a graph with n vertexs, m edges and weights less than 5
    test_data.input_writeln(graph) # Write the graph (the graph object will process the string)

    test_data.output_gen("~/Downloads/std_binary") # Use the solve programme to generate the output file
    
    # You don't need to close the files, the IO object will do it
