# Author: Mohamed Elafifi
"""Module for managing discounts in a branch."""
from psycopg2.errors import UniqueViolation

from src.utils.errors import InputError, AlreadyExistsError

from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .Discount import Discount
from .utils import validate_description, validate_name


class BranchDiscounts:
    """Class for managing discounts in a branch."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create(self, name: str, multiplier: float, description: str) -> Discount:
        """Create a new discount."""
        ActiveUser.get().raise_without_permission("discounts.create")
        
        if not validate_name(name):
            raise InputError("Invalid Name")
        
        if not validate_description(description):
            raise InputError("Invalid Description")

        try:
            cursor = Database.execute(
                "INSERT INTO public.discounts \
                (name, multiplier, description, branch_id) \
                VALUES(%s, %s, %s, %s) RETURNING id;",
                name, multiplier, description, self._branch_id)
        except UniqueViolation:
            raise AlreadyExistsError(f"A discount with the name {name} already exists.")

        Database.commit()
        result = cursor.fetchone()

        assert result is not None
        return Discount(result[0])

    def get_by_id(self, discount_id: str) -> Discount | None:
        """Get a discount by its id."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.discounts WHERE id=%s AND branch_id=%s",
            discount_id, self._branch_id)

        if result is not None:
            return Discount(result[0])

    def get_all(self) -> list[Discount]:
        """Get all discounts."""
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.discounts")

        return [Discount(record[0]) for record in result]
