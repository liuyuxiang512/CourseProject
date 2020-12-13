import json

data = []
with open("../data/tweets.json", "r") as file2read:
    for line in file2read.readlines():
        try:
            line = json.loads(line)
            data.append(line)
        except:
            continue

print(len(data))

data = sorted(data, key=lambda item: item["created_at"], reverse=True)

with open("../data/sorted_tweets.json", "w") as file2write:
    for line in data:
        line = json.dumps(line)
        file2write.write(line + "\n")
