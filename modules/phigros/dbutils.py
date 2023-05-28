from tenacity import retry, stop_after_attempt

from core.builtins import Bot
from database import session, auto_rollback_error
from .orm import PgrBindInfo


class PgrBindInfoManager:
    @retry(stop=stop_after_attempt(3), reraise=True)
    @auto_rollback_error
    def __init__(self, msg: Bot.MessageSession):
        self.targetId = msg.target.senderId
        self.query = session.query(PgrBindInfo).filter_by(targetId=self.targetId).first()
        if self.query is None:
            session.add_all([PgrBindInfo(targetId=self.targetId, sessiontoken='', username='Guest')])
            session.commit()
            self.query = session.query(PgrBindInfo).filter_by(targetId=self.targetId).first()

    @retry(stop=stop_after_attempt(3), reraise=True)
    @auto_rollback_error
    def get_bind_info(self):
        sessiontoken = self.query.sessiontoken
        if sessiontoken != '':
            return sessiontoken, self.query.username
        return None

    @retry(stop=stop_after_attempt(3), reraise=True)
    @auto_rollback_error
    def set_bind_info(self, sessiontoken, username='Guest'):
        self.query.sessiontoken = sessiontoken
        self.query.username = username
        session.commit()
        return True

    @retry(stop=stop_after_attempt(3), reraise=True)
    @auto_rollback_error
    def remove_bind_info(self):
        session.delete(self.query)
        session.commit()
        return True
