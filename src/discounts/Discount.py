# Author: Mohamed Elafifi
"""Module for managing specifc discounts."""
from decimal import Decimal
from src.user.ActiveUser import ActiveUser
from src.utils.errors import InputError
from ..utils.Database import Database
from .utils import validate_description, validate_name


class Discount:
    """Class for mananging specfic discounts."""

    def __init__(self, discount_id: str) -> None:
        """Don't call outside of BranchDiscounts."""
        self._discount_id = discount_id

    def get_id(self):
        """Get ID."""
        return self._discount_id

    def get_description(self) -> str:
        """Get description."""
        description = Database.execute_and_fetchone(
            "SELECT description FROM public.discounts WHERE id= %s",
            self._discount_id)

        assert description is not None
        return description[0]

    def get_multiplier(self) -> float:
        """Get multiplier."""
        multiplier = Database.execute_and_fetchone(
            "SELECT multiplier FROM public.discounts WHERE id= %s",
            self._discount_id)

        assert multiplier is not None

        multiplier_dec: Decimal = multiplier[0]
        return float(multiplier_dec)
    
    def get_name(self) -> str:
        """Get discount name"""
        name = Database.execute_and_fetchone(
            "SELECT name FROM public.discounts WHERE id = %s",
            self._discount_id)
        
        assert name is not None
        return name[0]

    def set_description(self, description: str) -> None:
        """Set description."""
        if not validate_description(description):
            raise InputError("Invalid description.")

        Database.execute_and_commit(
            "UPDATE public.discounts SET description = %s WHERE id = %s",
            description, self._discount_id)

    def set_multiplier(self, multiplier: float) -> None:
        """Set multiplier."""
        Database.execute_and_commit(
            "UPDATE public.discounts SET multiplier = %s WHERE id = %s",
            multiplier, self._discount_id)
        
    def set_name(self, name: str) -> None:
        """Set description."""
        if not validate_name(name):
            raise InputError("Invalid name.")

        Database.execute_and_commit(
            "UPDATE public.discounts SET name = %s WHERE id = %s",
            name, self._discount_id)

    def delete(self) -> None:
        """
        Delete the discount from the database.

        After calling you should immediately discard this object. Not doing so
        will cause errors.

        :raises PermissionError: If the current user does not have permission
        """
        
        sql = "DELETE FROM public.discounts WHERE id=%s;"

        ActiveUser.get().raise_without_permission("discount.delete")

        Database.execute_and_commit(sql, self._discount_id)
