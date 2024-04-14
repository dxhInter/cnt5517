import json
import socket
import struct
import requests

BASE_URL = "http://10.20.0.74:8888"

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
    json_name = parse_json_data(tweet_split[1])
    json_thing_id = parse_json_data(tweet_split[2])
    json_entity = parse_json_data(tweet_split[3])
    json_space = parse_json_data(tweet_split[4])

    if json_name and json_thing_id and json_entity and json_space:
        service_data = {
            'name': json_name.get('Name'),
            'thing': json_thing_id.get('Thing ID'),
            'entity': json_entity.get('Entity ID'),
            'space': json_space.get('Space ID')
        }
        print('Found service:', service_data)
        response = requests.post(BASE_URL + '/services', json=service_data)
        print(response)

def process_identity_thing_tweet(tweet_split):
    json_thing_id = parse_json_data(tweet_split[1])
    json_space_id = parse_json_data(tweet_split[2])
    json_name = parse_json_data(tweet_split[3])
    json_desc = parse_json_data(tweet_split[7])

    if json_thing_id and json_space_id and json_name and json_desc:
        thing_data = {
            'id': json_thing_id.get('Thing ID'),
            'space': json_space_id.get('Space ID'),
            'name': json_name.get('Name'),
            'desc': json_desc.get('Description'),
            'ip': get_rpi_ip()
        }
        print('Found thing:', thing_data)
        response = requests.post(BASE_URL + '/things', json=thing_data)
        print(response)

def process_relationship_tweet(tweet_split):
    print(tweet_split)
    json_thing_id = parse_json_data(tweet_split[1])
    json_space = parse_json_data(tweet_split[2])
    json_name = parse_json_data(tweet_split[3])
    json_type = parse_json_data(tweet_split[6])
    json_fs = parse_json_data(tweet_split[8])
    tweet_split[9] = tweet_split[9].replace('}', '')
    json_ss = parse_json_data(tweet_split[9])
    print(json_ss)
    # json_thing_id, json_space, json_name, json_type, json_fs, json_ss = (
    #     tweet_split[1], tweet_split[2], tweet_split[3], tweet_split[6], tweet_split[8], tweet_split[9])
    if json_thing_id and json_space and json_name and json_type and json_fs and json_ss:
        relationship_data = {
            'thing': json_thing_id.get('Thing ID'),
            'space': json_space.get('Space ID'),
            'name': json_name.get('Name'),
            'type': json_type.get('Type'),
            'fs': json_fs.get('FS name'),
            'ss': json_ss.get('SS name')
        }
        print('Found relationship:', relationship_data)
        response = requests.post(BASE_URL + '/relationships', json=relationship_data)
        print(response)


multicast_group = '232.2.2.2'
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
    elif 'Relationship' in tweet_type:
        process_relationship_tweet(tweet_split)