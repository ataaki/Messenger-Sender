# Messenger Sender

```
usage: messenger-sender.py [-h] [-e EMAIL] [-p PASSWORD]
                           [-c [COOKIES_FILE_PATH]] [-s] [-f] [-m MESSAGE]
                           [-uid USER_ID [USER_ID ...]]
                           [-uname USER_NAME [USER_NAME ...]]
                           [-gid GROUP_ID [GROUP_ID ...]]
                           [-gname GROUP_NAME [GROUP_NAME ...]]

Send Facebook messenger from a command line. This program is base on fbchat
module

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        specify email for the connection
  -p PASSWORD, --password PASSWORD
                        specify password for the connection
  -c [COOKIES_FILE_PATH], --cookies_file_path [COOKIES_FILE_PATH]
                        specify a cookie file
  -s, --store_cookie    this will store cookies after the connection on your
                        device (file is stored in program folder as
                        "./cookies"
  -f, --fetch_group     fetch group messages info
  -m MESSAGE, --message MESSAGE
                        this will send the message specified
  -uid USER_ID [USER_ID ...], --user_id USER_ID [USER_ID ...]
                        specify to which user id you want to send the message
  -uname USER_NAME [USER_NAME ...], --user_name USER_NAME [USER_NAME ...]
                        specify to which user name you want to send the
                        message
  -gid GROUP_ID [GROUP_ID ...], --group_id GROUP_ID [GROUP_ID ...]
                        specify to which group id you want to send the message
  -gname GROUP_NAME [GROUP_NAME ...], --group_name GROUP_NAME [GROUP_NAME ...]
                        specify to which group name you want to send the
                        message
```