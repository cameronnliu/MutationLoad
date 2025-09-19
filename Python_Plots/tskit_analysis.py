#!/usr/bin/python

#import necessary packages
import tskit
import math
import sys
import io
import numpy as np
import pandas as pd
import os
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description="Output of coalescent Ne of simulation")
parser.add_argument("popsize", type=int, help="Input census population size:")

# Parse command-line arguments
args = parser.parse_args()

#read tables for tskit
with open('sitetable.txt') as f:
    sites = f.read()

with open('nodetable.txt') as f:
    nodes = f.read()

with open('mutationtable.txt') as f:
    mutations = f.read()

with open('edgetable.txt') as f:
    edges = f.read()

#load in the tree sequence data
ts = tskit.load_text(
    nodes = io.StringIO(nodes),
    edges = io.StringIO(edges),
    sites = io.StringIO(sites),
    mutations = io.StringIO(mutations),
    strict = False)

#ts_2 = TableCollection.tree_sequence("tables.trees")

num_samples = ts.get_sample_size()
print(f"the size of the sample of text-based ts is {num_samples}.")
#num_samples = ts_2.get_sample_size()
#print(f"the size of the sample of direct load ts is {num_samples}.")

N = args.popsize

#Calculating Average branch length between pair of sample nodes
print("Calculating coalescent Ne: ", f'{(ts.diversity(mode="branch"))/(2*N)}')