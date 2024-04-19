import dao.mapping as dao


def response(code, result=None, message=''):
    return {'code': code, 'result': result, 'message': message}

def get_things():
    try:
        things = dao.get_all_things()
        return response(200, things)
    except Exception as e:
        return response(500, message=str(e))

# ... other get methods...

def create_thing(data):
    try:
        result = dao.create_thing(**data)
        if result:
            return response(201, message='Thing created successfully.')
        else:
            return response(400, message='Failed to create thing. Required fields are missing.')
    except Exception as e:
        return response(500, message=str(e))


def query_all_services():
    try:
        services = dao.query_all_services()
        return response(200, services)
    except Exception as e:
        return response(500, message=str(e))

# get services with thing_id
def query_service_with_thing(thing_id):
    try:
        services = dao.query_service_with_thing(thing_id)
        return response(200, services)
    except Exception as e:
        return response(500, message=str(e))

# ...其他 get 方法...

def create_service(data):
    try:
        result = dao.create_service(**data)
        if result:
            return response(201, message='Service created successfully.')
        else:
            return response(400, message='Failed to create service. Required fields are missing.')
    except Exception as e:
        return response(500, message=str(e))


def create_relationship(data):
    try:
        result = dao.create_relationship(**data)
        if result:
            return response(201, message='Relationship created successfully.')
        else:
            return response(400, message='Failed to create relationship. Required fields are missing.')
    except Exception as e:
        return response(500, message=str(e))


def create_app(data):
    try:
        result = dao.create_app(**data)
        if result:
            return response(201, message='App created successfully.')
        else:
            return response(400, message='Failed to create app. Required fields are missing.')
    except Exception as e:
        return response(500, message=str(e))

# data包含app_id, threshold
def run_app(data):
    print(f"run app is {data}")
    try:
        result = dao.run_app(**data)
        if result:
            return response(200, result)
        else:
            return response(400, message='Failed to run app.')
    except Exception as e:
        return response(500, message=str(e))


def get_app(app_id):
    try:
        apps = dao.get_app(app_id)
        return response(200, apps)
    except Exception as e:
        return response(500, message=str(e))


def put_threshold(data):
    try:
        result = dao.put_threshold(data)
        if result:
            return response(200, message='Threshold updated successfully.')
        else:
            return response(400, message='Failed to update threshold.')
    except Exception as e:
        return response(500, message=str(e))


def query_all_relationships():
    try:
        relationships = dao.query_all_relationships()
        return response(200, relationships)
    except Exception as e:
        return response(500, message=str(e))


def query_all_apps():
    try:
        apps = dao.query_all_apps()
        return response(200, apps)
    except Exception as e:
        return response(500, message=str(e))


def start_or_stop_app(data):
    try:
        result = dao.start_or_stop_app(**data)
        if result:
            return response(200, message='App started/stopped successfully.')
        else:
            return response(400, message='Failed to start/stop app.')
    except Exception as e:
        return response(500, message=str(e))


def delete_app(app_id):
    try:
        result = dao.delete_app(app_id)
        if result:
            return response(200, message='App deleted successfully.')
        else:
            return response(400, message='Failed to delete app.')
    except Exception as e:
        return response(500, message=str(e))


def stop_thread():
    try:
        result = dao.stop_thread()
        if result:
            return response(200, message='Thread stopped successfully.')
        else:
            return response(400, message='Failed to stop thread.')
    except Exception as e:
        return response(500, message=str(e))


def start_thread(data):
    try:
        result = dao.start_thread(**data)
        if result:
            return response(200, message='Thread started successfully.')
        else:
            return response(400, message='Failed to start thread.')
    except Exception as e:
        return response(500, message=str(e))


def update_app(data, app_id):
    try:
        result = dao.update_app(app_id, **data)
        if result:
            return response(200, message='App updated successfully.')
        else:
            return response(400, message='Failed to update app.')
    except Exception as e:
        return response(500, message=str(e))