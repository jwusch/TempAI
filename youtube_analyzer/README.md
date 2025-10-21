# YouTube Video Analyzer

A powerful Python tool to download and analyze YouTube videos using yt-dlp.

## 🆕 NEW: Collection Analyzer

**Analyze multiple videos at once!** Check out the new [Collection Analyzer](COLLECTION_ANALYZER.md) for:
- 📊 Batch analysis of multiple videos
- 🏆 Find top performers and trends
- 📈 Engagement rate calculations
- 🎨 Beautiful HTML dashboards
- 📑 Export to Markdown, CSV, JSON

[Read the Collection Analyzer Guide →](COLLECTION_ANALYZER.md)

## Features

### Single Video Analysis
- Extract detailed video metadata (title, description, views, likes, duration, etc.)
- Download videos in best quality
- Download audio only (MP3 format)
- Extract subtitles and captions
- Get transcript information
- JSON output support for automation
- Progress tracking during downloads

### Collection Analysis (NEW!)
- Analyze multiple videos in batch
- Generate comparison reports
- Create interactive dashboards
- Export to multiple formats
- Find patterns and insights

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Navigate to the youtube_analyzer directory:
   ```bash
   cd youtube_analyzer
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Commands

#### Get Video Information (No Download)
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --info
```

#### Download Video
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --download
```

#### Download Audio Only (MP3)
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio
```

#### Get Full Transcript/Captions (NEW!)
```bash
# Get English transcript
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript

# Get transcript in another language
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript --lang es

# Get transcript as JSON with timestamps
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript --json
```

The transcript feature now extracts the **full text** with:
- Complete transcript text
- Timestamped segments
- Multiple language support
- Automatic or manual captions

#### Custom Output Directory
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --download -o /path/to/output
```

#### JSON Output (for scripting)
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --json
```

### Using the Shell Wrapper

For easier usage, you can use the provided shell script:

```bash
./analyze.sh "https://www.youtube.com/watch?v=VIDEO_ID" --info
```

The script automatically:
- Creates and activates a virtual environment
- Installs dependencies if needed
- Runs the analyzer

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--info` | `-i` | Display video information only (default if no option specified) |
| `--download` | `-d` | Download the video in best quality |
| `--audio` | `-a` | Download audio only as MP3 |
| `--transcript` | `-t` | Extract full transcript/captions with text |
| `--output DIR` | `-o DIR` | Specify output directory (default: downloads) |
| `--lang CODE` | | Language code for transcript (default: en) |
| `--json` | | Output in JSON format for scripting |

## Examples

### Example 1: Get Basic Video Info
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=e2zIr_2JMbE" --info
```

Output:
```
============================================================
Title: Example Video Title
============================================================
Channel: Channel Name
Upload Date: 20241015
Duration: 0:10:45
Views: 1,234,567
Likes: 12,345
Video ID: e2zIr_2JMbE
URL: https://www.youtube.com/watch?v=e2zIr_2JMbE

Categories: Education, Science
Captions Available: True
Caption Languages: en, es, fr, de, ja

Description:
This is an example video description...
============================================================
```

### Example 2: Download Video and Audio
```bash
# Download video
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --download

# Download audio only
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio
```

### Example 3: Get JSON Output for Automation
```bash
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --json > video_info.json
```

### Example 4: Combine Multiple Operations
```bash
# Get info and transcript
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --info --transcript
```

## Output

Downloaded files are saved in the `downloads` directory (or custom directory specified with `-o`) with the following naming pattern:
- Videos: `{video_title}.{ext}`
- Audio: `{video_title}.mp3`
- Subtitles: `{video_title}.{lang}.{ext}`

## Metadata Extracted

The tool extracts comprehensive metadata including:

- **Basic Info**: Title, Channel, Video ID, URL
- **Statistics**: Views, Likes, Duration
- **Content**: Description, Categories, Tags
- **Media**: Thumbnail URL, Available formats
- **Captions**: Available languages, Manual vs Auto-generated
- **Timestamps**: Upload date

## Troubleshooting

### SSL Certificate Errors
The tool includes SSL certificate bypass options. If you still encounter SSL errors, ensure your system certificates are up to date.

### "Unable to extract player response"
This can occur due to:
- Network restrictions or firewalls
- YouTube API changes (update yt-dlp: `pip install --upgrade yt-dlp`)
- Geographic restrictions on the video

### FFmpeg Required for Audio Extraction
For audio-only downloads (MP3), FFmpeg must be installed:
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Advanced Usage

### Using as a Python Module
```python
from youtube_analyzer import YouTubeAnalyzer

analyzer = YouTubeAnalyzer(output_dir="my_downloads")

# Get video info
info = analyzer.get_video_info("https://www.youtube.com/watch?v=VIDEO_ID")
print(info['title'])

# Download video
result = analyzer.download_video("https://www.youtube.com/watch?v=VIDEO_ID")
print(result['filename'])

# Get transcript info
transcript = analyzer.get_transcript("https://www.youtube.com/watch?v=VIDEO_ID")
print(transcript['available_languages'])
```

## Dependencies

- **yt-dlp**: YouTube video downloader and metadata extractor
- **requests**: HTTP library for Python

## Notes

- The tool respects YouTube's terms of service
- Downloads are for personal use only
- Some videos may have download restrictions
- Age-restricted or private videos may not be accessible

## Environment Limitations

Note: Some containerized or restricted environments may not allow direct YouTube access. The tool is fully functional in standard Linux, macOS, and Windows environments with normal network access.

## License

This tool is provided as-is for educational and personal use.

## Support

For issues with:
- **yt-dlp**: Visit [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp/issues)
- **This tool**: Check your Python version, dependencies, and network access
