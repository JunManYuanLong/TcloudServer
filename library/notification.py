from flask import current_app, g

from library.trpc import Trpc


class Notification:
    def __init__(self):
        self.public_trpc = Trpc('public')
        self.message_trpc = Trpc('message')

    def send_notification(self, user_ids, text, creator=None, send_type=None):
        if not isinstance(user_ids, list):
            current_app.logger.warn(f'[接收者格式错误] {text}:{user_ids}')
            return
        user_ids = list(set(user_ids))
        if None in user_ids:
            current_app.logger.warn(f'[没有处理人，不发送通知] {text}:{user_ids}')
            return
        is_wx = 1
        is_message = 1
        if creator is None:
            creator = g.userid
        # 此时发送微信，不发送站内信
        if send_type == 1:
            is_wx = 1
            is_message = 0
        # 此时发送站内信，不发送微信
        elif send_type == 2:
            is_wx = 0
            is_message = 1

        if is_wx:
            result = self.public_trpc.requests('post', '/public/wxmessage', body={'user_ids': user_ids, 'text': text})
            if result == 'success':
                current_app.logger.info('发送企业微信通知成功')
            else:
                current_app.logger.warn('发送企业微信通知失败')
        if is_message:
            if self.message_trpc.requests('post', '/message',
                                          body={'send_id': creator, 'rec_id': user_ids, 'content': text}) is not None:
                current_app.logger.info('发送站内信成功')
            else:
                current_app.logger.warn('发送站内信失败')


notification = Notification()
