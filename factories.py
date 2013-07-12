from datetime import datetime

from asciify import asciify
from feed_objects import *


# Accounts for asciify's incorrect handling of None.
_asciify = asciify
def asciify(string):
	return _asciify(string) if string else None


class PostFactory(object):
	_POST_URL_FORMAT = "http://facebook.com/{user}/posts/{post}"

	@staticmethod
	def make_post(post_json):
		if post_json:
			id = post_json.get("id")
			
			timestamp = TimestampFactory.make_timestamp(post_json.get("created_time"))
			place = PlaceFactory.make_place(post_json.get("place"))

			from_ = UserFactory.make_user(post_json.get("from"))
			with_tags = PostFactory.get_users(post_json.get("with_tags"))
			msg_tags = PostFactory.get_message_tags(post_json)
			to_list = PostFactory.get_users(post_json.get("to"))
			to = PostFactory.extract_recipient(to_list,with_tags,msg_tags)
			users = PostUsers(from_,to,with_tags,msg_tags)

			message = asciify(post_json.get("message"))
			story = asciify(post_json.get("story"))
			photo = post_json.get("picture")
			video = post_json.get("source")
			link = LinkFactory.make_link(post_json)
			post_type = post_json.get("type")
			status_type = post_json.get("status_type")
			resources = PostResources(link,photo,video)
			contents = PostContents(message,story,resources,post_type,status_type)
			
			comments = PostFactory.get_comments(post_json)
			likes = PostFactory.get_likes(post_json)
			app = AppFactory.make_app(post_json.get("application"))
			metadata = PostMetadata(comments,likes,app)

			url = PostFactory._get_url(id,to,post_type,status_type)

			return Post(id,timestamp,place,url,users,contents,metadata)
		else:
			return None

	@staticmethod
	def get_message_tags(post_json):
		message_tags = post_json.get("message_tags")
		user_list = []
		if message_tags:
			for offset in message_tags:
				try:
					user_json = message_tags[offset][0]
				except TypeError:
					user_json = offset
				user_list.append(UserFactory.make_user(user_json))
		return user_list
	
	@staticmethod
	def extract_recipient(to_list, with_tags, msg_tags):
		to_list = list(set(to_list) - set(msg_tags) - set(with_tags))
		if not to_list:
			return None
		elif len(to_list) == 1:
			return to_list[0]
		else:
			raise AttributeError("Ended up with more than 1 recipient.")

	@staticmethod
	def get_users(tags_json):
		return PostFactory._get_tags(tags_json,UserFactory.make_user)
	
	@staticmethod
	def get_comments(post_json):
		comments_json = post_json.get("comments")
		return PostFactory._get_tags(comments_json,CommentFactory.make_comment)
	
	@staticmethod
	def get_likes(post_json):
		likes_json = post_json.get("likes")
		return PostFactory._get_tags(likes_json,UserFactory.make_user)
	
	@staticmethod
	def _get_tags(tags_json, factory_func):
		tags = []
		if tags_json:
			tag_list = tags_json.get("data",[])
			tags = [factory_func(tag) for tag in tag_list]
		return tags

	@staticmethod
	def _get_url(id, to, post_type, status_type):
		from_id,post_id = id.split('_')
		return PostFactory._POST_URL_FORMAT.format(user=from_id,post=post_id)


class TimestampFactory(object):
	EPOCH = datetime(1970,1,1,0,0)
	DATE_FORMAT = "%Y-%m-%d"
	TIME_FORMAT = "T%H:%M:%S"
	DATETIME_FORMAT = DATE_FORMAT + TIME_FORMAT

	@staticmethod
	def make_timestamp(timestamp_str=None):
		if timestamp_str:
			seconds = TimestampFactory.timestamp_to_seconds(timestamp_str)
			return TimestampFactory.from_seconds(seconds)
		else:
			return Timestamp()
	
	@staticmethod
	def from_seconds(seconds):
		return Timestamp(seconds)

	@staticmethod
	def timestamp_to_seconds(time_str):
		time_str,timezone = time_str[:-5],time_str[-5:]
		timestamp = datetime.strptime(time_str,TimestampFactory.DATETIME_FORMAT)
		since_epoch = timestamp - TimestampFactory.EPOCH
		return int(since_epoch.total_seconds())

class UserFactory(object):
	@staticmethod
	def make_user(user_json):
		if user_json:
			id = int(user_json.get("id"))
			name = asciify(user_json.get("name"))
			return User(id,name)
		else:
			return None

class CommentFactory(object):
	@staticmethod
	def make_comment(comment_json):
		if comment_json:
			id = comment_json.get("id")
			timestamp = TimestampFactory.make_timestamp(comment_json.get("created_time"))
			from_ = UserFactory.make_user(comment_json.get("from"))
			message = asciify(comment_json.get("message"))
			tags = PostFactory.get_message_tags(comment_json)
			like_count = comment_json.get("like_count")
			return Comment(id,timestamp,from_,message,tags,like_count)
		else:
			return None

class LinkFactory(object):
	@staticmethod
	def make_link(post_json):
		name = asciify(post_json.get("name"))
		url = post_json.get("link")
		caption = asciify(post_json.get("caption"))
		description = asciify(post_json.get("description"))
		if url:
			return Link(name,url,caption,description)
		else:
			return None

class PlaceFactory(object):
	@staticmethod
	def make_place(place_json):
		if place_json:
			id = int(place_json.get("id"))
			name = place_json.get("name")
			loc = LocationFactory.make_location(place_json.get("location"))
			return Place(id,name,loc)
		else:
			return None

class LocationFactory(object):
	@staticmethod
	def make_location(loc_json):
		if loc_json:
			if isinstance(loc_json, (str, unicode)):
				return loc_json
			else:
				street = loc_json.get("street")
				city = loc_json.get("city")
				state = loc_json.get("state")
				country = loc_json.get("country")
				return Location(street,city,state,country)
		else:
			return None

class AppFactory(object):
	@staticmethod
	def make_app(app_json):
		if app_json:
			id = int(app_json.get("id"))
			name = app_json.get("name")
			return App(id,name)
		else:
			return None
