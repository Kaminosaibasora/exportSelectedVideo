import logging

class Log :
    def __init__(self, file) -> None:
        self.format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            filename = file,
            filemode = "w",
            format   = self.format, 
            level    = logging.DEBUG
        )
        self.logger = logging.getLogger()

    def setLoggerLevel(self, lvl):
        if lvl == "DEBUG" :
            self.logger.setLevel(logging.DEBUG)
        elif lvl == "INFO" :
            self.logger.setLevel(logging.INFO)
        elif lvl == "ERROR" :
            self.logger.setLevel(logging.ERROR)
        elif lvl == "CRITICAL" :
            self.logger.setLevel(logging.CRITICAL)
    
    def debug(self, mes):
        self.logger.debug(mes)

    def info(self, mes):
        self.logger.info(mes)

    def warning(self, mes):
        self.logger.warning(mes)

    def error(self, mes):
        self.logger.error(mes)
        