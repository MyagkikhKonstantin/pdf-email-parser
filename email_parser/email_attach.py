import email
import imaplib
import os
from tempfile import NamedTemporaryFile

import settings


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(settings.log_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_msg_id(msg):
    items = dict(msg.items())
    if items.get('Message-ID', None) is not None:
        return items['Message-ID']
    if items.get('Message-Id', None) is not None:
        return items['Message-Id']
    return 'Unknown-ID'


class FetchEmail():

    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False)
        logger.info('Imap adapter opened')

    def close_connection(self):
        self.connection.close()
        logger.info('Imap adapter closed')

    def save_attachment(self, msg, download_folder="/tmp"):
        msg_id = get_msg_id(msg)
        logger.info('Handle attaches in msg_id: %s' % msg_id)
        attaches = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_type() == 'text/plain':
                continue
            try:
                fp = NamedTemporaryFile(mode='wb', delete=False)
                fp.write(part.get_payload(decode=True))
                fp.close()
                attaches.append(fp.name)
                logger.info('Msg successfully store attach into path: %s' %
                            (fp.name,))
            except:
                logger.error('Msg cant store attach!')
        return attaches


    def fetch_unread_messages(self):
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].split(' '):
                try: 
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    logger.info("No new emails to read.")
                    self.close_connection()
                    return []
                if data[0] is not None:
                    msg = email.message_from_string(data[0][1])
                    if isinstance(msg, str) == False:
                        emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS','\\Seen')
            return emails
        logger.error("Failed to retreive emails.")
        return emails

    def parse_email_address(self, email_address):
        return email.utils.parseaddr(email_address)


def get_unseen_msg_attachments():
    adapter = FetchEmail(settings.mail_server, settings.email_login, settings.email_password)
    unread_messages = adapter.fetch_unread_messages()
    unread_messages_attaches = []
    for msg in unread_messages:
        msg_attaches = adapter.save_attachment(msg, download_folder="/tmp")
        if msg_attaches:
            unread_messages_attaches.extend(msg_attaches)
        else:
            logger.error('Msg: %s has no attach file' % get_msg_id(msg))
            continue
    logger.info('Unseen messages attaches number: %d' % len(unread_messages_attaches))
    return unread_messages_attaches


def main():
    for x in get_unseen_msg_attachments():
        print 'attach', x

if __name__ == '__main__':
    main()
