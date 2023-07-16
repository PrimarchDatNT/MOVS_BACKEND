import socket
import requests
import os.path
import datamapper as mapper
from flask import request
from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = False

ALT_CATE_URL = 'https://api2.videoshow.mobi/getCate?name=$'
ALT_DETAIL_URL = 'https://api2.videoshow.mobi/getDetail?group_code=$'


@app.route('/')
def home():
    return "---MOVIS---"


@app.route('/getCate', methods=['GET'])
def getcate():
    name_arg = request.args['name']
    if mapper.source_category_dict.__contains__(name_arg):
        cate_file = 'resource/' + mapper.source_category_dict[name_arg]
        if os.path.exists(cate_file):
            with open(cate_file, encoding="utf8", mode='r') as file:
                print('Getting cate resource')
                return app.response_class(
                    response=file.read(),
                    status=200,
                    mimetype='application/json')
    print('No resouce request alt api')
    response = requests.get(ALT_CATE_URL.replace('$', name_arg))
    return app.response_class(
        response=response.text,
        status=200,
        mimetype='application/json')


@app.route('/getDetail', methods=['GET'])
def getdetail():
    groupcode_arg = request.args['group_code']
    if mapper.source_detail_dict.__contains__(groupcode_arg):
        detail_file = 'resource/' + mapper.source_detail_dict[groupcode_arg]
        if os.path.exists(detail_file):
            with open(detail_file, encoding="utf8", mode='r') as file:
                print('Getting detail resource')
                return app.response_class(
                    response=file.read(),
                    status=200,
                    mimetype='application/json')
    print('No resouce request alt api')
    response = requests.get(ALT_DETAIL_URL.replace('$', groupcode_arg))
    return app.response_class(
        response=response.text,
        status=200,
        mimetype='application/json')


if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)
    app.run()
