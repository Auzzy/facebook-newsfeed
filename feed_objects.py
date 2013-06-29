from datetime import datetime
import time

class Post(object):
	def __init__(self, id, timestamp, place, url, users, contents, metadata):
		self.id = id
		self.timestamp = timestamp
		self.place = place
		self.url = url
		self.users = users
		self.contents = contents
		self.metadata = metadata
	
	def update(self, new_post):
		self.timestamp = new_post.timestamp
		self.place = new_post.place
		self.users = new_post.users
		self.contents = new_post.contents
		self.metadata = new_post.metadata

	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		return self.id == other.id
	
	def to_string(self, **kwargs):
		post_str = "Posted by {users}\n".format(users=self.users.to_string(**kwargs))
		post_str += "Posted at {timestamp}".format(timestamp=self.timestamp)
		if self.place:
			post_str += " from {place}".format(place=self.place)
		post_str += '\n' + str(self.contents.to_string(**kwargs)) + '\n'
		post_str += str(self.metadata.to_string(**kwargs))
		return post_str

	def __str__(self):
		return self.to_string()

class PostUsers(object):
	def __init__(self, from_, to, with_tags, msg_tags):
		self.from_ = from_
		self.to = to
		self.with_tags = with_tags
		self.msg_tags = msg_tags
	
	def to_string(self, **kwargs):
		users_str = str(self.from_)
		if self.with_tags:
			with_str = ", ".join([str(user) for user in self.with_tags])
			users_str += " with ({with_})".format(with_=with_str)
		if self.to:
			to_str = str(self.to)
			users_str += " to {to}".format(to=to_str)
		return users_str
	
	def __str__(self):
		return self.to_string()

class PostContents(object):
	def __init__(self, message, story, resources, post_type, status_type):
		self.message = message
		self.story = story
		self.resources = resources
		self.post_type = post_type
		self.status_type = status_type
	
	def to_string(self, **kwargs):
		contents_str = "Post:\n"
		contents_str += str(self.message if self.message else self.story)
		if self.resources:
			resource_str = ", ".join(self.resources.resource_types())
			contents_str += "\nResources in this post: {0}".format(resource_str)
		return contents_str

	def __str__(self):
		return self.to_string()

class PostResources(object):
	def __init__(self, link, photo, video):
		self.link = link
		self.photo = photo
		self.video = video
	
	def resource_types(self):
		resources = []
		if self.link:
			resources.append("link")
		if self.photo:
			resources.append("photo")
		if self.video:
			resources.append("video")
		return resources
	
	def __nonzero__(self):
		return bool(self.link or self.photo or self.video)

	def __str__(self):
		pass

class PostMetadata(object):
	def __init__(self, comments, likes, app):
		self.comments = comments
		self.likes = likes
		self.app = app
	
	def to_string(self, **kwargs):
		show_comments = kwargs.get("comments")

		meta_str = "There are {comments} comments and {likes} likes on this post.".format(comments=len(self.comments),likes=len(self.likes))
		if self.app:
			meta_str += "\nPosted using {app}".format(app=self.app)
		if show_comments and self.comments:
			meta_str += '\n' + self._comment_list_to_string(self.comments)
		return meta_str
	
	def _comment_list_to_string(self, comments):
		sep = '\t' + 60*'-' + '\n'

		comment_str_list = ['\t' + ('\n\t'.join(str(comment).splitlines())) for comment in comments]
		comment_list_str = ('\n' + sep).join(comment_str_list)
		return sep + comment_list_str + '\n' + sep

	def __str__(self):
		return self.to_string()


class Timestamp(object):
	DATE_FORMAT = "%B %d, %Y"
	TIME_FORMAT = "%H:%M:%S"
	TIMESTAMP_FORMAT = "{time} on {date}".format(date=DATE_FORMAT,time=TIME_FORMAT)
	
	def __init__(self, seconds=None):
		self.seconds = seconds if seconds else int(time.time())
		self.datetime = datetime.fromtimestamp(self.seconds)

	def as_seconds(self):
		return self.seconds
	
	def date(self):
		return self.datetime.strftime(Timestamp.DATE_FORMAT)

	def time(self):
		return self.datetime.strftime(Timestamp.TIME_FORMAT)

	def __lt__(self, other):
		return self.datetime < other.datetime

	def __le__(self, other):
		return self.datetime <= other.datetime
	
	def __eq__(self, other):
		return self.datetime == other.datetime

	def __ne__(self, other):
		return self.datetime != other.datetime

	def __gt__(self, other):
		return self.datetime > other.datetime

	def __ge__(self, other):
		return self.datetime >= other.datetime

	def __str__(self):
		return self.datetime.strftime(Timestamp.TIMESTAMP_FORMAT)

class User(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
	
	def __hash__(self):
		return self.id

	def __eq__(self, other):
		return self.id == other.id

	def __str__(self):
		return self.name

class Comment(object):
	def __init__(self, id, timestamp, from_, message, tags, like_count):
		self.id = id
		self.timestamp = timestamp
		self.from_ = from_
		self.message = message
		self.tags = tags
		self.like_count = like_count
	
	def __hash__(self):
		return int(self.id.replace('_',''))
	
	def __eq__(self, other):
		return self.id == other.id

	def __str__(self):
		comment_str = "Posted at {timestamp} by {from_}".format(timestamp=self.timestamp,from_=self.from_)
		comment_str += "\nPost:\n{message}".format(message=self.message)
		comment_str += "\nThere are {likes} likes on this comment.".format(likes=self.like_count)
		return comment_str

class Link(object):
	def __init__(self, name, url, caption, description):
		self.name = name
		self.url = url
		self.caption = caption
		self.description = description
	
	def __eq__(self, other):
		return self.url == other.url
	
	def __str__(self):
		pass

class Place(object):
	def __init__(self, id, name, loc):
		self.id = id
		self.name = name
		self.loc = loc
	
	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		return self.id == other.id

	def __str__(self):
		return "{name} ({loc})".format(name=self.name,loc=self.loc)

class Location(object):
	def __init__(self, street, city, state, country):
		self.street = street
		self.city = city
		self.state = state
		self.country = country
	
	def __eq__(self, other):
		return self.street == other.street and \
			self.city == other.city and \
			self.state == other.state and \
			self.country == other.country

	def __str__(self):
		return ','.join([self.street,self.city,self.state,self.country])

class App(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
	
	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		return self.id == other.id

	def __str__(self):
		return self.name
