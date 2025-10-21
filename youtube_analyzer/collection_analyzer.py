#!/usr/bin/env python3
"""
YouTube Collection Analyzer
Analyzes multiple YouTube videos, generates comparisons, and creates insightful reports
"""

import argparse
import json
import sys
from datetime import timedelta, datetime
from pathlib import Path
from typing import List, Dict
import re
from collections import Counter

try:
    from youtube_analyzer import YouTubeAnalyzer
    from dashboard_generator import DashboardGenerator
except ImportError as e:
    print(f"Error: Required module not found: {e}")
    print("Make sure youtube_analyzer.py and dashboard_generator.py are in the same directory.")
    sys.exit(1)


class CollectionAnalyzer:
    """Analyzes collections of YouTube videos."""

    def __init__(self, output_dir="collections"):
        """Initialize the collection analyzer."""
        self.analyzer = YouTubeAnalyzer()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.videos = []

    def extract_video_id(self, url):
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def analyze_multiple(self, urls: List[str], progress=True):
        """
        Analyze multiple YouTube videos.

        Args:
            urls: List of YouTube video URLs
            progress: Show progress messages

        Returns:
            list: List of video info dictionaries
        """
        results = []
        total = len(urls)

        for idx, url in enumerate(urls, 1):
            if progress:
                print(f"\n[{idx}/{total}] Analyzing: {url}")

            info = self.analyzer.get_video_info(url)

            if 'error' not in info:
                results.append(info)
                if progress:
                    print(f"  ✓ {info['title'][:60]}...")
            else:
                if progress:
                    print(f"  ✗ Error: {info['error']}")

        self.videos = results
        return results

    def compare_videos(self, videos: List[Dict] = None):
        """
        Compare multiple videos and find insights.

        Args:
            videos: List of video info dicts (uses self.videos if None)

        Returns:
            dict: Comparison insights
        """
        if videos is None:
            videos = self.videos

        if not videos:
            return {"error": "No videos to compare"}

        total_duration = sum(v.get('duration_seconds', 0) for v in videos)
        total_views = sum(v.get('view_count', 0) for v in videos)
        total_likes = sum(v.get('like_count', 0) for v in videos)

        # Find most and least popular
        by_views = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
        by_likes = sorted(videos, key=lambda x: x.get('like_count', 0), reverse=True)
        by_duration = sorted(videos, key=lambda x: x.get('duration_seconds', 0), reverse=True)

        # Gather all categories and tags
        all_categories = []
        all_tags = []
        for v in videos:
            all_categories.extend(v.get('categories', []))
            all_tags.extend(v.get('tags', []))

        category_counts = Counter(all_categories)
        tag_counts = Counter(all_tags)

        # Channel analysis
        channels = Counter(v.get('channel', 'Unknown') for v in videos)

        # Calculate engagement rates
        engagement_rates = []
        for v in videos:
            views = v.get('view_count', 0)
            likes = v.get('like_count', 0)
            if views > 0:
                engagement = (likes / views) * 100
                engagement_rates.append({
                    'title': v.get('title', 'Unknown'),
                    'engagement_rate': round(engagement, 2),
                    'views': views,
                    'likes': likes
                })

        engagement_rates.sort(key=lambda x: x['engagement_rate'], reverse=True)

        return {
            'summary': {
                'total_videos': len(videos),
                'total_duration': str(timedelta(seconds=total_duration)),
                'total_duration_seconds': total_duration,
                'total_views': total_views,
                'total_likes': total_likes,
                'avg_views': total_views // len(videos) if videos else 0,
                'avg_likes': total_likes // len(videos) if videos else 0,
                'avg_duration': str(timedelta(seconds=total_duration // len(videos))) if videos else '0:00:00',
            },
            'most_viewed': {
                'title': by_views[0].get('title', 'Unknown') if by_views else None,
                'views': by_views[0].get('view_count', 0) if by_views else 0,
                'url': by_views[0].get('url', '') if by_views else '',
            },
            'most_liked': {
                'title': by_likes[0].get('title', 'Unknown') if by_likes else None,
                'likes': by_likes[0].get('like_count', 0) if by_likes else 0,
                'url': by_likes[0].get('url', '') if by_likes else '',
            },
            'longest_video': {
                'title': by_duration[0].get('title', 'Unknown') if by_duration else None,
                'duration': by_duration[0].get('duration', '0:00:00') if by_duration else '0:00:00',
                'url': by_duration[0].get('url', '') if by_duration else '',
            },
            'shortest_video': {
                'title': by_duration[-1].get('title', 'Unknown') if by_duration else None,
                'duration': by_duration[-1].get('duration', '0:00:00') if by_duration else '0:00:00',
                'url': by_duration[-1].get('url', '') if by_duration else '',
            },
            'top_categories': dict(category_counts.most_common(5)),
            'top_tags': dict(tag_counts.most_common(10)),
            'channels': dict(channels),
            'engagement_rates': engagement_rates[:5],  # Top 5 by engagement
        }

    def generate_markdown_report(self, comparison: Dict, filename: str = None):
        """
        Generate a Markdown report from comparison data.

        Args:
            comparison: Comparison dictionary from compare_videos()
            filename: Output filename (auto-generated if None)

        Returns:
            str: Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"youtube_collection_report_{timestamp}.md"

        filepath = self.output_dir / filename

        summary = comparison.get('summary', {})

        report = f"""# YouTube Collection Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Videos:** {summary.get('total_videos', 0)}
- **Total Duration:** {summary.get('total_duration', 'N/A')}
- **Total Views:** {summary.get('total_views', 0):,}
- **Total Likes:** {summary.get('total_likes', 0):,}
- **Average Views per Video:** {summary.get('avg_views', 0):,}
- **Average Likes per Video:** {summary.get('avg_likes', 0):,}
- **Average Duration:** {summary.get('avg_duration', 'N/A')}

## Top Performers

### Most Viewed Video
**{comparison.get('most_viewed', {}).get('title', 'N/A')}**
- Views: {comparison.get('most_viewed', {}).get('views', 0):,}
- URL: {comparison.get('most_viewed', {}).get('url', 'N/A')}

### Most Liked Video
**{comparison.get('most_liked', {}).get('title', 'N/A')}**
- Likes: {comparison.get('most_liked', {}).get('likes', 0):,}
- URL: {comparison.get('most_liked', {}).get('url', 'N/A')}

### Longest Video
**{comparison.get('longest_video', {}).get('title', 'N/A')}**
- Duration: {comparison.get('longest_video', {}).get('duration', 'N/A')}
- URL: {comparison.get('longest_video', {}).get('url', 'N/A')}

### Shortest Video
**{comparison.get('shortest_video', {}).get('title', 'N/A')}**
- Duration: {comparison.get('shortest_video', {}).get('duration', 'N/A')}
- URL: {comparison.get('shortest_video', {}).get('url', 'N/A')}

## Engagement Analysis

### Top Videos by Engagement Rate (Likes/Views)
"""

        for idx, item in enumerate(comparison.get('engagement_rates', []), 1):
            report += f"\n{idx}. **{item['title']}**\n"
            report += f"   - Engagement Rate: {item['engagement_rate']}%\n"
            report += f"   - Views: {item['views']:,} | Likes: {item['likes']:,}\n"

        report += "\n## Content Analysis\n\n"

        # Categories
        report += "### Top Categories\n\n"
        categories = comparison.get('top_categories', {})
        for category, count in categories.items():
            report += f"- **{category}**: {count} video(s)\n"

        # Tags
        report += "\n### Popular Tags\n\n"
        tags = comparison.get('top_tags', {})
        for tag, count in list(tags.items())[:10]:
            report += f"- {tag} ({count})\n"

        # Channels
        report += "\n## Channel Distribution\n\n"
        channels = comparison.get('channels', {})
        for channel, count in sorted(channels.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{channel}**: {count} video(s)\n"

        report += "\n---\n\n*Generated by YouTube Collection Analyzer*\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        return str(filepath)

    def export_csv(self, videos: List[Dict] = None, filename: str = None):
        """Export video data to CSV format."""
        import csv

        if videos is None:
            videos = self.videos

        if not videos:
            return None

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"youtube_collection_{timestamp}.csv"

        filepath = self.output_dir / filename

        headers = ['title', 'channel', 'duration', 'views', 'likes', 'upload_date', 'video_id', 'url']

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for video in videos:
                writer.writerow({
                    'title': video.get('title', 'Unknown'),
                    'channel': video.get('channel', 'Unknown'),
                    'duration': video.get('duration', 'N/A'),
                    'views': video.get('view_count', 0),
                    'likes': video.get('like_count', 0),
                    'upload_date': video.get('upload_date', 'N/A'),
                    'video_id': video.get('video_id', 'N/A'),
                    'url': video.get('url', 'N/A'),
                })

        return str(filepath)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='YouTube Collection Analyzer - Analyze multiple videos and generate insights'
    )
    parser.add_argument(
        'urls',
        nargs='*',
        help='YouTube video URLs (or use --file)'
    )
    parser.add_argument(
        '-f', '--file',
        help='File containing YouTube URLs (one per line)'
    )
    parser.add_argument(
        '-o', '--output',
        default='collections',
        help='Output directory (default: collections)'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate Markdown report'
    )
    parser.add_argument(
        '--csv',
        action='store_true',
        help='Export to CSV'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Export to JSON'
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Show comparison analysis'
    )
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Generate interactive HTML dashboard'
    )

    args = parser.parse_args()

    # Gather URLs
    urls = args.urls or []

    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                urls.extend(file_urls)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)

    if not urls:
        print("Error: No URLs provided. Use URLs as arguments or --file option.")
        parser.print_help()
        sys.exit(1)

    print(f"\n{'='*60}")
    print("YouTube Collection Analyzer")
    print(f"{'='*60}")
    print(f"Analyzing {len(urls)} video(s)...\n")

    # Initialize analyzer
    analyzer = CollectionAnalyzer(output_dir=args.output)

    # Analyze videos
    videos = analyzer.analyze_multiple(urls, progress=True)

    if not videos:
        print("\nNo videos were successfully analyzed.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Successfully analyzed {len(videos)}/{len(urls)} video(s)")
    print(f"{'='*60}")

    # Generate comparison
    if args.compare or args.report or args.dashboard:
        print("\nGenerating comparison analysis...")
        comparison = analyzer.compare_videos(videos)

        if args.compare:
            print("\n" + "="*60)
            print("COMPARISON ANALYSIS")
            print("="*60)
            print(json.dumps(comparison, indent=2))

        if args.report:
            report_path = analyzer.generate_markdown_report(comparison)
            print(f"\n✓ Markdown report saved to: {report_path}")

        if args.dashboard:
            dashboard_gen = DashboardGenerator()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dashboard_path = analyzer.output_dir / f"dashboard_{timestamp}.html"
            dashboard_gen.generate_html_dashboard(videos, comparison, str(dashboard_path))
            print(f"\n✓ Interactive dashboard saved to: {dashboard_path}")
            print(f"  Open it in your browser to view!")

    # Export formats
    if args.csv:
        csv_path = analyzer.export_csv(videos)
        print(f"✓ CSV exported to: {csv_path}")

    if args.json:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_path = analyzer.output_dir / f"youtube_collection_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2)
        print(f"✓ JSON exported to: {json_path}")

    print(f"\n{'='*60}")
    print("Analysis complete!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
