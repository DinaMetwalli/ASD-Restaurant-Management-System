from marshmallow import Schema, fields

from datetime import datetime
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_event
from src.branch.BranchService import BranchService
from src.utils.errors import AlreadyExistsError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    start_timestamp = fields.Int(required=True)
    end_timestamp = fields.Int(required=True)
    type = fields.Int(required=True)
    phone_number = fields.Int(required=True)
    email = fields.String(required=True)
    address = fields.String(required=False)
    


def post(body: dict, branch_id: str):
    start_timestamp = body["start_timestamp"]
    end_timestamp = body["end_timestamp"]
    type = body["type"]
    phone_number = body["phone_number"]
    email = body["email"]
    address = body["address"]
    
    start_datetime_obj = datetime.fromtimestamp(start_timestamp)
    end_datetime_obj = datetime.fromtimestamp(end_timestamp)

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    try:
        event = branch.events().create(
            start_datetime_obj, end_datetime_obj, type, phone_number, email, address)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_event(event))
