import json

array = []

with open("stopwords.txt", encoding="utf-8") as r:
    for i in r:
        n = i.lower().split(" ")
        if n != "":
            array.append(n)
            
with open("stopwords.json", "w", encoding="utf-8") as e:
    json.dump(array, e)