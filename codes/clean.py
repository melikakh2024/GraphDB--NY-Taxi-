import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal,BNode,XSD
import networkx as nx
import matplotlib.pyplot as plt

## Reading the parquet file and creating the edges
df=pd.read_parquet("taxi.parquet")
df=df[["PULocationID","DOLocationID","total_amount"]]
edges=df.groupby(["PULocationID","DOLocationID"]).size().reset_index(name="count_trips")
edges=edges[edges["PULocationID"]!=edges["DOLocationID"]]

## defining the graph
g = Graph()
EX = Namespace("http://example.org/")
for i, chunk in edges.iterrows():
    src = EX[str(chunk["PULocationID"])]
    dst = EX[str(chunk["DOLocationID"])]
    g.add((src, EX.hasToTrip, dst))

### business question3
df2=df.head(100000)
for index,row in df2.iterrows():
    src = EX[str(int(row["PULocationID"]))]
    dst = EX[str(int(row["DOLocationID"]))]
    g.add((src, EX.hasToTrip, dst))
    # Reification / BNode pattern for metadata (total_amount)
    trip_node = BNode()
    g.add((trip_node,EX.source,src))
    g.add((trip_node,EX.destination,dst))
    g.add((trip_node,EX.has_total_amount,Literal(float(row["total_amount"]),datatype=XSD.float)))

# Serialize to Turtle string
g.serialize(destination='knowledge_graph.ttl', format='turtle')
print("Saved to knowledge_graph.ttl")




