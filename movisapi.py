import json
import boto3
import botocore
import os
import datamapper as mapper
# import requests
BUCKET_NAME = os.environ['BUCKET_NAME']
s3 = boto3.resource('s3')

def get_detail_handler(event, context):
    params = event['queryStringParameters']
    if params is None or 'group_code' not in params:
        return get_default_response(400)
    groupcode_arg = params['group_code']
    if groupcode_arg.__contains__(','):
        result_dict = {'code': 200, 'count': 0, 'data': [], 'message': 'successful', 'success': True}
        count_result = 0
        data_detail = []
        for grc in groupcode_arg.split(','):
            if mapper.source_detail_dict.__contains__(grc):
                detail_file = 'resource/' + mapper.source_detail_dict[grc]
                print('Getting detail resource')
                json_data = get_file(BUCKET_NAME, detail_file)
                if json_data is None:
                    return get_default_response(404)
                if 'data' in json_data and 'count' in json_data:
                    count_result += json_data['count']
                    for d in json_data['data']:
                            data_detail.append(d)
        result_dict['count'] = count_result
        result_dict['data'] = data_detail
        return {
            "statusCode": 200,
            "body": json.dump(result_dict)
        }
    else:
        if mapper.source_detail_dict.__contains__(groupcode_arg):
            detail_file = 'resource/' + mapper.source_detail_dict[groupcode_arg]
            print('Getting detail resource')
            json_data = get_file(BUCKET_NAME, detail_file)
            if json_data is None:
                return get_default_response(404)
            return {
                "statusCode": 200,
                "body": json.dumps(json_data)
            }

    return get_default_response(404)

def get_cate_handler(event, context):
    params = event['queryStringParameters']
    if params is None or 'name' not in params:
        return get_default_response(400)
    name_arg = params['name']
    if mapper.source_category_dict.__contains__(name_arg):
        cate_file = 'resource/' + mapper.source_category_dict[name_arg]
        print('Getting cate resource')
        json_data = get_file(BUCKET_NAME, cate_file)
        if json_data is None:
            return get_default_response(404)
        return {
            "statusCode": 200,
            "body": json.dumps(json_data)
        }

def get_default_response(code):
    match code:
        case 400:
            return {
                "statusCode": code,
                "body": json.dumps({
                    "message": "Bad request"
                })
            }
        case 404:
            return {
                "statusCode": code,
                "body": json.dumps({
                    "message": "Record not found"
                })
            }

def get_file(bucket, key):
    print('Get file from s3 bucket:', bucket, "| Key:", key)
    try:
        content_object = s3.Object(bucket, key).get()['Body']
    except botocore.exceptions.ClientError as e:
        return None
    return json.load(content_object)