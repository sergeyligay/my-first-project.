import os
from dotenv import load_dotenv
load_dotenv()
app_name = os.getenv("APP_NAME")
api_key = os.getenv("API_KEY")
missing_variables = []
if not app_name:
    missing_variables.append("APP_NAME")
if not api_key:
    missing_variableS.append("API_KEY")
if missing_variables:
    print("Error: Missing variables:",", ".join(missing_variables))
else:
    print(f"App name: {app_name}")
    print(f"API_KEY loaded: {bool(api_key)}")
