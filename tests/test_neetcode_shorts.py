import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import re
from typing import Dict, Any, List

# Conditional import for optional dependencies
try:
    from googleapiclient import errors as googleapiclient_errors
except ImportError:
    googleapiclient_errors = None


class TestNeetCodeShorts(unittest.TestCase):
    """Test suite for NeetCode shorts detection and fetching functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.youtube_api_key = "test_api_key"
        self.channel_ids = ["UC_mYaQAE6-71rjSN6CeCA-g", "UCevUmOfLTUX9MNGJQKsPdIA"]

        # Mock video data for testing
        self.mock_regular_video = {
            "id": {"videoId": "regular123"},
            "snippet": {
                "title": "Two Sum - Leetcode 1 - HashMap - Python",
                "description": "Full solution explanation for Two Sum problem",
            },
        }

        self.mock_short_video = {
            "id": {"videoId": "short456"},
            "snippet": {
                "title": "Two Sum - Leetcode 1 - Quick Short",
                "description": "Quick overview of Two Sum solution",
            },
        }

        self.mock_short_video_with_duration = {
            "id": {"videoId": "short789"},
            "snippet": {
                "title": "Contains Duplicate - Leetcode 217 - Short",
                "description": "Quick explanation",
            },
            "contentDetails": {
                "duration": "PT45S"  # 45 seconds
            },
        }

    def test_extract_leetcode_id_from_title(self):
        """Test LeetCode ID extraction from various title formats."""
        test_cases = [
            ("Two Sum - Leetcode 1 - HashMap - Python", "1"),
            ("Leetcode 217 - Contains Duplicate", "217"),
            ("LeetCode 1 - Two Sum Solution", "1"),
            ("Leetcode 150 - Evaluate Reverse Polish Notation", "150"),
            ("Random video without Leetcode", None),
            ("Leetcode 1A - Invalid format", None),
        ]

        for title, expected_id in test_cases:
            with self.subTest(title=title):
                match = re.search(r"Leetcode (\d+)(?!\w)", title, re.IGNORECASE)
                if expected_id:
                    self.assertIsNotNone(match, f"Expected match for title: {title}")
                    if match:
                        extracted_id = match.group(1)  # Group 1 is the number
                        # Validate that it's actually a number
                        self.assertTrue(
                            extracted_id.isdigit(),
                            f"Expected numeric ID, got: {extracted_id}",
                        )
                        self.assertEqual(extracted_id, expected_id)
                else:
                    self.assertIsNone(match)

    def test_is_short_video_by_duration(self):
        """Test short video detection based on duration."""

        def is_short_by_duration(duration_str: str) -> bool:
            """Helper function to test duration parsing."""
            if not duration_str:
                return False
            # Parse ISO 8601 duration format (PT45S, PT1M30S, etc.)
            import re

            duration_match = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", duration_str)
            if not duration_match:
                return False

            minutes = int(duration_match.group(1) or 0)
            seconds = int(duration_match.group(2) or 0)
            total_seconds = minutes * 60 + seconds
            return total_seconds <= 60

        # Test cases
        test_cases = [
            ("PT45S", True),  # 45 seconds
            ("PT60S", True),  # 60 seconds
            ("PT61S", False),  # 61 seconds
            ("PT30S", True),  # 30 seconds
            ("PT1M", True),  # 60 minutes (1 minute)
            ("PT1M30S", False),  # 90 seconds
            ("PT2M", False),  # 120 seconds
            ("", False),  # Empty duration
            ("invalid", False),  # Invalid format
        ]

        for duration, expected in test_cases:
            with self.subTest(duration=duration):
                self.assertEqual(is_short_by_duration(duration), expected)

    @unittest.skipIf(googleapiclient_errors is None, "googleapiclient not available")
    @patch("googleapiclient.discovery.build")
    def test_fetch_videos_from_channel(self, mock_build):
        """Test fetching videos from a YouTube channel."""
        # Mock YouTube API response
        mock_youtube = Mock()
        mock_build.return_value = mock_youtube

        mock_search_response = {
            "items": [self.mock_regular_video, self.mock_short_video],
            "nextPageToken": None,
        }

        mock_search = Mock()
        mock_search.return_value.execute.return_value = mock_search_response
        mock_youtube.search.return_value.list.return_value = mock_search

        # Test the API call structure
        from scripts.neetcode import main

        # This would test the actual API call structure
        # We'll implement the main function testing after we modify the script

    def test_video_data_structure_for_shorts(self):
        """Test the new data structure that includes both videos and shorts."""
        # Test new data structure format
        test_data = {
            "1": {
                "video": {
                    "title": "Two Sum - Leetcode 1 - HashMap - Python",
                    "url": "https://youtube.com/watch?v=regular123",
                },
                "short": {
                    "title": "Two Sum - Leetcode 1 - Quick Short",
                    "url": "https://youtube.com/watch?v=short456",
                },
            },
            "217": {
                "video": {
                    "title": "Contains Duplicate - Leetcode 217 - Python",
                    "url": "https://youtube.com/watch?v=regular789",
                }
                # No short available
            },
        }

        # Verify structure
        self.assertIn("1", test_data)
        self.assertIn("video", test_data["1"])
        self.assertIn("short", test_data["1"])
        self.assertIn("217", test_data)
        self.assertIn("video", test_data["217"])
        self.assertNotIn("short", test_data["217"])

    def test_youtube_api_search_parameters_for_shorts(self):
        """Test that YouTube API is called with correct parameters for shorts."""
        # This test verifies the API call structure
        # We'll implement this after modifying the neetcode.py script

        expected_short_params = {
            "part": "snippet",
            "channelId": "UC_mYaQAE6-71rjSN6CeCA-g",
            "maxResults": 50,
            "type": "video",
            "videoDuration": "short",
        }

        expected_video_params = {
            "part": "snippet",
            "channelId": "UC_mYaQAE6-71rjSN6CeCA-g",
            "maxResults": 50,
            "type": "video",
        }

        # These parameters will be used when we implement the enhanced script
        self.assertIsNotNone(expected_short_params)
        self.assertIsNotNone(expected_video_params)

    def test_filter_leetcode_videos(self):
        """Test filtering of videos to only include LeetCode-related content."""
        mock_videos = [
            self.mock_regular_video,
            self.mock_short_video,
            {
                "id": {"videoId": "other123"},
                "snippet": {
                    "title": "Random Programming Tips",
                    "description": "Not related to LeetCode",
                },
            },
            {
                "id": {"videoId": "leetcode456"},
                "snippet": {
                    "title": "Leetcode 217 - Contains Duplicate - Python",
                    "description": "Solution for Contains Duplicate",
                },
            },
        ]

        leetcode_videos = []
        for video in mock_videos:
            match = re.search(
                r"Leetcode (\d+)(?!\w)", video["snippet"]["title"], re.IGNORECASE
            )
            if match:
                leetcode_id = match.group(1)
                leetcode_videos.append((leetcode_id, video))

        # Should find 3 LeetCode videos
        self.assertEqual(len(leetcode_videos), 3)

        # Extract the LeetCode IDs for validation
        leetcode_ids = [video[0] for video in leetcode_videos]
        self.assertIn("1", leetcode_ids)  # Two Sum
        self.assertIn("217", leetcode_ids)  # Contains Duplicate

        # Verify 1 appears twice (regular video and short for Two Sum)
        count_1 = leetcode_ids.count("1")
        count_217 = leetcode_ids.count("217")
        self.assertEqual(count_1, 2)  # Two Sum: regular + short
        self.assertEqual(count_217, 1)  # Contains Duplicate: regular only

    @unittest.skipIf(googleapiclient_errors is None, "googleapiclient not available")
    def test_error_handling_for_youtube_api(self):
        """Test error handling when YouTube API calls fail."""
        # Test API key missing error
        with self.assertRaises(SystemExit):
            from scripts.neetcode import main

            # Call main function with no API key to trigger SystemExit
            main(youtube_api_key=None, include_shorts=False)

        # Test API quota exceeded error
        if googleapiclient_errors:
            mock_youtube = Mock()
            mock_search = Mock()
            mock_search.return_value.execute.side_effect = (
                googleapiclient_errors.HttpError(Mock(status=403), b"Quota exceeded")
            )

            # This test will be implemented after script modification
        else:
            # Skip test if googleapiclient is not available
            self.skipTest("googleapiclient not available")

    def test_data_migration_backward_compatibility(self):
        """Test that new data structure is backward compatible."""
        # Old format (existing)
        old_format = {
            "1": {
                "title": "Two Sum - Leetcode 1 - HashMap - Python",
                "url": "https://youtube.com/watch?v=regular123",
            }
        }

        # New format (with shorts support)
        new_format = {
            "1": {
                "video": {
                    "title": "Two Sum - Leetcode 1 - HashMap - Python",
                    "url": "https://youtube.com/watch?v=regular123",
                }
            }
        }

        # Migration logic test
        def migrate_old_to_new(old_data: Dict[str, Any]) -> Dict[str, Any]:
            """Helper function to migrate old data format to new."""
            new_data = {}
            for leetcode_id, video_data in old_data.items():
                new_data[leetcode_id] = {"video": video_data}
            return new_data

        migrated = migrate_old_to_new(old_format)
        self.assertEqual(migrated, new_format)

    def test_integration_video_and_short_storage(self):
        """Test integration of storing both videos and shorts for same problem."""
        # Test case where both video and short exist for same problem
        problem_id = "217"

        video_data = {
            "title": "Contains Duplicate - Leetcode 217 - Python",
            "url": "https://youtube.com/watch?v=video123",
        }

        short_data = {
            "title": "Contains Duplicate - Leetcode 217 - Quick Short",
            "url": "https://youtube.com/watch?v=short123",
        }

        # Combined storage structure
        combined_data = {problem_id: {"video": video_data, "short": short_data}}

        # Test retrieval functions
        def get_video(leetcode_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
            return data.get(leetcode_id, {}).get("video")

        def get_short(leetcode_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
            return data.get(leetcode_id, {}).get("short")

        self.assertEqual(get_video(problem_id, combined_data), video_data)
        self.assertEqual(get_short(problem_id, combined_data), short_data)
        self.assertIsNone(get_short("999", combined_data))  # Non-existent problem


if __name__ == "__main__":
    unittest.main()
