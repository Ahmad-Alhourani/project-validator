# from app.project_config_manager import CurrentConfig

from json_schema import JsonSchema


class Validator:
    def __init__(self, json_data):
        self._status = True
        self._messages = []
        self._dict_config = {}
        self._collected_config = {}
        self._obj_config = None
        self.validate_schema(json_data)
        if self.get_status() is True:
            self.logic_validation(json_data)

    def validate_schema(self, json_data):
        """
        use this service to verify input config
        :param json_data: json config data
        """
        try:
            schema = JsonSchema()
            self._dict_config = schema.deserialize(json_data)
        except Exception as e:
            self._status = False
            self._messages.append(str(e))
        return True

    def logic_validation(self, json_data):
        self._obj_config = CurrentConfig.from_dict(json_data)
        self._collect_config_data()
        # if self.get_status() is True:
        self._parse_logic_config()

    def _collect_config_data(self):
        arr = {"entities": [],
               "models": [],
               "tables": []
               }

        if self._obj_config.entities:
            for entity in self._obj_config.entities:

                if entity.name in arr["entities"]:
                    self._messages.append(
                        self._error_message(entity.name, "entity", entity.name, "entity.name :duplicated value ",
                                            entity.name, ""))
                else:
                    if entity.table is not None:
                        if entity.table in arr["tables"]:
                            self._messages.append(
                                self._error_message(entity.name, "entity", entity.table,
                                                    "entity.table :duplicated value ",
                                                    entity.table, ""))
                        else:
                            arr["tables"].append(entity.table)

                    if entity.model is not None:
                        if entity.table in arr["models"]:
                            self._messages.append(
                                self._error_message(entity.name, "entity", entity.model,
                                                    "entity.model :duplicated value ",
                                                    entity.model, ""))
                        else:
                            arr["models"].append(entity.model)

                    entity_info = {
                        "fields": [],
                        "relations": []
                    }
                    arr["entities"].append(entity.name)
                    arr[entity.name] = entity_info

                    if entity.fields:
                        for field in entity.fields:
                            if field.name in arr[entity.name]["fields"]:
                                self._messages.append(
                                    self._error_message(entity.name, "field", field.name,
                                                        "field.name :duplicated value",
                                                        field.name, ""))
                            else:
                                arr[entity.name]["fields"].append(field.name)

                    if entity.relations:
                        for relation in entity.relations:
                            if relation.name in arr[entity.name]["relations"]:
                                self._messages.append(
                                    self._error_message(entity.name, "relation", relation.name,
                                                        "relation.name :duplicated value",
                                                        relation.name, ""))
                            else:
                                arr[entity.name]["relations"].append(relation.name)

        self._collected_config = arr

    def _parse_logic_config(self):

        if self._obj_config.entities:
            for entity in self._obj_config.entities:

                #  check fields
                if entity.fields is not None:
                    for field in entity.fields:
                        self._parse_field(field, entity.name)

                #  check relations
                if entity.relations is not None:
                    for rel in entity.relations:
                        self._parse_relation(rel, entity.name)

                #  check extra properties
                if entity.extra_properties is not None:
                    self._parse_extra_properties(entity.extra_properties, entity.name)

    def _parse_field(self, field, entity_name):
        # check dbtype type
        self._validate_db_type(field, entity_name)

        # check foreign
        if field.db_type.foreign:
            self._validate_db_foreign(field, entity_name)

        # check view type
        if field.view_type:
            self._validate_view_type(field, entity_name)

        # check validation
        # if field.validations:
        #     self._validate_validations(field, entity_name)

    def _parse_relation(self, rel, entity):
        # check  type
        if rel.relation.type not in ["mtm", "1tm"]:
            return self._messages.append(
                self._error_message(entity, "relation", rel.name, "relation.type :invalid value ",
                                    rel.rel.relation.type, ["mtm", "1tm"]))
        other_entities = self._collected_config["entities"].copy()
        other_entities.remove(entity)

        # check related entity
        if rel.relation.related_entity not in other_entities:
            return self._messages.append(
                self._error_message(entity, "relation", rel.name, "relation.relatedEntity :invalid value ",
                                    rel.relation.related_entity, other_entities))

        need_field_view = True
        if rel.in_form is False and rel.in_index is False:
            if rel.in_view is False:
                need_field_view = False

        if rel.relation.type == "1tm":
            if rel.relation.foreign_key not in self._collected_config[rel.relation.related_entity]["fields"]:
                self._messages.append(
                    self._error_message(entity, "relation", rel.name, "relation.foreignKey :invalid value ",
                                        rel.relation.foreign_key,
                                        self._collected_config[rel.relation.related_entity]["fields"]))

            if need_field_view is True:
                if rel.relation.field_view not in self._collected_config[rel.relation.related_entity]["fields"]:
                    self._messages.append(
                        self._error_message(entity, "relation", rel.name, "relation.fieldView :invalid value ",
                                            rel.relation.field_view,
                                            self._collected_config[rel.relation.related_entity]["fields"]))

        if rel.relation.type == "mtm":
            if rel.relation.pivot_fields:

                # check middle entity
                if rel.relation.middle_entity not in other_entities:
                    return self._messages.append(
                        self._error_message(entity, "relation", rel.name, "relation.middleEntity :invalid value ",
                                            rel.relation.middle_entity, other_entities))
                p_fields = self._collected_config[rel.relation.middle_entity]["fields"].copy()
                if rel.relation.foreign_key not in self._collected_config[rel.relation.middle_entity]["fields"]:
                    self._messages.append(
                        self._error_message(entity, "relation", rel.name, "relation.foreignKey :invalid value ",
                                            rel.relation.foreign_key,
                                            self._collected_config[rel.relation.middle_entity]["fields"]))
                else:
                    p_fields.remove(rel.relation.foreign_key)

                if rel.relation.other_key not in self._collected_config[rel.relation.middle_entity]["fields"]:
                    self._messages.append(
                        self._error_message(entity, "relation", rel.name, "relation.otherKey :invalid value ",
                                            rel.relation.other_key,
                                            self._collected_config[rel.relation.middle_entity]["fields"]))
                else:
                    p_fields.remove(rel.relation.other_key)

                for item in rel.relation.pivot_fields:
                    if item not in p_fields:
                        self._messages.append(
                            self._error_message(entity, "relation", rel.name, "relation.pivotFields :invalid value ",
                                                item, p_fields))

            else:
                # check middle entity
                if rel.relation.middle_entity == entity:
                    return self._messages.append(
                        self._error_message(entity, "relation", rel.name, "relation.middleEntity :invalid value ",
                                            rel.relation.middle_entity, other_entities))

                if rel.relation.middle_entity not in other_entities:
                    self._messages.append(
                        self._error_message(entity, "relation", rel.name, "Devyzer will create entity with name "
                                            + rel.relation.middle_entity,
                                            rel.relation.middle_entity,
                                            "", True))

                    # check field view
                    if need_field_view is True:
                        if rel.relation.field_view not in self._collected_config[rel.relation.related_entity]["fields"]:
                            self._messages.append(
                                self._error_message(entity, "relation", rel.name, "relation.fieldView :invalid value ",
                                                    rel.relation.field_view,
                                                    self._collected_config[rel.relation.related_entity]["fields"]))
                    else:
                        self._messages.append(
                            self._error_message(entity, "relation", rel.name,
                                                "You must enable relation inForm an inView at least",
                                                rel.relation.inForm,
                                                True, True))

                else:
                    if rel.relation.foreign_key not in self._collected_config[rel.relation.middle_entity]["fields"]:
                        self._messages.append(
                            self._error_message(entity, "relation", rel.name, "relation.foreignKey :invalid value ",
                                                rel.relation.foreign_key,
                                                self._collected_config[rel.relation.middle_entity]["fields"]))

                    if rel.relation.other_key not in self._collected_config[rel.relation.middle_entity]["fields"]:
                        self._messages.append(
                            self._error_message(entity, "relation", rel.name, "relation.otherKey :invalid value ",
                                                rel.relation.other_key,
                                                self._collected_config[rel.relation.middle_entity]["fields"]))

    def _parse_extra_properties(self, extra_pro, entity):
        if extra_pro.sluggable is not None:
            parts = extra_pro.sluggable.split(",")
            length = len(parts)
            if not length == 2:
                return self._messages.append(
                    self._error_message(entity, "extra_properties", "", "sluggable :invalid value ",
                                        extra_pro.sluggable, "field_name,slug"))
            if parts[0].replace(' ', '') not in self._collected_config[entity]["fields"]:
                self._messages.append(
                    self._error_message(entity, "extra_properties", "", "sluggable :invalid value ",
                                        parts[0], self._collected_config[entity]["fields"]))

            if length == 2 and not parts[1].replace(' ', '') == "slug":
                self._messages.append(
                    self._error_message(entity, "extra_properties", "", "sluggable :invalid value ",
                                        parts[1], "slug"))

    def _validate_db_foreign(self, field, entity):

        foreign = field.db_type.foreign
        other_entities = self._collected_config["entities"].copy()
        other_entities.remove(entity)
        if foreign.related_entity not in other_entities:
            return self._messages.append(
                self._error_message(entity, "field", field.name, "dbType.foreign.relatedEntity :invalid value ",
                                    foreign.related_entity, other_entities))

        if foreign.field_view not in self._collected_config[foreign.related_entity]["fields"]:
            self._messages.append(
                self._error_message(entity, "field", field.name, "dbType.foreign.fieldView :invalid value ",
                                    foreign.field_view, self._collected_config[foreign.related_entity]["fields"]))
        if foreign.related_field:
            if foreign.related_field not in self._collected_config[foreign.related_entity]["fields"]:
                return self._messages.append(
                    self._error_message(entity, "field", field.name, "dbType.foreign.relatedField :invalid value ",
                                        foreign.related_field,
                                        self._collected_config[foreign.related_entity]["fields"]))

        # check view type
        if not field.view_type:
            return self._messages.append(
                self._error_message(entity, "field", field.name, "viewType.type:invalid value ",
                                    field.view_type, "viewType.type: select"))

        if field.view_type.type not in ["select", "text"]:
            return self._messages.append(
                self._error_message(entity, "field", field.name, "viewType.type:invalid value ",
                                    field.view_type.type, "select"))

    def _validate_db_type(self, field, entity):

        db_types = ["bigIncrements", "bigInteger", "binary", "boolean", "char", "date", "dateTime", "dateTimeTz",
                    "decimal", "double", "enum", "float", "increments", "integer", "Integer", "ipAddress", "json",
                    "longText", "macAddress", "mediumInteger", "mediumText", "morphs", "nullabelTimestamps",
                    "rememberToken", "smallInteger", "string", "text", "time", "timeTz", "tinyInteger", "timestamp",
                    "timestampTz", "timestamps", "uuid", "jsonb", ]
        parts_2_db_types = ["char", "string"]
        parts_3_db_types = ["decimal", "double"]
        id_db_types = ["bigIncrements", "increments"]

        parts = field.db_type.type.split("|")
        length = len(parts)
        if field.name == "id" and parts[0] not in id_db_types:
            return self._messages.append(
                self._error_message(entity, "field", field.name, "dbType.type :invalid value ", parts[0], id_db_types))

        if length == 2:
            if parts[0] not in parts_2_db_types:
                return self._messages.append(
                    self._error_message(entity, "field", field.name, "dbType.type :invalid value ", parts[0],
                                        parts_2_db_types))

        if length == 2:
            if parts[0] not in parts_3_db_types:
                return self._messages.append(
                    self._error_message(entity, "field", field.name, "dbType.type :invalid value ", parts[0],
                                        parts_3_db_types))
        if parts[0] not in db_types:
            return self._messages.append(
                self._error_message(entity, "field", field.name, "dbType.type :invalid value ", parts[0], db_types))

        if parts[0] == "enum":
            expected_values = [{"label": "label1", "value": "value1"}, {"label": "label2", "value": "value2"}]
            if not field.view_type:
                expected_values_view_type = {"viewType": {
                    "type": "select",
                    "enums": expected_values
                }}
                return self._messages.append(
                    self._error_message(entity, "field", field.name, "viewType :invalid value ",
                                        "", expected_values_view_type))
            else:
                if not field.view_type.type == "select":
                    self._messages.append(
                        self._error_message(entity, "field", field.name, "viewType.type:invalid value ",
                                            field.view_type.type, "select"))
                if not field.view_type.enums:
                    expected_values = [{"label": "label1", "value": "value1"}, {"label": "label2", "value": "value2"}]
                    return self._messages.append(
                        self._error_message(entity, "field", field.name, "viewType.enums :invalid value ",
                                            "", expected_values))
                if not isinstance(field.view_type.enums, list):
                    expected_values = [{"label": "label1", "value": "value1"}, {"label": "label2", "value": "value2"}]
                    return self._messages.append(
                        self._error_message(entity, "field", field.name, "viewType.enums :invalid value ",
                                            field.view_type.enums, expected_values))

    def _validate_view_type(self, field, entity):
        view_type = field.view_type.type
        view_types = ["Integer", "integer", "decimal", "text", "textarea", "date", "checkbox", "select", "img", "image",
                      "multiselect", "password", "email", "datetime"]
        if view_type is not None:
            if view_type not in view_types:
                return self._messages.append(
                    self._error_message(entity, "field", field.name, "viewType.type :invalid value ",
                                        view_type, view_types))

            if view_type == "checkbox":
                if not field.db_type.type == "boolean":
                    return self._messages.append(
                        self._error_message(entity, "field", field.name, "dbType.type :invalid value ",
                                            field.db_type.type, "boolean"))

            if view_type in ["img", "image"]:
                if not field.db_type.type == "string":
                    return self._messages.append(
                        self._error_message(entity, "field", field.name, "dbType.type :invalid value ",
                                            field.db_type.type, "string"))

        else:
            if field.db_type.type not in ["increments", "bigIncrements"]:
                return self._messages.append(
                    self._error_message(entity, "field", field.name, "viewType.type :invalid value ",
                                        "", view_types))

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
