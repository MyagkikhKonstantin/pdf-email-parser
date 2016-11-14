import gspread
import settings
from email_parser import google_api_credentials_file
from oauth2client.service_account import ServiceAccountCredentials

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(settings.log_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(google_api_credentials_file, scope)
    gc = gspread.authorize(credentials)
    logger.info('Google drive opened')
    sheet = gc.open(settings.spreadsheet_name)
    logger.info('Worksheet %s opened' % settings.spreadsheet_name)
    worksheet = sheet.sheet1
    return worksheet


def insert_new_order(order):
    logger.info('Start inserting')
    worksheet = get_worksheet()
    cells_relation = {
                      'priority':                 [2, 'B', 'Priority Status'],
                      'description':              [3, 'C', 'Description'],
                      'school_name':              [4, 'D', 'School Name'],
                      'work_order':               [5, 'E', 'Work Order Number'],
                      'purchase_order_number':    [6, 'F', 'Purchase Order Number'],
                      'purchase_order_date':      [7, 'G', 'Purchase Order Date'],
                      'required_completion_date': [8, 'H', 'Required Completion Date'],
                      } 
    
    #
    # checking for existing
    work_order_column_id = cells_relation['work_order'][0]
    orders_list = [x for x in worksheet.col_values(work_order_column_id) if x]
    if order['work_order'] in orders_list:
        logger.error('Order %s almost in spreadsheet! Aborting.' % order['work_order'])
        return False
    #
    # Updating cell values
    order_id = len(orders_list) + 1
    for column, column_value in order.items():
        column_id = cells_relation[column][0]
        worksheet.update_cell(order_id, column_id, column_value)
    logger.info('End inserting')
    return True


def main():
    pass
if __name__ == '__main__':
    main()
