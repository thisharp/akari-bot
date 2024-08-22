from datetime import datetime, timedelta, timezone

from config import Config
from core.builtins import Bot
from core.utils.storedata import get_stored_list, update_stored_list


async def gained_petal(msg: Bot.MessageSession, amount: int):
    '''增加花瓣。

    :param msg: 消息会话。
    :param amount: 增加的花瓣数量。
    :returns: 增加花瓣的提示消息。
    '''
    if Config('enable_petal', False) and Config('enable_get_petal', False):
        limit = Config('gained_petal_limit', 10)
        p = get_stored_list(msg.target.client_name, 'gainedpetal')
        if not p:
            p = [{}]
        p = p[0]
        now = datetime.now(timezone.utc) + msg.timezone_offset
        tomorrow = (now + timedelta(days=1)).date()
        expired = datetime.combine(tomorrow, datetime.min.time())
        if msg.target.sender_id not in p:
            p[msg.target.sender_id] = {'time': now.timestamp(), 'amount': amount}
            p = [p]
            msg.info.modify_petal(amount)
            update_stored_list(msg.target.client_name, 'gainedpetal', p)
            return msg.locale.t('petal.message.gained.success', amount=amount)
        else:
            if p[msg.target.sender_id]['time'] > expired.timestamp():
                p[msg.target.sender_id] = {'time': now.timestamp(), 'amount': amount}
                p = [p]
                msg.info.modify_petal(amount)
                update_stored_list(msg.target.client_name, 'gainedpetal', p)
            else:
                if limit > 0:
                    if p[msg.target.sender_id]['amount'] >= limit:
                        return msg.locale.t('petal.message.gained.limit')
                    elif p[msg.target.sender_id]['amount'] + amount > limit:
                        amount = limit - p[msg.target.sender_id]['amount']
                p[msg.target.sender_id]['amount'] += amount
                p = [p]
                msg.info.modify_petal(amount)
                update_stored_list(msg.target.client_name, 'gainedpetal', p)
            return msg.locale.t('petal.message.gained.success', amount=amount)


async def lost_petal(msg: Bot.MessageSession, amount: int):
    '''减少花瓣。

    :param msg: 消息会话。
    :param amount: 减少的花瓣数量。
    :returns: 减少花瓣的提示消息。
    '''
    if Config('enable_petal', False) and Config('enable_get_petal', False):
        limit = Config('lost_petal_limit', 5)
        p = get_stored_list(msg.target.client_name, 'lostpetal')
        if not p:
            p = [{}]
        p = p[0]
        now = datetime.now(timezone.utc) + msg.timezone_offset
        tomorrow = (now + timedelta(days=1)).date()
        expired = datetime.combine(tomorrow, datetime.min.time())
        if msg.target.sender_id not in p:
            p[msg.target.sender_id] = {'time': now.timestamp(), 'amount': amount}
            p = [p]
            msg.info.modify_petal(-amount)
            update_stored_list(msg.target.client_name, 'lostpetal', p)
            return msg.locale.t('petal.message.lost.success', amount=amount)
        else:
            if p[msg.target.sender_id]['time'] > expired.timestamp():
                p[msg.target.sender_id] = {'time': now.timestamp(), 'amount': amount}
                p = [p]
                msg.info.modify_petal(-amount)
                update_stored_list(msg.target.client_name, 'lostpetal', p)
            else:
                if limit > 0:
                    if p[msg.target.sender_id]['amount'] >= limit:
                        return msg.locale.t('petal.message.lost.limit')
                    elif p[msg.target.sender_id]['amount'] + amount > limit:
                        amount = limit - p[msg.target.sender_id]['amount']
                p[msg.target.sender_id]['amount'] += amount
                p = [p]
                msg.info.modify_petal(-amount)
                update_stored_list(msg.target.client_name, 'lostpetal', p)
            return msg.locale.t('petal.message.lost.success', amount=amount)
