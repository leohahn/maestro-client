from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/scheduler/<scheduler_name>/rooms/<room_name>/address")
def address_polling(scheduler_name, room_name):
    return '{"host": "192.168.10.11", "ports": [{"port": 12000, "name": "tcp"}]}'

@app.route("/scheduler/<scheduler_name>/rooms/<room_name>/ping", methods=['PUT'])
def ping(scheduler_name, room_name):
    print "ping called with data: {0}".format(request.data)
    return '{"success":true}'

@app.route("/scheduler/<scheduler_name>/rooms/<room_name>/status", methods=['PUT'])
def update_status(scheduler_name, room_name):
    print "update status called with data: {0}".format(request.data)
    return '{"success":true}'

@app.route("/scheduler/<scheduler_name>/rooms/<room_name>/playerevent", methods=['PUT'])
def player_event(scheduler_name, room_name):
    print "player event called with data: {0}".format(request.data)
    return '{"success":true}'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
