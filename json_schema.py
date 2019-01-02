import colander

import json


class RelationData(colander.MappingSchema):
    type = colander.SchemaNode(colander.String(), validator=colander.OneOf(['mtm', '1tm']))
    fieldView = colander.SchemaNode(colander.String(), missing=None)
    relatedEntity = colander.SchemaNode(colander.String())
    middleEntity = colander.SchemaNode(colander.String(), missing=None)
    pivotFields = colander.SchemaNode(colander.List(), missing=None)

    foreignKey = colander.SchemaNode(colander.String(colander.String()))
    otherKey = colander.SchemaNode(colander.String(), missing=None)
    localKey = colander.SchemaNode(colander.String(), missing=None)


class Relation(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    type = colander.SchemaNode(colander.String(), missing=None)
    relation = RelationData()
    inForm = colander.SchemaNode(colander.Bool(), missing=None)
    inIndex = colander.SchemaNode(colander.Bool(), missing=None)
    inView = colander.SchemaNode(colander.Bool(), missing=None)


class Enum(colander.MappingSchema):
    label = colander.SchemaNode(colander.String())
    value = colander.SchemaNode(colander.String())


class Enums(colander.SequenceSchema):
    enum = Enum()


class ViewType(colander.MappingSchema):
    type = colander.SchemaNode(colander.String(), missing=None)
    enums = Enums(missing=None)


class Foreign(colander.MappingSchema):
    relatedEntity = colander.SchemaNode(colander.String())
    fieldView = colander.SchemaNode(colander.String())
    relatedField = colander.SchemaNode(colander.String(), missing=None)


class DbType(colander.MappingSchema):
    type = colander.SchemaNode(colander.String())
    # default = colander.SchemaNode( colander.String(),missing=None)
    foreign = Foreign(missing=None)
    primary = colander.SchemaNode(colander.Bool(), missing=None)


class Field(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), missing=None)
    name = colander.SchemaNode(colander.String())
    dbType = DbType()
    viewType = ViewType(missing=None)
    validations = colander.SchemaNode(colander.String(), missing=None)
    searchable = colander.SchemaNode(colander.Bool(), missing=None)
    fillable = colander.SchemaNode(colander.Bool(), missing=None)
    inForm = colander.SchemaNode(colander.Bool(), missing=None)
    inIndex = colander.SchemaNode(colander.Bool(), missing=None)
    inView = colander.SchemaNode(colander.Bool(), missing=None)


class Fields(colander.SequenceSchema):
    field = Field(missing=None)


class Relations(colander.SequenceSchema):
    relation = Relation(missing=None)


class ExtraProperties(colander.MappingSchema):
    SoftDelete = colander.SchemaNode(colander.Bool(), missing=None)
    metable = colander.SchemaNode(colander.Bool(), missing=None)
    cachable = colander.SchemaNode(colander.Bool(), missing=None)
    sluggable = colander.SchemaNode(colander.String(), missing=None)


class Extend(colander.MappingSchema):
    entity = colander.SchemaNode(colander.String())
    snipet = colander.SchemaNode(colander.String())


class Generation(colander.MappingSchema):
    model = colander.SchemaNode(colander.Bool(), missing=None)
    createEvent = colander.SchemaNode(colander.Bool(), missing=None)
    updateEvent = colander.SchemaNode(colander.Bool(), missing=None)
    deleteEvent = colander.SchemaNode(colander.Bool(), missing=None)
    listener = colander.SchemaNode(colander.Bool(), missing=None)
    repository = colander.SchemaNode(colander.Bool(), missing=None)
    createTable = colander.SchemaNode(colander.Bool(), missing=None)

    createRequest = colander.SchemaNode(colander.Bool(), missing=None)
    updateRequest = colander.SchemaNode(colander.Bool(), missing=None)
    controller = colander.SchemaNode(colander.Bool(), missing=None)
    route = colander.SchemaNode(colander.Bool(), missing=None)
    breadcrumbs = colander.SchemaNode(colander.Bool(), missing=None)
    lang = colander.SchemaNode(colander.Bool(), missing=None)
    view = colander.SchemaNode(colander.Bool(), missing=None)
    apiCreateRequest = colander.SchemaNode(colander.Bool(), missing=None)
    apiUpdateRequest = colander.SchemaNode(colander.Bool(), missing=None)
    apiController = colander.SchemaNode(colander.Bool(), missing=None)
    apiRoute = colander.SchemaNode(colander.Bool(), missing=None)


class Entity(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    model = colander.SchemaNode(colander.String(), missing=None)
    table = colander.SchemaNode(colander.String(), missing=None)
    fields = Fields(missing=None)
    relations = Relations(missing=None)
    extraProperties = ExtraProperties(missing=None)
    generation = Generation(missing=None)
    # extend = Extend(missing=None)


class Entities(colander.SequenceSchema):
    entity = Entity()


class JsonSchema(colander.MappingSchema):
    entities = Entities(missing=None)


def deserialize_config_schema(path):
    with open(path) as f:
        data = json.load(f)
    schema = JsonSchema()
    return schema.deserialize(data)
