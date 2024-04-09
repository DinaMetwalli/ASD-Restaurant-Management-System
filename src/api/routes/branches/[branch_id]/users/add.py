from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from src.branch.BranchService import BranchService
from src.user.UserService import UserService
from src.utils.errors import AuthorizationError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    username = fields.String(required=True)
    full_name = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Int(required=True)


def post(body, branch_id: str = ""):
    username = body["username"]
    full_name = body["full_name"]
    password = body["password"]
    role_id = body["role_id"]
    print(role_id, flush=True)
    
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    try:
        user = UserService.create(username, password, full_name, None, role_id)
        user.set_branch(branch)

    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)

    users = UserService.get_all_at_branch(branch)
    users_data = [dictify_user(u) for u in users]

    return OK({"users": users_data})
