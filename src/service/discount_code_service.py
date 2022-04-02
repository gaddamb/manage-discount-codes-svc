
from src.utils.utils import generate_random_code, verify_user_with_token_and_return_user
import pandas as pd
from src.config.config import config
import os
from os.path import exists
import shutil
import time

class DiscountCodeService():
    
    def __init__(self, data) -> None:
        self.data =  data
        if data is not None and config()['create_new_data_store']:        
            self.data_store_struct = {'discount_code':  [] , 'percentage':  [] , 'is_active':  [] , 'user_id':  [] }
            self.create_data_store(self.data_store_struct)
        
    def create_data_store(self, data_store_struct, delete_existing_file=False):    
        file_name='data/discount_table.csv'
        if exists(file_name):
            if delete_existing_file:
                try:
                    os.remove(file_name)
                except OSError as e:  ## if failed, report it back to the user ##
                    print ("Error: %s - %s." % (e.filename, e.strerror))
            else:
                bak_file_name = 'discount_table_' + time.strftime("%Y%m%d-%H%M%S") 
                shutil.move(file_name, 'data/{}.csv'.format(bak_file_name))
        self.write_to_data_store(data_store_struct)


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
            active_states.append(True)
            user_ids.append('NONE')
        
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

    def fetch_discount_code_for_user(self, token):
        user = verify_user_with_token_and_return_user(token=token)
        df = pd.read_csv('data/discount_table.csv')

        if not df[(df['user_id'] == 'NONE') & (df['is_active'] == True)].empty :
            index = df.index[(df['user_id'] == 'NONE') & (df['is_active'] == True)][0]
            discount_code = df.at[index, 'discount_code']
            percentage = df.at[index, 'percentage']
            df.at[index, 'user_id'] = user['userinfo']['email']
            self.create_data_store(data_store_struct=df.to_dict(), delete_existing_file=True)
            return { 'code' : discount_code, 'percentage': percentage}
        else :            
            return {'message' : 'could not fetch code'}

    def fetch_all_discount_codes(self):
        df = pd.read_csv('discount_table.csv')

    def notify_brand_about_user_recieving_code(self):
        pass