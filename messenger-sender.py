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

def fetch(type):
	if type == 'users':
		users = client.fetchAllUsers()
		userList = "{"
		for user in users:
			userList += "\"" + user.uid + "\":\"" + user.name + "\",\n "
		userList += userList[:-1]+"}"
		try:
			write_in_file("userList.json", userList, "w")
			print("File userList.json has been generated")
		except:
			print("Error while writing file")
	elif type == 'groups':
		groupList = "{"
		threads = client.fetchThreadList()
		for group in threads:
			if str(group)[:5] == 'Group':
				groupList += "\"" + str(group.uid) + "\": \n{" + \
				"\n\"Type\": \"" + str(group.type) + \
				"\",\n\"Photo\": \"" + str(group.photo) + \
				"\",\n\"Name\": \"" + str(group.name) + \
				"\",\n\"Last_message_timestamp\": \"" + str(group.last_message_timestamp) + \
				"\",\n\"Message_count\": \"" + str(group.message_count) + \
				"\",\n\"Plan\": \"" + str(group.plan) + \
				"\"\n},\n"
		groupList = groupList[:-2] + "}"
		write_in_file("groupList.json", str(groupList), "a")
	elif type == 'archived':
		archiveList = "{"
		archives = client.fetchThreadList(thread_location=ThreadLocation.ARCHIVED)
		for archive in archives:
			#if str(groups)[:5] == 'Group':
			archiveList += "\"" + str(archive.uid) + "\": \n{" + \
			"\n\"Type\": \"" + str(archive.type) + \
			"\",\n\"Photo\": \"" + str(archive.photo) + \
			"\",\n\"Name\": \"" + str(archive.name) + \
			"\",\n\"Last_message_timestamp\": \"" + str(archive.last_message_timestamp) + \
			"\",\n\"Message_count\": \"" + str(archive.message_count) + \
			"\",\n\"Plan\": \"" + str(archive.plan) + \
			"\"\n},\n"
		archiveList = archiveList[:-2] + "}"
		write_in_file("archiveList.json", str(archiveList), "a")

def fetchMessages(id):
	messageList = "{"
	messages = client.fetchThreadMessages(thread_id=id, limit=200)
	for message in messages:
		messageList += "\"" + str(message.text).replace("\"", "'") + "\": \n{" + \
		"\n\"uid\": \"" + str(message.uid) + \
		"\",\n\"mentions\": \"" + str(message.mentions) + \
		"\",\n\"author\": \"" + str(message.author) + \
		"\",\n\"timestamp\": \"" + str(message.timestamp) + \
		"\",\n\"read_by\": \"" + str(message.read_by) + \
		"\",\n\"sticker\": \"" + str(message.sticker) + \
		"\",\n\"attachments\": \"" + str(message.attachments).replace("\"", "'") + \
		"\",\n\"unsent\": \"" + str(message.unsent) + \
		"\",\n\"reply_to_id\": \"" + str(message.reply_to_id) + \
		"\",\n\"replied_to\": \"" + str(message.replied_to) + \
		"\",\n\"forwarded\": \"" + str(message.forwarded) + \
		"\"\n},\n"
	messageList = messageList[:-2] + "}"
	write_in_file(str(id)+"_message.json", str(messageList), "w")
	#print(messages)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Send Facebook messenger from a command line. This program is base on fbchat module")
	parser.add_argument('-e', '--email', help='specify email for the connection', type=str)
	parser.add_argument('-p', '--password', help='specify password for the connection')
	parser.add_argument('-c', '--cookies_file_path', help='specify a cookie file', nargs='?', const='./cookies')
	parser.add_argument('-s', '--store_cookie',help='this will store cookies after the connection on your device (file is stored in program folder as \"./cookies\"', action='store_true')
	parser.add_argument('-l', '--list_type',help='list info about groups/users/archived messages in json file', choices=['users', 'groups', 'archived'])
	parser.add_argument('-g', '--get_data',help='fetch content from group/user messages. must use -uid', action="store_true")
	parser.add_argument('-m', '--message',help='this will send the message specified')
	parser.add_argument('-uid', '--user_id',help='specify a list of user id', nargs='+')
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
			if args.list_type:
				fetch(args.list_type)
			if args.get_data and args.user_id:
				for uid in args.user_id:
					fetchMessages(uid)

