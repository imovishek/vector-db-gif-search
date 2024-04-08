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

# gifs = open("list.txt", "r", encoding="utf-8").read().split("\n")
# gifs = list(filter(lambda x: x != '', gifs))
# gifDocs = map(lambda x: [x.split("\t")[0], x.split("\t")[1], x.split("\t")[2]], gifs)


# for idx, gifDoc in enumerate(gifDocs):
#     collection.update(
#         metadatas={"id": gifDoc[2], "url": gifDoc[0]},
#         ids=gifDoc[2]
#     )
#     if idx % 500 == 0:
#         print(f"Done {idx} gifs")


query = sys.argv[1]


docs = collection.query(
    query_texts=query,
    n_results=10
)

# print(docs)

# for idx, doc in enumerate(docs["documents"][0]):
    # distance in 3 digits
    # distance = round(docs["distances"][0][idx], 3)
    # print(docs["documents"][0][idx], distance, docs["metadatas"][0][idx]["url"])

open("index.html", "w").write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Search results</title>
</head>
<body>
    <h1>Search results</h1>
    <ul>
        <li>Query: {query}</li>
        <li>Results:</li>
        <div style="width: 100%; display: grid; grid-template-columns: auto auto;">
            {"".join([f"<div>{doc} ({round(docs['distances'][0][idx], 3)}) <img src='{docs['metadatas'][0][idx]['url'].replace('38.media.tumblr.com', '64.media.tumblr.com')}'></img></div>" for idx, doc in enumerate(docs["documents"][0])])}
        </div>
    </ul>
</body>
</html>
""")
