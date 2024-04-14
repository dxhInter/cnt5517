import json


def load_data():
    try:
        with open('config.iot', 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise Exception(f"Error reading config.iot: {e}")
    except FileNotFoundError:
        raise Exception("config.iot file not found.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def save_data(data):
    try:
        with open('config.iot', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception(f"Error saving to config.iot: {e}")


def get_all_things():
    data = load_data()
    return data.get('things', [])


def create_thing(**kwargs):
    id = kwargs.get('id')
    name = kwargs.get('name')
    desc = kwargs.get('desc')
    icon = kwargs.get('icon')
    space = kwargs.get('space')
    ip = kwargs.get('ip')

    try:
        new = True
        data = load_data()
        generated_thing = {
            "id": id,
            "name": name,
            "desc": desc,
            "icon": icon,
            "space": space,
            "ip": ip
        }
        updated_things = []
        for thing in data['things']:
            if thing['id'] == id:
                updated_things.append(generated_thing)
                new = False
            else:
                updated_things.append(thing)

        if new:
            updated_things.append(generated_thing)

        data['things'] = updated_things

        f = open('config.iot', 'w')
        json.dump(data, f)
        f.close()
        return True
    except:
        return False

def get_all_services():
    data = load_data()
    return data.get('services', [])

# 获取特定thing的服务
def get_services_of_thing(thing_id):
    services = get_all_services()
    return [service for service in services if service.get('thing') == thing_id]

# ...其他 get 方法...

def create_service(**kwargs):
    required_fields = ['thing', 'name', 'entity', 'space']
    if not all(key in kwargs for key in required_fields):
        return False

    new_service = {field: kwargs[field] for field in required_fields}
    if 'icon' in kwargs:
        new_service['icon'] = kwargs['icon']
    else:
        new_service['icon'] = ''

    try:
        data = load_data()
        if any(service['name'] == new_service['name'] for service in data.get('services', [])):
            data['services'] = [service if service['name'] != new_service['name'] else new_service for service in data.get('services', [])]
        else:
            data.setdefault('services', []).append(new_service)

        save_data(data)
        return True
    except Exception as e:
        print(f"Error creating service: {e}")
        return False

# {'thing': 'g6', 'space': 'g6Space', 'name': 'REDANDGREEN', 'type': 'control', 'fs': 'TurnOnRedLED', 'ss': 'TurnOnGreenLED'}
def create_relationship(**kwargs):
    required_fields = ['thing', 'space', 'name', 'type', 'fs', 'ss']
    if not all(key in kwargs for key in required_fields):
        return False

    new_relationship = {field: kwargs[field] for field in required_fields}
    if 'icon' in kwargs:
        new_relationship['icon'] = kwargs['icon']
    else:
        new_relationship['icon'] = ''

    try:
        data = load_data()
        if any(relationship['name'] == new_relationship['name'] for relationship in data.get('relationships', [])):
            data['relationships'] = [relationship if relationship['name'] != new_relationship['name'] else new_relationship for relationship in data.get('relationships', [])]
        else:
            data.setdefault('relationships', []).append(new_relationship)

        save_data(data)
        return True
    except Exception as e:
        print(f"Error creating relationship: {e}")
        return False