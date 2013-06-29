# Combined what I found in the following 2 blog posts, as well as some of my own tweaks, in order to create this module.
# 	- http://facebook-python-library.docs-library.appspot.com/facebook-python/examples/oauth.html
# 	- http://blog.carduner.net/2010/05/26/authenticating-with-facebook-on-the-command-line-using-python/

import urllib
import urlparse
import BaseHTTPServer
import webbrowser
 
APP_ID = "168145173352287"
APP_SECRET = "75b314530c77b32c082aae5f0f4c581f"

CODE_URL = "https://www.facebook.com/dialog/oauth?"
TOKEN_URL = "https://graph.facebook.com/oauth/access_token?"
REDIRECT_URL = "http://127.0.0.1:8080/"
PERMISSIONS = [
		"read_stream",
		"user_status",
		"friends_status"
	      ]

CODE_ARGS = {
		"client_id":APP_ID,
		"redirect_uri":REDIRECT_URL,
		"scope":','.join(PERMISSIONS)
	    }
	
access_token = None
error = False

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		global access_token,error

		self.send_response(200)
	        self.send_header("Content-type", "text/html")
        	self.end_headers()

		code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
		if code is None:
			error = True
			return
		
		token_args = CODE_ARGS
		token_args["client_secret"] = APP_SECRET
		token_args["code"] = code[0]
		
		token_request = TOKEN_URL + urllib.urlencode(token_args)
		response = urllib.urlopen(token_request).read()
		response_dict = urlparse.parse_qs(response)
		access_token = response_dict["access_token"][-1]
		self.wfile.write("You have successfully logged into facebook. You can close this window now.")

	# Ensures 
	def log_request(self, code='-', size='-'):
		pass

def login():
	global access_token,error
	
	redirect_uri = urlparse.urlparse(CODE_ARGS["redirect_uri"])
	server_params = (redirect_uri.hostname,redirect_uri.port)
	httpd = BaseHTTPServer.HTTPServer(server_params, RequestHandler)	
	
	code_request = CODE_URL + urllib.urlencode(CODE_ARGS)
	webbrowser.open(code_request)
	while not access_token and not error:
		try:
			httpd.handle_request()
		except:
			error = True
	return access_token

if __name__=="__main__":
	print login()
