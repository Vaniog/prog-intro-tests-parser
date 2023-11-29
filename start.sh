#!/bin/bash
flask db upgrade
gunicorn -b 0.0.0.0:8000 "app:create_app()"