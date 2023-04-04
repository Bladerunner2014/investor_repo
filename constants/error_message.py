class ErrorMessage:

    BAD_REQUEST = "field missing"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not found"
    INTERNAL_ERROR = "internal error"
    ALREADY_EXISTS = "already exists"

    NEED_VALIDATION = "need validation"

    MIDGARD_ERROR_LOGS = {
        "REQUEST_TIMEOUT": "midgard request timeout",
        "CONNECTION_ERROR": "midgard connection error",
        "REQUEST_ERROR": "midgard request error"
    }

    DB_CONNECTION = "db connection error"
    DB_GET_CONNECTION_POOL = "db get connection from pool error"
    DB_CLOSE_CURSOR_CONNECTION = "db close cursor error"
    DB_PUT_CONNECTION_TO_POOL = "db put connection to pool error"
    DB_INSERT = "db insert error"
    DB_SELECT = "db select error"
    AUTH_INSERT = "auth insert error"
    URL_INSERT = "url insert error"
    INV_INSERT = "investor insert error"

    REDIS_CONNECTION = "redis connection error"
    REDIS_SET = "redis SET error"
    REDIS_GET = "redis GET error"
    REDIS_DELETE = "object does not exists"

    AUTH_SET = "auth SET error"
    VALIDATION_SET = "validation SET error"
    VALIDATION_GET = "validation GET error"

    KAFKA_PRODUCE = "kafka produce error"
    KAFKA_PRODUCE_HERMOD = "kafka produce hermod topic error"
    KAFKA_CONSUME = "kafka consume error"

