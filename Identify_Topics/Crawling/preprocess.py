import json
import itertools
import gc


def merge_data():
    data = []
    with open("data/sorted_tweets_owl.json", "r") as file2read:
        for line in file2read.readlines():
            line = json.loads(line)
            data.append(line)

    data_tmp = itertools.groupby(data)
    del data
    gc.collect()
    data = []
    for key, value in data_tmp:
        data.append(key)
    data_tmp = sorted(data, key=lambda item: item["created_at"], reverse=True)
    del data
    gc.collect()
    data = []
    previous_line = None
    for line in data_tmp:
        if line != previous_line:
            data.append(line)
        previous_line = line
    del data_tmp
    gc.collect()
    print(len(data))  # 681223

    with open("data/sorted_tweets.json", "w") as file2write:
        for line in data:
            line = json.dumps(line)
            file2write.write(line + "\n")


if __name__ == "__main__":
    merge_data()
