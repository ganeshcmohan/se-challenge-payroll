#!/bin/bash
gunicorn run:app -w 1 --bind 0.0.0.0:5000 --log-level debug  # Start gunicorn
