from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response

from lib.data import DB
from notify.handler import Notify
from notify.model import NotificationRequest, NotificationResponse


def notify(db: DB) -> APIRouter:

    router = APIRouter(
        prefix="/notify",
        tags=["notify"],
    )

    def get_handler() -> Notify:
        return Notify(db)

    # set healthcheck endpoint
    @router.get("/health")
    async def health() -> Response:
        return Response(status_code=200)

    @router.get("/notifications/{user_id}")
    async def get_notifications_user(
        handler: Annotated[Notify, Depends(get_handler)],
        user_id: int,
    ) -> Sequence[NotificationResponse]:
        return handler.get_notifications(user_id)

    @router.post("/notification")
    async def post_notification(
        handler: Annotated[Notify, Depends(get_handler)], req: NotificationRequest
    ) -> NotificationResponse:
        return handler.post_notification(req)
    
    @router.post("/notification/{notificaiton_id}")
    async def post_notification(
        handler: Annotated[Notify, Depends(get_handler)],
        notificaiton_id: int,
    ) -> NotificationResponse:
        return handler.post_notification(notificaiton_id)

    return router
