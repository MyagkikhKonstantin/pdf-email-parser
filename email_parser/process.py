import traceback
from optparse import OptionParser

from email_attach import get_unseen_msg_attachments
from parse_order import parse_document
from spreadsheet_update import insert_new_order
import settings

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(settings.log_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    parser = OptionParser()
    options, _ = parser.parse_args()
    logger.info('Start process')
    attaches = get_unseen_msg_attachments()
    for attach in attaches:
        try:
            order = parse_document(attach)
        except Exception as e:
            logger.error('Attach is not PDF or: %s', traceback.print_exc())
            continue
        insert_new_order(order)
    logger.info('End process')

if __name__ == '__main__':
    main()
