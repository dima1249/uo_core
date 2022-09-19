import ipaddress
import json
import math
import os
# for regular expressions
import re
from datetime import date, datetime
from json import JSONEncoder
from uuid import uuid4

import requests
from django.utils.deconstruct import deconstructible
from rest_framework_jwt.utils import jwt_payload_handler
from user_agents import parse

# email shalgah regex (config file-s unshdag bolgoh)
# for validating an Email

REGEX_EMAIL = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
VALID_MOBICOM_REGEX = '^(99|95|94|85)(\\d{6})$'
VALID_SKYTEL_REGEX = '^(91|96|90)(\d{6})$'
VALID_GMOBILE_REGEX = '^(98|97|93)(\d{6})$'
VALID_UNITEL_REGEX = '^(89|88|86|80)(\d{6})$'
VALID_MGL_REGEX = '^(976)(\d{8})'


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, o):
        if isinstance(o, (date)):
            return o.strftime('%Y-%m-%d')

        if isinstance(o, (datetime)):
            return o.strftime("%Y-%m-%d %H:%M:%S")


def convert_json_to_erase_underscore(_json):
    if isinstance(_json, list):
        _tmp = []
        for item in _json:
            _tmp.append(convert_json_to_erase_underscore(item))

        return _tmp

    else:
        _new = dict()
        for key, value in _json.items():
            new_key = key.replace("_", "")
            if isinstance(value, list):
                _new[new_key] = convert_json_to_erase_underscore(
                    value)  # Adding Modified key
            else:
                _new[new_key] = value  # Adding Modified key
        return _new


def convert_newline(_text):
    return _text.replace('\n', '<br>')


def encode_email_sabre(email):
    return email.replace("@", "//").replace("-", "./").replace("_", "..")


# check IP address is private/public


def check_ip_type(device_ip):
    try:
        addr = ipaddress.IPv4Address(device_ip)
    except ValueError:
        raise
    if addr.is_private:
        return True
    else:
        return False


def convert_json_to_upper_case(_json):
    if isinstance(_json, list):
        _tmp = []
        for item in _json:
            _tmp.append(convert_json_to_erase_underscore(item))

        return _tmp

    else:
        for key, value in _json.iteritems():
            new_key = key.replace("_", "")
            del _json[key]  # Deleting Previous Key
            # float, int, str, list, dict, tuple
            if isinstance(value, list):
                _json[new_key] = convert_json_to_erase_underscore(
                    value)  # Adding Modified key
            else:
                _json[new_key] = value  # Adding Modified key

        return _json


def element_by_id(array, id):
    res = [k for k in array if k['id'] == id]
    if not res:
        return None
    return res[0]


def element_by_id_lambda(array, id):
    res = filter(lambda x: 'id' in x and x['id'] == id, array)
    if not res:
        return None
    return res[0]


def element_by_key(array, key, key_value):
    res = filter(lambda x: key in x and x[key] == key_value, array)
    if not res:
        return None
    for x in res:
        return x


def element_by_key_lambda(array, key, key_value):
    return [k for k in array if k[key] == key_value]


def calculate_age(born, date_str=""):
    today = datetime.today()
    if date_str is not None and len(date_str) > 0:
        today = datetime.strptime(date_str, format='%Y-%m-%d')
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def calculate_age_days(born, dep_date=None):
    today = datetime.now()
    if dep_date is not None:
        today = dep_date
    elapsedTime = today - born
    return elapsedTime.days


def calculate_month(born):
    today = date.today()
    return (today.year - born.year) * 12 + (today.month - born.month)


def tapa_print(*argv):
    if os.environ.get('DEBUG') == 'TRUE':

        for arg in argv:
            print(arg)


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        # get filename
        if instance.pk:
            filename = '{}.{}'.format(uuid4().hex, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
            # return the whole path to the file
        return os.path.join(self.path, filename)


def send_sms(dial_code, number, content):
    try:
        headers = {'Content-Type': 'application/json'}

        LOGIN_URL = os.environ.get('SMS_LOCAL_URL') + 'user/login'
        # URL = 'http://sms.api.tapatrip.com:8081/message/sendByApi'
        URL = os.environ.get('SMS_LOCAL_URL') + 'message/send'

        _login_data = {"username": os.environ.get('SMS_LOCAL_USER'), "password": os.environ.get('SMS_LOCAL_PASSWORD')}

        _response = requests.post(LOGIN_URL, headers=headers, json=_login_data)

        if _response.status_code == requests.codes.ok:

            token = _response.json().get("token")
            headers["authorization"] = token
            _post_data = {"dialCode": dial_code,
                          "number": number, "content": str(content)}
            _response = requests.post(URL, headers=headers, json=_post_data)

            if _response.status_code == requests.codes.ok:
                _req_data = _response.json()
                # tapa_print('_req_data', _req_data)
                return _response.json().get("content")

            else:
                return None
        else:
            return None
    except Exception:
        pass


def check_is_email(email):
    if re.search(REGEX_EMAIL, email):
        return True
    else:
        print("invalid email")
        return False


def check_is_phone_number(phone):
    if re.search(VALID_MGL_REGEX, phone):
        return True
    else:
        print("invalid phone number")
        return False


def device_info_added_jwt_payload_handler(user, device):
    payload = jwt_payload_handler(user)
    payload['device_ip'] = device.ip
    payload['device_name'] = device.name
    payload['device_os'] = device.os
    return payload


def get_country_info(request=None, device_ip=None):
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            device_ip = x_forwarded_for.split(',')[0]
        else:
            device_ip = request.META.get('REMOTE_ADDR')
    # request_url = 'https://geolocation-db.com/jsonp/' + device_ip
    # if is private IP then set device_ip to default(our server ip)
    if check_ip_type(device_ip):
        device_ip = '103.14.36.82'
    # print(device_ip)
    request_url = 'http://www.geoplugin.net/json.gp?ip=' + device_ip
    response = requests.get(request_url)

    result = response.content.decode()
    # result = result.split("(")[1].strip(")")
    result = json.loads(result)
    # print(result)

    return result


def int_format(value, decimal_points=3, seperator=u','):
    value = str(value)
    if len(value) <= decimal_points:
        return value
    # say here we have value = '12345' and the default params above
    parts = []
    while value:
        parts.append(value[-decimal_points:])
        value = value[:-decimal_points]
    # now we should have parts = ['345', '12']
    parts.reverse()
    # and the return value should be u'12.345'
    return seperator.join(parts)


def is_mobile_rq(request):
    user_agent = parse(request.headers['User-Agent'])
    return user_agent.is_mobile or user_agent.is_tablet


def xmlArrayBug(data):
    if type(data) is list:
        return data
    else:
        return [data]


def roundup(x):
    return int(math.ceil(x / 1000.0)) * 1000
