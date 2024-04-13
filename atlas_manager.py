import socket
import json

# 维护一个hashmap，key是thing，value是thing的ip
# g6 对应 10.20.0.58，g62 对应 10.20.0.22
things = {
    'g6': '10.20.0.58',
    'g62': '10.20.0.22'
}



def execute_service(service, result):
    if result is not None:
        print(result[0])
        result = result[1]
        if result['Status'] == 'Successful':
            input = "({},)".format(result['Service Result'])
        else:
            input = "(1,)"
    else:
        input = "(1,)"

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
    s.connect((things[service['thing']['id']], 6668))
    s.sendall(bytes(message, 'utf-8'))
    data = s.recv(1024)
    s.close()
    return True, json.loads(data.decode())