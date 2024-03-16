from marshmallow import Schema, fields

from datetime import datetime
from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_event
from src.branch.BranchService import BranchService
from src.utils.errors import InputError

guard = perm_guard("event.update.end_time")
cleanup = auth_cleanup


class PostSchema(Schema):
    end_time = fields.Integer(required=True)


def post(body: dict, event_id: str = "", branch_id: str = ""):
    
    end_time = body["end_timestamp"]
    end_datetime_obj = datetime.fromtimestamp(end_time)

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")
        
        event = branch.events().get_by_id(event_id)
        if event is None:
            return Error(Status.NOT_FOUND, "Event not found.")

        event.set_end_time(end_datetime_obj)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_event(event))

