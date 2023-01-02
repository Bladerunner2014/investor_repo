import json
import logging
import requests

from constants.status_code import StatusCode


class RequestHandler:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_post_request(self, host: str, port: str, body: dict, timeout: str, error_log_dict: dict) -> (dict, int):
        """
        post_request send post request .

        :param host: destination host
        :param port: destination port
        :param body: request body
        :param timeout: request timeout
        :param error_log_dict: error log dictionary for specified destination service
        :return: returns the response
        """
        default_headers = {"Content-Type": "application/json"}
        try:
            r = requests.post(url=host + ":" + port, json=json.dumps(body), headers=default_headers,
                              timeout=int(timeout))
        except requests.exceptions.Timeout as error:
            self.logger.error(error_log_dict["REQUEST_TIMEOUT"])
            self.logger.error(error)
            raise error
        except requests.exceptions.ConnectionError as error:
            self.logger.error(error_log_dict["CONNECTION_ERROR"])
            self.logger.error(error)
            raise error
        except Exception as error:
            self.logger.error(error_log_dict["REQUEST_ERROR"])
            self.logger.error(error)
            raise error
        if r.status_code == StatusCode.SUCCESS:
            return r.json(), r.status_code
        else:
            return r.text, r.status_code

    def send_put_request(self, host: str, port: str, body: dict, timeout: str, error_log_dict: dict) -> (dict, int):
        """
        post_request send post request .

        :param host: destination host
        :param port: destination port
        :param body: request body
        :param timeout: request timeout
        :param error_log_dict: error log dictionary for specified destination service
        :return: returns the response
        """
        default_headers = {"Content-Type": "application/json"}
        try:
            r = requests.put(url=host + ":" + port, json=json.dumps(body), headers=default_headers,
                             timeout=int(timeout))
        except requests.exceptions.Timeout as error:
            self.logger.error(error_log_dict["REQUEST_TIMEOUT"])
            self.logger.error(error)
            raise error
        except requests.exceptions.ConnectionError as error:
            self.logger.error(error_log_dict["CONNECTION_ERROR"])
            self.logger.error(error)
            raise error
        except Exception as error:
            self.logger.error(error_log_dict["REQUEST_ERROR"])
            self.logger.error(error)
            raise error
        if r.status_code == StatusCode.SUCCESS:
            return r.json(), r.status_code
        else:
            return r.text, r.status_code

    @staticmethod
    def create_json_from_args(**kwargs):
        return locals()["kwargs"]


