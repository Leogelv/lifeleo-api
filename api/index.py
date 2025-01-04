from fastapi import FastAPI
import sys
import os

# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Экспортируем app для Vercel
app = app 