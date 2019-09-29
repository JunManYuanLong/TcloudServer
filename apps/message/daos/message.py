from sqlalchemy import func, desc

from apps.message.models.message import Content, Message
from library.api.db import db
# from library.api.db import t_redis
from library.api.exceptions import SaveObjectException
from library.api.render import row2list

"""站内性的一些构思

当前只用到了第一种

第一种 点到个别
  采用和私信相同的方式，在发送一条消息时在Content表中插入消息内容并且设置Type=Private,同时在Message表中插入多条记录设置RecID=各接收者ID，Status=未读
  
  用户B查找RecID=B,并且Staus为未读，Type=Private,显示为私信未读，点击阅读后改变Status=已读

  用户B查找RecID=B,并且Staus为已读，Type=Private,显示为私信已读，删除设置Status=删除

第二种 点到局部
   点到局部是一对某角色或某用户组发送，例如管理员向普通用户组发送，在Content表插入消息内容，且设置Type=Public 和Group为用户组ID

   用户登录后分两种情况：

  1、未找到RecId=自己ID 且 Content中（Type=Public 和Group=自己所在组 ）  的消息ID不包含在Messgae的MessageID中

       提取出来显示为用户公共消息未读，在用户点击阅读的时候，将消息阅读状态写入Messgae表，Status=已读。

  2、找到RecId=自己ID 且 Content中（Type=Public 和Group=自己所在组 ） 的消息ID包含在Messgae的MessageID中

      将此部分消息提取出来，显示为用户公共消息已读，如果想“删除”（当然是逻辑上的删除，并非物理数据库删除），设置该Status=删除。

      注：此时可以不验证Group=自己所在组

第三种 点到全部
    点到全部和点到局部采用类似的处理方式。例如管理员向普通用户组发送，在Content表插入消息内容，且设置Type=Global

    用户登录后分两种情况：

    1、未找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID不包含在Messgae的MessageID中

        提取出来显示为用户系统消息未读，在用户点击阅读的时候，将消息阅读状态写入Messgae表，Status=已读。

    2、找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID包含在Messgae的MessageID中

        将此部分消息提取出来，显示为用户系统消息已读，如果想“删除”（逻辑上的删除，并非物理数据库删除），设置该Status=删除。


处理流程

1、Messgae表中RecId=自己ID 且Status=未读，显示为私信未读
2、Messgae表中RecId=自己ID 且Status=已读 且 Type=Private,显示为私信已读
3、Messgae表中未找到RecId=自己ID 且 Content中（Type=Public 和Group=自己所在组 ） 的消息ID不包含在Messgae的MessageID中，显示为公共消息未读            
4、Messgae表中找到RecId=自己ID 且 Content中（Type=Public ） 的消息ID包含在Messgae的MessageID中 ，显示为公共消息已读
5、Messgae表中未找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID不包含在Messgae的MessageID中 ，显示为系统消息未读
6、Messgae表中找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID包含在Messgae的MessageID中 ，显示为系统消息已读

"""

# 需配置redis，解除注释
def push2redis(user):
    pass
    # count = _get_unread_count(user)
    # if isinstance(count, int):
    #     t_redis.set(f'message_{user}', count)


def create_by_one2one(send_id, rec_ids, content, message_type, group):
    """
    创建一条私密消息，用于少量用户的流程通知
    :param send_id: 发送者
    :param rec_ids: 接收者
    :param content: 内容
    :param message_type: 类型
    :param group: 用户组
    :return: code
    """
    rec_ids = list(set(rec_ids))
    if not message_type:
        message_type = Content.PRIVATE
    if not group:
        group = 'public'
    if send_id is not None and content:
        with db.auto_commit():
            content = Content(send_id=send_id, content=content, type=message_type, group=group)
            db.session.add(content)
            db.session.flush()
            content_id = content.id
            if content_id:
                with db.auto_commit():
                    for i in rec_ids:
                        db.session.add(Message(rec_id=int(i), content_id=content_id, status=Message.UNREAD))
        for i in rec_ids:
            push2redis(i)
        return 0
    raise SaveObjectException()


def _get_message_query_by_user_id(user_id):
    ret = Message.query.outerjoin(
        Content, Message.content_id == Content.id).add_columns(Content.content.label('content'),
                                                               Message.status.label('status'),
                                                               Message.id.label('id'),
                                                               func.date_format(Content.create_time,
                                                                                "%Y-%m-%d %H:%i:%s").label(
                                                                   'create_time')).filter(
        Message.rec_id == user_id, Content.type == Content.PRIVATE, Message.status != Message.DISABLE).order_by(
        desc(Message.id))
    return ret


# 获取未读的通知
def _get_unread_count(user_id):
    count = Message.query.filter(Message.rec_id == user_id, Message.status == Message.UNREAD).count()
    return count


def get_all_message_by_user_id(user_id, page_size, page_index):
    total = _get_message_query_by_user_id(user_id).count()
    messages = _get_message_query_by_user_id(user_id).limit(
        int(page_size)).offset((int(page_index) - 1) * int(page_size)).all()
    data = row2list(messages)
    return 0, data, total


def get_5_message_by_user_id(user_id):
    """
    获取一个用户10最近10信息，不论已读或者未读
    :param user_id: 用户
    :return: ['id', 'content', 'status', 'create_time']
    """
    # ret_user = user_trpc.requests('get', '/test')
    # if not ret_user:
    #     raise Exception("Error:cls.user_trpc.requests('get', '/allflow')")

    messages = _get_message_query_by_user_id(user_id).filter(Message.status == Message.UNREAD).limit(5).all()
    data = row2list(messages)
    if len(data) < 5:
        rows = 5 - len(data)
        rows_messages = _get_message_query_by_user_id(user_id).filter(
            Message.status != Message.UNREAD).limit(rows).all()
        rows_data = row2list(rows_messages)
        if rows_data:
            data.extend(rows_data)
    total = len(data)
    return 0, data, total


def get_all_read_message_by_user_id(user_id, page_size, page_index):
    total = _get_message_query_by_user_id(user_id).filter(
        Message.status == Message.READ).count()

    messages = _get_message_query_by_user_id(user_id).filter(
        Message.status == Message.READ).limit(
        int(page_size)).offset((int(page_index) - 1) * int(page_size)).all()
    data = row2list(messages)
    return 0, data, total


def get_all_unread_message_by_user_id(user_id, page_size, page_index):
    total = _get_message_query_by_user_id(user_id).filter(
        Message.status == Message.UNREAD).count()
    messages = _get_message_query_by_user_id(user_id).filter(
        Message.status == Message.UNREAD).limit(
        int(page_size)).offset((int(page_index) - 1) * int(page_size)).all()
    data = row2list(messages)
    return 0, data, total


def delete_status(user, message_ids=None, isall=None):
    """
    修改通知的状态，已读改为1，删除改为2
    :return: 修改成功
    """
    if message_ids:
        with db.auto_commit():
            query = f"UPDATE message SET status={Message.DISABLE} WHERE rec_id={user} and id in ({message_ids})"
            db.engine.execute(query)
        push2redis(user)
        return 0, ''
    elif isall:
        with db.auto_commit():
            query = f"UPDATE message SET status={Message.DISABLE} WHERE rec_id={user}"
            db.engine.execute(query)
        push2redis(user)
        return 0, ''
    else:
        raise SaveObjectException()


def change_status(user, message_ids=None, isall=None):
    if message_ids:
        with db.auto_commit():
            query = f"UPDATE message SET status={Message.READ} WHERE rec_id={user} and id in ({message_ids})"
            db.engine.execute(query)
        push2redis(user)
        return 0, ''
    elif isall:
        with db.auto_commit():
            query = f"UPDATE message SET status={Message.READ} WHERE rec_id={user}"
            db.engine.execute(query)
        push2redis(user)
        return 0, ''
    else:
        raise SaveObjectException()
