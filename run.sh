#!/usr/bin/env bash
cd "$(dirname "$0")"

if [[ ! -f venv/Scripts/python.exe ]]; then
  echo "Virtual muhit yaratilmoqda..."
  py -3.12 -m venv venv
  venv/Scripts/python.exe -m pip install -r requirements.txt
fi

venv/Scripts/python.exe bot.py
