# Python ASPSMS

Command-line SMS client for [ASPSMS](http://www.aspsms.com/).
Message text can be given as argument or read from standard input.

## Dependencies
The SMS clients uses `requests` for the API calls. This module has to be installed before the script can be used.
```
pip install requests
```

## Configuration
Before you can start you have to fill-in the configuration parameters in the
header of the script:
```
...
## Config
USERKEY = ''       # ASPSMS user key (https://www.aspsms.com/de/userkey/)
PASSWORD = ''      # ASPSMS password
ORIGINATOR = ''    # Originator in E.164 or up to 11 alphabetic characters
...
```

## Usage
### Send message
Send message to recpipient +41791234567 (uses originator from configuration):
```
./aspsms.py -m 'message' -r +41791234567
```
Send message to recpipient +41791234567 with originator '+41797654321':
```
./aspsms.py -m 'message' -r +41791234567 -o '+41797654321'
```
Pipe message from _STDIN_:
```
echo "test" | ./aspsms.py -r +41791234567
```

### Check Credit Balance
```
./aspsms.py credits
```

### Help
```
./aspsms.py -h
```

## ASPSMS REST API
- [RESTful ASPSMS JSON API](https://json.aspsms.com/)