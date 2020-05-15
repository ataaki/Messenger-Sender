# Messenger Sender

I'm using this script to automatically share a song from Spotify to a messenger group, where we share some songs with some friends.

This script is hosted on my server.
I've created a siri shortcut to get the current playing song on Spotify thanks to Shortcutify iOS app, and then I'm passing this info throught an http request to my server, which triggers the python script with the params.

```
usage: messenger-sender.py [-h] [-e EMAIL] [-p PASSWORD]
                           [-c [COOKIES_FILE_PATH]] [-s]
                           [-l {users,groups,archived}] [-g] [-m MESSAGE]
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
  -l {users,groups,archived}, --list_type {users,groups,archived}
                        list info about groups/users/archived messages in json
                        file
  -g, --get_data        fetch content from group/user messages. must use -uid
  -m MESSAGE, --message MESSAGE
                        this will send the message specified
  -uid USER_ID [USER_ID ...], --user_id USER_ID [USER_ID ...]
                        specify a list of user id
  -uname USER_NAME [USER_NAME ...], --user_name USER_NAME [USER_NAME ...]
                        specify to which user name you want to send the
                        message
  -gid GROUP_ID [GROUP_ID ...], --group_id GROUP_ID [GROUP_ID ...]
                        specify to which group id you want to send the message
  -gname GROUP_NAME [GROUP_NAME ...], --group_name GROUP_NAME [GROUP_NAME ...]
                        specify to which group name you want to send the
                        message
```