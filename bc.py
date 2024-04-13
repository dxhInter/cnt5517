import json
import socket
import struct
import requests

BASE_URL = "http://10.20.0.24:8888"

def get_rpi_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
        print("Could not extract IP address", Exception)
    finally:
        st.close()
    return IP

def parse_json_data(data_str):
    try:
        json_data = json.loads('{' + data_str.strip() + '}')
        return json_data
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return None

def process_service_tweet(tweet_split):
    jsonified_name = parse_json_data(tweet_split[1])
    jsonified_thing_id = parse_json_data(tweet_split[2])
    jsonified_entity = parse_json_data(tweet_split[3])
    jsonified_space = parse_json_data(tweet_split[4])

    if jsonified_name and jsonified_thing_id and jsonified_entity and jsonified_space:
        service_data = {
            'name': jsonified_name.get('Name'),
            'thing': jsonified_thing_id.get('Thing ID'),
            'entity': jsonified_entity.get('Entity ID'),
            'space': jsonified_space.get('Space ID')
        }
        print('Found service:', service_data)
        response = requests.post(BASE_URL + '/services', json=service_data)

def process_identity_thing_tweet(tweet_split):
    jsonified_thing_id = parse_json_data(tweet_split[1])
    jsonified_space_id = parse_json_data(tweet_split[2])
    jsonified_name = parse_json_data(tweet_split[3])
    jsonified_desc = parse_json_data(tweet_split[7])

    if jsonified_thing_id and jsonified_space_id and jsonified_name and jsonified_desc:
        thing_data = {
            'id': jsonified_thing_id.get('Thing ID'),
            'space': jsonified_space_id.get('Space ID'),
            'name': jsonified_name.get('Name'),
            'desc': jsonified_desc.get('Description'),
            'ip': get_rpi_ip()
        }
        print('Found thing:', thing_data)
        response = requests.post(BASE_URL + '/things', json=thing_data)

multicast_group = '224.1.1.1'
server_address = ('', 1235)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    data, _ = sock.recvfrom(1024)
    decoded = data.decode('utf-8')
    tweet_split = decoded.split(',')
    tweet_type = tweet_split[0].strip()

    if 'Service' in tweet_type:
        process_service_tweet(tweet_split)
    elif 'Identity_Thing' in tweet_type:
        process_identity_thing_tweet(tweet_split)