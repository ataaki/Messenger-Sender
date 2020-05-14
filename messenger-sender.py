import json
import ast
import os.path
import argparse
from datetime import date
from fbchat import Client
from fbchat.models import *

session_cookies_dict = {}
cookies_file_exists = False
client = ''

def write_in_file(filename, data, rights):
	f = open(filename, rights)
	f.write(data)
	f.close

def login(email=' ', password=' ', cookies='./cookies', save_cookies=''):
	if email != ' ' and password != ' ':
		print("Connecting using email/password")
		client = Client(email, password)
		if save_cookies:
			print("Saving cookies...")
			session_cookies_str = json.dumps(client.getSession())
			write_in_file('./cookies', session_cookies_str, "w")
			print("Done!")
			return  client
	if cookies:
		print("Connecting using cookies")
		try:
			os.path.isfile(cookies)
		except:
			print("File not found")
		f = open(cookies, "r")
		session_cookies_dict = ast.literal_eval(f.read())
		f.close()				
		client = Client(' ', ' ', session_cookies = session_cookies_dict)
		return client
	else:
		return "Error while connecting"

def sendMessage(message, id, type):
	if client.isLoggedIn():
		client.send(Message(text=message), thread_id=id, thread_type=type)

def findUserIdFromName(uname):
	users = client.fetchAllUsers()
	user_found = {}
	for user in users:
		for name in uname:
			if user.name == name:
				user_found[user.name] = user.uid
	if user_found:
		print("Found " + str(len(user_found)) + " user(s)")
		return user_found
	else:
		print("No user found")
		return

def findGroupIdFromName(gname):
	groups = client.fetchThreadList()
	group_found = {}
	for group in groups:
		for name in gname:
			if group.name == name:
				group_found[group.name] = group.uid
	if group_found:
		print("Found " + str(len(group_found)) + " group(s)")
		return group_found
	else:
		print("No group found")
		return

def fetch_group_info():
	users = client.fetchAllUsers()
	userList = "{"
	for user in users:
		userList += "\"" + user.uid + "\":\"" + user.name + "\",\n "
	userList += userList[:-1]+"}"
	write_in_file("userList.json", userList, "w")
	threads = client.fetchThreadList()
	write_in_file("last20Convos.json", str(threads), "w")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Send Facebook messenger from a command line. This program is base on fbchat module")
	parser.add_argument('-e', '--email', help='specify email for the connection', type=str)
	parser.add_argument('-p', '--password', help='specify password for the connection')
	parser.add_argument('-c', '--cookies_file_path', help='specify a cookie file', nargs='?', const='./cookies')
	parser.add_argument('-s', '--store_cookie',help='this will store cookies after the connection on your device (file is stored in program folder as \"./cookies\"', action='store_true')
	parser.add_argument('-f', '--fetch_group',help='fetch group messages info', action='store_true')
	parser.add_argument('-m', '--message',help='this will send the message specified')
	parser.add_argument('-uid', '--user_id',help='specify to which user id you want to send the message', nargs='+')
	parser.add_argument('-uname', '--user_name',help='specify to which user name you want to send the message', nargs='+')
	parser.add_argument('-gid', '--group_id',help='specify to which group id you want to send the message', nargs='+')
	parser.add_argument('-gname', '--group_name',help='specify to which group name you want to send the message', nargs='+')
	args = parser.parse_args()
	if args.cookies_file_path:
		client = login(cookies=args.cookies_file_path)
	elif args.email and args.password and args.store_cookie:
		client = login(email=args.email, password=args.password, cookies=None, save_cookies=True)
	elif args.email and args.password:
		client = login(email=args.email, password=args.password, cookies=None)
	if client != '':
		if client.isLoggedIn():
			print("Connected")
			print("Own id: {}".format(client.uid))
			if args.message:
				if args.user_id:
					for uid in args.user_id:
						sendMessage(args.message, uid, type=ThreadType.USER)
				if args.user_name:
					userDict = findUserIdFromName(args.user_name)
					for name, id in userDict.items():
						sendMessage(args.message, id, type=ThreadType.USER)
				if args.group_id:
					for gid in args.group_id:
						sendMessage(args.message, gid, type=ThreadType.GROUP)
				if args.group_name:
					groupDict = findGroupIdFromName(args.group_name)
					for name, id in groupDict.items():
						print(name, id)
						sendMessage(args.message, id, type=ThreadType.GROUP)
			if args.fetch_group:
				fetch_group_info()

