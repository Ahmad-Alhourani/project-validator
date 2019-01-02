import json


def read_data_from_json_file(path):
    """
    use this function to read data from json file
    :param path: path of file
    :return: content of file
    """
    with open(path) as f:
        out_data = json.load(f)

    return out_data


def get_diff_config(current_config, last_config):
    """
    this will return the difference between  current config and input config
    :param last_config:  old config data
    :type last_config: dict
    :return: dict with keys
      "added" : array of added entities
      "deleted" array of deleted entities

      "const" array of other entities
      "count" count of old entities
    """
    results = {
        "added": [],
        "deleted": [],
        "const": [],
        "count": 0,
    }

    current_data = parse_config_schema(current_config)
    old_data = parse_config_schema(last_config)

    # find new entities
    results["added"] = diff(current_data['entities_names'], old_data['entities_names'])
    results["deleted"] = diff(old_data['entities_names'], current_data['entities_names'])
    results["count"] = len(old_data['entities_names'])

    # find deletes entities
    if current_config["entities"]:
        for entity in current_config["entities"]:
            if entity["name"] not in results["added"]:
                entity_name = entity["name"]

                # check fields
                if diff(current_data[entity["name"]]["fields"], old_data[entity["name"]]["fields"]):
                    if entity_name not in results["deleted"]:
                        results["deleted"].append(entity_name)
                        results["added"].append(entity_name)
                        continue

                if diff(old_data[entity["name"]]["fields"], current_data[entity["name"]]["fields"]):
                    if entity_name not in results["deleted"]:
                        results["deleted"].append(entity_name)
                        results["added"].append(entity_name)
                        continue

                # check relations
                if diff(current_data[entity["name"]]["relations"], old_data[entity["name"]]["relations"]):
                    if entity_name not in results["deleted"]:
                        results["deleted"].append(entity_name)
                        results["added"].append(entity_name)
                        continue

                if diff(old_data[entity["name"]]["relations"], current_data[entity["name"]]["relations"]):
                    if entity_name not in results["deleted"]:
                        results["deleted"].append(entity_name)
                        results["added"].append(entity_name)
                        continue

                curr_index = is_entity_exist(current_config, entity_name)
                old_index = is_entity_exist(last_config, entity_name)

                # check if entity update
                if dict_diff(current_config["entities"][curr_index], last_config["entities"][old_index]):
                    if entity_name not in results["deleted"]:
                        results["deleted"].append(entity_name)
                        results["added"].append(entity_name)
                        continue

                # check extra properties
                if "extraProperties" in current_config["entities"][curr_index]:
                    if dict_diff(current_config["entities"][curr_index]["extraProperties"],
                                 last_config["entities"][old_index]["extraProperties"]):
                        if entity_name not in results["deleted"]:
                            results["deleted"].append(entity_name)
                            results["added"].append(entity_name)
                            continue

                # check generation
                if "generation" in current_config["entities"][curr_index]:
                    if dict_diff(current_config["entities"][curr_index]["generation"],
                                 last_config["entities"][old_index]["generation"]):
                        if entity_name not in results["deleted"]:
                            results["deleted"].append(entity_name)
                            results["added"].append(entity_name)
                            continue

                # check if fields are deleted
                if entity["fields"]:
                    for field in entity["fields"]:
                        field_name = field["name"]
                        curr_index_field = is_field_exist(current_config, entity_name, field_name)
                        old_index_field = is_field_exist(last_config, entity_name, field_name)

                        # check if field is deleted
                        if dict_diff(current_config["entities"][curr_index]["fields"][curr_index_field],
                                     last_config["entities"][old_index]["fields"][old_index_field]):
                            if entity_name not in results["deleted"]:
                                results["deleted"].append(entity_name)
                                results["added"].append(entity_name)
                                continue
                        # check if field db type is deleted
                        if dict_diff(current_config["entities"][curr_index]["fields"][curr_index_field]["dbType"],
                                     last_config["entities"][old_index]["fields"][old_index_field]["dbType"]):
                            if entity_name not in results["deleted"]:
                                results["deleted"].append(entity_name)
                                results["added"].append(entity_name)
                                continue
                            # check foreign
                            if "foreign" in \
                                    current_config["entities"][curr_index]["fields"][curr_index_field]["dbType"]:
                                if dict_diff(
                                        current_config["entities"][curr_index]["fields"][curr_index_field]["dbType"]
                                        ["foreign"], last_config["entities"][old_index]["fields"][old_index_field]
                                        ["dbType"]["foreign"]):
                                    if entity_name not in results["deleted"]:
                                        results["deleted"].append(entity_name)
                                        results["added"].append(entity_name)
                                        continue

                        # check if field view type is deleted
                        if "viewType" in current_config["entities"][curr_index]["fields"][curr_index_field]:
                            if dict_diff(current_config["entities"][curr_index]["fields"][curr_index_field]["viewType"],
                                         last_config["entities"][old_index]["fields"][old_index_field]["viewType"]):
                                if entity_name not in results["deleted"]:
                                    results["deleted"].append(entity_name)
                                    results["added"].append(entity_name)
                                    continue

                            # check enum
                            if "enums" in current_config["entities"][curr_index]["fields"][curr_index_field][
                                "viewType"]:
                                if current_config["entities"][curr_index]["fields"][curr_index_field]["viewType"][
                                    "enums"]:
                                    j = 0
                                    for enum in \
                                            current_config["entities"][curr_index]["fields"][curr_index_field][
                                                "viewType"][
                                                "enums"]:
                                        if dict_diff(enum,
                                                     last_config["entities"][old_index]["fields"][old_index_field][
                                                         "viewType"]["enums"][j]):
                                            if entity_name not in results["deleted"]:
                                                results["deleted"].append(entity_name)
                                                results["added"].append(entity_name)
                                                continue
                                        j = j + 1

                # check if relations are deleted
                if entity["relations"]:
                    for relation in entity["relations"]:
                        relation_name = relation["name"]
                        curr_index_relation = is_relation_exist(current_config, entity_name, relation_name)
                        old_index_relation = is_relation_exist(last_config, entity_name, relation_name)

                        # check if relation  is deleted
                        if dict_diff(current_config["entities"][curr_index]["relations"][curr_index_relation],
                                     last_config["entities"][old_index]["relations"][old_index_relation]):
                            if entity_name not in results["deleted"]:
                                results["deleted"].append(entity_name)
                                results["added"].append(entity_name)
                                continue

                        if dict_diff(
                                current_config["entities"][curr_index]["relations"][curr_index_relation]["relation"],
                                last_config["entities"][old_index]["relations"][old_index_relation]["relation"]):
                            if entity_name not in results["deleted"]:
                                results["deleted"].append(entity_name)
                                results["added"].append(entity_name)
                                continue

    results["const"] = diff(old_data['entities_names'], results['deleted'])

    return results


def diff(li1, li2):
    """
    :type li1: array
      :type li2: array
    """
    return (list(set(li1) - set(li2)))


def dict_diff(first, second):
    """ Return a dict of keys that differ with another config object.  If a value is
        not found in one fo the configs, it will be represented by KEYNOTFOUND.
        @param first:   Fist dictionary to diff.
        @param second:  Second dicationary to diff.
        @return diff:   Dict of Key => (first.val, second.val)
    """
    if first is None:
        first = {}
    if second is None:
        second = {}

    KEYNOTFOUNDIN1 = '<KEYNOTFOUNDIN1>'  # KeyNotFound for dictDiff
    KEYNOTFOUNDIN2 = '<KEYNOTFOUNDIN2>'  # KeyNotFound for dictDiff

    diff = {}
    sd1 = set(first)
    sd2 = set(second)
    # Keys missing in the second dict
    for key in sd1.difference(sd2):
        diff[key] = KEYNOTFOUNDIN2
    # Keys missing in the first dict
    for key in sd2.difference(sd1):
        diff[key] = KEYNOTFOUNDIN1
    # Check for differences
    for key in sd1.intersection(sd2):

        if first[key] != second[key]:
            diff[key] = (first[key], second[key])
    return diff


def parse_config_schema(obj_schema):
    entities_names = {
        'entities_names': []
    }
    if obj_schema['entities']:
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
                    entities_names[entity['name']]['relations'].append(relation['relation']['relatedEntity'])

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
