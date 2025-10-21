# Claude Code Skills for TempAI

This directory contains skills that extend Claude Code's capabilities for this project.

## Available Skills

### youtube-analyzer

Analyzes YouTube videos using the youtube_analyzer tool.

**Capabilities:**
- Extract video metadata (title, channel, views, duration, etc.)
- Download videos in best quality
- Download audio only (MP3 format)
- Extract transcripts and captions
- Export data to JSON

**How to invoke:**
- Use the slash command: `/youtube` followed by a YouTube URL
- Or invoke directly: Use the `youtube-analyzer` skill and provide a URL

**Example usage:**
```
/youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Slash Commands

### /youtube

Quick command to analyze YouTube videos.

**Usage:**
```
/youtube <youtube-url>
```

**What it does:**
1. Extracts video information
2. Displays metadata clearly
3. Asks if you want to download or extract more info
4. Executes your choice

## Direct Tool Usage

You can also use the YouTube analyzer tool directly:

```bash
# From repository root
cd youtube_analyzer
source venv/bin/activate
python3 youtube_analyzer.py "URL" [options]
```

**Options:**
- `--info` - Get video information
- `--download` - Download video
- `--audio` - Download audio only
- `--transcript` - Get transcript info
- `--json` - Output as JSON

See `youtube_analyzer/README.md` for complete documentation.

## Adding New Skills

To add a new skill:

1. Create a new `.md` file in `.claude/skills/`
2. Write clear instructions for what the skill should do
3. Include workflow steps and examples
4. Optionally create a slash command in `.claude/commands/`

## Notes

- Skills are loaded automatically by Claude Code
- Use descriptive names for easy invocation
- Include error handling instructions
- Provide clear examples and workflows
