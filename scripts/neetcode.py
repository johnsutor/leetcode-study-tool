#!/usr/bin/env python
# encoding: utf-8
# Utility script to generate a mapping between leetcode question IDs to their respective Neetcode video.
# The output will be stored in a file named youtube.json, and this script assumes that the environmental
# variable YOUTUBE_API_KEY is set to a valid Google API key with the YouTube API enabled. You can also
# optionally pass in the API key as a command line argument.

import json
import os
import re
import sys
from typing import Union

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main(youtube_api_key: Union[str, None] = None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if not youtube_api_key:
        youtube_api_key = os.environ.get("YOUTUBE_API_KEY", None)
        if not youtube_api_key:
            print(
                "Please set the environmental variable YOUTUBE_API_KEY to a"
                " valid Google API key with the YouTube API enabled."
            )
            sys.exit(1)

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=youtube_api_key
    )

    # Obtain all videos from NeetCode channel
    all_videos = []
    channel_ids = ["UC_mYaQAE6-71rjSN6CeCA-g", "UCevUmOfLTUX9MNGJQKsPdIA"]
    for channel in channel_ids:
        next_page_token = None
        while True:
            if next_page_token:
                request = youtube.search().list(
                    part="snippet",
                    channelId=channel,
                    maxResults=50,
                    pageToken=next_page_token,
                )
            else:
                request = youtube.search().list(
                    part="snippet",
                    channelId=channel,
                    maxResults=50,
                )
            response = request.execute()
            all_videos.extend(response["items"])
            if response.get("nextPageToken", False):
                next_page_token = response["nextPageToken"]
            else:
                break

    print(f"Found {len(all_videos)} videos from NeetCode channel(s).")

    # Create dictionary mapping Leetcode ID to each video with metadata
    leetcode_id_to_video = {}
    for video in all_videos:
        match = re.search("Leetcode \d+", video["snippet"]["title"])
        if match:
            leetcode_id = match.group(0).split(" ")[1]
            leetcode_id_to_video[leetcode_id] = {
                "title": video["snippet"]["title"],
                "url": "https://youtube.com/watch?v=" + video["id"]["videoId"],
            }

    print(f"Found {len(leetcode_id_to_video)} videos related to Leetcode problems.")
    with open("youtube.json", "w") as f:
        json.dump(leetcode_id_to_video, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    if sys.argv[1]:
        youtube_api_key = sys.argv[1]
    main(youtube_api_key)
