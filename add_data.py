import sys

import chromadb
from flask import Flask

client = chromadb.HttpClient(host="localhost", port=8000)

print(client.list_collections())
collection = client.get_collection("gifs")

# collection.add(
#     documents=['something different'],
#     ids=['#3']
# )

gifs = open("tgif-v1.0.tsv", "r", encoding="utf-8").read().split("\n")
gifs = list(filter(lambda x: x != '', gifs))
gifDocs = [[x.split("\t")[0], x.split("\t")[1], f"#{i+1}"] for i,x in enumerate(gifs)]


for idx, gifDoc in enumerate(gifDocs):
    if idx < 10000:
        continue
    collection.add(
        documents=gifDoc[1],
        metadatas={"id": gifDoc[2], "url": gifDoc[0]},
        ids=gifDoc[2]
    )
    if idx % 500 == 0:
        print(f"Done {idx} gifs")

doc = collection.get(
    ids=["#1"]
)

print(doc)
