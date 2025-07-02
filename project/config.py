"""
Module: config.py
Description: Application configuration settings, including database and secret key.
"""

import os

class Config:
    """
    Base configuration class using environment variables or defaults.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
