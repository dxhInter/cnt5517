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


def get_all_services():
    try:
        services = dao.get_all_services()
        return response(200, services)
    except Exception as e:
        return response(500, message=str(e))

# 获取指定thing的服务
def get_services(thing_id):
    try:
        services = dao.get_services_of_thing(thing_id)
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
    try:
        result = dao.run_app(data)
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