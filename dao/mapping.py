import json

import atlas_manager
from flask import current_app


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

def get_services_of_thing(thing_id):
    services = get_all_services()
    return [service for service in services if service.get('thing') == thing_id]


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


def create_app(**kwargs):
    required_fields = ['name', 'id', 'relationships', 'service1', 'service2', 'enabled']
    if not all(key in kwargs for key in required_fields):
        return False

    new_app = {field: kwargs[field] for field in required_fields}
    if 'icon' in kwargs:
        new_app['icon'] = kwargs['icon']
    else:
        new_app['icon'] = ''

    try:
        data = load_data()
        if any(app['name'] == new_app['name'] for app in data.get('apps', [])):
            data['apps'] = [app if app['name'] != new_app['name'] else new_app for app in data.get('apps', [])]
        else:
            data.setdefault('apps', []).append(new_app)

        save_data(data)
        return True
    except Exception as e:
        print(f"Error creating app: {e}")
        return False


def get_app(app_id):
    data = load_data()
    for app in data.get('apps', []):
        if app['id'] == app_id:
            return app
    return None

def run_app(**kwargs):
    required_fields = ['app_id', 'threshold', 'relationship']
    if not all(key in kwargs for key in required_fields):
        return False
    try:
        print(1)
        app = get_app(kwargs['app_id'])
        current_app.logger.error(f"App: {app['name']}, ID: {app['id']}")
        if app is None:
            return False

        relationship = kwargs['relationship']
        current_app.logger.error(f"Relationship: {relationship}")
        if relationship == 'order':
            return atlas_manager.order(app)
        elif relationship == 'condition':
            return atlas_manager.execute_service_condition(app, None, kwargs['threshold'])

    except Exception as e:
        print(f"Error running app: {e}")
        return False

def put_threshold(data):
    return None