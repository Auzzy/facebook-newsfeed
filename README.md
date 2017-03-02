facebook-newsfeed
=================

A minimalistic command line Facebook Newsfeed reader.

Not my proudest work, but one that enough people were asking for when I off-handedly mentioned it. I wrote it mostly with my own usecases in mind, which primarily had to do with ensuring Facebook stories came up in chonological order. I encountered a number of frustrations when coding against the Graph API in early 2013, so development never advanced very far. Once I got it working well-enough for people to mess with, I abandoned it.

## Requirements
Python 2.7: http://www.python.org/download/

The Facebook SDK for Python: https://github.com/pythonforfacebook/facebook-sdk/blob/master/facebook.py

## Known Bugs
If you try to load posts from more than a few days ago, the results are non-deterministic. Subsequent calls may miss posts that showed up originally. My brief investigation into this problem did not reveal an answer. I don't know if this is due to the Graph API or something I'm doing.

## Commands
### comments
Displays comments on the specified post(s).
comments [<int> ...]
    Redisplays currently displayed posts with the corresponding indices along with all associated comments. Invalid indices will be ignored.
    Providing no arguments will reload all currently displayed posts with all associated comments.

### go
Opens the posts with the specified indices in your default browser.
go [<int> ...]
    Open the post(s) with the provided indices in your default browser.
    Providing no arguments will open all currently displayed posts in your default browser.

### help
Prints help messages.
help [<command>]
    If no arguments are provided, displays a brief description of what each available command does.
    If the name of a command is provided, prints detailed usage information for that command.

### load
Loads posts from your newsfeed.
load [<since> [<until>]]
    If present, since and until are expected to be a UNIX timestamp (seconds since 1/1/1970 (the epoch)).
    Loads up to 1000 posts between since and until. If until is not provided, loads up to 1000 posts between since and the time the command was issued. With no arguments, loads the most recent 25 posts.

### next
Displays the next post(s) in the feed, loading more posts if necessary.
next [<<post_count> or 'all'>]
    'all' will display all posts from the next one until the most recent post. Any unloaded posts are loaded, then all are displayed.
    Providing a post_count will cause that many posts to be displayed. Any unloaded posts are loaded, then all are displayed.
    If no arguments are provided, post_count is set equal to 1.

### prev
Displays the previous post(s) in the feed, loading more posts if necessary.
prev [<post_count>]
    Providing a post_count will cause that many posts to be displayed. Any unloaded posts are loaded, then all are displayed.
    If no arguments are provided, post_count is set equal to 1.

### print
Redisplays posts with the corresponding indices.
print [comments] [<int> ...]
    Redisplays just the posts with the provided indices. Invalid indices will be ignored.
    If the first argument is 'comments', displays the appropriate posts with all comments.
    Providing no arguments will reload all currently displayed posts.
 
