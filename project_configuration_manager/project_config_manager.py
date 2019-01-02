from typing import Optional, Any, Union, List, Dict, TypeVar, Type, cast, Callable

T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


class Rules:
    required: Optional[str]

    def __init__(self, required: Optional[str]) -> None:
        self.required = required

    @staticmethod
    def from_dict(obj: Any) -> 'Rules':
        assert isinstance(obj, dict)
        required = from_union([from_str, from_none], obj.get("required"))
        return Rules(required)

    def to_dict(self) -> dict:
        result: dict = {}
        result["required"] = from_union([from_str, from_none], self.required)
        return result


class SelectedData:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'SelectedData':
        assert isinstance(obj, dict)
        return SelectedData()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class ServerStoreRules:
    required: Optional[str]
    type: Optional[str]

    def __init__(self, required: Optional[str], type: Optional[str]) -> None:
        self.required = required
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'ServerStoreRules':
        assert isinstance(obj, dict)
        required = from_union([from_str, from_none], obj.get("required"))
        type = from_union([from_str, from_none], obj.get("type"))
        return ServerStoreRules(required, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["required"] = from_union([from_str, from_none], self.required)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


class Column:
    name: Optional[str]
    title: Optional[str]
    in_form: Optional[bool]
    in_index: Optional[bool]
    in_view: Optional[bool]
    selected_data: Optional[SelectedData]
    type: Optional[str]
    dbtype: Optional[str]
    extra_db_values: Optional[List[Any]]
    server_store_rules: Optional[ServerStoreRules]
    server_update_rules: Optional[Rules]
    frontend_rules: Optional[Rules]
    validations: Optional[str]
    front_type: Optional[str]
    foreign: Optional[Any]

    def __init__(self, name: Optional[str], title: Optional[str], in_form: Optional[bool], in_index: Optional[bool],
                 in_view: Optional[bool], selected_data: Optional[SelectedData], type: Optional[str],
                 dbtype: Optional[str], extra_db_values: Optional[List[Any]],
                 server_store_rules: Optional[ServerStoreRules], server_update_rules: Optional[Rules],
                 frontend_rules: Optional[Rules], validations: Optional[str], front_type: Optional[str],
                 foreign: Optional[Any]) -> None:
        self.name = name
        self.title = title
        self.in_form = in_form
        self.in_index = in_index
        self.in_view = in_view
        self.selected_data = selected_data
        self.type = type
        self.dbtype = dbtype
        self.extra_db_values = extra_db_values
        self.server_store_rules = server_store_rules
        self.server_update_rules = server_update_rules
        self.frontend_rules = frontend_rules
        self.validations = validations
        self.front_type = front_type
        self.foreign = foreign

    @staticmethod
    def from_dict(obj: Any) -> 'Column':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        title = from_union([from_str, from_none], obj.get("title"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        selected_data = from_union([SelectedData.from_dict, from_none], obj.get("selected_data"))
        type = from_union([from_str, from_none], obj.get("type"))
        dbtype = from_union([from_str, from_none], obj.get("dbtype"))
        extra_db_values = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("extraDbValues"))
        server_store_rules = from_union([ServerStoreRules.from_dict, from_none], obj.get("serverStoreRules"))
        server_update_rules = from_union([Rules.from_dict, from_none], obj.get("serverUpdateRules"))
        frontend_rules = from_union([Rules.from_dict, from_none], obj.get("frontendRules"))
        validations = from_union([from_str, from_none], obj.get("validations"))
        front_type = from_union([from_str, from_none], obj.get("front_type"))
        foreign = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("foreign"))
        return Column(name, title, in_form, in_index, in_view, selected_data, type, dbtype, extra_db_values,
                      server_store_rules, server_update_rules, frontend_rules, validations, front_type, foreign)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["title"] = from_union([from_str, from_none], self.title)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["selected_data"] = from_union([lambda x: to_class(SelectedData, x), from_none], self.selected_data)
        result["type"] = from_union([from_str, from_none], self.type)
        result["dbtype"] = from_union([from_str, from_none], self.dbtype)
        result["extraDbValues"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.extra_db_values)
        result["serverStoreRules"] = from_union([lambda x: to_class(ServerStoreRules, x), from_none],
                                                self.server_store_rules)
        result["serverUpdateRules"] = from_union([lambda x: to_class(Rules, x), from_none], self.server_update_rules)
        result["frontendRules"] = from_union([lambda x: to_class(Rules, x), from_none], self.frontend_rules)
        result["validations"] = from_union([from_str, from_none], self.validations)
        result["front_type"] = from_union([from_str, from_none], self.front_type)
        result["foreign"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.foreign)
        return result


class Paths:
    model: Optional[str]
    create_event: Optional[str]
    update_event: Optional[str]
    delete_event: Optional[str]
    listener: Optional[str]
    repository: Optional[str]
    migrate: Optional[str]
    create_request: Optional[str]
    update_request: Optional[str]
    controller: Optional[str]
    route: Optional[str]
    breadcrumbs: Optional[str]
    lang: Optional[str]
    view: Optional[str]
    api_create_request: Optional[str]
    api_update_request: Optional[str]
    api_controller: Optional[str]
    api_route: Optional[str]

    def __init__(self, model: Optional[str], create_event: Optional[str], update_event: Optional[str],
                 delete_event: Optional[str], listener: Optional[str], repository: Optional[str],
                 migrate: Optional[str], create_request: Optional[str], update_request: Optional[str],
                 controller: Optional[str], route: Optional[str], breadcrumbs: Optional[str], lang: Optional[str],
                 view: Optional[str], api_create_request: Optional[str], api_update_request: Optional[str],
                 api_controller: Optional[str], api_route: Optional[str]) -> None:
        self.model = model
        self.create_event = create_event
        self.update_event = update_event
        self.delete_event = delete_event
        self.listener = listener
        self.repository = repository
        self.migrate = migrate
        self.create_request = create_request
        self.update_request = update_request
        self.controller = controller
        self.route = route
        self.breadcrumbs = breadcrumbs
        self.lang = lang
        self.view = view
        self.api_create_request = api_create_request
        self.api_update_request = api_update_request
        self.api_controller = api_controller
        self.api_route = api_route

    @staticmethod
    def from_dict(obj: Any) -> 'Paths':
        assert isinstance(obj, dict)
        model = from_union([from_str, from_none], obj.get("model"))
        create_event = from_union([from_str, from_none], obj.get("createEvent"))
        update_event = from_union([from_str, from_none], obj.get("updateEvent"))
        delete_event = from_union([from_str, from_none], obj.get("deleteEvent"))
        listener = from_union([from_str, from_none], obj.get("listener"))
        repository = from_union([from_str, from_none], obj.get("repository"))
        migrate = from_union([from_str, from_none], obj.get("migrate"))
        create_request = from_union([from_str, from_none], obj.get("createRequest"))
        update_request = from_union([from_str, from_none], obj.get("updateRequest"))
        controller = from_union([from_str, from_none], obj.get("controller"))
        route = from_union([from_str, from_none], obj.get("route"))
        breadcrumbs = from_union([from_str, from_none], obj.get("breadcrumbs"))
        lang = from_union([from_str, from_none], obj.get("lang"))
        view = from_union([from_str, from_none], obj.get("view"))
        api_create_request = from_union([from_str, from_none], obj.get("APICreateRequest"))
        api_update_request = from_union([from_str, from_none], obj.get("APIUpdateRequest"))
        api_controller = from_union([from_str, from_none], obj.get("APIController"))
        api_route = from_union([from_str, from_none], obj.get("APIRoute"))
        return Paths(model, create_event, update_event, delete_event, listener, repository, migrate, create_request,
                     update_request, controller, route, breadcrumbs, lang, view, api_create_request, api_update_request,
                     api_controller, api_route)

    def to_dict(self) -> dict:
        result: dict = {}
        result["model"] = from_union([from_str, from_none], self.model)
        result["createEvent"] = from_union([from_str, from_none], self.create_event)
        result["updateEvent"] = from_union([from_str, from_none], self.update_event)
        result["deleteEvent"] = from_union([from_str, from_none], self.delete_event)
        result["listener"] = from_union([from_str, from_none], self.listener)
        result["repository"] = from_union([from_str, from_none], self.repository)
        result["migrate"] = from_union([from_str, from_none], self.migrate)
        result["createRequest"] = from_union([from_str, from_none], self.create_request)
        result["updateRequest"] = from_union([from_str, from_none], self.update_request)
        result["controller"] = from_union([from_str, from_none], self.controller)
        result["route"] = from_union([from_str, from_none], self.route)
        result["breadcrumbs"] = from_union([from_str, from_none], self.breadcrumbs)
        result["lang"] = from_union([from_str, from_none], self.lang)
        result["view"] = from_union([from_str, from_none], self.view)
        result["APICreateRequest"] = from_union([from_str, from_none], self.api_create_request)
        result["APIUpdateRequest"] = from_union([from_str, from_none], self.api_update_request)
        result["APIController"] = from_union([from_str, from_none], self.api_controller)
        result["APIRoute"] = from_union([from_str, from_none], self.api_route)
        return result


class RelationElement1111:
    name: Optional[str]
    related_table: Optional[str]
    related_model_name: Optional[str]
    related_class: Optional[str]
    related_model_name_plural: Optional[str]
    related_model_variable_name: Optional[str]
    foreign_key: Optional[str]
    in_form: Optional[bool]
    in_index: Optional[bool]
    in_view: Optional[bool]
    field_view: Optional[str]
    other_key: Optional[str]
    local_key: Optional[str]
    pivot_fields: Optional[List[str]]
    weakness: Optional[bool]
    middle_table: Optional[str]
    middle_table_model: Optional[str]

    def __init__(self, name: Optional[str], related_table: Optional[str], related_model_name: Optional[str],
                 related_class: Optional[str], related_model_name_plural: Optional[str],
                 related_model_variable_name: Optional[str], foreign_key: Optional[str], in_form: Optional[bool],
                 in_index: Optional[bool], in_view: Optional[bool], field_view: Optional[str], other_key: Optional[str],
                 local_key: Optional[str], pivot_fields: Optional[List[str]], weakness: Optional[bool],
                 middle_table: Optional[str], middle_table_model: Optional[str]) -> None:
        self.name = name
        self.related_table = related_table
        self.related_model_name = related_model_name
        self.related_class = related_class
        self.related_model_name_plural = related_model_name_plural
        self.related_model_variable_name = related_model_variable_name
        self.foreign_key = foreign_key
        self.in_form = in_form
        self.in_index = in_index
        self.in_view = in_view
        self.field_view = field_view
        self.other_key = other_key
        self.local_key = local_key
        self.pivot_fields = pivot_fields
        self.weakness = weakness
        self.middle_table = middle_table
        self.middle_table_model = middle_table_model

    @staticmethod
    def from_dict(obj: Any) -> 'RelationElement':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        related_table = from_union([from_str, from_none], obj.get("related_table"))
        related_model_name = from_union([from_str, from_none], obj.get("related_model_name"))
        related_class = from_union([from_str, from_none], obj.get("related_class"))
        related_model_name_plural = from_union([from_str, from_none], obj.get("related_model_name_plural"))
        related_model_variable_name = from_union([from_str, from_none], obj.get("related_model_variable_name"))
        foreign_key = from_union([from_str, from_none], obj.get("foreignKey"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        field_view = from_union([from_str, from_none], obj.get("field_view"))
        other_key = from_union([from_str, from_none], obj.get("otherKey"))
        local_key = from_union([from_str, from_none], obj.get("localKey"))
        pivot_fields = from_union([lambda x: from_list(from_str, x), from_none], obj.get("pivotFields"))
        weakness = from_union([from_bool, from_none], obj.get("weakness"))
        middle_table = from_union([from_str, from_none], obj.get("middleTable"))
        middle_table_model = from_union([from_str, from_none], obj.get("middleTableModel"))
        return RelationElement(name, related_table, related_model_name, related_class, related_model_name_plural,
                               related_model_variable_name, foreign_key, in_form, in_index, in_view, field_view,
                               other_key, local_key, pivot_fields, weakness, middle_table, middle_table_model)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["related_table"] = from_union([from_str, from_none], self.related_table)
        result["related_model_name"] = from_union([from_str, from_none], self.related_model_name)
        result["related_class"] = from_union([from_str, from_none], self.related_class)
        result["related_model_name_plural"] = from_union([from_str, from_none], self.related_model_name_plural)
        result["related_model_variable_name"] = from_union([from_str, from_none], self.related_model_variable_name)
        result["foreignKey"] = from_union([from_str, from_none], self.foreign_key)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["field_view"] = from_union([from_str, from_none], self.field_view)
        result["otherKey"] = from_union([from_str, from_none], self.other_key)
        result["localKey"] = from_union([from_str, from_none], self.local_key)
        result["pivotFields"] = from_union([lambda x: from_list(from_str, x), from_none], self.pivot_fields)
        result["weakness"] = from_union([from_bool, from_none], self.weakness)
        result["middleTable"] = from_union([from_str, from_none], self.middle_table)
        result["middleTableModel"] = from_union([from_str, from_none], self.middle_table_model)
        return result


class RelElement:
    name: Optional[str]
    related_table: Optional[str]
    related_model_name: Optional[str]
    related_class: Optional[str]
    related_model_name_plural: Optional[str]
    related_model_variable_name: Optional[str]
    foreign_key: Optional[str]
    in_form: Optional[bool]
    in_index: Optional[bool]
    in_view: Optional[bool]
    field_view: Optional[str]
    other_key: Optional[str]
    local_key: Optional[str]
    pivot_fields: Optional[List[str]]
    weakness: Optional[bool]
    middle_table: Optional[str]
    middle_table_model: Optional[str]

    def __init__(self, name: Optional[str], related_table: Optional[str], related_model_name: Optional[str],
                 related_class: Optional[str], related_model_name_plural: Optional[str],
                 related_model_variable_name: Optional[str], foreign_key: Optional[str], in_form: Optional[bool],
                 in_index: Optional[bool], in_view: Optional[bool], field_view: Optional[str], other_key: Optional[str],
                 local_key: Optional[str], pivot_fields: Optional[List[str]], weakness: Optional[bool],
                 middle_table: Optional[str], middle_table_model: Optional[str]) -> None:
        self.name = name
        self.related_table = related_table
        self.related_model_name = related_model_name
        self.related_class = related_class
        self.related_model_name_plural = related_model_name_plural
        self.related_model_variable_name = related_model_variable_name
        self.foreign_key = foreign_key
        self.in_form = in_form
        self.in_index = in_index
        self.in_view = in_view
        self.field_view = field_view
        self.other_key = other_key
        self.local_key = local_key
        self.pivot_fields = pivot_fields
        self.weakness = weakness
        self.middle_table = middle_table
        self.middle_table_model = middle_table_model

    @staticmethod
    def from_dict(obj: Any) -> 'RelElement':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        related_table = from_union([from_str, from_none], obj.get("related_table"))
        related_model_name = from_union([from_str, from_none], obj.get("related_model_name"))
        related_class = from_union([from_str, from_none], obj.get("related_class"))
        related_model_name_plural = from_union([from_str, from_none], obj.get("related_model_name_plural"))
        related_model_variable_name = from_union([from_str, from_none], obj.get("related_model_variable_name"))
        foreign_key = from_union([from_str, from_none], obj.get("foreignKey"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        field_view = from_union([from_str, from_none], obj.get("field_view"))
        other_key = from_union([from_str, from_none], obj.get("otherKey"))
        local_key = from_union([from_str, from_none], obj.get("localKey"))
        pivot_fields = from_union([lambda x: from_list(from_str, x), from_none], obj.get("pivotFields"))
        weakness = from_union([from_bool, from_none], obj.get("weakness"))
        middle_table = from_union([from_str, from_none], obj.get("middleTable"))
        middle_table_model = from_union([from_str, from_none], obj.get("middleTableModel"))
        return RelElement(name, related_table, related_model_name, related_class, related_model_name_plural,
                          related_model_variable_name, foreign_key, in_form, in_index, in_view, field_view, other_key,
                          local_key, pivot_fields, weakness, middle_table, middle_table_model)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["related_table"] = from_union([from_str, from_none], self.related_table)
        result["related_model_name"] = from_union([from_str, from_none], self.related_model_name)
        result["related_class"] = from_union([from_str, from_none], self.related_class)
        result["related_model_name_plural"] = from_union([from_str, from_none], self.related_model_name_plural)
        result["related_model_variable_name"] = from_union([from_str, from_none], self.related_model_variable_name)
        result["foreignKey"] = from_union([from_str, from_none], self.foreign_key)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["field_view"] = from_union([from_str, from_none], self.field_view)
        result["otherKey"] = from_union([from_str, from_none], self.other_key)
        result["localKey"] = from_union([from_str, from_none], self.local_key)
        result["pivotFields"] = from_union([lambda x: from_list(from_str, x), from_none], self.pivot_fields)
        result["weakness"] = from_union([from_bool, from_none], self.weakness)
        result["middleTable"] = from_union([from_str, from_none], self.middle_table)
        result["middleTableModel"] = from_union([from_str, from_none], self.middle_table_model)
        return result


class Relations:
    belongs_to_many: Optional[List[RelElement]]
    belongs_to: Optional[List[RelElement]]
    has_many: Optional[List[RelElement]]

    def __init__(self, belongs_to_many: Optional[List[RelElement]], belongs_to: Optional[List[RelElement]],
                 has_many: Optional[List[RelElement]]) -> None:
        self.belongs_to_many = belongs_to_many
        self.belongs_to = belongs_to
        self.has_many = has_many

    @staticmethod
    def from_dict(obj: Any) -> 'Relations':
        assert isinstance(obj, dict)
        belongs_to_many = from_union([lambda x: from_list(RelElement.from_dict, x), from_none],
                                     obj.get("belongsToMany"))
        belongs_to = from_union([lambda x: from_list(RelElement.from_dict, x), from_none], obj.get("belongsTo"))
        has_many = from_union([lambda x: from_list(RelElement.from_dict, x), from_none], obj.get("hasMany"))
        return Relations(belongs_to_many, belongs_to, has_many)

    def to_dict(self) -> dict:
        result: dict = {}
        result["belongsToMany"] = from_union([lambda x: from_list(lambda x: to_class(RelElement, x), x), from_none],
                                             self.belongs_to_many)
        result["belongsTo"] = from_union([lambda x: from_list(lambda x: to_class(RelElement, x), x), from_none],
                                         self.belongs_to)
        result["hasMany"] = from_union([lambda x: from_list(lambda x: to_class(RelElement, x), x), from_none],
                                       self.has_many)
        return result


class SoftDeleteDatum:
    name: Optional[str]
    model_name: Optional[str]
    foreign_key: Optional[str]
    other_key: Optional[str]
    relation_name: Optional[str]

    def __init__(self, name: Optional[str], model_name: Optional[str], foreign_key: Optional[str],
                 other_key: Optional[str], relation_name: Optional[str]) -> None:
        self.name = name
        self.model_name = model_name
        self.foreign_key = foreign_key
        self.other_key = other_key
        self.relation_name = relation_name

    @staticmethod
    def from_dict(obj: Any) -> 'SoftDeleteDatum':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        model_name = from_union([from_str, from_none], obj.get("modelName"))
        foreign_key = from_union([from_str, from_none], obj.get("foreignKey"))
        other_key = from_union([from_str, from_none], obj.get("otherKey"))
        relation_name = from_union([from_str, from_none], obj.get("relationName"))
        return SoftDeleteDatum(name, model_name, foreign_key, other_key, relation_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["modelName"] = from_union([from_str, from_none], self.model_name)
        result["foreignKey"] = from_union([from_str, from_none], self.foreign_key)
        result["otherKey"] = from_union([from_str, from_none], self.other_key)
        result["relationName"] = from_union([from_str, from_none], self.relation_name)
        return result


class InputEntity:
    searchable: Optional[List[str]]
    fillable: Optional[List[str]]
    in_form: Optional[List[str]]
    in_index: Optional[List[str]]
    validations: Optional[List[Any]]
    hidden: Optional[List[Any]]
    translatable: Optional[List[Any]]
    timestamps: Optional[List[Any]]
    dates: Optional[List[Any]]
    columns: Optional[List[Column]]
    foreign: Optional[List[Any]]
    unique: Optional[List[Any]]
    generation: Optional[Dict[str, bool]]
    soft_delete_tables: Optional[List[str]]
    soft_delete_data: Optional[List[SoftDeleteDatum]]
    check_boxes_fields: Optional[List[Any]]
    img_fields: Optional[List[Any]]
    relations: Optional[Relations]
    has_soft_delete: Optional[bool]
    timestamp: Optional[bool]
    cachable: Optional[bool]
    metable: Optional[bool]
    sluggable: Optional[List[Any]]
    relation_classes: Optional[List[Any]]
    relation_tables: Optional[List[str]]
    models_names: Optional[List[str]]
    weakness: Optional[List[Any]]
    weakness_relation: Optional[List[Any]]
    select_data: Optional[List[Any]]
    entity_name: Optional[str]
    model_name: Optional[str]
    table_name: Optional[str]
    model_base_name: Optional[str]
    model_plural: Optional[str]
    migrate_name: Optional[str]
    title: Optional[str]
    model_variable: Optional[str]
    model_dot_notation: Optional[str]
    model_dash_variable: Optional[str]
    resource: Optional[str]
    relation_names: Optional[List[str]]
    related_tables: Optional[List[str]]
    paths: Optional[Paths]

    def __init__(self, searchable: Optional[List[str]], fillable: Optional[List[str]], in_form: Optional[List[str]],
                 in_index: Optional[List[str]], validations: Optional[List[Any]], hidden: Optional[List[Any]],
                 translatable: Optional[List[Any]], timestamps: Optional[List[Any]], dates: Optional[List[Any]],
                 columns: Optional[List[Column]], foreign: Optional[List[Any]],
                 unique: Optional[List[Any]], generation: Optional[Dict[str, bool]],
                 soft_delete_tables: Optional[List[str]], soft_delete_data: Optional[List[SoftDeleteDatum]],
                 check_boxes_fields: Optional[List[Any]], img_fields: Optional[List[Any]],
                 relations: Optional[Relations], has_soft_delete: Optional[bool], timestamp: Optional[bool],
                 cachable: Optional[bool], metable: Optional[bool], sluggable: Optional[List[Any]],
                 relation_classes: Optional[List[Any]], relation_tables: Optional[List[str]],
                 models_names: Optional[List[str]], weakness: Optional[List[Any]],
                 weakness_relation: Optional[List[Any]], select_data: Optional[List[Any]], entity_name: Optional[str],
                 model_name: Optional[str], table_name: Optional[str], model_base_name: Optional[str],
                 model_plural: Optional[str], migrate_name: Optional[str], title: Optional[str],
                 model_variable: Optional[str], model_dot_notation: Optional[str], model_dash_variable: Optional[str],
                 resource: Optional[str], relation_names: Optional[List[str]], related_tables: Optional[List[str]],
                 paths: Optional[Paths]) -> None:
        self.searchable = searchable
        self.fillable = fillable
        self.in_form = in_form
        self.in_index = in_index
        self.validations = validations
        self.hidden = hidden
        self.translatable = translatable
        self.timestamps = timestamps
        self.dates = dates
        self.columns = columns
        self.foreign = foreign
        self.unique = unique
        self.generation = generation
        self.soft_delete_tables = soft_delete_tables
        self.soft_delete_data = soft_delete_data
        self.check_boxes_fields = check_boxes_fields
        self.img_fields = img_fields
        self.relations = relations
        self.has_soft_delete = has_soft_delete
        self.timestamp = timestamp
        self.cachable = cachable
        self.metable = metable
        self.sluggable = sluggable
        self.relation_classes = relation_classes
        self.relation_tables = relation_tables
        self.models_names = models_names
        self.weakness = weakness
        self.weakness_relation = weakness_relation
        self.select_data = select_data
        self.entity_name = entity_name
        self.model_name = model_name
        self.table_name = table_name
        self.model_base_name = model_base_name
        self.model_plural = model_plural
        self.migrate_name = migrate_name
        self.title = title
        self.model_variable = model_variable
        self.model_dot_notation = model_dot_notation
        self.model_dash_variable = model_dash_variable
        self.resource = resource

        self.relation_names = relation_names
        self.related_tables = related_tables
        self.paths = paths

    @staticmethod
    def from_dict(obj: Any) -> 'InputEntity':
        assert isinstance(obj, dict)
        searchable = from_union([lambda x: from_list(from_str, x), from_none], obj.get("searchable"))
        fillable = from_union([lambda x: from_list(from_str, x), from_none], obj.get("fillable"))
        in_form = from_union([lambda x: from_list(from_str, x), from_none], obj.get("inForm"))
        in_index = from_union([lambda x: from_list(from_str, x), from_none], obj.get("inIndex"))
        validations = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("validations"))
        hidden = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("hidden"))
        translatable = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("translatable"))
        timestamps = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("timestamps"))
        dates = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("dates"))
        columns = from_union([lambda x: from_list(Column.from_dict, x), from_none], obj.get("columns"))
        foreign = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("foreign"))
        unique = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("unique"))
        generation = from_union([lambda x: from_dict(from_bool, x), from_none], obj.get("generation"))
        soft_delete_tables = from_union([lambda x: from_list(from_str, x), from_none], obj.get("softDeleteTables"))
        soft_delete_data = from_union([lambda x: from_list(SoftDeleteDatum.from_dict, x), from_none],
                                      obj.get("softDeleteData"))
        check_boxes_fields = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("checkBoxesFields"))
        img_fields = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("imgFields"))
        relations = from_union([Relations.from_dict, from_none], obj.get("relations"))
        has_soft_delete = from_union([from_bool, from_none], obj.get("hasSoftDelete"))
        timestamp = from_union([from_bool, from_none], obj.get("timestamp"))
        cachable = from_union([from_bool, from_none], obj.get("cachable"))
        metable = from_union([from_bool, from_none], obj.get("metable"))
        sluggable = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("sluggable"))
        relation_classes = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("relationClasses"))
        relation_tables = from_union([lambda x: from_list(from_str, x), from_none], obj.get("relationTables"))
        models_names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("modelsNames"))
        weakness = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("weakness"))
        weakness_relation = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("weaknessRelation"))
        select_data = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("selectData"))
        entity_name = from_union([from_str, from_none], obj.get("entityName"))
        model_name = from_union([from_str, from_none], obj.get("modelName"))
        table_name = from_union([from_str, from_none], obj.get("tableName"))
        model_base_name = from_union([from_str, from_none], obj.get("modelBaseName"))
        model_plural = from_union([from_str, from_none], obj.get("modelPlural"))
        migrate_name = from_union([from_str, from_none], obj.get("migrateName"))
        title = from_union([from_str, from_none], obj.get("title"))
        model_variable = from_union([from_str, from_none], obj.get("modelVariable"))
        model_dot_notation = from_union([from_str, from_none], obj.get("modelDotNotation"))
        model_dash_variable = from_union([from_str, from_none], obj.get("modelDashVariable"))
        resource = from_union([from_str, from_none], obj.get("resource"))
        relation_names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("relationNames"))
        related_tables = from_union([lambda x: from_list(from_str, x), from_none], obj.get("relatedTables"))
        paths = from_union([Paths.from_dict, from_none], obj.get("paths"))
        return InputEntity(searchable, fillable, in_form, in_index, validations, hidden, translatable, timestamps,
                           dates, columns, foreign, unique, generation, soft_delete_tables,
                           soft_delete_data, check_boxes_fields, img_fields, relations, has_soft_delete, timestamp,
                           cachable, metable, sluggable, relation_classes, relation_tables, models_names, weakness,
                           weakness_relation, select_data, entity_name, model_name, table_name, model_base_name,
                           model_plural, migrate_name, title, model_variable, model_dot_notation, model_dash_variable,
                           resource, relation_names, related_tables, paths)

    def to_dict(self) -> dict:
        result: dict = {}
        result["searchable"] = from_union([lambda x: from_list(from_str, x), from_none], self.searchable)
        result["fillable"] = from_union([lambda x: from_list(from_str, x), from_none], self.fillable)
        result["inForm"] = from_union([lambda x: from_list(from_str, x), from_none], self.in_form)
        result["inIndex"] = from_union([lambda x: from_list(from_str, x), from_none], self.in_index)
        result["validations"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.validations)
        result["hidden"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.hidden)
        result["translatable"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.translatable)
        result["timestamps"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.timestamps)
        result["dates"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.dates)
        result["columns"] = from_union([lambda x: from_list(lambda x: to_class(Column, x), x), from_none], self.columns)
        result["foreign"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.foreign)
        result["unique"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.unique)
        result["generation"] = from_union([lambda x: from_dict(from_bool, x), from_none], self.generation)
        result["softDeleteTables"] = from_union([lambda x: from_list(from_str, x), from_none], self.soft_delete_tables)
        result["softDeleteData"] = from_union(
            [lambda x: from_list(lambda x: to_class(SoftDeleteDatum, x), x), from_none], self.soft_delete_data)
        result["checkBoxesFields"] = from_union([lambda x: from_list(lambda x: x, x), from_none],
                                                self.check_boxes_fields)
        result["imgFields"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.img_fields)
        result["relations"] = from_union([lambda x: to_class(Relations, x), from_none], self.relations)
        result["hasSoftDelete"] = from_union([from_bool, from_none], self.has_soft_delete)
        result["timestamp"] = from_union([from_bool, from_none], self.timestamp)
        result["cachable"] = from_union([from_bool, from_none], self.cachable)
        result["metable"] = from_union([from_bool, from_none], self.metable)
        result["sluggable"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.sluggable)
        result["relationClasses"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.relation_classes)
        result["relationTables"] = from_union([lambda x: from_list(from_str, x), from_none], self.relation_tables)
        result["modelsNames"] = from_union([lambda x: from_list(from_str, x), from_none], self.models_names)
        result["weakness"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.weakness)
        result["weaknessRelation"] = from_union([lambda x: from_list(lambda x: x, x), from_none],
                                                self.weakness_relation)
        result["selectData"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.select_data)
        result["entityName"] = from_union([from_str, from_none], self.entity_name)
        result["modelName"] = from_union([from_str, from_none], self.model_name)
        result["tableName"] = from_union([from_str, from_none], self.table_name)
        result["modelBaseName"] = from_union([from_str, from_none], self.model_base_name)
        result["modelPlural"] = from_union([from_str, from_none], self.model_plural)
        result["migrateName"] = from_union([from_str, from_none], self.migrate_name)
        result["title"] = from_union([from_str, from_none], self.title)
        result["modelVariable"] = from_union([from_str, from_none], self.model_variable)
        result["modelDotNotation"] = from_union([from_str, from_none], self.model_dot_notation)
        result["modelDashVariable"] = from_union([from_str, from_none], self.model_dash_variable)
        result["resource"] = from_union([from_str, from_none], self.resource)

        result["relationNames"] = from_union([lambda x: from_list(from_str, x), from_none], self.relation_names)
        result["relatedTables"] = from_union([lambda x: from_list(from_str, x), from_none], self.related_tables)
        result["paths"] = from_union([lambda x: to_class(Paths, x), from_none], self.paths)
        return result


def input_entity_from_dict(s: Any) -> InputEntity:
    return InputEntity.from_dict(s)


def input_entity_to_dict(x: InputEntity) -> Any:
    return to_class(InputEntity, x)


class PurpleExtraProperties:
    soft_delete: Optional[bool]
    timestamp: Optional[bool]
    cachable: Optional[bool]
    metable: Optional[bool]
    sluggable: Optional[str]

    def __init__(self, soft_delete: Optional[bool], timestamp: Optional[bool], cachable: Optional[bool],
                 metable: Optional[bool], sluggable: Optional[str]) -> None:
        self.soft_delete = soft_delete
        self.timestamp = timestamp
        self.cachable = cachable
        self.metable = metable
        self.sluggable = sluggable

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleExtraProperties':
        assert isinstance(obj, dict)
        soft_delete = from_union([from_bool, from_none], obj.get("softDelete"))
        timestamp = from_union([from_bool, from_none], obj.get("timestamp"))
        cachable = from_union([from_bool, from_none], obj.get("cachable"))
        metable = from_union([from_bool, from_none], obj.get("metable"))
        sluggable = from_union([from_str, from_none], obj.get("sluggable"))
        return PurpleExtraProperties(soft_delete, timestamp, cachable, metable, sluggable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["softDelete"] = from_union([from_bool, from_none], self.soft_delete)
        result["timestamp"] = from_union([from_bool, from_none], self.timestamp)
        result["cachable"] = from_union([from_bool, from_none], self.cachable)
        result["metable"] = from_union([from_bool, from_none], self.metable)
        result["sluggable"] = from_union([from_str, from_none], self.sluggable)
        return result


class PurpleForeign:
    related_entity: Optional[str]
    field_view: Optional[str]
    related_field: Optional[str]

    def __init__(self, related_entity: Optional[str], field_view: Optional[str], related_field: Optional[str]) -> None:
        self.related_entity = related_entity
        self.field_view = field_view
        self.related_field = related_field

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleForeign':
        assert isinstance(obj, dict)
        related_entity = from_union([from_str, from_none], obj.get("relatedEntity"))
        field_view = from_union([from_str, from_none], obj.get("fieldView"))
        related_field = from_union([from_str, from_none], obj.get("relatedField"))
        return PurpleForeign(related_entity, field_view, related_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["relatedEntity"] = from_union([from_str, from_none], self.related_entity)
        result["fieldView"] = from_union([from_str, from_none], self.field_view)
        result["relatedField"] = from_union([from_str, from_none], self.related_field)
        return result


class PurpleDBType:
    type: Optional[str]
    primary: Optional[bool]
    foreign: Optional[PurpleForeign]
    default: Union[float, None, str, int]

    def __init__(self, type: Optional[str], primary: Optional[bool], foreign: Optional[PurpleForeign],
                 default: Union[float, None, str, int]) -> None:
        self.type = type
        self.primary = primary
        self.foreign = foreign
        self.default = default

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleDBType':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        primary = from_union([from_bool, from_none], obj.get("primary"))
        foreign = from_union([PurpleForeign.from_dict, from_none], obj.get("foreign"))
        default = from_union([from_float, from_str, from_none, from_int], obj.get("default"))
        return PurpleDBType(type, primary, foreign, default)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["primary"] = from_union([from_bool, from_none], self.primary)
        result["foreign"] = from_union([lambda x: to_class(PurpleForeign, x), from_none], self.foreign)
        result["default"] = from_union([to_float, from_str, from_none], self.default)
        return result


class EnumElement:
    label: Optional[str]
    value: Optional[str]

    def __init__(self, label: Optional[str], value: Optional[str]) -> None:
        self.label = label
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'EnumElement':
        assert isinstance(obj, dict)
        label = from_union([from_str, from_none], obj.get("label"))
        value = from_union([from_str, from_none], obj.get("value"))
        return EnumElement(label, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_union([from_str, from_none], self.label)
        result["value"] = from_union([from_str, from_none], self.value)
        return result


class PurpleViewType:
    type: Optional[str]
    enums: Optional[List[EnumElement]]

    def __init__(self, type: Optional[str], enums: Optional[List[EnumElement]]) -> None:
        self.type = type
        self.enums = enums

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleViewType':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        enums = from_union([lambda x: from_list(EnumElement.from_dict, x), from_none], obj.get("enums"))
        return PurpleViewType(type, enums)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["enums"] = from_union([lambda x: from_list(lambda x: to_class(EnumElement, x), x), from_none],
                                     self.enums)
        return result


class PurpleField:
    title: Optional[str]
    name: Optional[str]
    db_type: Optional[PurpleDBType]
    view_type: Optional[PurpleViewType]
    searchable: Optional[bool]
    fillable: Optional[bool]
    in_form: Optional[bool]
    in_view: Optional[bool]
    in_index: Optional[bool]
    validations: Optional[str]

    def __init__(self, title: Optional[str], name: Optional[str], db_type: Optional[PurpleDBType],
                 view_type: Optional[PurpleViewType], searchable: Optional[bool], fillable: Optional[bool],
                 in_form: Optional[bool], in_view: Optional[bool], in_index: Optional[bool],
                 validations: Optional[str]) -> None:
        self.title = title
        self.name = name
        self.db_type = db_type
        self.view_type = view_type
        self.searchable = searchable
        self.fillable = fillable
        self.in_form = in_form
        self.in_view = in_view
        self.in_index = in_index
        self.validations = validations

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleField':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        name = from_union([from_str, from_none], obj.get("name"))
        db_type = from_union([PurpleDBType.from_dict, from_none], obj.get("dbType"))
        view_type = from_union([PurpleViewType.from_dict, from_none], obj.get("viewType"))
        searchable = from_union([from_bool, from_none], obj.get("searchable"))
        fillable = from_union([from_bool, from_none], obj.get("fillable"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        validations = from_union([from_str, from_none], obj.get("validations"))
        return PurpleField(title, name, db_type, view_type, searchable, fillable, in_form, in_view, in_index,
                           validations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["name"] = from_union([from_str, from_none], self.name)
        result["dbType"] = from_union([lambda x: to_class(PurpleDBType, x), from_none], self.db_type)
        result["viewType"] = from_union([lambda x: to_class(PurpleViewType, x), from_none], self.view_type)
        result["searchable"] = from_union([from_bool, from_none], self.searchable)
        result["fillable"] = from_union([from_bool, from_none], self.fillable)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["validations"] = from_union([from_str, from_none], self.validations)
        return result


class RelationRelation:
    type: Optional[str]
    field_view: Optional[str]
    related_entity: Optional[str]
    middle_entity: Optional[str]
    pivot_fields: Optional[List[str]]
    foreign_key: Optional[str]
    other_key: Optional[str]
    local_key: Optional[str]

    def __init__(self, type: Optional[str], field_view: Optional[str], related_entity: Optional[str],
                 middle_entity: Optional[str], pivot_fields: Optional[List[str]], foreign_key: Optional[str],
                 other_key: Optional[str], local_key: Optional[str]) -> None:
        self.type = type
        self.field_view = field_view
        self.related_entity = related_entity
        self.middle_entity = middle_entity
        self.pivot_fields = pivot_fields
        self.foreign_key = foreign_key
        self.other_key = other_key
        self.local_key = local_key

    @staticmethod
    def from_dict(obj: Any) -> 'RelationRelation':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        field_view = from_union([from_str, from_none], obj.get("fieldView"))
        related_entity = from_union([from_str, from_none], obj.get("relatedEntity"))
        middle_entity = from_union([from_str, from_none], obj.get("middleEntity"))
        pivot_fields = from_union([lambda x: from_list(from_str, x), from_none], obj.get("pivotFields"))
        foreign_key = from_union([from_str, from_none], obj.get("foreignKey"))
        other_key = from_union([from_str, from_none], obj.get("otherKey"))
        local_key = from_union([from_str, from_none], obj.get("localKey"))
        return RelationRelation(type, field_view, related_entity, middle_entity, pivot_fields, foreign_key, other_key,
                                local_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["fieldView"] = from_union([from_str, from_none], self.field_view)
        result["relatedEntity"] = from_union([from_str, from_none], self.related_entity)
        result["middleEntity"] = from_union([from_str, from_none], self.middle_entity)
        result["pivotFields"] = from_union([lambda x: from_list(from_str, x), from_none], self.pivot_fields)
        result["foreignKey"] = from_union([from_str, from_none], self.foreign_key)
        result["otherKey"] = from_union([from_str, from_none], self.other_key)
        result["localKey"] = from_union([from_str, from_none], self.local_key)
        return result


class RelationElement:
    name: Optional[str]
    type: Optional[str]
    relation: Optional[RelationRelation]
    in_form: Optional[bool]
    in_view: Optional[bool]
    in_index: Optional[bool]

    def __init__(self, name: Optional[str], type: Optional[str], relation: Optional[RelationRelation],
                 in_form: Optional[bool], in_view: Optional[bool], in_index: Optional[bool]) -> None:
        self.name = name
        self.type = type
        self.relation = relation
        self.in_form = in_form
        self.in_view = in_view
        self.in_index = in_index

    @staticmethod
    def from_dict(obj: Any) -> 'RelationElement':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([from_str, from_none], obj.get("type"))
        relation = from_union([RelationRelation.from_dict, from_none], obj.get("relation"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        return RelationElement(name, type, relation, in_form, in_view, in_index)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([from_str, from_none], self.type)
        result["relation"] = from_union([lambda x: to_class(RelationRelation, x), from_none], self.relation)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        return result


class EntityEntity:
    name: Optional[str]
    model: Optional[str]
    table: Optional[str]
    fields: Optional[List[PurpleField]]
    relations: Optional[List[RelationElement]]
    extra_properties: Optional[PurpleExtraProperties]
    generation: Optional[Dict[str, bool]]

    def __init__(self, name: Optional[str], model: Optional[str], table: Optional[str],
                 fields: Optional[List[PurpleField]], relations: Optional[List[RelationElement]],
                 extra_properties: Optional[PurpleExtraProperties], generation: Optional[Dict[str, bool]]) -> None:
        self.name = name
        self.model = model
        self.table = table
        self.fields = fields
        self.relations = relations
        self.extra_properties = extra_properties
        self.generation = generation

    @staticmethod
    def from_dict(obj: Any) -> 'EntityEntity':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        model = from_union([from_str, from_none], obj.get("model"))
        table = from_union([from_str, from_none], obj.get("table"))
        fields = from_union([lambda x: from_list(PurpleField.from_dict, x), from_none], obj.get("fields"))
        relations = from_union([lambda x: from_list(RelationElement.from_dict, x), from_none], obj.get("relations"))
        extra_properties = from_union([PurpleExtraProperties.from_dict, from_none], obj.get("extraProperties"))
        generation = from_union([lambda x: from_dict(from_bool, x), from_none], obj.get("generation"))
        return EntityEntity(name, model, table, fields, relations, extra_properties, generation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["model"] = from_union([from_str, from_none], self.model)
        result["table"] = from_union([from_str, from_none], self.table)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(PurpleField, x), x), from_none],
                                      self.fields)
        result["relations"] = from_union([lambda x: from_list(lambda x: to_class(RelationElement, x), x), from_none],
                                         self.relations)
        result["extraProperties"] = from_union([lambda x: to_class(PurpleExtraProperties, x), from_none],
                                               self.extra_properties)
        result["generation"] = from_union([lambda x: from_dict(from_bool, x), from_none], self.generation)
        return result


class FluffyDBType:
    type: Optional[str]
    primary: Optional[bool]
    foreign: Optional[PurpleForeign]
    default: Optional[any]
    unsigned: Optional[bool]

    def __init__(self, type: Optional[str], primary: Optional[bool], foreign: Optional[PurpleForeign],
                 default: Optional[any], unsigned: Optional[bool]) -> None:
        self.type = type
        self.primary = primary
        self.foreign = foreign
        self.default = default
        self.unsigned = unsigned

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyDBType':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        primary = from_union([from_bool, from_none], obj.get("primary"))
        foreign = from_union([PurpleForeign.from_dict, from_none], obj.get("foreign"))
        default = from_union([from_float, from_int, from_bool, from_str, from_none], obj.get("default"))
        unsigned = from_union([from_bool, from_none], obj.get("unsigned"))
        return FluffyDBType(type, primary, foreign, default, unsigned)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["primary"] = from_union([from_bool, from_none], self.primary)
        result["foreign"] = from_union([lambda x: to_class(PurpleForeign, x), from_none], self.foreign)
        result["default"] = from_union([from_float, from_int, from_bool, from_str, from_none], self.default)
        result["unsigned"] = from_union([from_bool, from_none], self.unsigned)
        return result


class FluffyField:
    title: Optional[str]
    name: Optional[str]
    db_type: Optional[FluffyDBType]
    view_type: Optional[PurpleViewType]
    searchable: Optional[bool]
    fillable: Optional[bool]
    in_form: Optional[bool]
    in_index: Optional[bool]
    validations: Optional[str]
    in_view: Optional[bool]

    def __init__(self, title: Optional[str], name: Optional[str], db_type: Optional[FluffyDBType],
                 view_type: Optional[PurpleViewType], searchable: Optional[bool], fillable: Optional[bool],
                 in_form: Optional[bool], in_index: Optional[bool], validations: Optional[str],
                 in_view: Optional[bool]) -> None:
        self.title = title
        self.name = name
        self.db_type = db_type
        self.view_type = view_type
        self.searchable = searchable
        self.fillable = fillable
        self.in_form = in_form
        self.in_index = in_index
        self.validations = validations
        self.in_view = in_view

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyField':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        name = from_union([from_str, from_none], obj.get("name"))
        db_type = from_union([FluffyDBType.from_dict, from_none], obj.get("dbType"))
        view_type = from_union([PurpleViewType.from_dict, from_none], obj.get("viewType"))
        searchable = from_union([from_bool, from_none], obj.get("searchable"))
        fillable = from_union([from_bool, from_none], obj.get("fillable"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        validations = from_union([from_str, from_none], obj.get("validations"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        return FluffyField(title, name, db_type, view_type, searchable, fillable, in_form, in_index, validations,
                           in_view)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["name"] = from_union([from_str, from_none], self.name)
        result["dbType"] = from_union([lambda x: to_class(FluffyDBType, x), from_none], self.db_type)
        result["viewType"] = from_union([lambda x: to_class(PurpleViewType, x), from_none], self.view_type)
        result["searchable"] = from_union([from_bool, from_none], self.searchable)
        result["fillable"] = from_union([from_bool, from_none], self.fillable)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["validations"] = from_union([from_str, from_none], self.validations)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        return result


class ConfigEntity:
    name: Optional[str]
    table: Optional[str]
    model: Optional[str]
    fields: Optional[List[FluffyField]]
    relations: Optional[List[RelationElement]]
    extra_properties: Optional[PurpleExtraProperties]
    generation: Optional[Dict[str, bool]]
    input_entity: Optional[InputEntity]

    def __init__(self, name: Optional[str], table: Optional[str],
                 model: Optional[str], fields: Optional[List[FluffyField]], relations: Optional[List[RelationElement]],
                 extra_properties: Optional[PurpleExtraProperties], generation: Optional[Dict[str, bool]],
                 input_entity: Optional[InputEntity]) -> None:
        self.name = name
        self.table = table
        self.model = model
        self.fields = fields
        self.relations = relations
        self.extra_properties = extra_properties
        self.generation = generation
        self.input_entity = input_entity

    @staticmethod
    def from_dict(obj: Any) -> 'ConfigEntity':
        assert isinstance(obj, dict)

        name = from_union([from_str, from_none], obj.get("name"))
        table = from_union([from_str, from_none], obj.get("table"))
        model = from_union([from_str, from_none], obj.get("model"))
        fields = from_union([lambda x: from_list(FluffyField.from_dict, x), from_none], obj.get("fields"))
        relations = from_union([lambda x: from_list(RelationElement.from_dict, x), from_none], obj.get("relations"))
        extra_properties = from_union([PurpleExtraProperties.from_dict, from_none], obj.get("extraProperties"))
        generation = from_union([lambda x: from_dict(from_bool, x), from_none], obj.get("generation"))
        input_entity = from_union([InputEntity.from_dict, from_none], obj.get("inputEntity"))

        return ConfigEntity(name, table, model, fields, relations, extra_properties, generation, input_entity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["table"] = from_union([from_str, from_none], self.table)
        result["model"] = from_union([from_str, from_none], self.model)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(FluffyField, x), x), from_none],
                                      self.fields)
        result["relations"] = from_union([lambda x: from_list(lambda x: to_class(RelationElement, x), x), from_none],
                                         self.relations)
        result["extraProperties"] = from_union([lambda x: to_class(PurpleExtraProperties, x), from_none],
                                               self.extra_properties)
        result["generation"] = from_union([lambda x: from_dict(from_bool, x), from_none], self.generation)
        result["inputEntity"] = from_union([lambda x: to_class(InputEntity, x), from_none],
                                           self.input_entity)
        return result


class CurrentConfig:
    entities: Optional[List[ConfigEntity]]

    # input_entities: Optional[List[InputEntity]]

    def __init__(self, entities: Optional[List[ConfigEntity]]) -> None:
        self.entities = entities
        # self.input_entities = input_entities

    @staticmethod
    def from_dict(obj: Any) -> 'CurrentConfig':
        assert isinstance(obj, dict)
        entities = from_union([lambda x: from_list(ConfigEntity.from_dict, x), from_none], obj.get("entities"))
        # input_entities = from_union([InputEntity.from_dict, from_none], obj.get("input_entities"))
        return CurrentConfig(entities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_union([lambda x: from_list(lambda x: to_class(ConfigEntity, x), x), from_none],
                                        self.entities)
        # result["input_entities"] = from_union([lambda x: to_class(InputEntity, x), from_none],
        #                                       self.input_entities)

        return result


class FluffyExtraProperties:
    soft_delete: Optional[bool]
    timestamp: Optional[bool]
    cachable: Optional[bool]

    def __init__(self, soft_delete: Optional[bool], timestamp: Optional[bool], cachable: Optional[bool]) -> None:
        self.soft_delete = soft_delete
        self.timestamp = timestamp
        self.cachable = cachable

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyExtraProperties':
        assert isinstance(obj, dict)
        soft_delete = from_union([from_bool, from_none], obj.get("softDelete"))
        timestamp = from_union([from_bool, from_none], obj.get("timestamp"))
        cachable = from_union([from_bool, from_none], obj.get("cachable"))
        return FluffyExtraProperties(soft_delete, timestamp, cachable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["softDelete"] = from_union([from_bool, from_none], self.soft_delete)
        result["timestamp"] = from_union([from_bool, from_none], self.timestamp)
        result["cachable"] = from_union([from_bool, from_none], self.cachable)
        return result


class FluffyForeign:
    related_entity: Optional[str]
    field_view: Optional[str]
    related_field: Optional[str]
    foreign_field_view: Optional[str]
    foreign_related_field: Optional[str]
    model_name: Optional[str]
    table: Optional[str]
    lower_model_name: Optional[str]
    capital_model_name_plural: Optional[str]

    def __init__(self, related_entity: Optional[str], field_view: Optional[str], related_field: Optional[str],
                 foreign_field_view: Optional[str], foreign_related_field: Optional[str], model_name: Optional[str],
                 table: Optional[str], lower_model_name: Optional[str],
                 capital_model_name_plural: Optional[str]) -> None:
        self.related_entity = related_entity
        self.field_view = field_view
        self.related_field = related_field
        self.foreign_field_view = foreign_field_view
        self.foreign_related_field = foreign_related_field
        self.model_name = model_name
        self.table = table
        self.lower_model_name = lower_model_name
        self.capital_model_name_plural = capital_model_name_plural

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyForeign':
        assert isinstance(obj, dict)
        related_entity = from_union([from_str, from_none], obj.get("relatedEntity"))
        field_view = from_union([from_str, from_none], obj.get("fieldView"))
        related_field = from_union([from_str, from_none], obj.get("relatedField"))
        foreign_field_view = from_union([from_str, from_none], obj.get("field_view"))
        foreign_related_field = from_union([from_str, from_none], obj.get("related_field"))
        model_name = from_union([from_str, from_none], obj.get("modelName"))
        table = from_union([from_str, from_none], obj.get("table"))
        lower_model_name = from_union([from_str, from_none], obj.get("lowerModelName"))
        capital_model_name_plural = from_union([from_str, from_none], obj.get("CapitalModelNamePlural"))
        return FluffyForeign(related_entity, field_view, related_field, foreign_field_view, foreign_related_field,
                             model_name, table, lower_model_name, capital_model_name_plural)

    def to_dict(self) -> dict:
        result: dict = {}
        result["relatedEntity"] = from_union([from_str, from_none], self.related_entity)
        result["fieldView"] = from_union([from_str, from_none], self.field_view)
        result["relatedField"] = from_union([from_str, from_none], self.related_field)
        result["field_view"] = from_union([from_str, from_none], self.foreign_field_view)
        result["related_field"] = from_union([from_str, from_none], self.foreign_related_field)
        result["modelName"] = from_union([from_str, from_none], self.model_name)
        result["table"] = from_union([from_str, from_none], self.table)
        result["lowerModelName"] = from_union([from_str, from_none], self.lower_model_name)
        result["CapitalModelNamePlural"] = from_union([from_str, from_none], self.capital_model_name_plural)
        return result


class TentacledDBType:
    type: Optional[str]
    primary: Optional[bool]
    foreign: Optional[FluffyForeign]
    default: Optional[int]

    def __init__(self, type: Optional[str], primary: Optional[bool], foreign: Optional[FluffyForeign],
                 default: Optional[int]) -> None:
        self.type = type
        self.primary = primary
        self.foreign = foreign
        self.default = default

    @staticmethod
    def from_dict(obj: Any) -> 'TentacledDBType':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        primary = from_union([from_bool, from_none], obj.get("primary"))
        foreign = from_union([FluffyForeign.from_dict, from_none], obj.get("foreign"))
        default = from_union([from_int, from_none], obj.get("default"))
        return TentacledDBType(type, primary, foreign, default)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["primary"] = from_union([from_bool, from_none], self.primary)
        result["foreign"] = from_union([lambda x: to_class(FluffyForeign, x), from_none], self.foreign)
        result["default"] = from_union([from_int, from_none], self.default)
        return result


class FluffyViewType:
    type: Optional[str]

    def __init__(self, type: Optional[str]) -> None:
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyViewType':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        return FluffyViewType(type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        return result


class TentacledField:
    title: Optional[str]
    name: Optional[str]
    db_type: Optional[TentacledDBType]
    view_type: Optional[FluffyViewType]
    searchable: Optional[bool]
    fillable: Optional[bool]
    in_form: Optional[bool]
    in_view: Optional[bool]
    in_index: Optional[bool]
    validations: Optional[str]

    def __init__(self, title: Optional[str], name: Optional[str], db_type: Optional[TentacledDBType],
                 view_type: Optional[FluffyViewType], searchable: Optional[bool], fillable: Optional[bool],
                 in_form: Optional[bool], in_view: Optional[bool], in_index: Optional[bool],
                 validations: Optional[str]) -> None:
        self.title = title
        self.name = name
        self.db_type = db_type
        self.view_type = view_type
        self.searchable = searchable
        self.fillable = fillable
        self.in_form = in_form
        self.in_view = in_view
        self.in_index = in_index
        self.validations = validations

    @staticmethod
    def from_dict(obj: Any) -> 'TentacledField':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        name = from_union([from_str, from_none], obj.get("name"))
        db_type = from_union([TentacledDBType.from_dict, from_none], obj.get("dbType"))
        view_type = from_union([FluffyViewType.from_dict, from_none], obj.get("viewType"))
        searchable = from_union([from_bool, from_none], obj.get("searchable"))
        fillable = from_union([from_bool, from_none], obj.get("fillable"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        validations = from_union([from_str, from_none], obj.get("validations"))
        return TentacledField(title, name, db_type, view_type, searchable, fillable, in_form, in_view, in_index,
                              validations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["name"] = from_union([from_str, from_none], self.name)
        result["dbType"] = from_union([lambda x: to_class(TentacledDBType, x), from_none], self.db_type)
        result["viewType"] = from_union([lambda x: to_class(FluffyViewType, x), from_none], self.view_type)
        result["searchable"] = from_union([from_bool, from_none], self.searchable)
        result["fillable"] = from_union([from_bool, from_none], self.fillable)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["validations"] = from_union([from_str, from_none], self.validations)
        return result


class TConfig:
    entities: Optional[List[ConfigEntity]]

    def __init__(self, entities: Optional[List[ConfigEntity]]) -> None:
        self.entities = entities

    @staticmethod
    def from_dict(obj: Any) -> 'TConfig':
        assert isinstance(obj, dict)
        entities = from_union([lambda x: from_list(ConfigEntity.from_dict, x), from_none], obj.get("entities"))
        return TConfig(entities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_union([lambda x: from_list(lambda x: to_class(ConfigEntity, x), x), from_none],
                                        self.entities)
        return result


class AddedEntity:
    entity: Optional[str]
    commit_id: Optional[str]

    def __init__(self, entity: Optional[str], commit_id: Optional[str]) -> None:
        self.entity = entity
        self.commit_id = commit_id

    @staticmethod
    def from_dict(obj: Any) -> 'AddedEntity':
        assert isinstance(obj, dict)
        entity = from_union([from_str, from_none], obj.get("entity"))
        commit_id = from_union([from_str, from_none], obj.get("commit_id"))
        return AddedEntity(entity, commit_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entity"] = from_union([from_str, from_none], self.entity)
        result["commit_id"] = from_union([from_str, from_none], self.commit_id)
        return result


class Info:
    added_entity: Optional[List[AddedEntity]]
    deleted_entity: Optional[List[Any]]

    def __init__(self, added_entity: Optional[List[AddedEntity]], deleted_entity: Optional[List[Any]]) -> None:
        self.added_entity = added_entity
        self.deleted_entity = deleted_entity

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        assert isinstance(obj, dict)
        added_entity = from_union([lambda x: from_list(AddedEntity.from_dict, x), from_none], obj.get("addedEntity"))
        deleted_entity = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("deletedEntity"))
        return Info(added_entity, deleted_entity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["addedEntity"] = from_union([lambda x: from_list(lambda x: to_class(AddedEntity, x), x), from_none],
                                           self.added_entity)
        result["deletedEntity"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.deleted_entity)
        return result


class History:
    build_no: Optional[int]
    info: Optional[Info]
    current_config: Optional[TConfig]
    last_config: Optional[TConfig]

    def __init__(self, build_no: Optional[int], info: Optional[Info], current_config: Optional[TConfig],
                 last_config: Optional[TConfig]) -> None:
        self.build_no = build_no
        self.info = info
        self.current_config = current_config
        self.last_config = last_config

    @staticmethod
    def from_dict(obj: Any) -> 'History':
        assert isinstance(obj, dict)
        build_no = from_union([from_int, from_none], obj.get("build_no"))
        info = from_union([Info.from_dict, from_none], obj.get("info"))
        current_config = from_union([TConfig.from_dict, from_none], obj.get("current_config"))
        last_config = from_union([TConfig.from_dict, from_none], obj.get("last_config"))
        return History(build_no, info, current_config, last_config)

    def to_dict(self) -> dict:
        result: dict = {}
        result["build_no"] = from_union([from_int, from_none], self.build_no)
        result["info"] = from_union([lambda x: to_class(Info, x), from_none], self.info)
        result["current_config"] = from_union([lambda x: to_class(TConfig, x), from_none], self.current_config)
        result["last_config"] = from_union([lambda x: to_class(TConfig, x), from_none], self.last_config)
        return result


class StickyField:
    title: Optional[str]
    name: Optional[str]
    db_type: Optional[FluffyDBType]
    view_type: Optional[FluffyViewType]
    searchable: Optional[bool]
    fillable: Optional[bool]
    in_form: Optional[bool]
    in_view: Optional[bool]
    in_index: Optional[bool]
    validations: Optional[str]

    def __init__(self, title: Optional[str], name: Optional[str], db_type: Optional[FluffyDBType],
                 view_type: Optional[FluffyViewType], searchable: Optional[bool], fillable: Optional[bool],
                 in_form: Optional[bool], in_view: Optional[bool], in_index: Optional[bool],
                 validations: Optional[str]) -> None:
        self.title = title
        self.name = name
        self.db_type = db_type
        self.view_type = view_type
        self.searchable = searchable
        self.fillable = fillable
        self.in_form = in_form
        self.in_view = in_view
        self.in_index = in_index
        self.validations = validations

    @staticmethod
    def from_dict(obj: Any) -> 'StickyField':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        name = from_union([from_str, from_none], obj.get("name"))
        db_type = from_union([FluffyDBType.from_dict, from_none], obj.get("dbType"))
        view_type = from_union([FluffyViewType.from_dict, from_none], obj.get("viewType"))
        searchable = from_union([from_bool, from_none], obj.get("searchable"))
        fillable = from_union([from_bool, from_none], obj.get("fillable"))
        in_form = from_union([from_bool, from_none], obj.get("inForm"))
        in_view = from_union([from_bool, from_none], obj.get("inView"))
        in_index = from_union([from_bool, from_none], obj.get("inIndex"))
        validations = from_union([from_str, from_none], obj.get("validations"))
        return StickyField(title, name, db_type, view_type, searchable, fillable, in_form, in_view, in_index,
                           validations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["name"] = from_union([from_str, from_none], self.name)
        result["dbType"] = from_union([lambda x: to_class(FluffyDBType, x), from_none], self.db_type)
        result["viewType"] = from_union([lambda x: to_class(FluffyViewType, x), from_none], self.view_type)
        result["searchable"] = from_union([from_bool, from_none], self.searchable)
        result["fillable"] = from_union([from_bool, from_none], self.fillable)
        result["inForm"] = from_union([from_bool, from_none], self.in_form)
        result["inView"] = from_union([from_bool, from_none], self.in_view)
        result["inIndex"] = from_union([from_bool, from_none], self.in_index)
        result["validations"] = from_union([from_str, from_none], self.validations)
        return result


class LastConfig:
    entities: Optional[List[ConfigEntity]]

    def __init__(self, entities: Optional[List[ConfigEntity]]) -> None:
        self.entities = entities

    @staticmethod
    def from_dict(obj: Any) -> 'LastConfig':
        assert isinstance(obj, dict)
        entities = from_union([lambda x: from_list(ConfigEntity.from_dict, x), from_none], obj.get("entities"))
        return LastConfig(entities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_union([lambda x: from_list(lambda x: to_class(ConfigEntity, x), x), from_none],
                                        self.entities)

        return result


class Options:
    force: Optional[bool]
    default_lang: Optional[str]
    push: Optional[bool]
    pull_request: Optional[bool]

    def __init__(self, force: Optional[bool], default_lang: Optional[str], push: Optional[bool],
                 pull_request: Optional[bool]) -> None:
        self.force = force
        self.default_lang = default_lang
        self.push = push
        self.pull_request = pull_request

    @staticmethod
    def from_dict(obj: Any) -> 'Options':
        assert isinstance(obj, dict)
        force = from_union([from_bool, from_none], obj.get("force"))
        default_lang = from_union([from_str, from_none], obj.get("default_lang"))
        push = from_union([from_bool, from_none], obj.get("push"))
        pull_request = from_union([from_bool, from_none], obj.get("pullRequest"))
        return Options(force, default_lang, push, pull_request)

    def to_dict(self) -> dict:
        result: dict = {}
        result["force"] = from_union([from_bool, from_none], self.force)
        result["default_lang"] = from_union([from_str, from_none], self.default_lang)
        result["push"] = from_union([from_bool, from_none], self.push)
        result["pullRequest"] = from_union([from_bool, from_none], self.pull_request)
        return result


class ProjectConfiguration:
    _project_url: Optional[str]
    _access_token: Optional[str]
    _project_active_branch: Optional[str]
    _project_name: Optional[str]
    _slug: Optional[str]
    _organization_name: Optional[str]
    _project_id: Optional[int]
    _base_boilerplate: Optional[str]
    _boilerplate_active_branch: Optional[str]
    _base_templates: Optional[str]
    _current_config: Optional[CurrentConfig]
    _last_config: Optional[LastConfig]
    _options: Optional[Options]
    _technology_stack: Optional[str]
    _history: Optional[List[Any]]

    def __init__(self, project_url: Optional[str], access_token: Optional[str], project_active_branch: Optional[str],
                 project_name: Optional[str], slug: Optional[str],
                 organization_name: Optional[str], project_id: Optional[int], base_boilerplate: Optional[str],
                 boilerplate_active_branch: Optional[str], base_templates: Optional[str],
                 current_config: Optional[CurrentConfig],
                 last_config: Optional[LastConfig], options: Optional[Options], technology_stack: Optional[str],
                 history: Optional[List[Any]]) -> None:
        self._project_url = project_url
        self._access_token = access_token
        self._project_active_branch = project_active_branch

        self._project_name = project_name
        self._slug = slug
        self._organization_name = organization_name
        self._project_id = project_id
        self._base_boilerplate = base_boilerplate
        self._boilerplate_active_branch = boilerplate_active_branch
        self._base_templates = base_templates

        self._current_config = current_config
        self._last_config = last_config
        self._options = options
        self._technology_stack = technology_stack
        self._history = history
        self._operations = []
        self._capabilities = []
        self._parsed_data = []
        self.paths = []
        self._templates = {}
        self._build_no = None
        self._added_entities = []
        self._deleted_entities = []

    def load_project_configuration_manager_from_dict(self, obj: Any) -> 'ProjectConfiguration':
        assert isinstance(obj, dict)
        self._project_url = from_union([from_str, from_none], obj.get("projectUrl"))
        self._access_token = from_union([from_str, from_none], obj.get("accessToken"))
        self._project_active_branch = from_union([from_str, from_none], obj.get("projectActiveBranch"))
        self._project_name = from_union([from_str, from_none], obj.get("projectName"))
        self._slug = from_union([from_str, from_none], obj.get("slug"))
        self._organization_name = from_union([from_str, from_none], obj.get("organizationName"))
        self._project_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("projectId"))
        self._base_boilerplate = from_union([from_str, from_none], obj.get("baseBoilerplate"))
        self._boilerplate_active_branch = from_union([from_str, from_none], obj.get("boilerplateActiveBranch"))
        self._base_templates = from_union([from_str, from_none], obj.get("baseTemplates"))
        self._current_config = from_union([CurrentConfig.from_dict, from_none], obj.get("currentConfig"))
        self._last_config = from_union([LastConfig.from_dict, from_none], obj.get("lastConfig"))
        self._options = from_union([Options.from_dict, from_none], obj.get("options"))
        self._technology_stack = from_union([from_str, from_none], obj.get("technologyStack"))
        self._history = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("history"))
        self._added_entities = []
        self._deleted_entities = []

    def set_to_added_entities(self, entity):
        """
         add entity to added entities
        """
        self._added_entities.append(entity)

    def set_to_deleted_entities(self, entity):
        """
         add entity to deleted entities
        """
        self._deleted_entities.append(entity)

    @staticmethod
    def from_dict(self, obj: Any) -> 'ProjectConfiguration':
        assert isinstance(obj, dict)
        _project_url = from_union([from_str, from_none], obj.get("projectUrl"))
        _access_token = from_union([from_str, from_none], obj.get("accessToken"))
        _project_active_branch = from_union([from_str, from_none], obj.get("projectActiveBranch"))
        _project_name = from_union([from_str, from_none], obj.get("projectName"))
        _slug = from_union([from_str, from_none], obj.get("slug"))
        _organization_name = from_union([from_str, from_none], obj.get("organizationName"))
        _project_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("projectId"))
        _base_boilerplate = from_union([from_str, from_none], obj.get("baseBoilerplate"))
        _boilerplate_active_branch = from_union([from_str, from_none], obj.get("boilerplateActiveBranch"))
        _base_templates = from_union([from_str, from_none], obj.get("baseTemplates"))
        _current_config = from_union([CurrentConfig.from_dict, from_none], obj.get("currentConfig"))
        _last_config = from_union([LastConfig.from_dict, from_none], obj.get("lastConfig"))
        _options = from_union([Options.from_dict, from_none], obj.get("options"))
        _technology_stack = from_union([from_str, from_none], obj.get("technologyStack"))
        _history = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("history"))
        _added_entities = []
        _deleted_entities = []
        return ProjectConfiguration(_project_url, _access_token, _project_active_branch, _project_name,
                                    _slug,
                                    _organization_name, _project_id, _base_boilerplate, _boilerplate_active_branch,
                                    _base_templates, _current_config, _last_config, _options,
                                    _technology_stack, _history, _added_entities, _deleted_entities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["projectUrl"] = from_union([from_str, from_none], self._project_url)
        result["accessToken"] = from_union([from_str, from_none], self._access_token)
        result["projectActiveBranch"] = from_union([from_str, from_none], self._project_active_branch)
        result["projectName"] = from_union([from_str, from_none], self._project_name)
        result["slug"] = from_union([from_str, from_none], self._slug)
        result["organizationName"] = from_union([from_str, from_none], self._organization_name)
        result["projectId"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                          lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                         self._project_id)
        result["baseBoilerplate"] = from_union([from_str, from_none], self._base_boilerplate)
        result["boilerplateActiveBranch"] = from_union([from_str, from_none], self._boilerplate_active_branch)
        result["baseTemplates"] = from_union([from_str, from_none], self._base_templates)
        result["currentConfig"] = from_union([lambda x: to_class(CurrentConfig, x), from_none], self._current_config)
        result["lastConfig"] = from_union([lambda x: to_class(LastConfig, x), from_none], self._last_config)
        result["options"] = from_union([lambda x: to_class(Options, x), from_none], self._options)
        result["technologyStack"] = from_union([from_str, from_none], self._technology_stack)
        result["history"] = from_union([lambda x: from_list(lambda x: x, x), from_none],
                                       self._history)
        return result


def project_configuration_to_dict(x: ProjectConfiguration) -> Any:
    return to_class(ProjectConfiguration, x)
