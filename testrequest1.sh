#!/bin/bash

curl -i -s -X POST --data "PASSKEY=12345678901234567890123456789012D&stationtype=EasyWeatherPro_V5.1.1&runtime=0&dateutc=2023-05-16+17:44:59&tempinf=71.8&humidityin=42&baromrelin=29.920&baromabsin=29.689&tempf=59.4&humidity=38&winddir=136&windspeedmph=0.67&windgustmph=1.12&maxdailygust=1.12&solarradiation=34.89&uv=0&rainratein=0.000&eventrainin=0.000&hourlyrainin=0.000&dailyrainin=0.000&weeklyrainin=0.031&monthlyrainin=0.031&yearlyrainin=0.031&totalrainin=0.031&wh65batt=0&freq=868M&model=WS2900_V2.01.18&interval=10" http://127.0.0.1:8081

