#!/bin/bash
uvicorn chat_app.app.main:app --host 0.0.0.0 --port 7777 --reload
