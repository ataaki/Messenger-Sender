# Messenger Sender

```
usage: messenger-sender.py [-h] [-e EMAIL] [-p PASSWORD] [-c] [-s] [-f]
                           [-m MESSAGE] [-gid GROUP_ID [GROUP_ID ...]]
                           [-gname GROUP_NAME]

Send Facebook messenger from a command line

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        specify email for the connection
  -p PASSWORD, --password PASSWORD
                        specify password for the connection
  -c, --cookies         specify a cookie string
  -s, --store_cookie    this will store cookies after the connection on your
                        device
  -f, --fetch_group     fetch group messages info
  -m MESSAGE, --message MESSAGE
                        this will send the message specified
  -gid GROUP_ID [GROUP_ID ...], --group_id GROUP_ID [GROUP_ID ...]
                        specify to which group id you want to send the message
  -gname GROUP_NAME, --group_name GROUP_NAME
                        specify to which group name you want to send the
                        message
```