import sys 
from network_security.logging import logger

class NetworkSecurityException(Exception):
    #Check out error message and details 
    def __init__(self, error_message, error_details :sys) :
        self.error_message = error_message 
        _,_,exc_tb = error_details.exc_info()
        #Get the line number and file name where the error occured
        self.lineno = exc_tb.tb_lineno
        #Get the file name where the error occured
        self.filename = exc_tb.tb_frame.f_code.co_filename 

    def __str__(self):
        return f"Error: {self.error_message} at {self.filename} line {self.lineno}"
    
if __name__ == "__main__":
    try:
        logger.logging.info("Enter the try block")
        a = 1/0
        print("This will not print",a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)