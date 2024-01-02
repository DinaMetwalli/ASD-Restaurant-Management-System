"""Module for managing specific orders."""


from src.order.OrderStatus import OrderStatus
from src.user.User import User
from src.utils.Database import Database


class Order:
    """Class for managing an order."""

    def __init__(self, order_id: str):
        """Don't call outside of OrderService."""
        self._order_id = order_id

    def get_number(self) -> int:
        """Get order's number."""
        sql = "SELECT number FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)
        assert result is not None
        return result[0]

    def get_status(self) -> OrderStatus:
        """Get order's status."""
        sql = "SELECT status FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        assert result is not None
        return OrderStatus(result[0])

    def get_assigned_staff(self) -> User | None:
        """Get staff member assigned to this order."""
        sql = "SELECT assigned_staff FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        print(result)
        if result is not None and result[0] is not None:
            return User(result[0])

    def set_status(self, status: OrderStatus) -> None:
        """Set order status."""
        sql = "UPDATE public.order SET status = %s WHERE id = %s"
        Database.execute_and_commit(sql, status.value, self._order_id)

    def assign_staff(self, user: User) -> None:
        """Assign given staff to order."""
        sql = "UPDATE public.order SET assigned_staff=%s WHERE id=%s"
        Database.execute_and_commit(sql, user.get_id(), self._order_id)
