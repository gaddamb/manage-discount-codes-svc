from src.service.discount_code_service import DiscountCodeService
from pytest_bdd import given, when, then, scenario, parsers
from src.config.config import config
import logging

@scenario("features/tc_manage_discount_codes.feature", "As a brand I want to have discount codes generated for me so that I don’t have to deal with this administration myself.")
def test_create_discount_codes():
    pass

@given(parsers.parse("number {noOfDiscountCodes} of codes to be generated"), target_fixture="context")
def given_number_codes_to_be_generated(noOfDiscountCodes):
    context = dict(noOfDiscountCodes = int(noOfDiscountCodes))
    return context

@when('the service end point is called')
def when_req_is_made_to_service(context):    
    ds = DiscountCodeService(context, config(filename='src/config/config_test.ini'))
    discount_codes = ds.create_discount_code()
    ds.write_to_data_store(discount_dict=discount_codes)
    context['discount_codes'] = discount_codes

@then('generate the codes and store in data store.')
def verify_the_generated_codes(context):
    logging.info(context['discount_codes'])
    assert 0 < len(context['discount_codes'])
    assert int(context['noOfDiscountCodes']) == len(context['discount_codes']['discount_code'])


