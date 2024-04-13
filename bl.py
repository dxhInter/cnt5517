import da
from atlas_manager import execute_service


def get_things():
    return {
        'code': 200,
        'result': da.get_all_things()
    }


def get_all_services():
    return {
        'code': 200,
        'result': da.get_all_services()
    }


def get_services(thing_id):
    return {
        'code': 200,
        'result': da.get_services_of_thing(thing_id)
    }


def get_relationships():
    return {
        'code': 200,
        'result': da.get_all_relationships()
    }


def create_relationship(data):
    if 'name' not in data or 'desc' not in data or 'service1' not in data or 'service2' not in data:
        return {
            'code': 400,
            'msg': 'Name, Description, or Services not provided'
        }

    name = data['name']
    desc = data['desc']
    service_1 = data['service1']
    service_2 = data['service2']
    if 'icon' in data:
        icon = data['icon']
    else:
        icon = ''

    result = da.create_relationship(
        name=name, icon=icon, desc=desc, service_1=service_1, service_2=service_2)
    if result:
        return {
            'code': 201,
            'msg': 'Relationship created'
        }
    else:
        return {
            'code': 500,
            'msg': 'Server error. It is not you, it is us.'
        }


def create_thing(data):
    if 'id' not in data or 'name' not in data or 'desc' not in data or 'space' not in data or 'ip' not in data:
        return {
            'code': 400,
            'msg': 'ID, Name, Description, IP address or Space not provided'
        }
    print(data)
    id = data['id']
    name = data['name']
    desc = data['desc']
    space = data['space']
    ip = data['ip']
    if 'icon' in data:
        icon = data['icon']
    else:
        icon = ''

    result = da.create_thing(
        id=id, name=name, icon=icon, desc=desc, space=space, ip=ip)
    if result:
        return {
            'code': 201,
            'msg': 'Thing created'
        }
    else:
        return {
            'code': 500,
            'msg': 'Server error. It is not you, it is us.'
        }


def create_service(data):
    if 'thing' not in data or 'name' not in data or 'entity' not in data or 'space' not in data:
        return {
            'code': 400,
            'msg': 'Thing, Name, Entity or Space not provided'
        }
    print(data)
    thing = data['thing']
    name = data['name']
    entity = data['entity']
    space = data['space']

    if 'icon' in data:
        icon = data['icon']
    else:
        icon = ''

    result = da.create_service(
        thing=thing, name=name, icon=icon, entity=entity, space=space)
    if result:
        return {
            'code': 201,
            'msg': 'Service {} created'.format(name)
        }
    else:
        return {
            'code': 501,
            'msg': 'Server error. It is not you, it is us.'
        }


def create_recipe(data):
    if 'name' not in data or 'relationships' not in data or 'relationships' not in data:
        return {
            'code': 400,
            'msg': 'Name or relationships not provided'
        }

    name = data['name']
    id = name
    relationships = data['relationships']

    if 'icon' in data:
        icon = data['icon']
    else:
        icon = ''

    result = da.create_recipe(
        id=id, name=name, icon=icon, relationships=relationships)
    if result:
        return {
            'code': 201,
            'msg': 'Recipe {} created'.format(name)
        }
    else:
        return {
            'code': 500,
            'msg': 'Server error. It is not you, it is us.'
        }


def get_recipes():
    return {
        'code': 200,
        'result': da.get_recipes()
    }


def run_recipe(recipe_id):
    recipe = da.get_recipe(recipe_id)

    recipe_results = {
        'recipe': recipe,
        'result': []
    }

    for relationship in recipe['relationships']:
        relationship_results = {
            'relationship': relationship,
            'result': []
        }
        result_1 = execute_service(relationship['service1'], None)
        result_2 = execute_service(relationship['service2'], result_1)
        relationship_results['result'].append({
            'service': relationship['service1'],
            'result': result_1
        })
        relationship_results['result'].append({
            'service': relationship['service2'],
            'result': result_2
        })

        recipe_results['result'].append(relationship_results)

    return {
        'code': 200,
        'msg': 'Actions performed',
        'result': recipe_results
    }


def enable_disable_recipe(recipe_id):
    result = da.enable_disable_recipe(recipe_id)
    if result:
        return {
            'code': 200,
            'msg': 'Recipe enabled/disabled',
        }
    else:
        return {
            'code': 500,
            'msg': 'Server error. It is not you, it is us.'
        }


def delete_recipe(recipe_id):
    result = da.delete_recipe(recipe_id)
    if result:
        return {
            'code': 200,
            'msg': 'Recipe deleted'
        }
    else:
        return {
            'code': 500,
            'msg': 'Server error. It is not you, it is us.'
        }


def import_recipe(data):
    try:
        relationships = data['relationships']
        for relationship in relationships:
            service_1 = relationship['service1']
            service_2 = relationship['service2']
            da.create_relationship(name=relationship['name'], desc=relationship['desc'], service_1=service_1['name'],
                                   service_2=service_2['name'])
            da.create_service(thing=service_1['thing']['id'], name=service_1['name'], entity=service_1['entity'],
                              space=service_1['space'], icon=service_1['icon'])
            da.create_service(thing=service_2['thing']['id'], name=service_2['name'], entity=service_2['entity'],
                              space=service_2['space'], icon=service_2['icon'])

        da.create_recipe(id=data['id'], name=data['name'],
                         relationships=[relationship['name'] for relationship in relationships], icon=data['icon'],
                         enabled=False)
        return {
            'code': 200,
            'msg': 'Recipe imported'
        }
    except:
        return {
            'code': 500,
            'msg': 'Error importing'
        }