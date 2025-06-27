# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'eec6ce93fa5949bda84836e62d8f2107cc2e1d26b1844139')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flask_session_data')

    IP_WHITELIST_ENABLED = os.getenv('IP_WHITELIST_ENABLED', 'False').lower() == 'true'
    IP_WHITELIST = [ip.strip() for ip in os.getenv('IP_WHITELIST', '').split(',') if ip.strip()]

    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'adminpass')
    ADMIN_RECOVERY_KEY = os.getenv('ADMIN_RECOVERY_KEY', 'recovery123')

    # ✅ Yeh do line uncomment karke chhodo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
