facebook-newsfeed
=================

A minimalistic command line Facebook Newsfeed reader.

I started this project when Facebook completely forgot how to give me posts in chronological order, completely destroying my flow and usage of their product. SO I set out to make a command line Facebook Newsreader app to get around this issue and to decrease the amount of time I had to spend on their site.

This, to put it simply, has been an ENORMOUS pain.

The Facebook Graph API is utter crap. It is incredibly hard to work with due to its inconsistency. Fields are inconsistently applied across posts of the same type.  Classsifying the type of post is hard due to seemingly random and illogical values for a post's 'status_type' field. A post which one person made to another's wall gives an ID which maps to a link to that post, not its actual URL. Determining if something is a wall post is not difficult, but is FAR more difficult than it should be. You cannot tell through Graph if a person has posted that they're with someone else. There is an ambiguous and unreported limit on how far back you can retrieve posts from, which seems to be about a week. The amount of posts you request is processed before FB runs the post list through some filters, meaning the further back you go, the less likely you are to get anything close to the amount of posts you request.

And the list goes on.

The result is that I simply don't care any more. I stopped caring a while ago due to the frustrations of delaing with their API. In fact, I only bothered continuing because I have a couple friends who were interested in contributing.

The code isn't bad, but it's not a great design either, as I didn't care enough to fix design flaws that became apparent late in the game. I tried to adhere to good design principles, but the design of their API made that difficult in some places. And I had a couple ideas to make this app better, but I just want to be done with this.

So have at it. If you want to make this better, feel free. I'm not putting any more of my time into bashing my head against this wall. Or should I say Book. =D

## Requirements
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
    Loads up to 1000 posts between since and until. If until is not provided, loads up to 1000 posts between since and the time the command was issued. With no argume
nts, loads the most recent 25 posts.

### next
Displays the next post(s) in the feed, loading more posts if necessary.
next [<<post_count> or all>]
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
 
