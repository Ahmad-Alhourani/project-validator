import inflect as inflect

from project_configuration_manager.project_config_manager import InputEntity, LastConfig, CurrentConfig, ConfigEntity, \
    Relations, Column, RelElement, SoftDeleteDatum, Paths
from project_configuration_manager.utils import get_diff_config

p = inflect.engine()
import re


class Parser:
    project_config = None
    input_entity = None

    def __init__(self, project_config):
        self.added_entities = []
        self.deleted_entities = []
        self.extra_entities = []
        self.parsed_entities = {}
        self.project_config = project_config
        self.extract_entities()
        self.parser_added_entities()

    def extract_entities(self):

        if self.project_config.get_last_config().entities:
            last_config_dict = LastConfig.to_dict(self.project_config.get_last_config())
            curr_config_dict = CurrentConfig.to_dict(self.project_config.get_current_config())
            result = get_diff_config(curr_config_dict, last_config_dict)

            for entity in self.project_config.get_current_config().entities:
                if entity.name in result["added"]:
                    self.added_entities.append(entity.name)

            for entity in self.project_config.get_last_config().entities:
                if entity.name in result["deleted"]:
                    self.init_input_entity()
                    self.parse_basic_data(entity)
                    entity.input_entity = self.input_entity
                    self.project_config.set_to_deleted_entities(entity)
                    self.deleted_entities.append(entity.name)

            deleted_extra_entities = self._get_deleted_extra_entities()
            for entity_name in deleted_extra_entities:
                if entity_name not in self.deleted_entities:
                    entity = ConfigEntity(entity_name, None, None, None, None, None, None, None)
                    self.init_input_entity()
                    self.parse_basic_data(entity)
                    entity.input_entity = self.input_entity
                    self.project_config.set_to_deleted_entities(entity)
                    self.deleted_entities.append(entity.name)
        else:
            for entity in self.project_config.get_current_config().entities:
                self.added_entities.append(entity.name)

    def parser_added_entities(self):
        # parse public data
        for entity in self.project_config.get_current_config().entities:
            self.init_input_entity()
            self.parse_basic_data(entity)
            entity.input_entity = self.input_entity
            self.parsed_entities[self.input_entity.entity_name] = self.input_entity

        # parse other data
        for entity in self.project_config.get_current_config().entities:
            if entity.name in self.added_entities:
                self.input_entity = entity.input_entity
                self.parse_other_data(entity)
                entity.input_entity = self.input_entity
                # self.parsed_entities[self.input_entity.entity_name] = self.input_entity
                self.project_config.set_to_added_entities(entity)

        for entity_dict in self.extra_entities:
            entity = ConfigEntity.from_dict(entity_dict)
            if not entity.name in self.added_entities:
                self.init_input_entity()
                self.parse_basic_data(entity)
                self.parse_other_data(entity)
                entity.input_entity = self.input_entity
                self.parsed_entities[self.input_entity.entity_name] = self.input_entity
                self.project_config.set_to_added_entities(entity)
                self.added_entities.append(entity.name)

    def _get_deleted_extra_entities(self):
        """
        use this function to get deleted extra entities
        :param obj_schema: configuration schema
        :return: all extra deleted entities
        """
        arr = []
        for entity in self.project_config.get_last_config().entities:
            if entity.name in self.deleted_entities:
                if entity.relations:
                    for rel in entity.relations:
                        if rel.relation.type == "mtm":
                            if not rel.relation.pivot_fields:
                                if rel.relation.middle_entity not in arr:
                                    arr.append(rel.relation.middle_entity)

        return arr

    def init_input_entity(self):
        gen = {}
        gen["generate_model"] = True
        gen["generate_create_event"] = True
        gen["generate_update_event"] = True
        gen["generate_delete_event"] = True
        gen["generate_listener"] = True
        gen["generate_repository"] = True
        gen["generate_table_migrate"] = True
        gen["generate_migrate"] = True
        gen["generate_create_request"] = True
        gen["generate_update_request"] = True
        gen["generate_controller"] = True
        gen["generate_route"] = True
        gen["generate_breadcrumbs"] = True
        gen["generate_lang"] = True
        gen["generate_view"] = True
        gen["generate_api_create_request"] = True
        gen["generate_api_update_request"] = True
        gen["generate_api_controller"] = True
        gen["generate_api_route"] = True

        paths = Paths.from_dict(self.project_config.get_paths())

        relations = Relations([], [], [])
        self.input_entity = InputEntity([], [], [], [], [], [], [], [], [], [], [], [], gen, [], [], [], [],
                                        relations, False, False, False, False, [], [], [], [], [], [], [], [], None,
                                        None, None, None, None, None, None, None, None, None, [], [], paths)

    def parse_basic_data(self, entity):

        self.input_entity.entity_name = entity.name

        if entity.model:
            self.input_entity.model_name = entity.model
        else:
            self.input_entity.model_name = self.get_model_name_from_entity(entity.name)

        if entity.table:
            self.input_entity.table_name = entity.table
        else:
            self.input_entity.table_name = self.get_table_name_from_model(self.input_entity.model_name)

        self.parse_general_info()

    def parse_general_info(self):
        self.input_entity.model_base_name = self.input_entity.model_name
        self.input_entity.model_plural = p.plural(self.input_entity.model_name)
        self.input_entity.migrate_name = self.get_migrate_name_from_table(self.input_entity.table_name)
        self.input_entity.title = self.get_title_from_entity(self.input_entity.entity_name)
        self.input_entity.model_variable = self.input_entity.model_name.lower()
        if p.singular_noun(self.input_entity.table_name):
            self.input_entity.model_dot_notation = p.singular_noun(self.input_entity.table_name)
        else:
            self.input_entity.model_dot_notation = self.input_entity.table_name
        self.input_entity.model_dash_variable = self.input_entity.model_dot_notation.replace("_", "-")
        self.input_entity.resource = self.input_entity.table_name.replace("_", "-")

    def parse_field(self, field):

        curr_field = {}

        curr_field["name"] = field.name
        if field.title:
            curr_field["title"] = field.title
        else:
            curr_field["title"] = field.name

        curr_field["inForm"] = True
        curr_field["inIndex"] = True
        curr_field["inView"] = True
        if field.in_form is False:
            curr_field["inForm"] = False

        if field.in_index is False:
            curr_field["inIndex"] = False

        if field.in_view is False:
            curr_field["inView"] = False

        # view type
        if field.view_type:
            if field.view_type.type:
                curr_field["front_type"] = field.view_type.type
                if field.view_type.type == "checkbox" and curr_field["inForm"] is True:
                    self.input_entity.check_boxes_fields.append(curr_field["name"])

                if curr_field["inForm"] is True:
                    if field.view_type.type == "img" or field.view_type.type == "image":
                        img_field = {}
                        img_field["name"] = curr_field["name"]
                        img_field["title"] = self.get_function_name_from_field(curr_field["name"])
                        self.input_entity.img_fields.append(img_field)
                        self.input_entity.hidden.append()

                if field.view_type.type == 'hidden':
                    self.input_entity.hidden.append(field.name)

            select_data = {}
            if field.view_type.enums:
                for item in field.view_type.enums:
                    select_data[item.value] = item.label
            curr_field["selected_data"] = select_data

        # Db Type
        unsigned = ''
        if field.db_type.unsigned is True:
            unsigned = 'unsigned'
        if field.db_type.default is not None:
            curr_field["default"] = field.db_type.default
        if field.db_type.foreign is not None:
            unsigned = 'unsigned'
            arr = {}
            arr["field_name"] = field.name
            arr["related_field"] = field.db_type.foreign.related_field
            arr["field_view"] = field.db_type.foreign.field_view
            arr["modelName"] = self.parsed_entities[field.db_type.foreign.related_entity].model_name
            table = self.parsed_entities[field.db_type.foreign.related_entity].table_name
            arr["table"] = table

            if p.singular_noun(table):
                arr["lowerModelName"] = p.singular_noun(table)
            else:
                arr["lowerModelName"] = arr["table"]
            arr["CapitalModelNamePlural"] = p.plural(arr["modelName"])

            curr_field["foreign"] = arr
            self.input_entity.foreign.append(arr)

        # dbType
        parts = field.db_type.type.split("|")
        extra_db_values = []
        for index, part in enumerate(parts):
            if index == 0:
                curr_field["type"] = part
                curr_field["dbtype"] = unsigned + part
            else:
                extra_db_values.append(part)

        curr_field["extraDbValues"] = extra_db_values
        if field.db_type.type == 'datetime' or field.db_type.type == 'date':
            self.input_entity.dates.append(field.name)

        z = self.parse_validation(field).copy()  # start with x's keys and values
        z.update(curr_field)

        col = Column.from_dict(z)
        self.input_entity.columns.append(col)

        if field.searchable is True:
            self.input_entity.searchable.append(field.name)
        if field.fillable is True:
            self.input_entity.fillable.append(field.name)
        if field.in_form is True:
            self.input_entity.in_form.append(field.name)
        if field.in_index is True:
            self.input_entity.in_index.append(field.name)
        if field.validations:
            self.input_entity.validations.append(field.name)

    def parse_extra_properities(self, prop):

        if prop.soft_delete is True:
            self.input_entity.has_soft_delete = True

        if prop.metable is True:
            self.input_entity.metable = True

        if prop.cachable is True:
            self.input_entity.cachable = True
        if prop.timestamp is True:
            self.input_entity.timestamp = True

        if prop.sluggable:
            self.input_entity.sluggable = prop.sluggable.split(",")

    def parse_other_data(self, entity):

        if entity.fields:
            for field in entity.fields:
                self.parse_field(field)
        if entity.extra_properties:
            self.parse_extra_properities(entity.extra_properties)

        if entity.generation:
            self.parse_generations(entity.generation)

        if entity.relations:
            for relation in entity.relations:
                self.parse_relation(relation)
        self.input_entity.relation_classes = self.get_relation_classes()
        self.input_entity.relation_names = self.get_relation_names()
        self.input_entity.relation_tables = self.get_relation_tables()
        self.input_entity.models_names = self.get_related_models_Names()
        self.input_entity.related_tables = self.get_related_tables()

    def parse_relation(self, relation):
        arr = {}
        arr["name"] = self.get_function_name_from_entity(relation.name)
        arr["related_table"] = self.parsed_entities[relation.relation.related_entity].table_name
        arr["related_model_name"] = self.parsed_entities[relation.relation.related_entity].model_name
        if p.singular_noun(arr["related_table"]):
            arr["related_class"] = p.singular_noun(arr["related_table"])
        else:
            arr["related_class"] = arr["related_table"]

        arr["related_model_name_plural"] = p.plural(arr["related_model_name"])
        arr["related_model_variable_name"] = arr["related_class"]
        arr["foreignKey"] = relation.relation.foreign_key

        arr["inForm"] = True
        arr["inIndex"] = True
        arr["inView"] = True
        if relation.in_form is False:
            arr["inForm"] = False

        if relation.in_index is False:
            arr["inIndex"] = False

        if relation.in_view is False:
            arr["inView"] = False

        if relation.relation.field_view:
            arr["field_view"] = relation.relation.field_view

        type = relation.relation.type
        if type == "1tm":
            arr["otherKey"] = "id"
            arr["localKey"] = "id"
            rel = RelElement.from_dict(arr)
            self.input_entity.relations.has_many.append(rel)
            # self._data["relations"]["hasMany"].append(arr)
            if not arr["related_table"] in self.input_entity.soft_delete_tables:
                soft_delete_data = {}
                soft_delete_data['name'] = arr["related_table"]
                soft_delete_data['modelName'] = arr["related_model_name"]
                soft_delete_data['foreignKey'] = arr["foreignKey"]
                soft_delete_data['otherKey'] = arr["otherKey"]
                soft_delete_data['relationName'] = self.get_function_name_from_table(arr["related_table"], "Cascade")
                obj = SoftDeleteDatum.from_dict(soft_delete_data)
                self.input_entity.soft_delete_data.append(obj)
                self.input_entity.soft_delete_tables.append(arr["related_table"])

        if type == "mtm":
            arr["otherKey"] = relation.relation.other_key
            arr["localKey"] = relation.relation.local_key
            arr["pivotFields"] = []
            if relation.relation.middle_entity in self.parsed_entities:
                if relation.relation.pivot_fields:
                    arr["pivotFields"] = relation.relation.pivot_fields
                arr["weakness"] = False

                arr["middleTable"] = self.parsed_entities[relation.relation.middle_entity].table_name
                arr["middleTableModel"] = self.parsed_entities[relation.relation.middle_entity].model_name

            else:
                arr["weakness"] = True
                arr["middleTable"] = self.get_table_name_from_entity(relation.relation.middle_entity)
                arr["middleTableModel"] = self.get_model_name_from_entity(relation.relation.middle_entity)

                # create empty entity
                f1 = {"name": relation.relation.foreign_key, "relatedEntity": self.input_entity.entity_name}
                f2 = {"name": relation.relation.other_key, "relatedEntity": relation.relation.related_entity}
                fields = [f1, f2]

                self.extra_entities.append(self.get_middle_entity(relation.relation.middle_entity, fields))

                self.input_entity.weakness_relation.append(arr)
                self.input_entity.weakness.append(arr['related_table'])
                self.input_entity.select_data.append('selected' + arr['related_model_name'])
            rel = RelElement.from_dict(arr)
            self.input_entity.relations.belongs_to_many.append(rel)
            if not arr["middleTable"] in self.input_entity.soft_delete_tables:
                soft_delete_data = {}
                soft_delete_data['name'] = arr["middleTable"]
                soft_delete_data['modelName'] = arr["middleTableModel"]
                soft_delete_data['foreignKey'] = arr["foreignKey"]
                soft_delete_data['otherKey'] = arr["otherKey"]
                soft_delete_data['relationName'] = self.get_function_name_from_table(arr["related_table"], "Cascade")

                obj = SoftDeleteDatum.from_dict(soft_delete_data)
                self.input_entity.soft_delete_data.append(obj)
                self.input_entity.soft_delete_tables.append(arr["middleTable"])

        # if type == "mt1":
        #     self._data["relations"]["belongsTo"].append(arr)

    def parse_generations(self, gen):

        if "model" in gen:
            self.input_entity.generation["generate_model"] = gen["model"]
        if "createEvent" in gen:
            self.input_entity.generation["generate_create_event"] = gen["createEvent"]
        if "updateEvent" in gen:
            self.input_entity.generation["generate_update_event"] = gen["updateEvent"]
        if "deleteEvent" in gen:
            self.input_entity.generation["generate_delete_event"] = gen["deleteEvent"]
        if "listener" in gen:
            self.input_entity.generation["generate_listener"] = gen["listener"]
        if "repository" in gen:
            self.input_entity.generation["generate_repository"] = gen["repository"]
        if "createTable" in gen:
            self.input_entity.generation["generate_table_migrate"] = gen["createTable"]
        if "migrateTable" in gen:
            self.input_entity.generation["generate_migrate"] = gen["migrateTable"]
        if "createRequest" in gen:
            self.input_entity.generation["generate_create_request"] = gen["createRequest"]
        if "updateRequest" in gen:
            self.input_entity.generation["generate_update_request"] = gen["updateRequest"]
        if "controller" in gen:
            self.input_entity.generation["generate_controller"] = gen["controller"]
        if "route" in gen:
            self.input_entity.generation["generate_route"] = gen["route"]
        if "breadcrumbs" in gen:
            self.input_entity.generation["generate_breadcrumbs"] = gen["breadcrumbs"]
        if "lang" in gen:
            self.input_entity.generation["generate_lang"] = gen["lang"]
        if "view" in gen:
            self.input_entity.generation["generate_view"] = gen["view"]
        if "apiCreateRequest" in gen:
            self.input_entity.generation["generate_api_create_request"] = gen["apiCreateRequest"]
        if "apiUpdateRequest" in gen:
            self.input_entity.generation["generate_api_update_request"] = gen["apiUpdateRequest"]
        if "apiController" in gen:
            self.input_entity.generation["generate_api_controller"] = gen["apiController"]
        if "apiRoute" in gen:
            self.input_entity.generation["generate_api_route"] = gen["apiRoute"]

    def get_middle_entity(self, entity_name, fields_arr):
        entity = {}
        entity["name"] = entity_name
        field_id = {
            "title": "Id",
            "name": "id",
            "dbType": {
                "type": "increments",
                "primary": True
            },
            "viewType": {},
            "searchable": False,
            "fillable": False,
            "inForm": False,
            "inIndex": False
        }
        entity["fields"] = [field_id]
        entity["relations"] = []
        for field in fields_arr:
            curr_field = {
                "title": "Name",
                "name": field["name"],
                "dbType": {
                    "type": "Integer",
                    "foreign": {
                        "relatedEntity": field["relatedEntity"],
                        "fieldView": "",
                        "relatedField": "id"
                    }
                },
                "viewType": {
                    "type": "text"
                },
                "validations": "required",
                "searchable": True,
                "fillable": True,
                "inForm": True,
                "inIndex": True
            }
            entity["fields"].append(curr_field)
        entity["extraProperties"] = {
            "softDelete": True,
            "metable": True,
            "cachable": True,
            "sluggable": ""
        }
        entity["generation"] = {
            "model": True,
            "createEvent": False,
            "updateEvent": False,
            "deleteEvent": False,
            "listener": False,
            "repository": False,
            "createTable": True,
            "migrateTable": False,
            "createRequest": False,
            "updateRequest": False,
            "controller": False,
            "route": False,
            "breadcrumbs": False,
            "lang": False,
            "view": False,
            "apiCreateRequest": False,
            "apiUpdateRequest": False,
            "apiController": False,
            "apiRoute": False
        }
        return entity

    def get_model_name_from_entity(self, entity_name):
        """
        use to calculate model name from entity name
        :param entity_name: name of entity
        :return: model name
        """
        model_name = ""
        parts = entity_name.split(" ")
        for part in parts:
            name = part.title()
            model_name = model_name + name

        return model_name

    def get_table_name_from_entity(self, entity_name):
        """
        use to calculate table name from entity name
        :param entity_name: name of entity
        :return: table name
        """
        model_name = self.get_model_name_from_entity(entity_name)
        return self.get_table_name_from_model(model_name)

    def get_function_name_from_entity(self, name):
        """
        use to calculate function name from entity name
        :param name: name of entity
        :return: function name
        """
        func_name = ""
        parts = name.split(" ")
        for index, part in enumerate(parts):

            if index == 0:
                name = part.lower()
            else:
                name = part.title()
            func_name = func_name + name

        return func_name

    def get_migrate_name_from_table(self, name):
        """
        use to calculate migrate name from table name
        :param name: name of entity
        :return: function name
        """
        mig_name = ""
        parts = name.split("_")
        for index, part in enumerate(parts):
            mig_name = mig_name + part.title()

        return mig_name

    def get_title_from_entity(self, entity_name):
        """
        use to calculate model plural from emtity name
        :param name: name of entity
        :return: function name
        """

        parts = entity_name.split(" ")
        length = len(parts)
        plural_model = ""
        for key, part in enumerate(parts):
            if key == length - 1:
                part = part.lower()
                name = p.plural(part)
                name = name.title()
            else:
                name = part.title()

            plural_model = plural_model + " " + name
        return plural_model

    def get_function_name_from_field(self, name, ):
        """
        use to calculate function name from field name
        :param name: name of entity
        :return: function name
        """
        func_name = ""
        parts = name.split("_")
        for part in parts:
            name = part.title()
            func_name = func_name + name
        return func_name

    def get_function_name_from_table(self, name, ext=None):
        """
        use to calculate function name from table name
        :param name: name of entity
        :return: function name
        """
        func_name = ""
        parts = name.split("_")
        for index, part in enumerate(parts):
            if index == 0:
                name = part.lower()
            else:
                name = part.title()
            func_name = func_name + name

        if ext:
            func_name = func_name + ext
        return func_name

    def get_model_name_from_table(self, table_name):

        table = table_name.split("_")
        model = ""
        for part in table:
            name = part.title()
            if p.singular_noun(name):
                name = p.singular_noun(name)
            model = model + name
        return model

    def get_table_name_from_model(self, model_name):
        """
          use to calculate table name from entity name
          :param entity_name: name of entity
          :return: table name
          """
        table = re.sub('([A-Z])', r'_\1', model_name).lower()
        table = table[1:]
        return p.plural(table)

    def get_relation_classes(self):

        ret_arr = []
        for key, element in self.input_entity.relations.__dict__.items():
            for item in element:
                if key == 'belongsTo':
                    ret_arr.append(item.related_class)

                if key == 'hasMany':
                    ret_arr.append(item.related_table)

        for item in self.input_entity.foreign:
            if not item['lowerModelName'] in ret_arr:
                ret_arr.append(item['lowerModelName'])

        return ret_arr

    def get_relation_names(self):

        ret_arr = []
        for key, element in self.input_entity.relations.__dict__.items():
            for item in element:
                if item.name not in ret_arr:
                    ret_arr.append(item.name)
        for item in self.input_entity.foreign:
            if not item['lowerModelName'] in ret_arr:
                ret_arr.append(item['lowerModelName'])

        return ret_arr

    def get_relation_tables(self):

        ret_arr = []
        for key, element in self.input_entity.relations.__dict__.items():
            for item in element:
                if key == 'belongsTo':
                    ret_arr.append(item.related_model_variable_name)

                if key == 'belongsToMany':
                    ret_arr.append(item.related_model_variable_name)
        for item in self.input_entity.foreign:
            if not item['lowerModelName'] in ret_arr:
                ret_arr.append(item['lowerModelName'])

        return ret_arr

    def get_related_models_Names(self):

        ret_arr = []
        for key, element in self.input_entity.relations.__dict__.items():
            for item in element:
                if key == 'belongsTo':
                    if item.related_model_name not in ret_arr:
                        ret_arr.append(item.related_model_name)
                if key == 'hasMany':
                    if item.related_model_name not in ret_arr:
                        ret_arr.append(item.related_model_name)

                if key == 'belongsToMany':
                    if item.related_model_name not in ret_arr:
                        ret_arr.append(item.related_model_name)
                    if item['middleTableModel'] not in ret_arr:
                        ret_arr.append(item['middleTableModel'])

        for item in self.input_entity.foreign:
            if not item['modelName'] in ret_arr:
                ret_arr.append(item['modelName'])

        return ret_arr

    def get_related_tables(self):

        ret_arr = []
        for key, element in self.input_entity.relations.__dict__.items():
            for item in element:
                if key == 'hasMany':
                    if item.related_table not in ret_arr:
                        ret_arr.append(item.related_table)

                if key == 'belongsToMany':
                    if item.related_table not in ret_arr:
                        ret_arr.append(item.related_table)

        return ret_arr

    def parse_validation(self, field):
        str = "nullable"
        ret_arr = {}
        if field.name == "id":
            return ret_arr

        ret_arr['serverStoreRules'] = {}
        ret_arr['serverUpdateRules'] = {}
        ret_arr['frontendRules'] = {}
        ret_arr['serverStoreRules']["type"] = ''

        ret_arr['serverStoreRules']['required'] = 'nullable'
        ret_arr['serverUpdateRules']['required'] = 'nullable'
        ret_arr['frontendRules']['required'] = 'nullable'

        if field.validations:
            str = field.validations
            data = field.validations.split("|")
            for elem in data:
                valid = elem.split(":")
                if valid[0] == 'required':
                    ret_arr['serverStoreRules']['required'] = 'required'
                    ret_arr['serverUpdateRules']['required'] = 'required'
                    ret_arr['frontendRules']['required'] = 'required'

                if valid[0] == 'min':
                    ret_arr['serverStoreRules']['min'] = valid[1]
                    ret_arr['serverUpdateRules']['min'] = valid[1]
                    ret_arr['frontendRules']['min'] = valid[1]

                if valid[0] == 'max':
                    ret_arr['serverStoreRules']['max'] = valid[1]
                    ret_arr['serverUpdateRules']['max'] = valid[1]
                    ret_arr['frontendRules']['max'] = valid[1]

                if valid[0] == 'email':
                    ret_arr['serverStoreRules']['email'] = True
                    ret_arr['serverUpdateRules']['email'] = True
                    ret_arr['frontendRules']['email'] = True
        ret_arr["validations"] = str

        return ret_arr
