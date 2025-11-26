"""
Monthly Concert Program Update Script
======================================
Master script that runs the complete monthly update workflow:
1. Scrape concerts from all venues
2. Generate HTML program page

Usage:
    python run_monthly_update.py

Configuration:
    Month and year are read from kluby.json
"""

import subprocess
import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from kluby.json"""
    try:
        with open('kluby.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config['config']
    except Exception as e:
        logger.error(f"Failed to load kluby.json: {e}")
        sys.exit(1)


def run_script(script_name, description):
    """Run a Python script and check for errors"""
    logger.info(f"\n{'=' * 60}")
    logger.info(f"STEP: {description}")
    logger.info(f"{'=' * 60}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        logger.info(f"\n✅ {description} - COMPLETED")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"\n❌ {description} - FAILED")
        logger.error(f"Error: {e}")
        return False


def main():
    """Run the complete monthly update workflow"""
    logger.info("\n" + "=" * 60)
    logger.info("MONTHLY CONCERT PROGRAM UPDATE")
    logger.info("=" * 60)

    # Load configuration
    config = load_config()
    month_name = config['mesic']
    year = config['rok']

    logger.info(f"Month: {month_name} {year}")
    logger.info(f"Days in month: {config['pocet_dni']}")
    logger.info("=" * 60)

    # Step 1: Scrape concerts
    if not run_script('scrape_concerts.py', 'Scraping concerts from all venues'):
        logger.error("\n⚠️  Scraping failed! HTML generation skipped.")
        sys.exit(1)

    # Check if events_data.json was created
    if not Path('events_data.json').exists():
        logger.error("\n⚠️  events_data.json not found! Cannot generate HTML.")
        sys.exit(1)

    # Step 2: Generate HTML
    if not run_script('generate_html.py', 'Generating HTML program page'):
        logger.error("\n⚠️  HTML generation failed!")
        sys.exit(1)

    # Success summary
    logger.info("\n" + "=" * 60)
    logger.info("✅ MONTHLY UPDATE COMPLETE")
    logger.info("=" * 60)

    # Load events data for summary
    try:
        with open('events_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_events = data['total_events']
            total_venues = len(data['venues'])

            logger.info(f"Total events collected: {total_events}")
            logger.info(f"Venues with data: {total_venues}")
            logger.info(f"Output: programy/index.html")
    except Exception as e:
        logger.warning(f"Could not load summary: {e}")

    logger.info("=" * 60)
    logger.info("\nNext steps:")
    logger.info("1. Open programy/index.html in your browser to review")
    logger.info("2. If satisfied, commit and push:")
    logger.info(f"   git add .")
    logger.info(f"   git commit -m \"feat: add {month_name} {year} program\"")
    logger.info(f"   git push origin main")
    logger.info("=" * 60 + "\n")


if __name__ == '__main__':
    main()
