#!/usr/bin/env python3
"""
YouTube Collection Dashboard Generator
Creates beautiful HTML dashboards from video collection analysis
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List
import json


class DashboardGenerator:
    """Generates HTML dashboards for video collection analysis."""

    def __init__(self):
        """Initialize the dashboard generator."""
        pass

    def generate_html_dashboard(self, videos: List[Dict], comparison: Dict, output_path: str = None):
        """
        Generate an interactive HTML dashboard.

        Args:
            videos: List of video info dictionaries
            comparison: Comparison analysis dictionary
            output_path: Path to save HTML file

        Returns:
            str: Path to generated HTML file
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"dashboard_{timestamp}.html"

        summary = comparison.get('summary', {})

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Collection Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}

        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header .timestamp {{
            opacity: 0.9;
            font-size: 1.1em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}

        .stat-card .value {{
            color: #333;
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .section h2 {{
            color: #333;
            margin-bottom: 25px;
            font-size: 2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        .top-video {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        .top-video h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        .top-video .video-title {{
            color: #667eea;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .top-video .stats {{
            color: #666;
            font-size: 1em;
        }}

        .top-video a {{
            color: #667eea;
            text-decoration: none;
            word-break: break-all;
        }}

        .top-video a:hover {{
            text-decoration: underline;
        }}

        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}

        .video-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }}

        .video-card:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left-width: 8px;
        }}

        .video-card .title {{
            color: #333;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}

        .video-card .channel {{
            color: #667eea;
            margin-bottom: 8px;
        }}

        .video-card .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}

        .tag-cloud {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .tag {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            transition: transform 0.2s ease;
        }}

        .tag:hover {{
            transform: scale(1.1);
        }}

        .engagement-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            margin: 10px 0;
            overflow: hidden;
            position: relative;
        }}

        .engagement-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
            transition: width 1s ease;
        }}

        .chart-container {{
            margin: 20px 0;
        }}

        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .bar-label {{
            min-width: 200px;
            color: #333;
            font-weight: 500;
        }}

        .bar {{
            flex: 1;
            background: #e0e0e0;
            border-radius: 5px;
            height: 25px;
            position: relative;
            overflow: hidden;
        }}

        .bar-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            transition: width 1s ease;
        }}

        .bar-value {{
            min-width: 80px;
            text-align: right;
            color: #666;
            font-weight: bold;
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.9;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 YouTube Collection Dashboard</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">Total Videos</div>
                <div class="value">{summary.get('total_videos', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Views</div>
                <div class="value">{self._format_number(summary.get('total_views', 0))}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Likes</div>
                <div class="value">{self._format_number(summary.get('total_likes', 0))}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Duration</div>
                <div class="value">{summary.get('total_duration', 'N/A')}</div>
            </div>
        </div>

        <div class="section">
            <h2>🏆 Top Performers</h2>

            <div class="top-video">
                <h3>🎥 Most Viewed</h3>
                <div class="video-title">{comparison.get('most_viewed', {}).get('title', 'N/A')}</div>
                <div class="stats">Views: {self._format_number(comparison.get('most_viewed', {}).get('views', 0))}</div>
                <a href="{comparison.get('most_viewed', {}).get('url', '#')}" target="_blank">Watch Video →</a>
            </div>

            <div class="top-video">
                <h3>❤️ Most Liked</h3>
                <div class="video-title">{comparison.get('most_liked', {}).get('title', 'N/A')}</div>
                <div class="stats">Likes: {self._format_number(comparison.get('most_liked', {}).get('likes', 0))}</div>
                <a href="{comparison.get('most_liked', {}).get('url', '#')}" target="_blank">Watch Video →</a>
            </div>

            <div class="top-video">
                <h3>⏱️ Longest Video</h3>
                <div class="video-title">{comparison.get('longest_video', {}).get('title', 'N/A')}</div>
                <div class="stats">Duration: {comparison.get('longest_video', {}).get('duration', 'N/A')}</div>
                <a href="{comparison.get('longest_video', {}).get('url', '#')}" target="_blank">Watch Video →</a>
            </div>
        </div>

        <div class="section">
            <h2>📈 Engagement Analysis</h2>
            {self._generate_engagement_html(comparison.get('engagement_rates', []))}
        </div>

        <div class="section">
            <h2>🎯 Top Categories</h2>
            <div class="chart-container">
                {self._generate_category_chart(comparison.get('top_categories', {}))}
            </div>
        </div>

        <div class="section">
            <h2>🏷️ Popular Tags</h2>
            <div class="tag-cloud">
                {self._generate_tags(comparison.get('top_tags', {}))}
            </div>
        </div>

        <div class="section">
            <h2>📺 All Videos</h2>
            <div class="video-grid">
                {self._generate_video_cards(videos)}
            </div>
        </div>

        <div class="footer">
            <p>Generated by YouTube Collection Analyzer</p>
            <p>Powered by yt-dlp</p>
        </div>
    </div>

    <script>
        // Animate bars on load
        window.addEventListener('load', () => {{
            document.querySelectorAll('.bar-fill, .engagement-fill').forEach(el => {{
                const width = el.style.width;
                el.style.width = '0%';
                setTimeout(() => {{
                    el.style.width = width;
                }}, 100);
            }});
        }});
    </script>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path

    def _format_number(self, num):
        """Format large numbers with K, M, B suffixes."""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)

    def _generate_engagement_html(self, engagement_rates):
        """Generate HTML for engagement rate display."""
        if not engagement_rates:
            return "<p>No engagement data available</p>"

        html = '<div class="bar-chart">'
        max_rate = max([e['engagement_rate'] for e in engagement_rates], default=1)

        for item in engagement_rates[:5]:
            width = (item['engagement_rate'] / max_rate * 100) if max_rate > 0 else 0
            html += f"""
            <div class="bar-item">
                <div class="bar-label">{item['title'][:30]}...</div>
                <div class="bar">
                    <div class="bar-fill" style="width: {width}%"></div>
                </div>
                <div class="bar-value">{item['engagement_rate']}%</div>
            </div>
            """

        html += '</div>'
        return html

    def _generate_category_chart(self, categories):
        """Generate HTML for category chart."""
        if not categories:
            return "<p>No category data available</p>"

        html = '<div class="bar-chart">'
        max_count = max(categories.values(), default=1)

        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            width = (count / max_count * 100) if max_count > 0 else 0
            html += f"""
            <div class="bar-item">
                <div class="bar-label">{category}</div>
                <div class="bar">
                    <div class="bar-fill" style="width: {width}%"></div>
                </div>
                <div class="bar-value">{count}</div>
            </div>
            """

        html += '</div>'
        return html

    def _generate_tags(self, tags):
        """Generate HTML for tag cloud."""
        if not tags:
            return "<p>No tags available</p>"

        html = ""
        for tag, count in list(tags.items())[:15]:
            html += f'<span class="tag">{tag} ({count})</span>'

        return html

    def _generate_video_cards(self, videos):
        """Generate HTML for video cards."""
        if not videos:
            return "<p>No videos available</p>"

        html = ""
        for video in videos:
            html += f"""
            <div class="video-card">
                <div class="title">{video.get('title', 'Unknown')[:80]}</div>
                <div class="channel">📺 {video.get('channel', 'Unknown')}</div>
                <div class="meta">👁️ {self._format_number(video.get('view_count', 0))} views</div>
                <div class="meta">❤️ {self._format_number(video.get('like_count', 0))} likes</div>
                <div class="meta">⏱️ {video.get('duration', 'N/A')}</div>
                <div class="meta">📅 {video.get('upload_date', 'N/A')}</div>
            </div>
            """

        return html


if __name__ == '__main__':
    print("This module is meant to be imported, not run directly.")
    print("Use collection_analyzer.py with --dashboard option to generate dashboards.")
