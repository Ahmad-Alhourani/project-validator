import json

import inflect as inflect

p = inflect.engine()


class Manager:
    config_data = {}

    def __init__(self, config_dict):
        self.config_data = config_dict

    # def validate_config_schema(self):
    #     '''
    #     use this service for logic validation
    #     :return: true or error messege
    #     '''
    #     error_messeges = []
    #     # parse data as adictionary with keys entities names
    #     data = self.helper.parse_config_schema(self.config_data)
    #     for entity in self.config_data['entities']:
    #         if entity['fields']:
    #             for field in entity['fields']:
    #
    #                 # validate foreign data (field && Model)
    #                 if field['dbType']['foreign']:
    #                     table = field['dbType']['foreign']['table']
    #                     model = table.title()
    #                     model = p.singular_noun(model)
    #
    #                     # validate model if it is founded  or not
    #                     if model not in data['entities_names']:
    #                         error_messeges.append(MyError("threre isn't tabel has model with name ", model))
    #                     # vlidate field if it is founded in other entity or not
    #                     if field['dbType']['foreign']['fieldView'] not in data[model]['fields']:
    #                         error_messeges.append(MyError("The model  " + model + "  dose not have  field with name " +
    #                                                       field['dbType']['foreign']['fieldView'],
    #                                                       field['dbType']['foreign']['fieldView']))
    #
    #         # validate relation
    #         if entity['relations']:
    #             for relation in entity['relations']:
    #                 # validate model  if it is founded  or not
    #                 if relation['relation']['relatedModelName'] not in data['entities_names']:
    #                     error_messeges.append(
    #                         MyError("threre isn't tabel has model with name ",
    #                                 relation['relation']['relatedModelName']))
    #
    #                 if relation['relation']['type'] == "1tm":
    #                     # validate foreign key if it is founded in other entity or not
    #                     if relation['relation']['foreignKey'] not in data[relation['relation']['relatedModelName']][
    #                         'fields']:
    #                         error_messeges.append(
    #                             MyError("The model  " + relation['relation'][
    #                                 'relatedModelName'] + "  dose not have  field with name " + relation['relation'][
    #                                         'foreignKey'],
    #                                     relation['relation']['foreignKey']))
    #
    #                 if relation['relation']['type'] == "mtm":
    #                     middle = (relation['relation']['middleTable'])
    #                     middle = p.singular_noun(middle)
    #                     middle = middle.title()
    #                     # validate table
    #                     if middle not in data['entities_names']:
    #                         error_messeges.append(
    #                             MyError("threre isn't tabel has model with name", middle))
    #
    #                     # validate foreign key if it is founded in other entity or not
    #                     if relation['relation']['foreignKey'] not in data[middle]['fields']:
    #                         error_messeges.append(
    #                             MyError(
    #                                 "The model  " + middle + "  dose not have  field with name " + relation['relation'][
    #                                     'foreignKey'],
    #                                 relation['relation']['foreignKey']))
    #                     # validate other key if it is founded in other entity or not
    #                     if relation['relation']['otherKey'] not in data[middle]['fields']:
    #                         error_messeges.append(
    #                             MyError(
    #                                 "The model  " + middle + "  dose not have  field with name " + relation['relation'][
    #                                     'otherKey'],
    #                                 relation['relation']['otherKey']))
    #
    #     if error_messeges:
    #         return error_messeges
    #     return True

    def inheritance_config(self):
        '''
        use this service to inheritance data from snipets
        :return: update config data and return true
        '''
        temp = self.config_data.copy();
        for entity in self.config_data['entities']:
            if ("extend") in entity:
                entity_name = entity["extend"]['entity']
                with open(entity["extend"]['snipet']) as f:
                    data = json.load(f)
                schema = JsonSchema()
                secondary_conf = schema.deserialize(data)
                index = self.helper.is_entity_exist(secondary_conf, entity_name)
                new_entity = secondary_conf["entities"][index]
                origin_name = entity["name"]
                entity.update(new_entity)
                entity['name'] = origin_name

        return True

    def add_entity(self, entity):
        """
        use this service to add entity to config data
        :param entity:  data of entity
        :return: update config data and return true
        """

        error_messeges = []

        res = self.helper.is_entity_exist(self.config_data, entity['name'])
        if (res != -1):
            error_messeges.append(MyError('Entity is founded', entity['name']))
            return error_messeges
        validate_entity(entity, error_messeges)
        if error_messeges:
            return error_messeges
        if 'entities' not in self.config_data:
            self.config_data = {"entities": []}
        self.config_data['entities'].append(entity)

        return True

    def upadte_entity(self, olg_entity, new_entity):
        '''
          use this service to update entity in config data
        :param olg_entity: origin entity name
        :param new_entity: updated data of entity
        :return:  update config data and return true
        '''
        error_messeges = []

        old_res = self.helper.is_entity_exist(self.config_data, olg_entity)
        if (old_res == -1):
            error_messeges.append(MyError('Entity is not founded', olg_entity))
            return error_messeges
        valid_value_empty_string_requierd(new_entity["name"], "new_entity", error_messeges)
        new_res = self.helper.is_entity_exist(self.config_data, new_entity["name"])
        if (new_res != -1):
            error_messeges.append(MyError('Entity is  founded', new_entity["name"]))
            return error_messeges
        temp = self.config_data['entities'][old_res]['name']
        self.config_data['entities'][old_res]['name'] = new_entity
        if error_messeges:
            self.config_data['entities'][old_res]['name'] = temp
            return error_messeges
        return True

    def delete_entity(self, entity_name):
        '''
          use this service to deltete entity from config data
        :param entity_name: entity name
        :return:  update config data and return true
        '''
        error_messeges = []

        res = self.helper.is_entity_exist(self.config_data, entity_name)
        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges
        del self.config_data['entities'][res]
        if error_messeges:
            return error_messeges

        return True

    def add_field(self, entity_name, field):
        '''
          use this service to add field to config data
        :param entity_name: name of entity
        :param field: data of field
        :return:  update config data and return true
        '''
        error_messeges = []

        res = self.helper.is_field_exist(self.config_data, entity_name, field['name'])
        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges
        if (res != -2):
            error_messeges.append(MyError('Field name is  founded', field['name']))
            return error_messeges
        validate_field(field, error_messeges)
        self.config_data['entities'][res]['fields'].append(field)
        if error_messeges:
            return error_messeges
        return True

    def upadte_field(self, entity_name, old_field_name, new_field):
        '''
          use this service to update field in config data
        :param entity_name: entity name
        :param old_field_name: origin field
        :param new_field: data of new field
        :return:  update config data and return true
        '''
        error_messeges = []

        old_res = self.helper.is_field_exist(self.config_data, entity_name, old_field_name)
        if (old_res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges
        if (old_res == -2):
            error_messeges.append(MyError('Field name is not founded', old_field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        temp = self.config_data['entities'][entity_index]['fields'][old_res].copy()
        if "name" in new_field and old_field_name != new_field['name']:
            valid_value_empty_string_requierd(new_field['name'], "field['name']", error_messeges)
            new_res = self.helper.is_field_exist(self.config_data, entity_name, new_field['name'])
            if (new_res >= 0):
                error_messeges.append(MyError('Field name is  founded', new_field['name']))
                return error_messeges
            self.config_data['entities'][entity_index]['fields'][old_res]['name'] = new_field['name']

        if "title" in new_field:
            valid_value_empty_string_requierd(new_field['title'], "field['title']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][old_res]['title'] = new_field['title']
        if "fillable" in new_field:
            is_bool(new_field['fillable'], "field['fillable']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][old_res]['fillable'] = new_field['fillable']
        if "inForm" in new_field:
            is_bool(new_field['inForm'], "field['inForm']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][old_res]['inForm'] = new_field['inForm']
        if "inIndex" in new_field:
            is_bool(new_field['inIndex'], "field['inIndex']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][old_res]['inIndex'] = new_field['inIndex']
        if "searchable" in new_field:
            is_bool(new_field['searchable'], "field['searchable']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][old_res]['searchable'] = new_field['searchable']

        if error_messeges:
            self.config_data['entities'][entity_index]['fields'][old_res] = temp
            return error_messeges
        return True

    def delete_field(self, entity_name, field_name):
        '''
          use this service to delete field from config data
        :param entity_name: entity name
        :param field_name: fielf name
        :return:  update config data and return true
        '''
        error_messeges = []

        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)
        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges
        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        del self.config_data['entities'][entity_index]['fields'][res]
        return True

    def add_db_type(self, entity_name, field_name, dbType):
        '''
          use this service to add db type to config data
        :param entity_name:entity name
        :param field_name: field name
        :param dbType: data of db type
        :return:  update config data and return true
        '''
        error_messeges = []

        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)
        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges
        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges
        validateDbtype(dbType, error_messeges)
        if error_messeges:
            return error_messeges
        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        self.config_data['entities'][entity_index]['fields'][res]['dbType'] = dbType

        return True

    def update_db_type(self, entity_name, field_name, dbType):
        '''
          use this service to update db type in config data
        :param entity_name: entity name
        :param field_name: fielf name
        :param dbType: data of db type
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        temp = self.config_data['entities'][entity_index]['fields'][res]['dbType'].copy()

        if "type" in dbType:
            valid_value_empty_string_requierd(dbType['type'], "dbType['type']", error_messeges)
            is_db_type(dbType['type'], error_messeges, "dbType['type']")
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['dbType']['type'] = dbType['type']

        if 'primary' in dbType:
            is_bool(dbType['primary'], "dbType['primary']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['dbType']['primary'] = dbType['primary']

        if 'default' in dbType:
            valid_value_empty_string_requierd(dbType['default'], "dbType['default']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['dbType']['default'] = dbType['default']

        if error_messeges:
            self.config_data['entities'][entity_index]['fields'][res]['dbType'] = temp
            return error_messeges

        return True

    def delete_db_type(self, entity_name, field_name):
        '''
          use this service to delete db type from config data
        :param entity_name:entity name
        :param field_name: field name
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        del self.config_data['entities'][entity_index]['fields'][res]['dbType']

        if error_messeges:
            return error_messeges

        return True

    def add_db_type_foreign(self, entity_name, field_name, foreign):
        '''
          use this service to ad  db type foreign to config data
        :param entity_name: entity name
        :param field_name: field name
        :param foreign: data of foreign
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        validateDbtypeForeign(foreign, error_messeges)
        if error_messeges:
            return error_messeges
        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign'] = foreign

        return True

    def update_db_type_foreign(self, entity_name, field_name, foreign):
        '''
        use this service to update  db type foreign in config data
        :param entity_name: entity name
        :param field_name: field name
        :param foreign: data of foreign
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        temp = self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign'].copy()

        if "relatedField" in foreign:
            valid_value_empty_string_requierd(foreign['relatedField'], "foreign['relatedField']", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign']['relatedField'] = \
                    foreign[
                        'relatedField']

        if "table" in foreign:
            valid_value_empty_string_requierd(foreign['table'], "foreign['table']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign']['table'] = foreign[
                    'table']

        if "fieldView" in foreign:
            valid_value_empty_string_requierd(foreign['fieldView'], "foreign['fieldView']", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign']['fieldView'] = foreign[
                    'fieldView']
        if error_messeges:
            self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign'] = temp
            return error_messeges
        return True

    def delete_db_type_foreign(self, entity_name, field_name):
        '''
        use this service to delete  db type foreign from config data
        :param entity_name: entity name
        :param field_name: field name
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        del self.config_data['entities'][entity_index]['fields'][res]['dbType']['foreign']

        if error_messeges:
            return error_messeges
        return True

    def add_view_type(self, entity_name, field_name, viewType):
        '''
        use this service to add  view type to config data
        :param entity_name: entity name
        :param field_name: field name
        :param viewType: data of view type
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        validate_view_type(viewType, error_messeges)
        if error_messeges:
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        self.config_data['entities'][entity_index]['fields'][res]['viewType'] = viewType

        return True

    def update_view_type(self, entity_name, field_name, viewType):
        '''
        use this service to update view type  in config data
        :param entity_name: entity name
        :param field_name: field name
        :param viewType: data of view type
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        temp = self.config_data['entities'][entity_index]['fields'][res]['viewType'].copy()

        if 'type' in viewType:
            valid_value_empty_string_requierd(viewType['type'], "viewType['type']", error_messeges, 1)
            is_view_type(viewType['type'], error_messeges, "viewType['type']")
            if not error_messeges:
                self.config_data['entities'][entity_index]['fields'][res]['viewType']['type'] = viewType['type']

        if error_messeges:
            self.config_data['entities'][entity_index]['fields'][res]['viewType'] = temp
            return error_messeges

        return True

    def delete_view_type(self, entity_name, field_name):
        '''
        use this service to delete view type from config data
        :param entity_name: entity name
        :param field_name: field name
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        del self.config_data['entities'][entity_index]['fields'][res]['viewType']

        return True

    def add_view_type_enums(self, entity_name, field_name, enum):
        '''
        use this service to add view type enums  to config data
        :param entity_name:entity name
        :param field_name: field name
        :param enum: enum data   label && value
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        for element in enum:
            validateEnum(element, error_messeges)

        if error_messeges:
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        self.config_data['entities'][entity_index]['fields'][res]['viewType']['enums'] = enum

        return True

    def delete_view_type_enums(self, entity_name, field_name):
        '''
        use this service to delete view type enums from config data
         :param entity_name:entity name
         :param field_name: field name
         :return:  update config data and return true
         '''
        error_messeges = []
        res = self.helper.is_field_exist(self.config_data, entity_name, field_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Field name is not founded', field_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        del self.config_data['entities'][entity_index]['fields'][res]['viewType']['enums']

        return True

    def add_relation(self, entity_name, relation):
        '''
        use this service to add  relation to config data
        :param entity_name: entity name
        :param relation: relation data
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_relation_exist(self.config_data, entity_name, relation['name'])

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res != -2):
            error_messeges.append(MyError('Relation name is  founded', relation['name']))
            return error_messeges

        validate_relation(relation, error_messeges)
        if error_messeges:
            return error_messeges

        self.config_data['entities'][res]['relations'].append(relation)
        return True

    def upadte_relation(self, entity_name, olg_relation_name, relation):
        '''
        use this service to update  relation in config data
        :param entity_name:entity name
        :param olg_relation_name:origin relation
        :param relation:updated relation date
        :return:update config data and return true
        '''
        error_messeges = []
        old_res = self.helper.is_relation_exist(self.config_data, entity_name, olg_relation_name)

        if (old_res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (old_res == -2):
            error_messeges.append(MyError('Relation name is not founded', olg_relation_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        temp = self.config_data['entities'][entity_index]['relations'][old_res].copy()

        if "name" in relation and olg_relation_name != relation['name']:
            new_res = self.helper.is_relation_exist(self.config_data, entity_name, relation['name'])
            if (new_res >= 0):
                error_messeges.append(MyError('Relation name is founded', relation['name']))
                return error_messeges
            self.config_data['entities'][entity_index]['relations'][old_res]['name'] = relation['name']

        if "type" in relation:
            valid_value_empty_string_requierd(relation['type'], "relation['type", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][entity_index]['relations'][old_res]['type'] = relation['type']

        if "relation" in relation:

            relationData = relation['relation']
            if "type" in relationData:
                my_list = ["mtm", "1tm"]
                valid_value_empty_string_requierd(relationData['type'], "relationData['type", error_messeges)

                if not relationData['type'] in my_list:
                    error_messeges.append(MyError('Invalid Relation Type', relationData['type']))

                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['type'] = relationData[
                        'type']

                if relationData['type'] == "mtm":

                    if 'weakness' in relationData:
                        is_bool(relationData['weakness'], "relationData['weakness", error_messeges, 1)
                        if not error_messeges:
                            self.config_data['entities'][entity_index]['relations'][old_res]['relation']['weakness'] = \
                                relationData[
                                    'weakness']

                    if 'middleTable' in relationData:
                        valid_value_empty_string_requierd(relationData['middleTable'], "relationData['middleTable",
                                                          error_messeges)
                        if not error_messeges:
                            self.config_data['entities'][entity_index]['relations'][old_res]['relation'][
                                'middleTable'] = \
                                relationData[
                                    'middleTable']

            if "relatedModelName" in relationData:
                valid_value_empty_string_requierd(relationData['relatedModelName'], "relationData['relatedModelName",
                                                  error_messeges)
                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['relatedModelName'] = \
                        relationData['relatedModelName']

            if "relatedEntity" in relationData:
                valid_value_empty_string_requierd(relationData['relatedEntity'], "relationData['relatedEntity",
                                                  error_messeges)
                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['relatedEntity'] = \
                        relationData['relatedEntity']

            if "foreignKey" in relationData:
                valid_value_empty_string_requierd(relationData['foreignKey'], "relationData['foreignKey",
                                                  error_messeges)
                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['foreignKey'] = \
                        relationData['foreignKey']

            if "localKey" in relationData:
                valid_value_empty_string_requierd(relationData['localKey'], "relationData['localKey", error_messeges)
                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['localKey'] = \
                        relationData[
                            'localKey']

            if "otherKey" in relationData:
                valid_value_empty_string_requierd(relationData['otherKey'], "relationData['otherKey", error_messeges)
                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['otherKey'] = \
                        relationData[
                            'otherKey']

            if "type" in relationData:
                valid_value_empty_string_requierd(relationData['type'], "relationData['type", error_messeges)
                if not error_messeges:
                    self.config_data['entities'][entity_index]['relations'][old_res]['relation']['type'] = relationData[
                        'type']
        if error_messeges:
            self.config_data['entities'][entity_index]['relations'][old_res] = temp
            return error_messeges
        return True

    def delete_relation(self, entity_name, relation_name):
        '''
        use this service to delete relation in config data
        :param entity_name:entity name
        :param relation_name: relation name
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_relation_exist(self.config_data, entity_name, relation_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        if (res == -2):
            error_messeges.append(MyError('Relation name is not founded', relation_name))
            return error_messeges

        entity_index = self.helper.is_entity_exist(self.config_data, entity_name)
        del self.config_data['entities'][entity_index]['relations'][res]
        return True

    def add_extra_properties(self, entity_name, extra_properties):
        '''
        use this service to add  extra propereies data to  config data
        :param entity_name: entity name
        :param extra_properties: extra propereies data
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_entity_exist(self.config_data, entity_name, )

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges
        validate_extra_properties(extra_properties, error_messeges)

        if error_messeges:
            return error_messeges
        self.config_data['entities'][res]['extraProperties'] = extra_properties

        return True

    def upadte_extra_properties(self, entity_name, extra_properties):
        '''
        use this service to update  extra propereies data in  config data
        :param entity_name: entity name
        :param extra_properties: extra properties data
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_entity_exist(self.config_data, entity_name, )

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        temp = self.config_data['entities'][res]['extraProperties'].copy()
        if "sluggable" in extra_properties:
            valid_value_empty_string_requierd(extra_properties['sluggable'], "property['sluggable']", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][res]['extraProperties']['sluggable'] = extra_properties['sluggable']

        if "cachable" in extra_properties:
            is_bool(extra_properties['cachable'], "property['cachable']", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][res]['extraProperties']['cachable'] = extra_properties['cachable']

        if "metable" in extra_properties:
            is_bool(extra_properties['metable'], "property['metable']", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][res]['extraProperties']['metable'] = extra_properties['metable']

        if "softDelete" in extra_properties:
            is_bool(extra_properties['softDelete'], "property['softDelete']", error_messeges, 1)
            if not error_messeges:
                self.config_data['entities'][res]['extraProperties']['softDelete'] = extra_properties['softDelete']

        if error_messeges:
            self.config_data['entities'][res]['extraProperties'] = temp
            return error_messeges
        return True

    def delete_extra_properties(self, entity_name):
        '''
        use this service to delete extra propereies data from config data
        :param entity_name: entity name
        :return:  update config data and return true
        '''

        error_messeges = []
        res = self.helper.is_entity_exist(self.config_data, entity_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        del self.config_data['entities'][res]['extraProperties']
        return True

    def add_generation(self, entity_name, gen):
        '''
        use this service to add  generation data to  config data
        :param entity_name: entity name
        :param gen: generation data
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_entity_exist(self.config_data, entity_name, )

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        validate_generation(gen, error_messeges)
        if error_messeges:
            return error_messeges

        self.config_data['entities'][res]['generation'] = gen
        return True

    def upadte_generation(self, entity_name, gen):
        '''
        use this service to update generation data in  config data
        :param entity_name: entity name
        :param gen: generation data
        :return:  update config data and return true
        '''

        error_messeges = []
        res = self.helper.is_entity_exist(self.config_data, entity_name, )

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        temp = self.config_data['entities'][res]['generation'].copy()
        if 'model' in gen:
            is_bool(gen['model'], "generate['model']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['model'] = gen['model']

        if 'createEvent' in gen:
            is_bool(gen['createEvent'], "generate['createEvent']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['createEvent'] = gen['createEvent']

        if 'updateEvent' in gen:
            is_bool(gen['updateEvent'], "generate['updateEvent']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['updateEvent'] = gen['updateEvent']

        if 'deleteEvent' in gen:
            is_bool(gen['deleteEvent'], "generate['deleteEvent']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['deleteEvent'] = gen['deleteEvent']

        if 'listener' in gen:
            is_bool(gen['listener'], "generate['listener']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['listener'] = gen['listener']

        if 'repository' in gen:
            is_bool(gen['repository'], "generate['repository']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['repository'] = gen['repository']

        if 'createTable' in gen:
            is_bool(gen['createTable'], "generate['createTable']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['createTable'] = gen[
                    'createTable']

        if 'migrateTable' in gen:
            is_bool(gen['migrateTable'], "generate['migrateTable']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['migrateTable'] = gen['migrateTable']

        if 'createRequest' in gen:
            is_bool(gen['createRequest'], "generate['createRequest']")
            if not error_messeges:
                self.config_data['entities'][res]['generation']['createRequest'] = gen[
                    'createRequest']

        if 'updateRequest' in gen:
            is_bool(gen['updateRequest'], "generate['updateRequest']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['updateRequest'] = gen[
                    'updateRequest']

        if 'controller' in gen:
            is_bool(gen['controller'], "generate['controller']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['controller'] = gen['controller']

        if 'route' in gen:
            is_bool(gen['route'], "generate['route']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['route'] = gen['route']

        if 'breadcrumbs' in gen:
            is_bool(gen['breadcrumbs'], "generate['breadcrumbs']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['breadcrumbs'] = gen['breadcrumbs']

        if 'lang' in gen:
            is_bool(gen['lang'], "generate['lang']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['lang'] = gen['lang']

        if 'view' in gen:
            is_bool(gen['view'], "generate['view']")
            if not error_messeges:
                self.config_data['entities'][res]['generation']['view'] = gen['view']

        if 'apiCreateRequest' in gen:
            is_bool(gen['apiCreateRequest'], "generate['apiCreateRequest']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['apiCreateRequest'] = gen[
                    'apiCreateRequest']

        if 'apiUpdateRequest' in gen:
            is_bool(gen['apiUpdateRequest'], "generate['apiUpdateRequest']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['apiUpdateRequest'] = gen[
                    'apiUpdateRequest']

        if 'apiController' in gen:
            is_bool(gen['apiController'], "generate['apiController']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['apiController'] = gen[
                    'apiController']

        if 'apiRoute' in gen:
            is_bool(gen['apiRoute'], "generate['apiRoute']", error_messeges)
            if not error_messeges:
                self.config_data['entities'][res]['generation']['apiRoute'] = gen['apiRoute']
        if error_messeges:
            self.config_data['entities'][res]['generation'] = temp
            return error_messeges
        return True

    def delete_generation(self, entity_name):
        '''
        use this service to delete generation data from  config data
        :param entity_name:entity name
        :return:  update config data and return true
        '''
        error_messeges = []
        res = self.helper.is_entity_exist(self.config_data, entity_name)

        if (res == -1):
            error_messeges.append(MyError('Entity is not founded', entity_name))
            return error_messeges

        del self.config_data['entities'][res]['generation']
        return True
