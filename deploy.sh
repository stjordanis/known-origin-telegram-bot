#!/usr/bin/env bash

gcloud config configurations activate ko-bot

gcloud beta functions deploy telegram_webhook --set-env-vars "TELEGRAM_TOKEN=CHANGE_ME_NOW" --runtime python37 --trigger-http
