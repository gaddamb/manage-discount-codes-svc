from src.config.config import config
from src.service.discount_code_service import DiscountCodeService
from pytest_bdd import given, when, then, scenario, parsers
import logging

@scenario("features/tc_manage_discount_codes.feature", "As a logged in user I want to be able to get a discount code so that I can get a discount on a purchase.")
def test_get_discount_codes():
    pass

@given(parsers.parse("an authenticated user with {token}"), target_fixture="context")
def given_a_token(token):
    context = dict(token = token)
    return context

@when('the service end point is called to get a discount')
def when_req_is_made_to_service(context):    
    ds = DiscountCodeService(None, config=config(filename='src/config/config_test.ini'))
    discount_code = ds.fetch_discount_code_for_user(context['token'])
    context['discount_code'] = discount_code

@then('return with a discount code and percentage')
def verify_the_generated_codes(context):
    logging.info(context['discount_code'])
    assert 0 < len(context['discount_code'])


