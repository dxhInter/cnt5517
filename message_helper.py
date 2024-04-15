import json
import socket


# The port where Atlas IoT is running
PORT = 6668


# This function provides a json message as per the provided service name,
def json_message(service_name: str, entity_id: str, inputs=()):
    message = {
        "Tweet Type": "Service call",
        "Service Name": '{}'.format(service_name),
        "Thing ID": "g6",
        "Entity ID": '{}'.format(entity_id),
        "Space ID": "g6Space",
    }

    if inputs is not None:
        message["Service Inputs"] = '{}'.format(inputs).replace(', ', ',')

    return json.dumps(message)


# This function sends the service call json to the Atlas IoT.
def send_service_call(service_name, id, ip, inputs=None):
    global PORT
    message = json_message(service_name, id, inputs)
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