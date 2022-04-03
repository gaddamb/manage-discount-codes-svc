import os

from tornado.ioloop import IOLoop
from tornado.web import Application
from src.handler.discount_code_handler import CreateDiscountHandler, FetchDiscountHandler


def main():
    
    app = Application(
        [
            ('/createCode', CreateDiscountHandler),
            ('/fetchDiscCode', FetchDiscountHandler),
        ])

    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()