import unittest

from validator_manager.manager import Manager


class TestServices(unittest.TestCase):
    def init_manager(self):
        self.manager = Manager()
        entity = {"name": "test"}
        self.manager.add_entity(entity)

    def init_manager_with_relations(self):
        self.manager = Manager()
        entity1 = {"name": "test",
                   "fields": [
                       {
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
                       },
                       {
                           "title": "Name",
                           "name": "name",
                           "dbType": {
                               "type": "string"
                           },
                           "viewType": {
                               "type": "text"
                           },
                           "validations": "required",
                           "searchable": True,
                       }]}
        entity2 = {"name": "test1",
                   "fields": [
                       {
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
                       },
                       {
                           "title": "Name",
                           "name": "name",
                           "dbType": {
                               "type": "string"
                           },
                           "viewType": {
                               "type": "text"
                           },
                           "validations": "required",
                           "searchable": True,
                       },
                       {
                           "title": "Test",
                           "name": "test_id",
                           "dbType": {
                               "type": "Integer",
                               "foreign": {
                                   "relatedEntity": "test",
                                   "fieldView": "name",
                                   "relatedField": "id"
                               }
                           },
                           "viewType": {
                               "type": "select"
                           },
                           "validations": "required"

                       }
                   ]}
        self.manager.add_entity(entity1)
        self.manager.add_entity(entity2)

    def test_add_entities(self):
        self.init_manager()
        entities = [{"name": "test1"}, {"name": "test2"}, {"name": "test3"}]
        self.manager.add_entities(entities)
        expected_result = {'entities': [{'name': 'test'}, {'name': 'test1'}, {'name': 'test2'}, {'name': 'test3'}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_entity(self):
        self.init_manager()
        entity = {"name": "test1"}
        self.manager.add_entity(entity)
        expected_result = {'entities': [{'name': 'test'}, {'name': 'test1'}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_entity_failure(self):
        self.init_manager()
        entity = {"name": "test"}
        self.manager.add_entity(entity)
        expected_result = {'entities': [{'name': 'test'}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertFalse(self.manager.get_status())

    def test_update_entity(self):
        self.init_manager()
        entity = {"name": "test1"}
        self.manager.update_entity("test", entity)
        expected_result = {'entities': [{'name': 'test1'}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_delete_entity(self):
        self.init_manager()
        self.manager.delete_entity("test")
        expected_result = {'entities': []}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_field(self):
        self.init_manager()
        field = {"name": "field1", "dbType": {"type": "integer"}}
        self.manager.add_field("test", field)
        expected_result = {
            'entities': [{'name': 'test', 'fields': [{'name': 'field1', 'dbType': {'type': 'integer'}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_field_failure(self):
        self.init_manager()
        field = {"name": "field1", "dbType": {"type": "integer"}}
        self.manager.add_field("test", field)
        self.manager.add_field("test", field)
        expected_result = {
            'entities': [{'name': 'test', 'fields': [{'name': 'field1', 'dbType': {'type': 'integer'}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertFalse(self.manager.get_status())

    def test_update_field(self):
        self.init_manager()
        field = {"name": "field1", "dbType": {"type": "integer"}}
        self.manager.add_field("test", field)
        field2 = {"name": "field1", "dbType": {"type": "Integer"}}
        self.manager.update_field("test", "field1", field2)
        expected_result = {
            'entities': [{'name': 'test', 'fields': [{'name': 'field1', 'dbType': {'type': 'Integer'}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_delete_field(self):
        self.init_manager()
        field = {"name": "field1", "dbType": {"type": "integer"}}
        self.manager.add_field("test", field)
        self.manager.delete_field("test", "field1")
        expected_result = {'entities': [{'name': 'test', 'fields': []}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_db_type(self):
        self.init_manager()
        field = {"name": "id", "dbType": {"type": "bigIncrements"}}
        self.manager.add_field("test", field)

        db_type = {"type": "increments", "primary": True}
        self.manager.add_db_type("test", "id", db_type)
        expected_result = {'entities': [
            {'name': 'test', 'fields': [{'name': 'id', 'dbType': {'type': 'increments', 'primary': True}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_view_type(self):
        self.init_manager()
        field = {"name": "id", "dbType": {"type": "increments"}, "viewType": {"type": "Integer"}}
        self.manager.add_field("test", field)

        view_type = {"type": "integer"}
        self.manager.add_view_type("test", "id", view_type)
        expected_result = {'entities': [{'name': 'test', 'fields': [
            {'name': 'id', 'dbType': {'type': 'increments'}, 'viewType': {'type': 'integer'}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

        self.manager.add_view_type("test", "id")
        expected_result = {'entities': [{'name': 'test', 'fields': [
            {'name': 'id', 'dbType': {'type': 'increments'}, 'viewType': {}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_view_type_failure(self):
        self.init_manager()
        field = {"name": "field", "dbType": {"type": "Integer"}, "viewType": {"type": "Integer"}}
        self.manager.add_field("test", field)

        self.manager.add_view_type("test", "field")
        expected_result = {'entities': [{'name': 'test', 'fields': [
            {'name': 'field', 'dbType': {'type': 'Integer'}, 'viewType': {'type': 'Integer'}}]}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertFalse(self.manager.get_status())

    def test_add_relation(self):
        self.init_manager_with_relations()
        relation = {
            "name": "relation1",
            "type": "relation",
            "relation": {
                "type": "1tm",
                "fieldView": "name",
                "relatedEntity": "test1",
                "foreignKey": "test_id",
            },
            "inForm": True,
            "inView": True,
            "inIndex": True
        }
        self.manager.add_relation("test", relation)
        self.assertTrue(self.manager.get_status())

    def test_add_relation_failure(self):
        self.init_manager()
        relation = {
            "name": "relation1",
            "type": "relation",
            "relation": {
                "type": "1tm",
                "fieldView": "name",
                "relatedEntity": "test1",
                "foreignKey": "test1_id",
            },
            "inForm": True,
            "inView": True,
            "inIndex": True
        }
        self.manager.add_relation("test", relation)
        expected_result = {'entities': [{'name': 'test'}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertFalse(self.manager.get_status())

    def test_update_relation(self):
        self.init_manager_with_relations()
        relation = {
            "name": "relation1",
            "type": "relation",
            "relation": {
                "type": "1tm",
                "fieldView": "name",
                "relatedEntity": "test1",
                "foreignKey": "test_id",
            },
            "inForm": True,
            "inView": True,
            "inIndex": True
        }
        self.manager.add_relation("test", relation)
        new_relation = {
            "name": "relation2",
            "type": "relation",
            "relation": {
                "type": "1tm",
                "fieldView": "name",
                "relatedEntity": "test1",
                "foreignKey": "test_id",
            },
            "inForm": True,
            "inView": True,
            "inIndex": True
        }
        self.manager.update_relation("test", "relation1", new_relation)
        self.assertTrue(self.manager.get_status())

    def test_delete_relation(self):
        self.init_manager_with_relations()
        relation = {
            "name": "relation1",
            "type": "relation",
            "relation": {
                "type": "1tm",
                "fieldView": "name",
                "relatedEntity": "test1",
                "foreignKey": "test_id",
            },
            "inForm": True,
            "inView": True,
            "inIndex": True
        }
        self.manager.add_relation("test", relation)
        self.manager.delete_relation("test", "relation1")
        self.assertTrue(self.manager.get_status())

    def test_add_extra_properties(self):
        self.init_manager()
        extra_properties = {
            "softDelete": True,
            "timestamp": True
        }
        self.manager.add_extra_properties("test", extra_properties)
        expected_result = {'entities': [{'name': 'test', 'extraProperties': {'softDelete': True, 'timestamp': True}}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())
        self.manager.add_extra_properties("test")
        expected_result = {'entities': [{'name': 'test', 'extraProperties': {}}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())

    def test_add_generation(self):
        self.init_manager()
        generation = {
            "model": False,
            "controller": False
        }
        self.manager.add_generation("test", generation)
        expected_result = {'entities': [{'name': 'test', 'generation': {'model': False, 'controller': False}}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())
        self.manager.add_generation("test")
        expected_result = {'entities': [{'name': 'test', 'generation': {}}]}
        self.assertDictEqual(self.manager.get_config_dict(), expected_result)
        self.assertTrue(self.manager.get_status())
