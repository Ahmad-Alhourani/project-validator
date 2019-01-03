def parse_config_schema(obj_schema):
    entities_names = {
        'entities_names': []
    }
    for entity in obj_schema['entities']:
        entities_names['entities_names'].append(entity['name'])
        entities_names[entity['name']] = {
            'fields': [],
            'relations': [],
        }
        if entity['fields']:
            for field in entity['fields']:
                entities_names[entity['name']]['fields'].append(field['name'])
        if entity['relations']:
            for relation in entity['relations']:
                entities_names[entity['name']]['relations'].append(relation['relation']['relatedModelName'])

    return entities_names


def is_entity_exist(config_data, entity_name):
    index = 0
    if "entities" in config_data:
        for entity in config_data['entities']:
            if entity['name'] == entity_name:
                return index
            index = index + 1
    return -1


def is_field_exist(config_data, entity_name, field_name):
    res = is_entity_exist(config_data, entity_name)
    if res < 0:
        return res
    index = 0
    if "fields" in config_data['entities'][res]:
        for f in config_data['entities'][res]['fields']:
            if f['name'] == field_name:
                return index
            index = index + 1
    return -2


def is_relation_exist(config_data, entity_name, relation_name):
    res = is_entity_exist(config_data, entity_name)
    if res < 0:
        return res
    index = 0
    if "relations" in config_data['entities'][res]:
        for f in config_data['entities'][res]['relations']:
            if f['name'] == relation_name:
                return index
            index = index + 1
    return -2
