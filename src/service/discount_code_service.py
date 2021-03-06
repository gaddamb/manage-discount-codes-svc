import shutil
import time
import os
import pandas as pd

from src.config.config import logger
from os.path import exists
from src.utils.utils import generate_random_code, verify_user_with_token_and_return_user

class DiscountCodeService():
    '''DiscountCodeService handles functionality of managing the discount codes. '''
    
    def __init__(self, data, config) -> None:
        self.data =  data
        self.config = config
        if data is not None and self.config['create_new_data_store'] == 'True':        
            logger.info("Creating a new data store csv")
            self.data_store_struct = {'discount_code':  [] , 'percentage':  [] , 'is_active':  [] , 'user_id':  [] }
            self.create_data_store(self.data_store_struct)
        
    def create_data_store(self, data_store_struct, delete_existing_file=False):    
        file_name='data/{}.csv'.format(self.config['data_store_file_name'])
        if exists(file_name):
            if delete_existing_file:
                try:
                    os.remove(file_name)
                except OSError as e:  ## if failed, report it back to the user ##
                    print ("Error: %s - %s." % (e.filename, e.strerror))
            elif self.config['create_new_data_store'] == 'True':
                bak_file_name = self.config['data_store_file_name'] + '_' + time.strftime("%Y%m%d-%H%M%S")                 
                logger.info("Backup of data store file named with : " + bak_file_name)
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
        logger.info("New discount codes are generated : ")
        logger.info(discount_dict)
        return discount_dict

    def write_to_data_store(self, discount_dict = dict()):
        df = pd.DataFrame(discount_dict)
        data_store_file_name = 'data/{}.csv'.format(self.config['data_store_file_name'])
        if len(discount_dict) > 0:
            if exists(data_store_file_name):
                df.to_csv(data_store_file_name, mode='a', index=False, header=False)
            else:
                logger.info("Writing to a new data store csv")
                df.to_csv(data_store_file_name, index=False)

    def fetch_discount_code_for_user(self, token):
        user = verify_user_with_token_and_return_user(token=token)        
        if user is not None:
            logger.info("User has been authorized")
        
        data_store_file_name = 'data/{}.csv'.format(self.config['data_store_file_name'])
        df = pd.read_csv(data_store_file_name)
        
        logger.info("Checking whether any of the active discount codes are available")
        if not df[(df['user_id'] == 'NONE') & (df['is_active'] == True)].empty :

            logger.info("Active discount codes unassigned to user are available")

            index = df.index[(df['user_id'] == 'NONE') & (df['is_active'] == True)][0]
            discount_code = df.at[index, 'discount_code']
            percentage = df.at[index, 'percentage']
            logger.info("One of the discount code assigned to user!")
            df.at[index, 'user_id'] = user['userinfo']['email']

            logger.info("Updating the data store with user email")
            self.create_data_store(data_store_struct=df.to_dict(), delete_existing_file=True)
            return { 'code' : discount_code, 'percentage': percentage}
        else :            
            return {'message' : 'could not fetch code'}

    def fetch_all_discount_codes(self):
        df = pd.read_csv('discount_table.csv')

    def notify_brand_about_user_recieving_code(self):
        pass