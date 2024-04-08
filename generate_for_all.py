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


queries = open("queries.txt", "r", encoding="utf-8").read().split("\n")
queries = list(filter(lambda x: x != '', queries))

common_links = f"""
    <a href="index.html">Index</a>
    <div style="width: 100%; display: flex; flex-direction: row; flex-wrap: wrap; gap: 20px;">
        {"".join([f"<a href='{query.replace(' ', '_')}.html'>{query}</a>" for query in queries])}
    </div>
"""

for idx, query in enumerate(queries):
    docs = collection.query(
        query_texts=query,
        n_results=15
    )
    open(f"all_htmls/{query.replace(' ', '_')}.html", "w").write(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search results</title>
    </head>
    <body>
        {common_links}
        <h1>Search results</h1>
        <ul>
            <li>Query: {query}</li>
            <li>Results:</li>
            <div style="width: 100%; display: grid; grid-template-columns: auto auto auto; gap: 20px;">
                {"".join([f"<div style='display: flex; flex-direction: column;'><div>{doc} ({round(docs['distances'][0][idx], 3)})</div> <img src='{docs['metadatas'][0][idx]['url'].replace('38.media.tumblr.com', '64.media.tumblr.com')}'></img></div>" for idx, doc in enumerate(docs["documents"][0])])}
            </div>
        </ul>
    </body>
    </html>
    """.replace("'", '"'))

    if idx == 0:
        open("all_htmls/index.html", "w").write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Search results</title>
        </head>
        <body>
            {common_links}
            <h1>Search results</h1>
            <ul>
                <li>Query: {query} </li>
                <li>Results:</li>
                <div style="width: 100%; display: grid; grid-template-columns: auto auto;">
                    {"".join([f"<div>{doc} ({round(docs['distances'][0][idx], 3)}) <img src='{docs['metadatas'][0][idx]['url'].replace('38.media.tumblr.com', '64.media.tumblr.com')}'></img></div>" for idx, doc in enumerate(docs["documents"][0])])}
                </div>
            </ul>
        </body>
        </html>
        """)
    print(f"Done {idx} queries")
