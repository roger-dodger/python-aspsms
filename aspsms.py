#!/usr/bin/env python
#
# aspsms.py - console based SMS client for ASPSMS
# API reference: https://json.aspsms.com/
#
# Author: https://github.com/roger-dodger/

import sys
import requests
import json
import argparse
import textwrap


# Config
USERKEY = ''
PASSWORD = ''
ORIGINATOR = ''

# Base settings
BASE_URL = 'https://json.aspsms.com'
CALLS = dict()
CALLS['check_credits'] = '/CheckCredits'
CALLS['send_text_sms'] = '/SendSimpleTextSMS'
CONTENT_TYPE = 'application/json'


def make_request(method, body):
    '''
    Make HTTP request and return response
    '''
    r = requests.post(BASE_URL + CALLS[method],
                      headers={'Content-Type': CONTENT_TYPE},
                      data=json.dumps(body))

    response = r.json()
    if response['StatusCode'] == '1':
        return response
    else:
        sys.exit(response['StatusInfo'])


def check_credits():
    '''
    Check your credits
    '''
    data = dict()
    data['UserName'] = USERKEY
    data['Password'] = PASSWORD

    response = make_request('check_credits', data)

    print "Remaining credits: {}".format(response['Credits'])


def send_text_sms(recipient, message, originator):
    '''
    Send single or multipart text messages in GSM 7-bit or Unicode
    '''
    data = dict()
    data['UserName'] = USERKEY
    data['Password'] = PASSWORD
    data['Originator'] = originator
    data['Recipients'] = recipient
    data['MessageText'] = message

    make_request('send_text_sms', data)
    print "Message has been sent!"


def main():
    '''
    Main function
    '''
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
        default=ORIGINATOR,
        help='originator for message')
    parser.add_argument(
        '--message', '-m',
        help='message to be sent')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

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
            sys.exit("Message cannot be emtpy")

        # Send message
        send_text_sms(args.recipient, message, originator)

    elif args.command == 'credits':
        check_credits()


if __name__ == "__main__":
    main()
