from dotenv import load_dotenv
import os

load_dotenv()

HTTP_PORT = os.environ.get("HTTP_PORT", 5002)
HTTP_HOST = os.environ.get("HTTP_HOST", "0.0.0.0")
DEBUG_MODE = eval(os.environ.get("DEBUG_MODE", "False"))

OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
SLACK_BOT_TOKEN=os.environ.get("SLACK_BOT_TOKEN")
SPREADSHEET_ID=os.environ.get("SPREADSHEET_ID")
SLACK_WORKSPACE_ID=os.environ.get("SLACK_WORKSPACE_ID")
GCP_SERVICE_ACC_KEY=os.environ.get("GCP_SERVICE_ACC_KEY")

GENERAL_ANNOUCEMENT_SLACK_CHANNEL=os.environ.get("GENERAL_ANNOUCEMENT_SLACK_CHANNEL")
MADATORY_CHANNELS=os.environ.get("MADATORY_CHANNELS")
BOT_SLACK_USER_ID=os.environ.get("BOT_SLACK_USER_ID")
HR_SLACK_USER_ID=os.environ.get("HR_SLACK_USER_ID")