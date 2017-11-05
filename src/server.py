#!/usr/bin/env python
import Adafruit_DHT
import web
import json
import config
from raspberry import Raspberry
from model import models

urls = (
    '/help'  , 'help',
    '/model' , 'model',
    '/status', 'status',
    '/setup' , 'setup',
)

app = web.application(urls, globals())

card = Raspberry() 

class help:
    def GET(self):
	import datetime,time
        output = {}
        output ['help'] = 'This help'
	output['timestamp'] =  datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        output ['GET/model'] = 'Get the configuration of the current mode'
        output ['PUT/model'] = 'Set a model, you can choose among this list : ' + str(models.keys()) + ' Example : curl -X PUT  -H "Content-Type: application/json" -d \'{"model":"pi_zero_w"}\' http://0.0.0.0:8080/model'
        output ['GET/setup'] = 'Get the setup for the current board'
        output ['PUT/setup'] = 'Setup the board Example : curl -X PUT  -H "Content-Type: application/json" -d \'{"board_mode":"board","pins":[{"pin":3, "es":"out", "initial":"low"}, {"pin":20, "extra":"AM2302"}]}\' http://0.0.0.0:8080/setup'
        output ['GET/status'] = 'Get the status of the pins for the current board'
        output ['PUT/status'] = 'Change the value of one or more pins : curl -X PUT  -H "Content-Type: application/json" -d \'{"pins": [{ "pin" : "40", "value" : 1}] }\' http://0.0.0.0:8080/status'
        return str(output)

class model:
    def GET(self):
        return card.getModelInfo()

    def PUT(self):
        data = json.loads(web.data())
        card.setModel(data['model'])

class setup:
    def GET(self):
        return card.getSetup()

    def PUT(self):
        data = json.loads(web.data())
        card.setup(data)
        return card.getSetup()

class status:
    def GET(self):
        return card.getStatus()

    def PUT(self):
        data = json.loads(web.data())
        card.status(data)
        return card.getStatus()

if __name__ == "__main__":
    app.run()

