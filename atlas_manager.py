import socket
import json
import threading

from flask import current_app


def execute_service_order(service, result):
    if result is not None:
        print(result[0])
        result = result[1]
        if result['Status'] == 'Successful':
            input = "({},)".format(result['Service Result'])
        else:
            input = "(1,)"
    else:
        input = "(1,)"
    print(service)
    current_app.logger.error(
        f"Service: {service['name']}, Input: {input}, Thing: {service['thing']['id']}, Entity: {service['entity']}, Space: {service['space']}")
    message = json.dumps({
        "Tweet Type": "Service call",
        "Service Name": service['name'],
        "Thing ID": service['thing']['id'],
        "Entity ID": service['entity'],
        "Space ID": service['space'],
        "Service Inputs": input
    })

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((service['thing']['ip'], 6668))
    s.connect(("10.20.0.58", 6668))
    s.sendall(bytes(message, 'utf-8'))
    data = s.recv(1024)
    s.close()
    return True, json.loads(data.decode())


# 如果result大于设定的阈值，发送消息给thing
def execute_service_condition(service, result, threshold):
    if result > threshold:
        message = json.dumps({
            "Tweet Type": "Service call",
            "Service Name": service['name'],
            "Thing ID": service['thing']['id'],
            "Entity ID": service['entity'],
            "Space ID": service['space'],
            "Service Inputs": "(1,)"
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
    current_app.logger.debug(
        f"Service: {service_name1['name']}, Thing: {service_name1['thing']['id']}, Entity: {service_name1['entity']}, Space: {service_name1['space']}")
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
