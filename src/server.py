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
    '/status/pin/(\d+)', 'status_pin',
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
        output ['POST/setup'] = 'Setup the board Example : curl -X POST  -H "Content-Type: application/json" -d \'{"board_mode":"board","pins":[{"pin":3, "es":"out", "initial":"low"}, {"pin":20, "type":"AM2302"}]}\' http://0.0.0.0:8080/setup'
        output ['GET/status'] = 'Get the status of the pins for the current board'
        output ['PUT/status'] = 'Change the value of one or more pins : curl -X PUT  -H "Content-Type: application/json" -d \'{"pins": [{ "pin" : "40", "value" : 1}] }\' http://0.0.0.0:8080/status'
        return str(output)

class model:
    def GET(self):
        return json.dumps(card.getModelInfo())

    def PUT(self):
        data = json.loads(web.data())
        print "/PUT: model",[data]
        card.setModel(data['model'])

class setup:
    def GET(self):
        return json.dumps(card.getSetup())

    def POST(self):
        try:
            data = json.loads(web.data())
        except ValueError as e:
            print e, web.data()
            raise
        print "/POST : setup",[data]
        card.setup(data)
        return json.dumps(card.getSetup())

class status:
    def GET(self):
        return json.dumps(card.getStatus())

    def PUT(self):
        data = json.loads(web.data())
        print "/PUT : status",[data]
        card.status(data)
        return json.dumps(card.getStatus())

class status_pin:
    def GET(self, pin):
        print "/GET : single_pin", pin
        return json.dumps(card.getStatusByPin(int(pin)))

    def PUT(self, pin):
        data = json.loads(web.data())
        print "/PUT : single_pin",[data]
        card.status(data, int(pin))
        return json.dumps(card.getStatusByPin(int(pin)))

if __name__ == "__main__":
    app.run()

