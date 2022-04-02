
from src.utils.utils import generate_random_code
import pandas as pd
from src.config.config import config
from os.path import exists
import shutil
import time

class DiscountCodeService():
    
    def __init__(self, data) -> None:
        self.data =  data
        if data is not None and config()['create_new_data_store']:        
            self.data_store_struct = {'discount_code':  [] , 'percentage':  [] , 'is_active':  [] , 'user_id':  [] }
            self.create_data_store()
        
    def create_data_store(self):    
        if exists('data/discount_table.csv'):
            file_name = 'discount_table_' + time.strftime("%Y%m%d-%H%M%S") 
            shutil.move('data/discount_table.csv', 'data/{}.csv'.format(file_name))
        self.write_to_data_store(self.data_store_struct)


    def create_discount_code(self):
        no_disc_code_to_generate = self.data.get('noOfDiscountCodes', 1)
        discount_codes = []
        percentages= []
        active_states = []
        user_ids = []
        for i in range(int(no_disc_code_to_generate)):
            code, percentage = generate_random_code()
            discount_codes.append(code)
            percentages.append(percentage)
            active_states.append('active')
            user_ids.append('')
        
        discount_dict = {
            'discount_code' : discount_codes,
            'percentage' : percentages,
            'is_active' : active_states,
            'user_id': user_ids
        }
        return discount_dict

    def write_to_data_store(self, discount_dict = dict()):
        df = pd.DataFrame(discount_dict)
        if len(discount_dict) > 0:
            if exists('data/discount_table.csv'):
                df.to_csv('data/discount_table.csv', mode='a', index=False, header=False)
            else:
                df.to_csv('data/discount_table.csv', index=False)

    def fetch_discount_code_for_user(self, user):
        df = pd.read_csv('data/discount_table.csv')
        df.loc[df['is_active'] == 'active']
        return { 'code' : df.discount_code[0], 'percentage': df.percentage[0]}

    def fetch_all_discount_codes(self):
        df = pd.read_csv('discount_table.csv')

    def notify_brand_about_user_recieving_code(self):
        pass