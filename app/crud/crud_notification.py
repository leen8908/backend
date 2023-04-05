from typing import Any, Dict, Optional, List
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.models.notification_template import NotificationTemplate
from app.schemas.notification import NotificationCreate, NotificationUpdate


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_by_sender_uuid(self, db: Session, *, sender_uuid: UUID) -> Optional[List[str]]:
        notification_text_list = []
        notifications = db.query(Notification).filter(
            Notification.sender_uuid == sender_uuid).all()
        for notification in notifications:
            notification_text = db.query(NotificationTemplate).filter(
                NotificationTemplate.template_uuid == notification.template_uuid).first().text
            # loop to replace
            for idx, f in enumerate(notification.f_string.split(';')):
                notification_text = notification_text.replace('{'+str(idx)+'}', f)
            notification_text_list.append(notification_text)
        return notification_text_list

    def get_by_receiver_uuid(self, db: Session, *, receiver_uuid: UUID) -> Optional[List[str]]:
        notification_text_list = []
        notifications = db.query(Notification).filter(
            Notification.receiver_uuid == receiver_uuid).all()
        for notification in notifications:
            notification_text = db.query(NotificationTemplate).filter(
                NotificationTemplate.template_uuid == notification.template_uuid).first().text
            # loop to replace
            for idx, f in enumerate(notification.f_string.split(';')):
                notification_text = notification_text.replace('{'+str(idx)+'}', f)
            notification_text_list.append(notification_text)
        return notification_text_list

    # TODO: unfinished
    def create(self, db: Session, *, obj_in: NotificationCreate, from_MQ: bool) -> Notification:
        # TODO: notification寫入資料庫的時機? sender => 進到MQ前就存? receiver => 從MQ收到才存?
        # 發送通知
        if not from_MQ:
            notification_text = db.query(NotificationTemplate).filter(
                NotificationTemplate.template_uuid == obj_in.template_uuid).first()
            # loop to replace
            for idx, f in enumerate(obj_in.f_string.split(';')):
                notification_text = notification_text.replace('{'+str(idx)+'}', f)

            db_obj = Notification(
                notification_uuid=uuid.uuid4(),  # generate a uuid as notification_uuid
                receiver_uuid=obj_in.receiver_uuid,
                sender_uuid=obj_in.sender_uuid,
                send_time=obj_in.send_time,
                template_uuid=obj_in.template_uuid,  # ?
                f_string=notification_text
            )
        # 接收通知
        else:
            pass
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


notification = CRUDNotification(Notification)
