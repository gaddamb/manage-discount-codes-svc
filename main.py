import os

from tornado.ioloop import IOLoop
from tornado.web import Application
from src.handler.discount_code_handler import CreateDiscountHandler, FetchDiscountHandler
from src.config.config import logger

def main():
    
    app = Application(
        [
            ('/createCode', CreateDiscountHandler),
            ('/fetchDiscCode', FetchDiscountHandler),
        ])

    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    logger.info("Server started at port : " + str(port))
    IOLoop.current().start()


if __name__ == '__main__':
    main()