import socket
import json
import threading
import dao.mapping as mapping
from flask import current_app

ip = "10.20.0.58"
PORT = 6668


def execute_service_order(service_name, result):
    if result is not None:
        print(result[0])
        result = result[1]
        if result['Status'] == 'Successful':
            # input = "({},)".format(result['Service Result'])
            print(result['Service Result'])
    #     else:
    #         input = "(1,)"
    # else:
    #     input = "(1,)"
    print(f"order in {service_name}")
    data = mapping.load_data()
    services = data.get('services', [])
    for i in range(len(services)):
        if services[i]['name'] == service_name:
            break
    service = services[i]
    print(service)
    print(service['name'])
    print(service["thing"])
    print(service["entity"])
    print(service["space"])
    message = json.dumps({
        "Tweet Type": "Service call",
        "Service Name": '{}'.format(service['name']),
        "Thing ID": "g6",
        "Entity ID": '{}'.format(service['entity']),
        "Space ID": "g6Space",
        "Service Inputs": None
    })

    print(f"message is {message}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as st:
            global ip, PORT
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


# 如果result大于设定的阈值，发送消息给thing
def execute_service_condition(service, result, threshold):
    if result > threshold:
        message = json.dumps({
            "Tweet Type": "Service call",
            "Service Name": service['name'],
            "Thing ID": service['thing']['id'],
            "Entity ID": service['entity'],
            "Space ID": service['space'],
        })

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.20.0.58", 6668))
        s.sendall(bytes(message, 'utf-8'))
        data = s.recv(1024)
        s.close()
        return True, json.loads(data.decode())
    else:
        return False, None


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
    service_name1 = app['service1']
    res = execute_service_order(service_name1, None)
    service_name2 = app['service2']
    # 新建一个线程，执行service2
    new_thread(service_name2, res, threshold)
