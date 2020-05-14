import json
import ast
import os.path
import argparse
from datetime import date
from fbchat import Client
from fbchat.models import *

cookies_filename = "cookies.txt"
session_cookies_dict = {}
cookies_file_exists = False
client = ''

def write_in_file(filename, data, rights):
	f = open(filename, rights)
	f.write(data)
	f.close

def login(email=' ', password=' ', cookies='', save_cookies=''):
	if email != ' ' and password != ' ':
		print("Connecting using email/password")
		client = Client(email, password)
		if save_cookies:
			print("Saving cookies...")
			session_cookies_str = json.dumps(client.getSession())
			write_in_file(cookies_filename, session_cookies_str, "w")
			print("Done!")
			return  client
	if cookies:
		print("Connecting using cookies")
		if os.path.isfile(cookies_filename):
			f = open(cookies_filename, "r")
			session_cookies_dict = ast.literal_eval(f.read())
			f.close()
			client = Client(' ', ' ', session_cookies = session_cookies_dict)
			print("Connected")
			return client
	else:
		return "Error while connecting"

def sendMessage(message, id):
	if client.isLoggedIn():
		print("Own id: {}".format(client.uid))
		client.send(Message(text=message), thread_id=id, thread_type=ThreadType.GROUP)

def fetch_group_info():
	users = client.fetchAllUsers()
	userList = "{"
	for user in users:
		userList += "\"" + user.uid + "\":\"" + user.name + "\",\n "
	userList = userList[:-1]
	userList += "}"
	write_in_file("userList.json", userList, "w")
	threads = client.fetchThreadList()
	write_in_file("last20Convos.json", str(threads), "w")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Send Facebook messenger from a command line")
	parser.add_argument('-e', '--email', help='specify email for the connection', type=str)
	parser.add_argument('-p', '--password', help='specify password for the connection', type=str)
	parser.add_argument('-c', '--cookies', help='specify a cookie string', action='store_true')
	parser.add_argument('-s', '--store_cookie',help='this will store cookies after the connection on your device', action='store_true')
	parser.add_argument('-f', '--fetch_group',help='fetch group messages info', action='store_true')
	parser.add_argument('-m', '--message',help='this will send the message specified')
	parser.add_argument('-gid', '--group_id',help='specify to which group id you want to send the message', nargs='+')
	parser.add_argument('-gname', '--group_name',help='specify to which group name you want to send the message', nargs='+')
	args = parser.parse_args()

	if args.email and args.password:
		client = login(email=args.email, password=args.password)
	elif args.email and args.password and args.store_cookie:
		client = login(email=args.email, password=args.password, save_cookies=True)
	elif args.cookies:
		client = login(cookies=args.cookies)
	if client != '':
		if client.isLoggedIn():
			if args.message:
				if args.group_id:
					for gid in args.group_id:
						sendMessage(args.message, gid)
				if args.group_name:
					findGroupIdFromName(args.name)
			if args.fetch_group:
				fetch_group_info()

