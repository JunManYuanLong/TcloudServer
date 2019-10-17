from apps.public.models.guest import Guest
from library.api.db import db
from library.api.render import row2list


def get_guest_info():
    guest_query = Guest.query.add_columns(
        Guest.ip,
        Guest.platform,
        Guest.browser,
        Guest.string,
        Guest.version,
        Guest.count
    ).all()
    data = row2list(guest_query)
    return 0, data


def record_guest(ip, user_agent):
    # ip = request.remote_addr
    # user_agent = request.user_agent
    platform = user_agent.platform
    browser = user_agent.browser
    string = user_agent.string
    version = user_agent.version

    ret = Guest.query.filter(Guest.ip == ip,
                             Guest.platform == platform,
                             Guest.browser == browser,
                             Guest.version == version,
                             ).first()
    with db.auto_commit():
        if ret:
            ret.count += 1
        else:
            ret = Guest(
                ip=ip,
                platform=platform,
                browser=browser,
                string=string,
                version=version
            )
        db.session.add(ret)
