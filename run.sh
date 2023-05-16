#!/bin/bash

export PASSKEYS="12345678901234567890123456789012D=home"
export WRITE_URL="http://127.0.0.1:8082"

./ecowitt2openmetrics.py
