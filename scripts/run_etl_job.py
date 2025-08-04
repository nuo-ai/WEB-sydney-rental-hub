import subprocess
import sys
import os
import logging
from datetime import datetime
from typing import Tuple
import requests
from dotenv import load_dotenv

# Configure basic logging
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"etl_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(dotenv_path)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_notification(message: str, success: bool):
    """Sends a notification to the configured Discord webhook."""
    if not DISCORD_WEBHOOK_URL:
        logging.warning("DISCORD_WEBHOOK_URL not set. Skipping notification.")
        return

    color = 65280 if success else 16711680  # Green for success, Red for failure
    title = "✅ ETL任务成功" if success else "❌ ETL任务失败"

    payload = {
        "embeds": [{
            "title": title,
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("Successfully sent Discord notification.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Discord notification: {e}")

def run_etl_process() -> Tuple[bool, str]:
    """
    Runs the main ETL process script (process_csv.py) and captures its output.
    Returns a tuple of (success_boolean, summary_string).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    etl_script_path = os.path.join(script_dir, '..', 'database', 'process_csv.py')
    
    logging.info(f"Executing ETL script: {etl_script_path}")
    
    try:
        process = subprocess.run(
            [sys.executable, etl_script_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        logging.info("--- ETL Script Output ---")
        logging.info(process.stdout)
        if process.stderr:
            logging.warning("--- ETL Script Errors (stderr) ---")
            logging.warning(process.stderr)
        
        # Extract summary from stdout for notification
        summary = "\n".join(line for line in process.stdout.splitlines() if "房源" in line or "下架" in line)
        return True, summary

    except FileNotFoundError:
        error_message = f"ETL script not found at: {etl_script_path}"
        logging.error(error_message)
        return False, error_message
    except subprocess.CalledProcessError as e:
        error_message = f"ETL script failed with exit code {e.returncode}.\n**Error Output**:\n```\n{e.stderr[-1000:]}\n```"
        logging.error(error_message)
        return False, error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logging.error(error_message, exc_info=True)
        return False, error_message

def main():
    """
    Main function to orchestrate the ETL job and send notifications.
    """
    logging.info("="*50)
    logging.info("Starting Automated ETL Job")
    logging.info("="*50)
    
    success, summary = run_etl_process()
    
    if success:
        message = f"ETL任务成功完成。\n\n**处理结果**:\n```\n{summary}\n```"
        send_discord_notification(message, success=True)
    else:
        message = f"ETL任务执行失败。\n\n**错误详情**:\n{summary}"
        send_discord_notification(message, success=False)

    logging.info("="*50)
    logging.info("Automated ETL Job Finished")
    logging.info("="*50)

if __name__ == "__main__":
    main()
