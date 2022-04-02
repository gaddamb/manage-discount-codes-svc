from tornado.web import RequestHandler
import tornado
import json 
import logging
from src.service.discount_code_service import DiscountCodeService

class CreateDiscountHandler(RequestHandler):
    def prepare(self):
        super(CreateDiscountHandler, self).prepare()
        try:
            # Do something with request body
            self.request_payload = tornado.escape.json_decode(self.request.body)

        except json.decoder.JSONDecodeError:
            return self._return_response(self, { "message": 'Cannot decode request body!' }, 400)

    
    async def post(self):
        ds = DiscountCodeService(self.request_payload)

        discount_codes = ds.create_discount_code()

        ds.write_to_data_store(discount_dict=discount_codes)

class FetchDiscountHandler(RequestHandler):
    def prepare(self):
        super(FetchDiscountHandler, self).prepare()
    
    async def get(self):
        ds = DiscountCodeService(None)        
        auth_header = self.request.headers.get('Authorization')
        if auth_header is None:
            self.write("invlid user access")
        elif len(auth_header.split(' ')) > 2 or len(auth_header.split(' ')) == 0:
            self.write("invlid user token")
        else:
            token = auth_header.split(' ')[1]
            self.write(json.dumps(ds.fetch_discount_code_for_user(token)))