import logging


class BotLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger("bot_logger")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, level, message):
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)

    def log_info(self, message):
        self.log('info', message)

    def log_error(self, message):
        self.log('error', message)

    def log_debug(self, message):
        self.log('debug', message)
        print(message)

logger = BotLogger('bot.log')



