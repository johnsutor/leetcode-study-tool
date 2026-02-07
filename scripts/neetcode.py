#!/usr/bin/env python
# encoding: utf-8
# Utility script to generate a mapping between leetcode question IDs to their respective Neetcode video.
# The output will be stored in a file named youtube.json, and this script assumes that the environmental
# variable YOUTUBE_API_KEY is set to a valid Google API key with the YouTube API enabled. You can also
# optionally pass in the API key as a command line argument.

import argparse
import json
import os
import re
import sys
from typing import Union, Dict, Any, List, Tuple

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def fetch_videos_by_type(
    youtube, channel_ids: List[str], video_type: str = "video"
) -> List[Dict[str, Any]]:
    """
    Fetch videos from YouTube channels with specified type (video or short).

    Args:
        youtube: YouTube API client
        channel_ids: List of channel IDs to search
        video_type: "video" for regular videos, "short" for shorts

    Returns:
        List of video items from YouTube API
    """
    all_videos = []

    for channel in channel_ids:
        next_page_token = None
        while True:
            # Build request parameters based on video type
            request_params = {
                "part": "snippet",
                "channelId": channel,
                "maxResults": 50,
                "type": "video",
            }

            # Add videoDuration parameter for shorts
            if video_type == "short":
                request_params["videoDuration"] = "short"

            if next_page_token:
                request_params["pageToken"] = next_page_token

            request = youtube.search().list(**request_params)
            response = request.execute()
            all_videos.extend(response["items"])

            if response.get("nextPageToken", False):
                next_page_token = response["nextPageToken"]
            else:
                break

    return all_videos


def is_short_video(duration_str: str) -> bool:
    """
    Determine if a video is a short based on its duration.

    Args:
        duration_str: ISO 8601 duration string (e.g., "PT45S", "PT1M30S")

    Returns:
        True if duration is <= 60 seconds, False otherwise
    """
    if not duration_str:
        return False

    # Parse ISO 8601 duration format
    duration_match = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not duration_match:
        return False

    minutes = int(duration_match.group(1) or 0)
    seconds = int(duration_match.group(2) or 0)
    total_seconds = minutes * 60 + seconds
    return total_seconds <= 60


def extract_leetcode_id(title: str) -> Union[str, None]:
    """
    Extract LeetCode problem ID from video title.

    Args:
        title: Video title

    Returns:
        LeetCode ID as string or None if not found
    """
    match = re.search(r"Leetcode (\d+)(?!\w)", title, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def get_video_details(youtube, video_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Get detailed information for videos including duration.

    Args:
        youtube: YouTube API client
        video_ids: List of video IDs

    Returns:
        Dictionary mapping video ID to video details
    """
    if not video_ids:
        return {}

    video_details = {}
    # YouTube API can handle up to 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i : i + 50]
        try:
            request = youtube.videos().list(
                part="contentDetails,snippet", id=",".join(batch_ids)
            )
            response = request.execute()

            for item in response["items"]:
                video_id = item["id"]
                video_details[video_id] = {
                    "duration": item["contentDetails"].get("duration", ""),
                    "title": item["snippet"]["title"],
                }
        except Exception as e:
            print(f"Warning: Failed to fetch details for videos {batch_ids}: {e}")

    return video_details


def main(youtube_api_key: Union[str, None] = None, include_shorts: bool = False):
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

    # Channel IDs for NeetCode channels
    channel_ids = ["UC_mYaQAE6-71rjSN6CeCA-g", "UCevUmOfLTUX9MNGJQKsPdIA"]

    print("Fetching regular videos...")
    regular_videos = fetch_videos_by_type(youtube, channel_ids, "video")
    print(f"Found {len(regular_videos)} regular videos from NeetCode channel(s).")

    short_videos = []
    if include_shorts:
        print("Fetching shorts...")
        short_videos = fetch_videos_by_type(youtube, channel_ids, "short")
        print(f"Found {len(short_videos)} shorts from NeetCode channel(s).")

    # Get video details for duration detection
    all_video_ids = [video["id"]["videoId"] for video in regular_videos + short_videos]
    video_details = get_video_details(youtube, all_video_ids)

    # Process videos and create mapping
    leetcode_id_to_content = {}

    # Process regular videos
    for video in regular_videos:
        video_id = video["id"]["videoId"]
        leetcode_id = extract_leetcode_id(video["snippet"]["title"])

        if leetcode_id:
            if leetcode_id not in leetcode_id_to_content:
                leetcode_id_to_content[leetcode_id] = {}

            # Additional duration-based filtering for videos (exclude shorts that might appear in regular results)
            details = video_details.get(video_id, {})
            if not is_short_video(details.get("duration", "")):
                leetcode_id_to_content[leetcode_id]["video"] = {
                    "title": video["snippet"]["title"],
                    "url": "https://youtube.com/watch?v=" + video_id,
                }

    # Process shorts if requested
    if include_shorts:
        for short in short_videos:
            short_id = short["id"]["videoId"]
            leetcode_id = extract_leetcode_id(short["snippet"]["title"])

            if leetcode_id:
                if leetcode_id not in leetcode_id_to_content:
                    leetcode_id_to_content[leetcode_id] = {}

                leetcode_id_to_content[leetcode_id]["short"] = {
                    "title": short["snippet"]["title"],
                    "url": "https://youtube.com/watch?v=" + short_id,
                }

    # Count content types
    total_problems = len(leetcode_id_to_content)
    total_videos = sum(
        1 for content in leetcode_id_to_content.values() if "video" in content
    )
    total_shorts = sum(
        1 for content in leetcode_id_to_content.values() if "short" in content
    )

    print(f"Found content for {total_problems} LeetCode problems:")
    print(f"  - Regular videos: {total_videos}")
    print(f"  - Shorts: {total_shorts}")

    # Save the data
    output_filename = (
        "youtube.json" if not include_shorts else "youtube_with_shorts.json"
    )
    with open(output_filename, "w") as f:
        json.dump(leetcode_id_to_content, f, indent=4, sort_keys=True)

    print(f"Data saved to {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch LeetCode videos from NeetCode YouTube channels"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="YouTube Data API key (or set YOUTUBE_API_KEY environment variable)",
    )
    parser.add_argument(
        "--include-shorts",
        action="store_true",
        help="Include YouTube shorts in addition to regular videos",
    )

    args = parser.parse_args()
    main(args.api_key, args.include_shorts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch LeetCode videos from NeetCode YouTube channels"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="YouTube Data API key (or set YOUTUBE_API_KEY environment variable)",
    )
    parser.add_argument(
        "--include-shorts",
        action="store_true",
        help="Include YouTube shorts in addition to regular videos",
    )

    args = parser.parse_args()
    main(args.api_key, args.include_shorts)
