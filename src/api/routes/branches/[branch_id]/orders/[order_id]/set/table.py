from flask import render_template
from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_discount, dictify_order
from src.branch.BranchService import BranchService
from src.tables.BranchTables import BranchTables
from src.order.OrderService import OrderService
from marshmallow import Schema, fields

guard = perm_guard("order.make")
cleanup = auth_cleanup


class PostSchema(Schema):
    table_no = fields.Integer(required=True)


def post(body: dict, branch_id: str = "", order_id: str = ""):

    table_number = body["table_no"]

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    order = OrderService.get_by_id(order_id)
    if order is None or order.get_branch().get_id() != branch.get_id():
        return Error(Status.NOT_FOUND, "Order not found.")

    branch_tables = branch.tables()
    table = branch_tables.get_by_number(table_number)

    if table is None:
        return Error(Status.NOT_FOUND, "Table not found.")

    order.set_table(table)

    return OK({})
