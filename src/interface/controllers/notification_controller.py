from logging import getLogger

from domain.Notification.notification import Notification
from domain.Notification.database.notification_repository import (
    NotificationRepository,
)
from domain.Notification.usecase.notification_interactor import (
    NotificationInteractor,
)
from infrastructure.database.postgres.sqlhandler import SqlHandler

from exceptions.database import DuplicateKeyError
from exceptions.waf import DuplicateKeyHTTPException

logger = getLogger("daizu").getChild("NotificationController")


class NotificationController:
    def __init__(self, sqlhandler: SqlHandler):
        self.interactor = NotificationInteractor(
            NotificationRepository(sqlhandler)
        )

    async def notifications(self):
        notifications = []
        resp = dict()
        for notification in self.interactor.notifications():
            notifications.append(notification.as_json())

        resp["data"] = notifications
        resp["status"] = "Success"

        return resp

    async def create(self, notification: Notification):
        # I don't have to check Duplicate because id is generated by uuid.
        resp = dict()
        _id: str = notification.id

        try:
            self.interactor.store(notification)
            resp["status"] = "Success"
            resp["message"] = "Create notification"
        except DuplicateKeyError as e:
            message = f"Duplicate key. (key: {_id})"
            logger.debug(message, e)
            raise DuplicateKeyHTTPException()

        return resp

    async def update(self, notification: Notification):
        resp = {
            "status": "Success",
            "message": "Update notification",
        }
        self.interactor.update(notification)

        return resp

    async def delete(self, id: str):
        resp = {
            "status": "Success",
            "message": f"Delete notification. (notification={id})",
        }
        self.interactor.delete(id)

        return resp
