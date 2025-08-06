import sys
import logging
from src.logger import logging  


def error_message_detail(error: Exception, sys_detail: sys) -> str:
    """
    Extracts detailed error information including file name, line number, and the error message.
    """
    _, _, exc_tb = sys_detail.exc_info()  # Extract traceback

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in file [{file_name}] at line [{line_number}]: {str(error)}"
    )

    logging.error(error_message)  # Log automatically
    return error_message




class MyException(Exception):
    """
    Custom Exception class to handle errors efficiently and improve tracking.
    """

    def __init__(self, error_message: str, sys_detail: sys):
        super().__init__(error_message)  
        self.error_message = error_message_detail(error_message, sys_detail)

        

    def __str__(self) -> str:
        """Return the string representation of the error message."""
        return self.error_message
