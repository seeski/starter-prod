#!/bin/sh


gunicorn ./src/proj.wsgi:application --bind 0.0.0.0:8000