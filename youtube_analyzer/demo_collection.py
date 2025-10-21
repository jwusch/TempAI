#!/usr/bin/env python3
"""
Demo script for YouTube Collection Analyzer
Shows how to use the tool programmatically
"""

from collection_analyzer import CollectionAnalyzer
from dashboard_generator import DashboardGenerator

def main():
    print("="*60)
    print("YouTube Collection Analyzer - Demo")
    print("="*60)

    # Example URLs (these will work when you have network access)
    demo_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    ]

    print("\nDemo URLs:")
    for i, url in enumerate(demo_urls, 1):
        print(f"  {i}. {url}")

    print("\n" + "-"*60)
    print("Initializing Collection Analyzer...")
    print("-"*60)

    # Create analyzer
    analyzer = CollectionAnalyzer(output_dir="demo_output")

    print("\nAnalyzing videos...")
    print("(This will fail in restricted environments)")
    print()

    # Analyze videos
    videos = analyzer.analyze_multiple(demo_urls, progress=True)

    if not videos:
        print("\n⚠️  No videos could be analyzed in this environment.")
        print("This is normal for restricted/sandboxed environments.")
        print("\nTo see the tool in action:")
        print("  1. Run this on your local machine")
        print("  2. Or use the command line:")
        print("     python3 collection_analyzer.py --file example_urls.txt --dashboard")
        return

    print("\n" + "="*60)
    print(f"Successfully analyzed {len(videos)} video(s)!")
    print("="*60)

    # Generate comparison
    print("\nGenerating comparison analysis...")
    comparison = analyzer.compare_videos(videos)

    # Show some stats
    print("\n📊 Quick Stats:")
    summary = comparison.get('summary', {})
    print(f"  Total Videos: {summary.get('total_videos', 0)}")
    print(f"  Total Views: {summary.get('total_views', 0):,}")
    print(f"  Total Likes: {summary.get('total_likes', 0):,}")
    print(f"  Total Duration: {summary.get('total_duration', 'N/A')}")

    # Generate all outputs
    print("\n📝 Generating outputs...")

    # Markdown report
    report_path = analyzer.generate_markdown_report(comparison)
    print(f"  ✓ Markdown report: {report_path}")

    # CSV export
    csv_path = analyzer.export_csv(videos)
    print(f"  ✓ CSV export: {csv_path}")

    # JSON export
    import json
    from pathlib import Path
    from datetime import datetime

    json_path = analyzer.output_dir / f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_path, 'w') as f:
        json.dump(videos, f, indent=2)
    print(f"  ✓ JSON export: {json_path}")

    # HTML Dashboard
    dashboard_gen = DashboardGenerator()
    dashboard_path = analyzer.output_dir / f"demo_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    dashboard_gen.generate_html_dashboard(videos, comparison, str(dashboard_path))
    print(f"  ✓ HTML dashboard: {dashboard_path}")

    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print(f"\nCheck the 'demo_output' directory for all generated files.")
    print("Open the HTML dashboard in your browser for an interactive view!")


if __name__ == '__main__':
    main()
