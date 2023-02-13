import logging
from flask import Flask, request
from dotenv import dotenv_values

from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from blueprint import v1_blueprint

from managers.investor_manager import InvestorManager
from swagger import swagger
from log import log

app = Flask("investor")
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


# To send information of an investor and store it to the database
@v1_blueprint.route('/investor', methods=['POST'])
def get_investor():
    request_data = request.get_json()
    inv_manager = InvestorManager()
    result = inv_manager.handle_investor(request_data)
    if result:
        logger.info(InfoMessage.INV_SUCCESS)
    return result.generate_response()


# To get the information of an investor from database
@v1_blueprint.route('/investor/<string:user_id>', methods=['GET'])
def info_investor(user_id):
    if user_id is None:
        return logger.error(ErrorMessage.BAD_REQUEST)

    inv_detail = InvestorManager()
    return inv_detail.investor_detail(user_id).generate_response()


# To update the information of an investor
@v1_blueprint.route("/investor", methods=["PUT"])
def update_investor():
    request_data = request.get_json()
    inv_manager = InvestorManager()
    result = inv_manager.investor_update(request_data)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return result.generate_response()


swagger.run_swagger(app)
log.setup_logger()

app.register_blueprint(v1_blueprint)
app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])
