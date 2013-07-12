import json
import shlex
import time

import facebook
import login as fblogin
import feed as fbfeed
import errors

feed = None
last_cmd = None
week_secs = 7*24*60*60

def prompt_command():
	global feed,last_cmd
	cmd_str = raw_input(">>> ")
	if cmd_str:
		last_cmd = cmd_str
	cmd_args = shlex.split(last_cmd)
	last_cmd = cmd_args[0]
	try:
		feed = feed.execute_command(cmd_args[0],*cmd_args[1:])
	except (errors.CommandNotFoundError,errors.CommandError) as mess:
		print mess

def cleanup(config, token):
	new_config = {"last":str(int(time.time())), "token":token}
	config.update(new_config)
	json.dump(config,open("CONFIG",'w'), indent=4)

def login(config):
	graph = None
	if "token" in config:
		token = config["token"]
		try:
			graph = facebook.GraphAPI(token)
		except facebook.GraphAPIError:
			pass
	
	if not graph:
		token = fblogin.login()
		graph = facebook.GraphAPI(token)
	
	return token,graph

if __name__ == "__main__":
	config = json.load(open("CONFIG",'r'))

	try:
		token,graph = login(config)
	except facebook.GraphAPIError:
		print "There was a problem logging in, so the app will now close."
		exit(1)
	

	last_read = config.get("last", time.time() - week_secs)
	interval = config["interval"]
	init_args = [last_read]
	try:
		feed = fbfeed.init_feed(graph,interval,init_args)
	except errors.LoadError as mess:
		print mess
		exit(1)
	except errors.CommandError:
		print "Unexpected command execution caused an error during startup."
		exit(1)

	try:
		while True:
			prompt_command()
	except KeyboardInterrupt:
		print "\nClosing the Facebook Newsreader."
		cleanup(config,token)
