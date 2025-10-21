#!/usr/bin/env python3
"""
YouTube Video Analyzer
Downloads and analyzes YouTube videos using yt-dlp
"""

import argparse
import json
import sys
from datetime import timedelta
from pathlib import Path
import yt_dlp


class YouTubeAnalyzer:
    """Analyzes and downloads YouTube videos."""

    def __init__(self, output_dir="downloads"):
        """Initialize the analyzer with an output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def get_video_info(self, url):
        """
        Extract video metadata without downloading.

        Args:
            url: YouTube video URL

        Returns:
            dict: Video metadata
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return self._format_info(info)
        except Exception as e:
            return {"error": f"Failed to extract info: {str(e)}"}

    def _format_info(self, info):
        """Format video info into a clean dictionary."""
        duration_str = str(timedelta(seconds=info.get('duration', 0))) if info.get('duration') else 'Unknown'

        formatted = {
            'title': info.get('title', 'Unknown'),
            'channel': info.get('uploader', 'Unknown'),
            'channel_id': info.get('channel_id', 'Unknown'),
            'upload_date': info.get('upload_date', 'Unknown'),
            'duration': duration_str,
            'duration_seconds': info.get('duration', 0),
            'view_count': info.get('view_count', 0),
            'like_count': info.get('like_count', 0),
            'description': info.get('description', 'No description'),
            'categories': info.get('categories', []),
            'tags': info.get('tags', []),
            'thumbnail': info.get('thumbnail', ''),
            'url': info.get('webpage_url', ''),
            'video_id': info.get('id', ''),
        }

        # Add subtitles/captions info if available
        if info.get('subtitles') or info.get('automatic_captions'):
            formatted['has_captions'] = True
            formatted['caption_languages'] = list(info.get('subtitles', {}).keys()) + \
                                            list(info.get('automatic_captions', {}).keys())
        else:
            formatted['has_captions'] = False
            formatted['caption_languages'] = []

        return formatted

    def download_video(self, url, format_type='best', include_subtitles=True):
        """
        Download a YouTube video.

        Args:
            url: YouTube video URL
            format_type: 'best', 'audio', or specific format
            include_subtitles: Whether to download subtitles

        Returns:
            dict: Download result information
        """
        output_template = str(self.output_dir / '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if format_type == 'best' else format_type,
            'outtmpl': output_template,
            'writesubtitles': include_subtitles,
            'writeautomaticsub': include_subtitles,
            'subtitleslangs': ['en'],
            'progress_hooks': [self._progress_hook],
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }

        if format_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                # Determine the output filename
                if format_type == 'audio':
                    filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                else:
                    filename = ydl.prepare_filename(info)

                return {
                    'status': 'success',
                    'title': info.get('title'),
                    'filename': filename,
                    'duration': str(timedelta(seconds=info.get('duration', 0))),
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _progress_hook(self, d):
        """Hook to display download progress."""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'Unknown')
            eta = d.get('_eta_str', 'Unknown')
            print(f"\rDownloading: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\nDownload complete! Processing...")

    def get_transcript(self, url, lang='en', max_length=None):
        """
        Extract video transcript/captions with actual text.

        Args:
            url: YouTube video URL
            lang: Language code (default: 'en')
            max_length: Maximum number of characters to return (None for all)

        Returns:
            dict: Transcript data including text
        """
        import requests
        import re

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [lang],
            'skip_download': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                subtitles = info.get('subtitles', {})
                auto_captions = info.get('automatic_captions', {})

                # Try to get the requested language
                transcript_data = None
                source_type = None

                # Prefer manual subtitles over auto captions
                if lang in subtitles:
                    transcript_data = subtitles[lang]
                    source_type = 'manual'
                elif lang in auto_captions:
                    transcript_data = auto_captions[lang]
                    source_type = 'automatic'

                # If requested language not found, try English variants
                if not transcript_data:
                    for key in ['en', 'en-US', 'en-GB', 'en-orig']:
                        if key in subtitles:
                            transcript_data = subtitles[key]
                            source_type = 'manual'
                            lang = key
                            break
                        elif key in auto_captions:
                            transcript_data = auto_captions[key]
                            source_type = 'automatic'
                            lang = key
                            break

                result = {
                    'has_manual_subtitles': bool(subtitles),
                    'has_auto_captions': bool(auto_captions),
                    'available_languages': list(set(list(subtitles.keys()) + list(auto_captions.keys()))),
                    'language_used': lang,
                    'source_type': source_type,
                    'text': None,
                    'entries': []
                }

                # If we found transcript data, download and parse it
                if transcript_data:
                    # Find the best format (prefer JSON, then srv3, then vtt)
                    subtitle_url = None
                    for fmt in transcript_data:
                        if fmt.get('ext') == 'json3':
                            subtitle_url = fmt.get('url')
                            break

                    if not subtitle_url:
                        for fmt in transcript_data:
                            if fmt.get('ext') in ['srv3', 'vtt', 'ttml']:
                                subtitle_url = fmt.get('url')
                                break

                    if subtitle_url:
                        try:
                            response = requests.get(subtitle_url, timeout=10, verify=False)
                            response.raise_for_status()

                            # Parse JSON3 format
                            if 'json3' in subtitle_url or '"events"' in response.text:
                                import json
                                data = json.loads(response.text)

                                # Extract text from events
                                text_parts = []
                                entries = []

                                for event in data.get('events', []):
                                    segs = event.get('segs')
                                    if segs:
                                        segment_text = ''.join(seg.get('utf8', '') for seg in segs)
                                        if segment_text.strip():
                                            text_parts.append(segment_text.strip())

                                            # Create entry with timestamp
                                            start_time = event.get('tStartMs', 0) / 1000
                                            duration = event.get('dDurationMs', 0) / 1000
                                            entries.append({
                                                'start': start_time,
                                                'duration': duration,
                                                'text': segment_text.strip()
                                            })

                                full_text = ' '.join(text_parts)
                                result['text'] = full_text[:max_length] if max_length else full_text
                                result['entries'] = entries[:100]  # Limit entries for performance
                                result['total_entries'] = len(entries)

                            else:
                                # Parse VTT/SRT format
                                content = response.text

                                # Remove WebVTT header and styling
                                content = re.sub(r'WEBVTT\n.*?\n\n', '', content, flags=re.DOTALL)
                                content = re.sub(r'<[^>]+>', '', content)  # Remove HTML tags
                                content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', content)
                                content = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', content)

                                # Clean up
                                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().isdigit()]
                                full_text = ' '.join(lines)

                                result['text'] = full_text[:max_length] if max_length else full_text
                                result['entries'] = [{'text': full_text[:500]}]  # Preview

                        except Exception as e:
                            result['download_error'] = str(e)

                return result
        except Exception as e:
            return {'error': str(e)}


def print_info(info):
    """Pretty print video information."""
    if 'error' in info:
        print(f"Error: {info['error']}")
        return

    print("\n" + "="*60)
    print(f"Title: {info['title']}")
    print("="*60)
    print(f"Channel: {info['channel']}")
    print(f"Upload Date: {info['upload_date']}")
    print(f"Duration: {info['duration']}")
    print(f"Views: {info['view_count']:,}")
    print(f"Likes: {info['like_count']:,}")
    print(f"Video ID: {info['video_id']}")
    print(f"URL: {info['url']}")
    print(f"\nCategories: {', '.join(info.get('categories', []))}")
    print(f"Captions Available: {info['has_captions']}")
    if info['has_captions']:
        print(f"Caption Languages: {', '.join(info['caption_languages'][:5])}")

    print(f"\nDescription:\n{info['description'][:500]}")
    if len(info['description']) > 500:
        print("... (truncated)")
    print("="*60 + "\n")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='YouTube Video Analyzer - Download and analyze YouTube videos'
    )
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Display video information only (no download)'
    )
    parser.add_argument(
        '-d', '--download',
        action='store_true',
        help='Download the video'
    )
    parser.add_argument(
        '-a', '--audio',
        action='store_true',
        help='Download audio only (MP3)'
    )
    parser.add_argument(
        '-t', '--transcript',
        action='store_true',
        help='Get transcript/caption information'
    )
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Output directory for downloads (default: downloads)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    parser.add_argument(
        '--lang',
        default='en',
        help='Language code for transcript (default: en)'
    )

    args = parser.parse_args()

    analyzer = YouTubeAnalyzer(output_dir=args.output)

    # If no action specified, default to showing info
    if not (args.info or args.download or args.audio or args.transcript):
        args.info = True

    if args.info or args.json:
        info = analyzer.get_video_info(args.url)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print_info(info)

    if args.transcript:
        print("\nExtracting transcript...")
        transcript_info = analyzer.get_transcript(args.url, lang=args.lang)

        if args.json:
            print(json.dumps(transcript_info, indent=2))
        else:
            if 'error' in transcript_info:
                print(f"\nError: {transcript_info['error']}")
            else:
                print("\n" + "="*60)
                print("TRANSCRIPT")
                print("="*60)
                print(f"Language: {transcript_info.get('language_used', 'Unknown')}")
                print(f"Source: {transcript_info.get('source_type', 'Unknown')} captions")
                print(f"Manual Subtitles Available: {transcript_info.get('has_manual_subtitles', False)}")
                print(f"Auto Captions Available: {transcript_info.get('has_auto_captions', False)}")

                if transcript_info.get('text'):
                    print("\n" + "-"*60)
                    print("TRANSCRIPT TEXT:")
                    print("-"*60)
                    print(transcript_info['text'])
                    print("-"*60)

                    if transcript_info.get('total_entries'):
                        print(f"\nTotal segments: {transcript_info['total_entries']}")

                    # Show first few timestamped entries if available
                    if transcript_info.get('entries'):
                        print("\nFirst few segments with timestamps:")
                        for i, entry in enumerate(transcript_info['entries'][:5], 1):
                            start = entry.get('start', 0)
                            mins = int(start // 60)
                            secs = int(start % 60)
                            print(f"  [{mins}:{secs:02d}] {entry.get('text', '')[:80]}")
                else:
                    print("\n⚠️  Transcript text could not be extracted.")
                    if 'download_error' in transcript_info:
                        print(f"Error downloading captions: {transcript_info['download_error']}")
                    print(f"\nAvailable languages: {', '.join(transcript_info.get('available_languages', [])[:10])}")
                    print("Try using --json to see raw data.")

                print("="*60)

    if args.download:
        print("\nDownloading video...")
        result = analyzer.download_video(args.url, format_type='best')
        if result['status'] == 'success':
            print(f"\nSuccess! Downloaded: {result['filename']}")
        else:
            print(f"\nError: {result['error']}")

    if args.audio:
        print("\nDownloading audio...")
        result = analyzer.download_video(args.url, format_type='audio')
        if result['status'] == 'success':
            print(f"\nSuccess! Downloaded: {result['filename']}")
        else:
            print(f"\nError: {result['error']}")


if __name__ == '__main__':
    main()
