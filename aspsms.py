#!/usr/bin/env python
#
# aspsms.py - console based SMS client for ASPSMS
# API reference: https://json.aspsms.com/
#
# Author: https://github.com/roger-dodger/

import sys
import os
import requests
import json
import argparse
import textwrap


class Error(Exception):
    '''Base exception class for aspsms module.'''


class ConnectionError(Error):
    '''Error to use when the connection to ASPSMS fails.'''


class SmsClient(object):
    # Base settings
    BASE_URL = 'https://json.aspsms.com'
    CALLS = {
        'CHECK_CREDITS': '/CheckCredits',
        'SEND_TEXT_SMS': '/SendSimpleTextSMS',
    }
    CONTENT_TYPE = 'application/json'

    def __init__(self, conf):
        self._config = conf

    def _make_request(self, method, body=None):
        '''Make HTTP request and return response

        Args:
            method:
            body:

        Returns:

        Raises:
            ConnectionError: Connection to ASPSMS failed.
        '''
        # Append credentials
        if not body:
            body = dict()
        body['UserName'] = self._config['USERKEY']
        body['Password'] = self._config['PASSWORD']

        try:
            r = requests.post(self.BASE_URL + self.CALLS[method],
                              headers={'Content-Type': self.CONTENT_TYPE},
                              data=json.dumps(body))
        except requests.exceptions.RequestException as e:
            raise ConnectionError(e)

        response = r.json()
        if response['StatusCode'] == '1':
            return response
        raise ConnectionError(response['StatusInfo'])

    def check_credits(self):
        '''Check your credits.

        Returns:

        Raises:
            ConnectionError: Connection to ASPSMS failed.
        '''
        return self._make_request('CHECK_CREDITS')['Credits']

    def send_text_sms(self, recipient, message, originator):
        '''Send single or multipart text messages in GSM 7-bit or Unicode.

        Args:
            receipient: Message receipient
            message: Message text
            originator: Message originator

        Raises:
            ConnectionError: Connection to ASPSMS failed.
        '''
        data = dict()
        data['Originator'] = originator
        data['Recipients'] = recipient
        data['MessageText'] = message

        self._make_request('SEND_TEXT_SMS', data)


def main():
    '''
    Main function
    '''

    # Read config file
    CONF = 'aspsms.conf'
    script_directory = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(script_directory, CONF)
    if not os.path.isfile(config_file):
        sys.exit('Config file {} not found'.format(CONF))
    with open(config_file) as config_handler:
        conf = json.load(config_handler)

    parser = argparse.ArgumentParser(
        description='ASPSMS console client',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'command',
        choices=['send', 'credits'],
        nargs='?',
        default='send',
        help=textwrap.dedent('''\
            send - send a new message (default)
            credits - check credit balance'''))
    parser.add_argument(
        '--recipient', '-r',
        nargs='+',
        help='message recipient(s)')
    parser.add_argument(
        '--originator', '-o',
        default=conf['ORIGINATOR'],
        help='originator for message')
    parser.add_argument(
        '--message', '-m',
        help='message to be sent')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    sc = SmsClient(conf)

    if args.command == 'send':
        # Override originator from configuration if given
        if args.originator:
            originator = args.originator

        # Define emtpy message
        message = str()

        # Test if message was given with argument
        if args.message:
            message = args.message
        # Test if message was given in stdin
        elif not sys.stdin.isatty():
            message = sys.stdin.readline().strip()

        # No message was given - terminate
        if not message:
            sys.exit('Message cannot be emtpy')

        # Send message
        try:
            sc.send_text_sms(args.recipient, message, originator)
            print 'Message has been sent!'
        except ConnectionError as e:
            print 'Unable to send message: {}'.format(e)

    elif args.command == 'credits':
        try:
            print 'Remaining credits: {}'.format(sc.check_credits())
        except ConnectionError as e:
            print 'Unable to check credits: {}'.format(e)


if __name__ == "__main__":
    main()
