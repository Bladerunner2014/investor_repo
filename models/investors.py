import datetime
from datetime import timezone


# Class of investors
class InvestorsDB:
    __table_name__ = 'investors_table'
    id = 'id'
    user_id = 'user_id'
    api_key = 'api_key'
    is_subscribe = 'is_subscribe'
    exchange = 'exchange'
    expire_date = 'expire_date'
    sub_level = 'sub_level'
    created_at = 'created_at'
    updated_at = 'updated_at'

    def __init__(self):
        self.created_at = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        self.updated_at = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
