import sys
import traceback
import logging
from datetime import datetime
from helpers import save_data, json_to_html, send_email


class ExceptionHandler:
    """
    A class that handles exceptions and logs detailed information about them.
    Attributes:
        log_file (str): The name of the log file to store the exception information. Default is 'error_log.log'.
        log_level (int): The logging level for the exception. Default is logging.ERROR.
        log_format (str): The format of the log messages. Default is '%(asctime)s:%(levelname)s:%(message)s'.
    """

    def __init__(self, client, config, log_file='error_log.log', log_level=logging.ERROR, log_format='%(asctime)s:%(levelname)s:%(message)s'):
        """Initialize the ExceptionHandler with custom logging settings."""
        logging.basicConfig(filename=log_file,level=log_level, format=log_format)

        self.client = client
        self.config = config

    async def get_exception(self, exception, send_email=True):
        """Capture, log, and store detailed information about an exception."""
        error_info = {
            "error_message": str(exception),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat(),
            "exception_type": type(exception).__name__,
            "exception_args": exception.args,
            "exception_module": type(exception).__module__,
            "exception_file": exception.__traceback__.tb_frame.f_code.co_filename,
            "exception_line": exception.__traceback__.tb_lineno,
            "status": "pending"
        }

        # Store error information in the database and send an email
        if error_info:
            await self.store_error(error_info)
            if send_email:
                await self.send_error_report(error_info)

        return error_info

    async def handle_uncaught_exception(self, exc_type, exc_value, exc_traceback, send_email=False):
        """Handle uncaught exceptions."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        error_info = {
            "error_message": str(exc_value),
            "traceback": ''.join(traceback.format_tb(exc_traceback)),
            "timestamp": datetime.now().isoformat(),
            "exception_type": exc_type.__name__,
            "exception_args": exc_value.args,
            "exception_module": exc_type.__module__,
            "status": "pending"
        }
        logging.error(f"Uncaught Exception: {error_info}")

        # Store and/or email the error info
        if error_info:
            await self.store_error(error_info)
            if send_email:
                await self.send_error_report(error_info)

        return error_info

    async def store_error(self, error_info):
        """
        Store error information in the database using OpenIAP.

        Args:
            error_info (dict): Dictionary containing error details.
            client: OpenIAP client for database interaction.
        """
        try:
            success = await save_data(self.client, 'process_errors', [error_info])
            if success:
                logging.info(
                    "Error information stored in database successfully.")
            else:
                logging.error("Failed to store error information in database.")
        except Exception as e:
            logging.error(f"Exception while storing error information: {e}")

    async def send_error_report(self, error_info):
        """
        Sends an error report via email.

        Args:
            subject (str): The subject of the email.
            to (str): The recipient email address.
            error_info (dict): Information about the error.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        subject = self.config["report"]['subject']
        to = self.config["report"]['to']

        # Email settings
        message_body = json_to_html(error_info)

        if send_mail := await send_email(self.client, to, subject, message_body, html_body=True):
            return send_mail
