import socket
import json
import threading
import dao.mapping as mapping
from flask import current_app
import message_helper

ip = "10.20.0.58"
PORT = 6668


def json_message(service_name: str, thing_id: str, entity_id: str, space_id: str, inputs=()):
    message = {
        "Tweet Type": "Service call",
        "Service Name": '{}'.format(service_name),
        "Thing ID": '{}'.format(thing_id),
        "Entity ID": '{}'.format(entity_id),
        "Space ID": '{}'.format(space_id),
    }

    if inputs is not None:
        message["Service Inputs"] = '{}'.format(inputs).replace(', ', ',')

    return json.dumps(message)


def send_service_call(service_name, thing, entity, space, ip, inputs=None):
    global PORT
    message = json_message(service_name, thing, entity, space, inputs)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as st:
            st.connect((ip, PORT))
            st.sendall(bytes(message, 'utf-8'))
            data = st.recv(1024)
        # Validate and decode the JSON response
        if data:
            print("Received data:", data)  # Debug line to see what data was received
            return True, json.loads(data.decode())
        else:
            print("No data received")  # Debug line for no data case
            return False, {"error": "No data received"}
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return False, {"error": "JSON decode error"}
    except Exception as e:
        print("Unexpected error:", e)
        return False, {"error": "Unexpected error"}


def execute_service_order(service_name, result):
    print(1)
    if result is not None:
        print(result[0])
        result = result[1]
        if result['Status'] == 'Successful':
            input = result['Service Result']
        else:
            input = ()
    else:
        input = ()
    print(f"order in {service_name}")
    data = mapping.load_data()
    services = data.get('services', [])
    for i in range(len(services)):
        if services[i]['name'] == service_name:
            break
    service = services[i]
    res = send_service_call(service['name'], service['thing'], service['entity'], service['space'], ip, input)
    print(f"res1 is {res}")
    return res


# 如果result大于设定的阈值，发送消息给thing
def execute_service_condition(service_name, result, threshold):
    print("Flag2")
    if result is not None:
        result = result[1]
        if result['Status'] == 'Successful':
            input = result['Service Result'] + ',' + str(threshold)
        else:
            input = ()
    else:
        input = ()
    print(f"condition in {service_name}")
    data = mapping.load_data()
    services = data.get('services', [])
    for i in range(len(services)):
        if services[i]['name'] == service_name:
            break
    service = services[i]
    res = send_service_call(service['name'], service['thing'], service['entity'], service['space'], ip, input)
    print(f"res1 is {res}")
    return res


def order(app):
    # print(f"Ordering services...{app}")
    service_name1 = app["service1"]
    # print(service_name1)
    print(service_name1)
    res = execute_service_order(service_name1, None)
    print(f"res is{res}")
    service_name2 = app['service2']
    res2 = execute_service_order(service_name2, res)
    if res2[1]['Status'] == 'Successful':
        return True, res2[1]['Service Result']


threadISRunning = False


# TODO: 新建一个线程，执行service2，未完成，设置线程睡眠时间
def new_thread(service_name2, res, threshold):
    if threadISRunning:
        return
    thread = threading.Thread(target=execute_service_condition(), args=(service_name2, res, threshold))
    thread.start()


def condition(app, threshold):
    print("Flag1")
    service_name1 = app['service1']
    res = execute_service_order(service_name1, None)
    service_name2 = app['service2']
    res2 = execute_service_condition(service_name2, res, threshold)
    if res2[1]['Status'] == 'Successful':
        return True, res2[1]['Service Result']
    # 新建一个线程，执行service2
    # new_thread(service_name2, res, threshold)
