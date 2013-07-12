import webbrowser
from datetime import datetime,timedelta
from totimestamp import totimestamp

from errors import LoadError,NextError,PrevError,CommentsError,PrintError,GoError,HelpError

USER_ID = "me"
FEED_NAME = "home"
COMMANDS = []	# See bottom of the module for the defined list

# Add update command. This should reload each post, such that the post content, comments, and likes are up to date.

class Command(object):
	@staticmethod
	def run(feed, *args):
		raise NotImplementedError("Commands must implement the \"run\" function.")

	@staticmethod
	def get_name():
		raise NotImplementedError("Commands must have a name.")

	@staticmethod
	def get_help():
		raise NotImplementedError("Commands must provide a help message.")

	@staticmethod
	def get_usage():
		raise NotImplementedError("Commands must provide a usage string.")

	@staticmethod
	def get_description():
		raise NotImplementedError("Commands must provide a description.")

# FB only lets you get posts from up to a week ago...
# 
# load [<timestamp> [<timestamp>]]
class _Load(Command):
	NAME = "load"
	interval = 6
	limit = 1000

	@staticmethod
	def run(cmd_handler, *args):
		kwargs = _Load._verify(args)
		since = kwargs["since"] if "since" in kwargs else 0
		until = kwargs["until"] if "until" in kwargs else 0
		return cmd_handler.graph.get_connections(USER_ID,FEED_NAME,**kwargs),since,until
	
	@staticmethod
	def _verify(args):
		kwargs = {}
		interval = timedelta(hours=_Load.interval).total_seconds()
		try:
			kwargs["limit"] = _Load.limit
			kwargs["since"] = int(args[0])
			kwargs["until"] = int(args[1]) if len(args) >= 2 else int(kwargs["since"] + interval)
		except IndexError:
			return kwargs
		except:
			import sys
			print sys.exc_info()
			raise LoadError("A problem occurred while trying to execute the {command} command.".format(command=_Load.get_name()))
		
		one_week_ago = datetime.today() - timedelta(weeks=1)
		since_datetime = datetime.fromtimestamp(kwargs["since"])
		if one_week_ago > since_datetime:
			kwargs["since"] = int(totimestamp(one_week_ago))
			if len(args) < 2:
				kwargs["until"] = int(kwargs["since"] + interval)
			print "You cannot access posts over 1 week old; 'since' has been adjusted accordingly."
		else:
			until_datetime = datetime.fromtimestamp(kwargs["until"])
			if one_week_ago > until_datetime:
				kwargs["until"] = int(kwargs["since"] + interval)
				print "You cannot access posts over 1 week old. The ending timestamp has been adjusted accordingly."
		
		if kwargs["since"] > kwargs["until"]:
			raise LoadError("'since' cannot be after 'until': {since} > {until}".format(**kwargs))
		
		return kwargs
	
	@staticmethod
	def get_name():
		return _Load.NAME
	
	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=_Load.get_description(),usage=_Load.get_usage())
		
	@staticmethod
	def get_usage():
		return _Load.NAME + " [<since> [<until>]]\n" + \
			"    If present, since and until are expected to be a UNIX timestamp (seconds since 1/1/1970 (the epoch)).\n" + \
			"    Loads up to 1000 posts between since and until. If until is not provided, loads up to 1000 posts between since and the time the command was issued. With no arguments, loads the most recent 25 posts."

	@staticmethod
	def get_description():
		return "Loads posts from your newsfeed."

# next [<<int> or all>]
class Next(Command):
	NAME = "next"

	@staticmethod
	def run(cmd_handler, *args):
		kwargs = Next._verify(args)
		length = kwargs["length"]
		post_list = []
		while length:
			post = Next._next_post(cmd_handler)
			if not post:
				break
			post_list.append(post)
			length -= 1
	
		cmd_handler.feed._window = post_list
		cmd_handler.execute_command("print")
	
	@staticmethod
	def _verify(args):
		kwargs = {}
		if args:
			if args[0].lower() == "all":
				kwargs["length"] = -1
			else:
				try:
					kwargs["length"] = int(args[0])
				except ValueError:
					raise NextError("Each argument to {command} must be an integer or the word 'all'.".format(command=Next.get_name()))
		else:
			kwargs["length"] = 1
		return kwargs
	
	@staticmethod
	def _next_post(cmd_handler):
		feed = cmd_handler.feed
		try:
			return feed.next()
		except StopIteration:
			until = feed.until.as_seconds()
			cmd_handler.execute_command("load",str(until))
			try:
				return cmd_handler.feed.next()
			except StopIteration:
				return None
	

	@staticmethod
	def get_name():
		return Next.NAME
	
	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=Next.get_description(),usage=Next.get_usage())


	@staticmethod
	def get_usage():
		return Next.NAME + " [<<post_count> or all>]\n" + \
			"    'all' will display all posts from the next one until the most recent post. Any unloaded posts are loaded, then all are displayed.\n" + \
			"    Providing a post_count will cause that many posts to be displayed. Any unloaded posts are loaded, then all are displayed.\n" + \
			"    If no arguments are provided, post_count is set equal to 1."

	@staticmethod
	def get_description():
		return "Displays the next post(s) in the feed, loading more posts if necessary."

# prev [<int>]
class Prev(Command):
	NAME = "prev"

	@staticmethod	
	def run(cmd_handler, *args):
		kwargs = Prev._verify(args)
		length = kwargs["length"]
		post_list = []
		while length:
			post = Prev._prev_post(cmd_handler)
			if not post:
				break
			post_list.append(post)
			length -= 1

		cmd_handler.feed._window = post_list
		cmd_handler.execute_command("print")
	
	@staticmethod
	def _verify(args):
		kwargs = {}
		if args:
			try:
				kwargs["length"] = int(args[0])
			except ValueError:
				raise PrevError("Each argument to {command} must be an integer.".format(command=Prev.get_name()))
		else:
			kwargs["length"] = 1
		return kwargs

	@staticmethod
	def _prev_post(cmd_handler):
		feed = cmd_handler.feed
		try:
			return feed.prev()
		except StopIteration:
			since = feed.since.as_seconds()
			start = since - _Load.interval*360
			cmd_handler.execute_command("load",str(start),str(since))
			cmd_handler.feed.fastforward()
			try:
				return cmd_handler.feed.prev()
			except StopIteration:
				return None
	
	@staticmethod
	def get_name():
		return Prev.NAME

	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=Prev.get_description(),usage=Prev.get_usage())
	
	@staticmethod
	def get_usage():
		return Prev.NAME + " [<post_count>]\n" + \
			"    Providing a post_count will cause that many posts to be displayed. Any unloaded posts are loaded, then all are displayed.\n" + \
			"    If no arguments are provided, post_count is set equal to 1."

	@staticmethod
	def get_description():
		return "Displays the previous post(s) in the feed, loading more posts if necessary."

# comments [<int> ...]
class Comments(Command):
	NAME = "comments"

	@staticmethod	
	def run(cmd_handler, *args):
		kwargs = Comments._verify(cmd_handler.feed,args)
		indices = kwargs["indices"]
		indices_strs = [str(index) for index in indices]
		cmd_handler.execute_command("print","comments",*indices_strs)
	
	@staticmethod
	def _verify(feed, args):
		kwargs = {}
		window_size = len(feed.window())
		if args:
			kwargs["indices"] = [int(index) for index in args if Comments._valid_index(index,window_size)]
			if len(kwargs["indices"]) < len(args):
				print "Invalid indices have been ignored (valid indices are 1-{end}).".format(end=window_size)
		else:
			kwargs["indices"] = range(1,window_size+1)
		return kwargs
	
	@staticmethod
	def _valid_index(index_str, window_size):
		return index_str.isdigit() and int(index_str) in range(1,window_size+1)

	@staticmethod
	def get_name():
		return Comments.NAME

	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=Comments.get_description(),usage=Comments.get_usage())

	@staticmethod
	def get_usage():
		return "comments [<int> ...]\n" + \
			"    Redisplays currently displayed posts with the corresponding indices along with all associated comments. Invalid indices will be ignored.\n" + \
			"    Providing no arguments will reload all currently displayed posts with all associated comments."

	@staticmethod
	def get_description():
		return "Displays comments on the specified post(s)."

# print [<int> ...]
# print comments [<int> ...]
class Print(Command):
	NAME = "print"

	@staticmethod
	def run(cmd_handler, *args):
		print 
		feed = cmd_handler.feed
		window = feed.window()
		kwargs = Print._verify(feed,args)
		indices,to_str_args = kwargs["indices"],kwargs["to_str"]
		post_list = [window[index] for index in indices]
		Print.print_post_list(post_list,**to_str_args)
	
	@staticmethod
	def _verify(feed, args):
		kwargs = {}
		kwargs["to_str"] = {}
		if args and not args[0].isdigit():
			if args[0] == "comments":
				kwargs["to_str"]["comments"] = True
				args = args[1:]
			else:
				raise PrintError("Invalid command passed to the {command} command: {subcmd}".format(command=Print.get_name(),subcmd=args[0]))
		else:
			kwargs["to_str"]["comments"] = False
		window_size = len(feed.window())
		if args:
			kwargs["indices"] = [int(index)-1 for index in args if Print._valid_index(index,window_size)]
			if len(kwargs["indices"]) < len(args):
				print "Invalid indices have been ignored (valid: 1-{end}).".format(end=window_size)
		else:
			kwargs["indices"] = range(window_size)
		return kwargs
	
	@staticmethod
	def _valid_index(index_str, window_size):
		return index_str.isdigit() and int(index_str) in range(1,window_size+1)
	
	@staticmethod
	def print_post_list(post_list, **kwargs):
		sep = 100*'-' + '\n'
		post_list_str = ('\n\n' + sep).join([post.to_string(**kwargs) for post in post_list])
		if post_list_str:
			print sep + post_list_str + '\n\n' + sep
	
	@staticmethod
	def get_name():
		return Print.NAME

	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=Print.get_description(),usage=Print.get_usage())

	@staticmethod
	def get_usage():
		return "print [<int> ...]\n" + \
			"    Redisplays just the posts with the provided indices. Invalid indices will be ignored.\n" + \
			"    If the first argument is 'comments', displays the appropriate posts with all comments.\n" + \
			"    Providing no arguments will reload all currently displayed posts."

	@staticmethod
	def get_description():
		return "Redisplays posts with the corresponding indices."

# go [<int> ...]
class Go(Command):
	NAME = "go"

	@staticmethod
	def run(cmd_handler, *args):
		feed = cmd_handler.feed
		window = feed.window()
		kwargs = Go._verify(feed,args)
		indices = kwargs["indices"]
		posts = [window[index] for index in indices]
		for post in posts:
			webbrowser.open_new(post.url)
	
	@staticmethod
	def _verify(feed, args):
		kwargs = {}
		window_size = len(feed.window())
		if args:
			kwargs["indices"] = [int(index)-1 for index in args if Comments._valid_index(index,window_size)]
			if len(kwargs["indices"]) < len(args):
				print "Invalid indices have been ignored (valid: 1-{end}).".format(end=window_size)
		else:
			kwargs["indices"] = range(window_size)
		return kwargs
	
	@staticmethod
	def _valid_index(index_str, window_size):
		return index_str.isdigit() and int(index_str) in range(1,window_size+1)

	@staticmethod
	def get_name():
		return Go.NAME
	
	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=Go.get_description(),usage=Go.get_usage())

	@staticmethod
	def get_usage():
		return "go [<int> ...]\n" + \
			"    Open the post(s) with the provided indices in your default browser.\n" + \
			"    Providing no arguments will open all currently displayed posts in your default browser."

	@staticmethod
	def get_description():
		return "Opens the posts with the specified indices in your default browser."

# help [command]
class Help(Command):
	NAME = "help"

	@staticmethod
	def run(cmd_handler, *args):
		help_str = Help._verify(args)
		print help_str
	
	@staticmethod
	def _verify(args):
		command_dict = {command.NAME:command for command in (COMMANDS + [_Load])}
		if args:
			command = command_dict.get(args[0])
			if command:
				return command.get_help()
			else:
				raise HelpError("The provided command does not exist: {subcmd}".format(subcmd=args[0]))
		else:
			command_names = list(sorted(command_dict.keys()))
			help_str = ""
			for name in command_names:
				command = command_dict[name]
				descr = command.get_description()
				help_str += "{name}: {descr}\n".format(name=name,descr=descr)
			return help_str
	
	@staticmethod
	def get_name():
		return Help.NAME
	
	@staticmethod
	def get_help():
		return "{descr}\n{usage}".format(descr=Help.get_description(),usage=Help.get_usage())

	@staticmethod
	def get_usage():
		return "help [<command>]\n" + \
			"    If no arguments are provided, displays a brief description of what each available command does.\n" + \
			"    If the name of a command is provided, prints detailed usage information for that command."

	@staticmethod
	def get_description():
		return "Prints help messages."

COMMANDS = [Next,Prev,Comments,Print,Go,Help]
