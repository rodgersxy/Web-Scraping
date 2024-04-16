from instagrapi import Client
import openai
import json
import time
import random
import argparse

def get_comments(api_key, number, phrase, regarding):
    openai.api_key = api_key
    content_phrase = (f'generate {number} comments for instagram {phrase} post regarding {regarding} in informal slang'
                      f' in a form of structured data json like ') + '{"number" : "comment"} without any other text'
    print(content_phrase)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":content_phrase }]
    )

    return json.loads(completion.choices[0].message.content)

"""Parses command line arguments and uses them to get comments from OpenAI, 
then posts them as comments to medias from Instagram for a given hashtag.

The main functionality is in get_comments which uses OpenAI API to generate 
comments based on the provided phrase and regarding prompt.

Then it iterates through recent medias for the hashtag, waits a random interval,
and posts the generated comments to each media.
"""
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="InstaComment")
    parser.add_argument("--igusername", type=str, help="igusername")
    parser.add_argument("--igpass", type=str, help="igpass")
    parser.add_argument("--apikey", type=str, help="apikey")
    parser.add_argument("--phrase", type=str, help="phrase")
    parser.add_argument("--regarding", type=str, help="regarding")
    parser.add_argument("--number",type=int, help="number")
    parser.add_argument("--maxintervalminutes", type=int, help="maxintervalminutes")

    args = parser.parse_args()

    print(f"started with {args}")
    print("Connecting to IG")

    cl = Client()
    cl.login(args.igusername, args.igpass)
    medias = cl.hashtag_medias_recent_v1(args.phrase, args.number)

    for media in medias:
        print(media.id)
    print("Get comments from chat")
    comments = get_comments(args.apikey, args.number, args.phrase, args.regarding)
    print(comments)

    for index, media in enumerate(medias):
        timesleeprandom = random.randint(0, args.maxintervalminutes)*60
        print(timesleeprandom)
        time.sleep(timesleeprandom)
        print(media.id, comments[str(index+1)])
        cl.media_comment(media.id, comments[str(index+1)])