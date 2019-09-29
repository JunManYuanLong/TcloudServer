from abc import ABC

from aredis import StrictRedis
from tornado import websocket, web, ioloop, httpserver, gen
from tornado.options import define, options

from public_config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_DB

"""
优化方案：
监听当前用户的redis_key，看未读消息数，有变化就去返回该消息数，否则返回ping/pong
"""

define("port", default=9040, help="run on the given port", type=int)
redis_client = StrictRedis(host=REDIS_HOST, password=REDIS_PASSWORD,
                           port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


class MessageWSHandler(websocket.WebSocketHandler, ABC):
    """
    @api {ws} /v1/ws/message 站内信websocket接口
    @apiName MessageWsApi
    @apiGroup WebSocket
    @apiDescription 每隔几秒接收后端传来的数据，根据code判断是否未读数发生改变 来改变前端展示，前端打开未读弹窗时，再请求message接口获取最新消息
    @apiParam {int} user 用户ID
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     # 连接建立成功
     {
       "code": 0,
       'message': '连接成功'
     }
     # 传输数据中，未读数发生改变
     {
       "code": 0,
       'unread_count': 3
     }
     # 传输数据中，未读数未发生改变或没有未读数
     {
       "code": 101
     }
    """

    # CORS
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message({'code': 0, 'message': '连接成功'})

    async def on_message(self, message):
        user = self.get_argument('user', '')
        if not user:
            await self.write_message({'code': 411, 'message': '缺少用户id'})
        else:
            unread_count = 0
            while True:
                # 访问redis
                try:
                    nums_str = await redis_client.get(f'message_{user}')
                    if nums_str and nums_str.isdigit():
                        nums = int(nums_str)
                        if unread_count != nums:
                            unread_count = nums
                            await self.write_message({'code': 0, 'unread_count': unread_count})
                        else:
                            await self.write_message({'code': 101})
                    else:
                        await self.write_message({'code': 101})
                    await gen.sleep(5)
                except websocket.WebSocketClosedError:
                    self.on_close()
                    break

    def on_close(self):
        pass


class HealthyCheckHandler(web.RequestHandler, ABC):
    def get(self):
        self.write("Hello, world")


def make_app():
    return web.Application([
        ("/v1/ws/message", MessageWSHandler),
        ("/v1/ws/healthycheck", HealthyCheckHandler)
    ])


def main():
    ws_app = make_app()
    options.parse_command_line()
    server = httpserver.HTTPServer(ws_app)
    server.listen(options.port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        ioloop.IOLoop.current().stop()
        ioloop.IOLoop.current().close(True)
