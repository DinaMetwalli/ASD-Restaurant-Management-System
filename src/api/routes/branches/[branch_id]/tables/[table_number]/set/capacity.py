from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_table

from src.branch.BranchService import BranchService
from src.utils.errors import AlreadyExistsError, InputError

guard = auth_guard
cleanup = auth_cleanup

class PostSchema(Schema):
    capacity = fields.Int(required=True)

def post(body: dict, branch_id: str, table_number: int):
    capacity: int = body["capacity"]

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")
        
        table = branch.tables().get_by_number(table_number)
        if table is None:
            return Error(Status.NOT_FOUND,
                         f"No table with number {table_number} at branch")

        table.set_capacity(capacity)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_table(table))
