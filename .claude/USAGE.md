# Claude Code Usage Guide for TempAI

## YouTube Analyzer Skill

This project includes a powerful YouTube analysis skill that can be invoked in multiple ways.

### Quick Start

**Option 1: Use the slash command**
```
/youtube https://www.youtube.com/watch?v=VIDEO_ID
```

**Option 2: Invoke the skill**
```
Use the youtube-analyzer skill to analyze this video: https://www.youtube.com/watch?v=VIDEO_ID
```

**Option 3: Direct tool usage**
```bash
cd youtube_analyzer
source venv/bin/activate
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --info
```

### What the Skill Does

When you use the YouTube analyzer skill, Claude will:

1. **Extract video information**
   - Title, channel, duration
   - View count, likes
   - Upload date
   - Description
   - Categories and tags

2. **Present it clearly**
   - Formatted, easy-to-read output
   - Key metrics highlighted

3. **Offer options**
   - Download video
   - Download audio only (MP3)
   - Get transcript/captions
   - Export to JSON

4. **Execute your choice**
   - Downloads saved to `youtube_analyzer/downloads/`
   - Progress tracking shown
   - Success/error messages

### Example Workflows

#### Just Get Info
```
/youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
Claude will show you video details and ask what you want to do next.

#### Download Audio
```
/youtube https://www.youtube.com/watch?v=VIDEO_ID
```
Then when prompted, say: "Download the audio as MP3"

#### Export Metadata
```
/youtube https://www.youtube.com/watch?v=VIDEO_ID
```
Then: "Export the information to JSON"

### Available Commands

| Command | Description |
|---------|-------------|
| `/youtube <url>` | Analyze YouTube video |
| `/help` | Get help with Claude Code |

### Tips

- The skill handles SSL certificates automatically
- Downloads are saved to `youtube_analyzer/downloads/`
- JSON exports are saved to current directory
- The tool works best in environments with normal network access
- FFmpeg is required for audio extraction (MP3)

### Troubleshooting

**"Network error" or "Unable to extract"**
- You may be in a restricted environment
- Try running the tool locally on your machine

**"FFmpeg not found"**
- Install FFmpeg to enable audio extraction:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install ffmpeg

  # macOS
  brew install ffmpeg
  ```

**"Module not found"**
- Make sure dependencies are installed:
  ```bash
  cd youtube_analyzer
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Direct Python Usage

You can also use the YouTubeAnalyzer class in your own scripts:

```python
from youtube_analyzer import YouTubeAnalyzer

analyzer = YouTubeAnalyzer(output_dir="my_downloads")
info = analyzer.get_video_info("https://www.youtube.com/watch?v=VIDEO_ID")
print(info['title'])
```

See `youtube_analyzer/README.md` for complete API documentation.

### Adding More Skills

Skills are stored in `.claude/skills/` and can be extended. See `.claude/skills/README.md` for details on creating new skills.

---

For more information:
- YouTube Analyzer: `youtube_analyzer/README.md`
- Skills Documentation: `.claude/skills/README.md`
- Claude Code Docs: https://docs.claude.com/claude-code
