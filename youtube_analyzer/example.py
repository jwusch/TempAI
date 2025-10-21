#!/usr/bin/env python3
"""
Example usage of the YouTubeAnalyzer class
"""

from youtube_analyzer import YouTubeAnalyzer
import json

def main():
    # Initialize the analyzer
    analyzer = YouTubeAnalyzer(output_dir="example_downloads")

    # Example YouTube URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    print("=" * 60)
    print("YouTube Analyzer - Example Usage")
    print("=" * 60)

    # Example 1: Get video information
    print("\n1. Getting video information...")
    info = analyzer.get_video_info(url)

    if 'error' not in info:
        print(f"   Title: {info['title']}")
        print(f"   Channel: {info['channel']}")
        print(f"   Duration: {info['duration']}")
        print(f"   Views: {info['view_count']:,}")
    else:
        print(f"   Error: {info['error']}")

    # Example 2: Get transcript information
    print("\n2. Getting transcript information...")
    transcript_info = analyzer.get_transcript(url)

    if 'error' not in transcript_info:
        print(f"   Has manual subtitles: {transcript_info['has_manual_subtitles']}")
        print(f"   Has auto captions: {transcript_info['has_auto_captions']}")
        print(f"   Available languages: {', '.join(transcript_info['available_languages'][:5])}")
    else:
        print(f"   Error: {transcript_info['error']}")

    # Example 3: Export to JSON
    print("\n3. Exporting to JSON...")
    with open('video_info.json', 'w') as f:
        json.dump(info, f, indent=2)
    print("   Saved to video_info.json")

    # Example 4: Download video (commented out by default)
    # Uncomment the following lines to actually download
    # print("\n4. Downloading video...")
    # result = analyzer.download_video(url, format_type='best')
    # if result['status'] == 'success':
    #     print(f"   Downloaded: {result['filename']}")
    # else:
    #     print(f"   Error: {result['error']}")

    # Example 5: Download audio only (commented out by default)
    # print("\n5. Downloading audio...")
    # result = analyzer.download_video(url, format_type='audio')
    # if result['status'] == 'success':
    #     print(f"   Downloaded: {result['filename']}")
    # else:
    #     print(f"   Error: {result['error']}")

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
