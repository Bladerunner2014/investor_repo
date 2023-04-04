import logging
from flask import Flask, request
from dotenv import dotenv_values

from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from blueprint import v1_blueprint
from constants.status_code import StatusCode
from managers.investor_manager import InvestorManager
from swagger import swagger
from log import log

app = Flask("investor")
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


# To send information of an investor and store it to the database
@v1_blueprint.route('/investor', methods=['POST'])
def get_investor():
    user_id = request.headers.get('user_id')
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    request_data = request.get_json()
    print(request_data)
    print(user_id)
    inv_manager = InvestorManager()
    result = inv_manager.handle_investor(request_data, user_id)

    return result.generate_response()


# To get the information of an investor from database
@v1_blueprint.route('/investor', methods=['GET'])
def info_investor():
    user_id = request.headers.get('user_id')

    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST

    inv_detail = InvestorManager()
    return inv_detail.investor_detail(user_id).generate_response()


@v1_blueprint.route('/investor/id', methods=['GET'])
def info_investor_by_id():
    investor_id = request.headers.get('investor_id')

    if investor_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST

    inv_detail = InvestorManager()
    return inv_detail.investor_by_id(investor_id).generate_response()


# To update the information of an investor
@v1_blueprint.route("/investor", methods=["PUT"])
def update_investor():
    request_data = request.get_json()
    user_id = request.headers.get('user_id')
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST

    inv_manager = InvestorManager()
    result = inv_manager.investor_update(request_data, user_id)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return result.generate_response()


swagger.run_swagger(app)
log.setup_logger()

app.register_blueprint(v1_blueprint)
app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])
