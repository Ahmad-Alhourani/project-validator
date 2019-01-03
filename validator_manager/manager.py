from utils import is_entity_exist, is_field_exist, is_relation_exist
from validator import Validator
import copy


class Manager:
    def __init__(self):
        self._config_dict = {"entities": []}
        self._status = True
        self._messages = []

    def add_entities(self, entities_arr):
        """
        use this service to add array of entities to config data
        :param entities_arr:  array of entities
        :return: update config data and return true
        """
        temp = copy.deepcopy(self._config_dict)
        for entity in entities_arr:
            temp['entities'].append(entity)
        self._validate_operation(temp)

    def add_entity(self, entity):
        """
        use this service to add entity to config data
        :param entity:  data of entity
        :return: update config data and return true
        """
        temp = copy.deepcopy(self._config_dict)
        temp['entities'].append(entity)
        self._validate_operation(temp)

    def update_entity(self, old_entity, new_entity):
        """
        use this service to update entity in config data
        :param old_entity: origin entity name
        :param new_entity: updated data of entity
        :return:  update config data
       """
        temp = copy.deepcopy(self._config_dict)
        old_res = is_entity_exist(temp, old_entity)
        if old_res == -1:
            return self._messages.append(
                self._error_message(old_entity, "entity", old_entity, "Entity is not found",
                                    old_entity, ""))

        del temp['entities'][old_res]
        temp['entities'].append(new_entity)
        self._validate_operation(temp)

    def delete_entity(self, entity_name):
        """
        use this service to delete entity from config data
        :param entity_name: entity name
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        old_res = is_entity_exist(temp, entity_name)
        if old_res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))

        del temp['entities'][old_res]
        self._validate_operation(temp)

    def add_field(self, entity_name, field):
        """
        use this service to add field to config data
        :param entity_name: name of entity
        :param field: data of field
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        if "fields" not in temp['entities'][res]:
            temp['entities'][res]['fields'] = []

        temp['entities'][res]['fields'].append(field)
        self._validate_operation(temp)

    def update_field(self, entity_name, old_field_name, new_field):
        """
        use this service to update field in config data
        :param entity_name: entity name
        :param old_field_name: origin field
        :param new_field: data of new field
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        field_index = is_field_exist(temp, entity_name, old_field_name)
        if field_index == -2:
            return self._messages.append(
                self._error_message(entity_name, "field", old_field_name, "field is not found",
                                    old_field_name, ""))
        del temp['entities'][res]["fields"][field_index]
        temp['entities'][res]["fields"].append(new_field)
        self._validate_operation(temp)

    def delete_field(self, entity_name, field_name):
        """
        use this service to update field in config data
        :param entity_name: entity name
        :param field_name: field name
        :return:  update config data 
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        field_index = is_field_exist(temp, entity_name, field_name)
        if field_index == -2:
            return self._messages.append(
                self._error_message(entity_name, "field", field_name, "field is not found",
                                    field_name, ""))
        del temp['entities'][res]["fields"][field_index]
        self._validate_operation(temp)

    def add_db_type(self, entity_name, field_name, db_type):
        """
        use this service to add db type to config data
        :param entity_name:entity name
        :param field_name: field name
        :param db_type: data of db type
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        field_index = is_field_exist(temp, entity_name, field_name)
        if field_index == -2:
            return self._messages.append(
                self._error_message(entity_name, "field", field_name, "field is not found", field_name, ""))
        temp['entities'][res]['fields'][field_index]['dbType'] = db_type
        self._validate_operation(temp)

    def add_view_type(self, entity_name, field_name, view_type=None):
        """
        use this service to add db type to config data
        :param entity_name:entity name
        :param field_name: field name
        :param view_type: data of view type
        :return:  update config data
        """

        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        field_index = is_field_exist(temp, entity_name, field_name)
        if field_index == -2:
            return self._messages.append(
                self._error_message(entity_name, "field", field_name, "field is not found", field_name, ""))
        if view_type is None:
            view_type = {}
        temp['entities'][res]['fields'][field_index]['viewType'] = view_type
        self._validate_operation(temp)

    def add_relation(self, entity_name, relation):
        """
        use this service to add relation to config data
        :param entity_name: name of entity
        :param relation: data of relation
        :return:  update config data 
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        if "relations" not in temp['entities'][res]:
            temp['entities'][res]['relations'] = []

        temp['entities'][res]['relations'].append(relation)
        self._validate_operation(temp)

    def update_relation(self, entity_name, old_relation_name, new_relation):
        """
        use this service to update relation in config data
        :param entity_name: entity name
        :param old_relation_name: origin relation name
        :param new_relation: data of new relation
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        relation_index = is_relation_exist(temp, entity_name, old_relation_name)
        if relation_index == -2:
            return self._messages.append(
                self._error_message(entity_name, "relation", old_relation_name, "field is not found",
                                    old_relation_name, ""))
        del temp['entities'][res]["relations"][relation_index]
        temp['entities'][res]["relations"].append(new_relation)
        self._validate_operation(temp)

    def delete_relation(self, entity_name, relation_name):
        """
        use this service to delete relation from config data
        :param entity_name: entity name
        :param relation_name:  relation name
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        relation_index = is_relation_exist(temp, entity_name, relation_name)
        if relation_index == -2:
            return self._messages.append(
                self._error_message(entity_name, "relation", relation_name, "field is not found",
                                    relation_name, ""))
        del temp['entities'][res]["relations"][relation_index]
        self._validate_operation(temp)

    def add_extra_properties(self, entity_name, extra_properties=None):
        """
        use this service to add extra properties to config data
        :param entity_name: name of entity
        :param extra_properties: data of extra properties
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        if "extraProperties" not in temp['entities'][res]:
            temp['entities'][res]['extraProperties'] = {}
        if extra_properties is None:
            extra_properties = {}
        temp['entities'][res]['extraProperties'] = extra_properties
        self._validate_operation(temp)

    def add_generation(self, entity_name, generation=None):
        """
        use this service to add generation to config data
        :param entity_name: name of entity
        :param generation: data of generation
        :return:  update config data
        """
        temp = copy.deepcopy(self._config_dict)
        res = is_entity_exist(temp, entity_name)
        if res == -1:
            return self._messages.append(
                self._error_message(entity_name, "entity", entity_name, "Entity is not found",
                                    entity_name, ""))
        if "generation" not in temp['entities'][res]:
            temp['entities'][res]['generation'] = {}
        if generation is None:
            generation = {}
        temp['entities'][res]['generation'] = generation
        self._validate_operation(temp)

    def _validate_operation(self, config_dict):
        validator = Validator(config_dict)
        self._status = validator.get_status()
        self._messages = validator.get_messages()
        if self._status is True:
            self._config_dict = copy.deepcopy(config_dict)

    def _error_message(self, entity_name, error_mode, mode_name, message, current_value, expected_values, warning=None):
        message_type = "Warning"
        if warning is not True:
            self._status = False
            message_type = "Error"
        return {
            "entity": entity_name,
            "errorMode": error_mode,
            "modeName": mode_name,
            "currentValue": current_value,
            "message": message,
            "expectedValues": expected_values,
            "type": message_type
        }

    # ************************************************************************************************
    # ************************************************************************************************
    # ***************************************** GET Methods ******************************************
    # ************************************************************************************************
    # ************************************************************************************************

    def get_status(self):
        """
        :return: status
        """
        return self._status

    def get_messages(self):
        """
        :return: error messages
        """
        return self._messages

    def get_config_dict(self):
        """
        :return:  configuration as a dictionary
        """
        return self._config_dict
