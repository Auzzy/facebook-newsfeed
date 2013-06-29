from factories import PostFactory,TimestampFactory
from commands import COMMANDS,_Load
from bidiriter import BiDirIterator as FeedIter

import errors

class Feed(object):
	def __init__(self, feed_iter, post_list):
		self._feed_iter = feed_iter
		self._post_list = post_list
		self._window = []
		
		try:
			self.since = self._post_list[0].timestamp
			self.until = self._post_list[-1].timestamp
		except IndexError:
			self.since = self.until = TimestampFactory.make_timestamp()
	
	def next(self):
		return self._feed_iter.next()

	def prev(self):
		return self._feed_iter.prev()

	def fastforward(self):
		return self._feed_iter.fastforward()

	def rewind(self):
		return self._feed_iter.rewind()
	
	def window(self):
		return tuple(self._window)

	def __len__(self):
		return len(self._post_list)

	def __str__(self):
		sep = 100*'-'
		post_list_str = ('\n\n' + sep + '\n').join([str(post) for post in self._window])
		return (sep + '\n') + post_list_str + ('\n\n' + sep)


class FeedFactory(object):
	@staticmethod
	def make_feed(feed_json):
		posts_json = feed_json.get("data")
		post_list = FeedFactory.make_post_list(posts_json)
		feed_iter = FeedIter(post_list)
		return Feed(feed_iter,post_list)

	@staticmethod
	def make_post_list(posts_json):
		return [PostFactory.make_post(post_json) for post_json in reversed(posts_json)]


class _FeedCommandHandler(object):
	def __init__(self, graph, feed=None):
		self.graph = graph
		self.feed = feed
	
	def execute_command(self, cmd_str, *args):
		cmd = None
		if cmd_str == _Load.get_name():
			feed = self._load(*args)
			if feed or self.feed is None:	# Ensures the feed is initialized no matter what
				self.feed = feed
			if not self.feed:
				print "There are no more recent posts for you to read."
		else:
			for command in COMMANDS:
				if cmd_str == command.get_name():
					cmd = command
					break

			if not cmd:
				raise errors.CommandNotFoundError("The provided command does not exist: {0}".format(cmd_str))
			
			cmd.run(self,*args)

		return self
	
	def _load(self, *args):
		now = TimestampFactory.make_timestamp()
		
		feed_json,since,until = _Load.run(self,*args)
		since = TimestampFactory.from_seconds(since)
		until = TimestampFactory.from_seconds(until)
		while not feed_json["data"] and until < now:
			args = [until.as_seconds()]
			feed_json,since,until = _Load.run(self,*args)
			since = TimestampFactory.from_seconds(since)
			until = TimestampFactory.from_seconds(until)

		return FeedFactory.make_feed(feed_json)


def init_feed(graph, interval, init_args):
	interval = int(interval)
	_Load.interval = interval
	cmd_handler = _FeedCommandHandler(graph)
	cmd_handler.execute_command(_Load.NAME,*init_args)
	return cmd_handler
