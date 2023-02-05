from constants.status_code import StatusCode
from dao.investor_dao import InvestorDao
from http_handler.response_handler import ResponseHandler
from models.investors import InvestorsDB
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
import logging

from dotenv import dotenv_values
from constants.enums import SubLevel


# to handle the routes
class InvestorManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = InvestorDao()

    # insert new investor to the database
    def handle_investor(self, dt: dict):

        investor = InvestorsDB()
        investor.user_id = dt['user_id']
        investor.api_key = dt['api_key']
        investor.is_subscribe = True
        investor.exchange = dt.get('exchange', "binance")
        investor.sub_level = SubLevel(dt['sub_level']).name
        investor.expire_date = dt['expire_date']
        # investor.secret_key = dt['secret_key']

        try:
            self.dao.insert_new_investor(investor)
        except Exception as error:
            self.logger.error(ErrorMessage.INV_INSERT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        res.set_status_code(StatusCode.SUCCESS)
        res.set_response({"message": InfoMessage.INV_SUCCESS})
        return res

    # return the information of an investor
    def investor_detail(self, user_id):

        try:
            result = self.dao.select_investor(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception

        res = ResponseHandler()
        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            result = ErrorMessage.DB_SELECT
            res.set_status_code(StatusCode.NOT_FOUND)
        else:
            res.set_status_code(StatusCode.SUCCESS)

        res.set_response({"message": result})
        return res

    # update the information of an investor
    def investor_update(self, data: dict):
        try:
            result = self.dao.select_investor(data["user_id"])
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()

        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            res.set_status_code(StatusCode.NOT_FOUND)
            res.set_response({"message": ErrorMessage.DB_SELECT})
            return res
        else:

            try:
                self.dao.update_investor(data)
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.INV_UPDATE})

            return res
