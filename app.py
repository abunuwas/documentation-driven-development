import time
import uuid

from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields, EXCLUDE, validate

app = Flask(__name__)
app.config['API_TITLE'] = 'TODO API'
app.config['API_VERSION'] = '1.0.0'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_JSON_PATH'] = "api-spec.json"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/docs"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

API_TITLE = 'Orders API'
API_VERSION = '1.0.0'
api = Api(app)


class CreateTaskSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    priority = fields.String(
        default='low',
        validate=validate.OneOf(['low', 'medium', 'high']),
    )
    status = fields.String(
        default='pending',
        validate=validate.OneOf(['pending', 'progress', 'completed']),
    )
    task = fields.String()


class GetTaskSchema(CreateTaskSchema):
    created = fields.Integer(required=True)
    id = fields.UUID(required=True)


blueprint = Blueprint(
    'todo', 'todo', url_prefix='/todo',
    description='API that allows you to manage a to-do list',
)


TODO_LIST = []


@blueprint.route('/')
class TodoItems(MethodView):

    @blueprint.response(GetTaskSchema(many=True))
    def get(self):
        return TODO_LIST

    @blueprint.arguments(CreateTaskSchema)
    @blueprint.response(GetTaskSchema, code=201)
    def post(self, item):
        item['created'] = time.time()
        item['id'] = str(uuid.uuid4())
        TODO_LIST.append(item)
        return item


@blueprint.route('/<item_id>')
class TodoItem(MethodView):

    @blueprint.response(GetTaskSchema)
    def get(self, item_id):
        for item in TODO_LIST:
            if item['id'] == item_id:
                return item
        abort(404, message='Item not found.')

    @blueprint.arguments(CreateTaskSchema)
    @blueprint.response(GetTaskSchema)
    def put(self, update_data, item_id):
        for item in TODO_LIST:
            if item['id'] == item_id:
                item.update(update_data)
                return item
        abort(404, message='Item not found.')

    @blueprint.response(code=204)
    def delete(self, item_id):
        for index, item in enumerate(TODO_LIST):
            if item['id'] == item_id:
                TODO_LIST.pop(index)
                return
        abort(404, message='Item not found.')


api.register_blueprint(blueprint)
