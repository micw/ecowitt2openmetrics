#!/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl
from pprint import pprint
import sys,os
import requests

host = "0.0.0.0"
port = 8081
passkeys={}
write_url=None
debug=False

def addMetric(metrics,data,source_key,factor,metric,tags=[]):
    if not source_key in data:
        return
    value=float(data[source_key])
    if callable(factor):
        value=factor(value)
    else:
        value=value*factor
    metrics.append("%s{%s} %s" % (metric,','.join('%s="%s"'%(k,v) for k,v in tags.items()),value))

def fahrenheit_to_celsius(x):
    return (x-32)*5/9;    

def handle_request(data):
    if (debug):
        pprint(data)
    passkey=data.get("PASSKEY")
    if not passkey:
        print("Missing PASSKEY")
        return False
    sensor=passkeys.get(passkey,None)
    if not sensor:
        print("Unkown PASSKEY: %s" % passkey)
        return False
    
    metrics=[]
    # inside metrics
    addMetric(metrics,data,"tempinf",fahrenheit_to_celsius,"temperature", { "sensor": sensor, "loc": "in" })
    addMetric(metrics,data,"humidityin",1,"air_humidity", { "sensor": sensor, "loc": "in" })
    addMetric(metrics,data,"baromabsin",33.8639,"air_pressure", { "sensor": sensor, "loc": "in" })

    # outside metrics
    addMetric(metrics,data,"tempf",fahrenheit_to_celsius,"temperature", { "sensor": sensor, "loc": "out" })
    addMetric(metrics,data,"humidity",1,"air_humidity", { "sensor": sensor, "loc": "out" })
    addMetric(metrics,data,"winddir",1,"wind_direction", { "sensor": sensor })
    addMetric(metrics,data,"windspeedmph",1.609344,"wind_speed", { "sensor": sensor, "time": "instant" })
    addMetric(metrics,data,"windgustmph",1.609344,"wind_speed", { "sensor": sensor, "time": "gust" })
    addMetric(metrics,data,"maxdailygust",1.609344,"wind_speed", { "sensor": sensor, "time": "day" })
    addMetric(metrics,data,"rainratein",1,"rain_rate", { "sensor": sensor })
    addMetric(metrics,data,"eventrainin",1,"rain", { "sensor": sensor, "time": "event" })
    addMetric(metrics,data,"hourlyrainin",1,"rain", { "sensor": sensor, "time": "hour" })
    addMetric(metrics,data,"dailyrainin",1,"rain", { "sensor": sensor, "time": "day" })
    addMetric(metrics,data,"weeklyrainin",1,"rain", { "sensor": sensor, "time": "week" })
    addMetric(metrics,data,"monthlyrainin",1,"rain", { "sensor": sensor, "time": "month" })
    addMetric(metrics,data,"yearlyrainin",1,"rain", { "sensor": sensor, "time": "year" })
    addMetric(metrics,data,"totalrainin",1,"rain", { "sensor": sensor, "time": "total" })
    addMetric(metrics,data,"solarradiation",1,"solar_radiation", { "sensor": sensor })
    addMetric(metrics,data,"uv",1,"uv_index", { "sensor": sensor })

    requests.post(write_url, data="\n".join(metrics))

    return True

class RequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):

        try:
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len).decode("utf-8")
            data = dict(parse_qsl(post_body))
            if handle_request(data):
                self.send_response(200, "OK")
            else:
                self.send_error(403, 'Forbidden.')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            self.send_error(400, 'Bad request.')
            return

def start_webserver():
    webServer = HTTPServer((host, port), RequestHandler)
    print("Listening on http://%s:%s" % (host, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Shutdown")

if __name__ == "__main__":

    if not "PASSKEYS" in os.environ:
        print("Please set the PASSKEYS env variable")
        quit(1)
    if not "WRITE_URL" in os.environ:
        print("Please set the WRITE_URL env variable")
        quit(1)

    passkeys=dict(x.split("=") for x in os.environ.get("PASSKEYS").split())
    print("Using PASSKEYS:")
    pprint(passkeys)

    write_url=os.environ.get("WRITE_URL")
    print ("Using write URL: ",write_url)

    debug=bool(os.environ.get("DEBUG","False"))

    start_webserver()