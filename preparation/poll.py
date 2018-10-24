import pandas as pd
import re
import json

with open("民調原始.txt", encoding="utf8") as file:
    data = file.read()

data = data.split("\n\n")
all_polls = []
for d in data:
# d = data[3]
    poll = {}
    d = d.split("\n")
    poll['機構'] = re.search("\D+", d[0]).group().strip()
    poll['時間'] = re.search("\d+\/\d+\/\d+", d[0]).group().strip()
    poll['訪問主題'] = d[1].split("：")[1].strip()
    poll['有效樣本'] = d[2].split("：")[1].strip()
    percents = d[3].replace("%", "% ").split()
    candidates = d[4].split()
    poll['支持率'] = dict(zip(candidates, percents))
    all_polls.append(poll)

with open('polls.json', 'w') as outfile:
    json.dump(all_polls, outfile, ensure_ascii=False)


df = pd.read_json("polls.json")