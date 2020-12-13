import tweepy
import json

# Twitter keys
with open("../../authentication.txt", "r") as file2read:
    info = file2read.read().strip().split("\n")
consumer_key = info[0]
consumer_secret = info[1]
access_token = info[2]
access_token_secret = info[3]

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def process_status(status):
    id = status.id
    status_dict = {"created_at": str(status.created_at), "id": status.id, "id_str": status.id_str,
                   "text": status.text, "entities": status.entities, "source": status.source,
                   "source_url": status.source_url, "in_reply_to_status_id": status.in_reply_to_status_id,
                   "in_reply_to_status_id_str": status.in_reply_to_status_id_str,
                   "in_reply_to_user_id": status.in_reply_to_user_id,
                   "in_reply_to_user_id_str": status.in_reply_to_user_id_str,
                   "in_reply_to_screen_name": status.in_reply_to_screen_name,
                   "user_screen_name": status.user.screen_name, "geo": status.geo,
                   "coordinates": status.coordinates, "place": str(status.place),
                   "contributors": status.contributors, "is_quote_status": status.is_quote_status,
                   "retweet_count": status.retweet_count, "favorite_count": status.favorite_count,
                   "favorited": status.favorited, "retweeted": status.retweeted, "lang": status.lang}
    with open("../data/sorted_tweets.json", "r") as file2read:
        file2read = file2read.readlines()
        for line in file2read:
            line = json.loads(line)
            if id == line["id"]:
                exit()
    with open("../data/tweets.json", "a") as file2write:
        status_str = json.dumps(status_dict)
        file2write.write(status_str + '\n')


def crawl_tweets(field):
    # tweet #
    statuses = tweepy.Cursor(api.search, q=field, lang='en').items(18000)
    for status in statuses:
        process_status(status)


if __name__ == "__main__":
    field = "computer science"
    crawl_tweets(field=field)
