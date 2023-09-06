import socket
import os.path
import json
import datamapper as mapper
from flask import request
from flask import Flask
import wsgiserver

app = Flask(__name__)
app.config["DEBUG"] = False


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
    return "Record not found", 400


@app.route('/getDetail', methods=['GET'])
def getdetail():
    groupcode_arg = request.args['group_code']
    if groupcode_arg.__contains__(','):
        result_dict = {'code': 200, 'count': 0, 'data': [], 'message': 'successful', 'success': True}
        count_result = 0
        data_detail = []
        for grc in groupcode_arg.split(','):
            if mapper.source_detail_dict.__contains__(grc):
                detail_file = 'resource/' + mapper.source_detail_dict[grc]
                if os.path.exists(detail_file):
                    with open(detail_file, encoding="utf8", mode='r') as file:
                        print('Getting detail resource')
                        jsondata = json.load(file)
                        count_result += jsondata['count']
                        for d in jsondata['data']:
                            data_detail.append(d)

        result_dict['count'] = count_result
        result_dict['data'] = data_detail
        return app.response_class(
            response=json.dumps(result_dict),
            status=200,
            mimetype='application/json')
    else:
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
    return "Record not found", 400


if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)
    server = wsgiserver.WSGIServer(app)
    server.start()
