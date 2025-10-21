# YouTube Collection Analyzer 📊

A powerful tool for analyzing multiple YouTube videos at once, generating insights, and creating beautiful reports!

## What It Does

The Collection Analyzer extends the basic YouTube analyzer to work with **multiple videos**, providing:

- 📊 **Batch Analysis** - Analyze dozens of videos in one go
- 🏆 **Top Performers** - Find most viewed, most liked, longest videos
- 📈 **Engagement Metrics** - Calculate like-to-view ratios
- 🎯 **Pattern Discovery** - Identify trending categories and tags
- 📑 **Multiple Export Formats** - Markdown, CSV, JSON, HTML Dashboard
- 💎 **Beautiful Dashboards** - Interactive HTML visualizations

## Quick Start

### Analyze Multiple Videos

```bash
# From URLs directly
python3 collection_analyzer.py \
  "https://www.youtube.com/watch?v=VIDEO_ID_1" \
  "https://www.youtube.com/watch?v=VIDEO_ID_2" \
  "https://www.youtube.com/watch?v=VIDEO_ID_3" \
  --dashboard --report
```

### Using a URL File

```bash
# Create a file with YouTube URLs (one per line)
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > my_videos.txt
echo "https://www.youtube.com/watch?v=9bZkp7q19f0" >> my_videos.txt

# Analyze all videos in the file
python3 collection_analyzer.py --file my_videos.txt --dashboard --csv
```

## Features

### 1. Comparison Analysis

Automatically compares all videos and finds:

- **Most Viewed** - Which video got the most eyeballs
- **Most Liked** - Highest like count
- **Longest/Shortest** - Duration extremes
- **Best Engagement** - Highest like-to-view ratio
- **Popular Categories** - Trending content types
- **Common Tags** - Most used tags across videos
- **Channel Distribution** - Videos per channel

### 2. Interactive HTML Dashboard

Generate a stunning visual dashboard:

```bash
python3 collection_analyzer.py --file videos.txt --dashboard
```

**Dashboard Features:**
- 📊 Real-time stats with animations
- 🏆 Top performer highlights
- 📈 Engagement rate charts
- 🎯 Category distribution bars
- 🏷️ Interactive tag cloud
- 📺 All video cards with metadata

### 3. Markdown Reports

Professional reports perfect for documentation:

```bash
python3 collection_analyzer.py --file videos.txt --report
```

**Report Includes:**
- Summary statistics
- Top performers section
- Engagement analysis
- Content analysis (categories/tags)
- Channel distribution

### 4. Data Export

Export for further analysis:

```bash
# CSV for spreadsheets
python3 collection_analyzer.py --file videos.txt --csv

# JSON for programming
python3 collection_analyzer.py --file videos.txt --json
```

## Usage Examples

### Example 1: Tech Conference Playlist Analysis

```bash
# Create URL file
cat > tech_conf.txt <<EOF
https://www.youtube.com/watch?v=VIDEO_1
https://www.youtube.com/watch?v=VIDEO_2
https://www.youtube.com/watch?v=VIDEO_3
EOF

# Generate complete analysis
python3 collection_analyzer.py \
  --file tech_conf.txt \
  --dashboard \
  --report \
  --csv \
  --output tech_analysis
```

This will create:
- `tech_analysis/dashboard_TIMESTAMP.html` - Interactive dashboard
- `tech_analysis/youtube_collection_report_TIMESTAMP.md` - Markdown report
- `tech_analysis/youtube_collection_TIMESTAMP.csv` - CSV data

### Example 2: Compare Top Videos from Different Channels

```bash
python3 collection_analyzer.py \
  "https://www.youtube.com/watch?v=CHANNEL_A_VIDEO" \
  "https://www.youtube.com/watch?v=CHANNEL_B_VIDEO" \
  "https://www.youtube.com/watch?v=CHANNEL_C_VIDEO" \
  --compare \
  --dashboard
```

### Example 3: Educational Content Analysis

```bash
# Analyze educational videos to find patterns
python3 collection_analyzer.py \
  --file educational_videos.txt \
  --report \
  --dashboard \
  --output education_report

# Opens insights into:
# - Which topics get most views
# - Optimal video duration
# - Most effective tags
# - Engagement patterns
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `urls` | YouTube video URLs (space-separated) |
| `-f, --file FILE` | File containing URLs (one per line) |
| `-o, --output DIR` | Output directory (default: collections) |
| `--report` | Generate Markdown report |
| `--csv` | Export to CSV |
| `--json` | Export to JSON |
| `--compare` | Show comparison analysis in terminal |
| `--dashboard` | Generate interactive HTML dashboard |

## URL File Format

Create a text file with one URL per line:

```text
# YouTube Video Collection
# Lines starting with # are comments

https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://www.youtube.com/watch?v=VIDEO_ID_3

# You can add comments anywhere
https://www.youtube.com/watch?v=VIDEO_ID_4
```

## Output Files

All generated files are saved to the output directory (default: `collections/`):

- `dashboard_YYYYMMDD_HHMMSS.html` - Interactive HTML dashboard
- `youtube_collection_report_YYYYMMDD_HHMMSS.md` - Markdown report
- `youtube_collection_YYYYMMDD_HHMMSS.csv` - CSV export
- `youtube_collection_YYYYMMDD_HHMMSS.json` - JSON export

## Analysis Metrics

### Summary Statistics
- Total videos analyzed
- Total duration (all videos combined)
- Total views (cumulative)
- Total likes (cumulative)
- Average views per video
- Average likes per video
- Average duration

### Engagement Rate
Calculated as: `(Likes / Views) × 100`

Higher engagement rates indicate content that resonates strongly with viewers.

### Pattern Analysis
- **Categories**: Which content types are most common
- **Tags**: Most frequently used tags across all videos
- **Channels**: Distribution of videos across channels

## Real-World Use Cases

### 1. Content Creator Analysis
Analyze your own video collection to find:
- What content performs best
- Optimal video length
- Most effective tags
- Engagement trends

### 2. Competitor Research
Study competitor channels:
- Compare engagement rates
- Identify successful content types
- Discover trending topics

### 3. Playlist Evaluation
Evaluate educational playlists:
- Total learning time
- Content distribution
- Viewer engagement
- Popular topics

### 4. Research & Data Collection
Gather YouTube data for:
- Academic research
- Market analysis
- Trend identification
- Content planning

## Tips & Tricks

### 1. Combine Multiple Reports

```bash
# Analyze and export everything
python3 collection_analyzer.py \
  --file videos.txt \
  --dashboard \
  --report \
  --csv \
  --json
```

### 2. Quick Stats Only

```bash
# Just see the comparison without files
python3 collection_analyzer.py --file videos.txt --compare
```

### 3. Organized Output

```bash
# Create project-specific directories
python3 collection_analyzer.py \
  --file project_videos.txt \
  --output reports/project_alpha \
  --dashboard --report
```

### 4. Integration with Other Tools

The CSV/JSON exports can be imported into:
- **Excel/Google Sheets** - Further analysis and charts
- **Python/R** - Statistical analysis
- **Tableau/PowerBI** - Advanced visualizations
- **Databases** - Long-term storage and querying

## Troubleshooting

### "No videos were successfully analyzed"

- Check your internet connection
- Verify URLs are valid and public
- Some videos may be region-restricted
- Age-restricted videos might not work

### "Module not found"

```bash
# Make sure you're in the right directory and venv is activated
cd youtube_analyzer
source venv/bin/activate
python3 collection_analyzer.py --help
```

### Dashboard not opening

- Make sure the HTML file was generated
- Try opening it manually in your browser
- Check file permissions

## Advanced Usage

### As a Python Module

```python
from collection_analyzer import CollectionAnalyzer

# Initialize
analyzer = CollectionAnalyzer(output_dir="my_analysis")

# Analyze videos
urls = [
    "https://www.youtube.com/watch?v=VIDEO_1",
    "https://www.youtube.com/watch?v=VIDEO_2",
]

videos = analyzer.analyze_multiple(urls)

# Get insights
comparison = analyzer.compare_videos(videos)

# Generate reports
analyzer.generate_markdown_report(comparison)
analyzer.export_csv(videos)

# Create dashboard
from dashboard_generator import DashboardGenerator
dash = DashboardGenerator()
dash.generate_html_dashboard(videos, comparison, "dashboard.html")
```

## Performance

- Analyzes ~1 video per 2-3 seconds
- 100 videos: ~3-5 minutes
- Network speed affects performance
- No API rate limits (uses yt-dlp)

## Requirements

- Python 3.7+
- yt-dlp
- Active internet connection
- All dependencies from `requirements.txt`

## Examples Included

See `example_urls.txt` for a template URL file.

## Credits

Built on top of:
- `youtube_analyzer.py` - Single video analysis
- `yt-dlp` - YouTube data extraction
- `dashboard_generator.py` - HTML dashboard creation

---

**Pro Tip**: Start with a small set of videos to get familiar with the tool, then scale up to larger collections!

## What's Next?

Want to analyze even more? Consider:
- Tracking videos over time
- Comparing different playlists
- Building a video database
- Creating custom visualizations

Happy analyzing! 🚀
