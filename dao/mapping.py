import json
import time

from flask import current_app

from flask import Flask

app = Flask(__name__)

import dao.service_impl as service_impl
from util.Singleton import Singleton
singleton_thread_manager = Singleton()
ipg6 = "10.20.0.58"
ipe62 = "10.20.0.22"
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
    if id == 'g6':
        ip = ipg6
    elif id == 'e62':
        ip = ipe62
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


def query_all_services():
    data = load_data()
    return data.get('services', [])


def query_service_with_thing(thing_id):
    services = query_all_services()
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
            data['services'] = [service if service['name'] != new_service['name'] else new_service for service in
                                data.get('services', [])]
        else:
            data.setdefault('services', []).append(new_service)

        save_data(data)
        return True
    except Exception as e:
        print(f"Error creating service: {e}")
        return False


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
            data['relationships'] = [
                relationship if relationship['name'] != new_relationship['name'] else new_relationship for relationship
                in data.get('relationships', [])]
        else:
            data.setdefault('relationships', []).append(new_relationship)

        save_data(data)
        return True
    except Exception as e:
        print(f"Error creating relationship: {e}")
        return False


def create_app(**kwargs):
    # required_fields = ['name', 'id', 'relationships', 'service1', 'service2', 'enabled']
    required_fields = ['name', 'id', 'relationship', 'service1', 'service2']
    if not all(key in kwargs for key in required_fields):
        return False

    new_app = {field: kwargs[field] for field in required_fields}
    if 'enabled' in kwargs:
        new_app['enabled'] = kwargs['enabled']
    else:
        new_app['enabled'] = "active"
    if 'status' in kwargs:
        new_app['status'] = kwargs['status']
    else:
        new_app['status'] = "incomplete"

    if 'icon' in kwargs:
        new_app['icon'] = kwargs['icon']
    else:
        new_app['icon'] = ''
    new_app['id'] = str(kwargs['id'])
    if 'threshold' in kwargs:
        new_app['threshold'] = kwargs['threshold']
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
        app = get_app(kwargs['app_id'])
        if app is None:
            return False
        # to check if app is enabled
        app_enabled = app.get('enabled')
        if app_enabled == "stopped":
            current_app.logger.error(f"App is disabled: {app}")
            return False

        relationship = app.get('relationship')
        current_app.logger.error(f"Relationship: {relationship}")
        if relationship == 'order':
            running_app(kwargs['app_id'])
            # if app run successfully, modify the app status to completed
            res = service_impl.order(app)
            if res[0]:
                completed_app(kwargs['app_id'])
            return res

        elif relationship == 'condition':
            running_app(kwargs['app_id'])
            res = service_impl.condition(app, kwargs['threshold'])
            if res[0]:
                completed_app(kwargs['app_id'])
            return res
    except Exception as e:
        print(f"Error running app: {e}")
        return False


def thread_function(**kwargs):
    with app.app_context():
        while not singleton_thread_manager.should_stop():
            result = run_app(**kwargs)  # Assuming run_app is defined elsewhere and returns a boolean
            if not result:
                break  # Exit the loop if the task fails or completes with a specific condition
            time.sleep(1)

def start_thread(**kwargs):
    thread = singleton_thread_manager.start_thread(target=thread_function, **kwargs)
    return thread


def stop_thread():
    return singleton_thread_manager.stop_thread()

def completed_app(app_id):
    try:
        data = load_data()
        for app in data.get('apps', []):
            if app['id'] == app_id:
                app['status'] = 'completed'
                break

        save_data(data)
        return True
    except Exception as e:
        print(f"Error starting/stopping app: {e}")
        return False

def running_app(app_id):
    try:
        data = load_data()
        for app in data.get('apps', []):
            if app['id'] == app_id:
                app['status'] = 'running'
                break

        save_data(data)
        return True
    except Exception as e:
        print(f"Error starting/stopping app: {e}")
        return False

def put_threshold(data):
    return None


def query_all_relationships():
    data = load_data()
    return data.get('relationships', [])


def query_all_apps():
    data = load_data()
    return data.get('apps', [])


def start_or_stop_app(**kwargs):
    required_fields = ['app_id', 'enabled']
    if not all(key in kwargs for key in required_fields):
        return False

    try:
        app_id = kwargs['app_id']
        enabled = kwargs['enabled']
        data = load_data()
        for app in data.get('apps', []):
            if app['id'] == app_id:
                app['enabled'] = enabled
                break

        save_data(data)
        return True
    except Exception as e:
        print(f"Error starting/stopping app: {e}")
        return False


def delete_app(app_id):
    try:
        data = load_data()
        data['apps'] = [app for app in data.get('apps', []) if app['id'] != app_id]
        save_data(data)
        return True
    except Exception as e:
        print(f"Error deleting app: {e}")
        return False


def update_app(app_id, **kwargs):
    # required_fields = ['app_id']
    # if not all(key in kwargs for key in required_fields):
    #     return False
    if app_id is None:
        return False

    try:
        # app_id = kwargs['app_id']
        data = load_data()
        for app in data.get('apps', []):
            if app['id'] == app_id:
                for key in kwargs:
                    if key != 'app_id':
                        app[key] = kwargs[key]
                break
        save_data(data)
        return True
    except Exception as e:
        print(f"Error updating app: {e}")
        return False