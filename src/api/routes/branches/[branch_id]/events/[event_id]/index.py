from flask import render_template
from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_event
from src.branch.BranchService import BranchService

guard = perm_guard("event.view")
cleanup = auth_cleanup

def post(branch_id: str = "", event_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    event = branch.events().get_by_id(event_id)
    if event is None:
        return Error(Status.NOT_FOUND, "Event not found.")

    return OK(dictify_event(event))

# def get(branch_id: str = "", event_id: str = ""):
#     return render_template("event-update.html")
