from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect, QWidget
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt, QPoint
from PyQt5.QtGui import QFont
from typing import List

from pyqtier.static.qss.styles import NOTIFICATION_STYLES


class _Notification(QLabel):

    def __init__(self, parent: QWidget, message: str, message_type: str, position: QPoint, on_closed: callable):
        super().__init__(parent)
        self._on_closed = on_closed
        self._is_closing = False

        self.setText(message)
        self.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.setWordWrap(True)
        self.setFixedWidth(330)
        self.setStyleSheet(NOTIFICATION_STYLES.get(message_type, NOTIFICATION_STYLES['info']))
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        self.adjustSize()
        self.move(position)
        self.show()
        self._fade_in()

    def _fade_in(self):
        self._animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self._animation.setDuration(300)
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._animation.start()

    def close_notification(self):
        if self._is_closing:
            return
        self._is_closing = True

        self._animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self._animation.setDuration(300)
        self._animation.setStartValue(1.0)
        self._animation.setEndValue(0.0)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._animation.finished.connect(lambda: (self._on_closed(self), self.deleteLater()))
        self._animation.start()

    def mousePressEvent(self, event):
        self.close_notification()


class NotificationMixin:
    _MARGIN = 20
    _SPACING = 10

    def _get_notifications(self) -> List[_Notification]:
        if not hasattr(self, '_notifications'):
            self._notifications = []
        return self._notifications

    def _calculate_position(self) -> QPoint:
        parent_rect = self.rect()
        x = parent_rect.width() - 330 - self._MARGIN
        y = parent_rect.height() - self._MARGIN - 50
        return QPoint(x, y)

    def _on_notification_closed(self, notification: _Notification):
        notifications = self._get_notifications()
        if notification in notifications:
            notifications.remove(notification)
            self._reposition_notifications()

    def _reposition_notifications(self):
        parent_rect = self.rect()
        y = parent_rect.height() - self._MARGIN

        for notif in reversed(self._get_notifications()):
            y -= notif.height()
            notif.move(parent_rect.width() - notif.width() - self._MARGIN, y)
            y -= self._SPACING

    def _show_notification(self, message: str, message_type: str, duration: int):
        notification = _Notification(
            parent=self,
            message=message,
            message_type=message_type,
            position=self._calculate_position(),
            on_closed=self._on_notification_closed
        )
        self._get_notifications().append(notification)

        self._reposition_notifications()

        if duration > 0:
            QTimer.singleShot(duration, notification.close_notification)

    def notify_success(self, message: str, duration: int = 3000):
        self._show_notification(message, 'success', duration)

    def notify_error(self, message: str, duration: int = 4000):
        self._show_notification(message, 'error', duration)

    def notify_warning(self, message: str, duration: int = 3500):
        self._show_notification(message, 'warning', duration)

    def notify_info(self, message: str, duration: int = 3000):
        self._show_notification(message, 'info', duration)

    def clear_notifications(self):
        for notif in self._get_notifications()[:]:
            notif.close_notification()
