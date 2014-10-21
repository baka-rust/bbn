from bottle import route, post, template, run, static_file
import dataset
import jinja2
import feedparser
import markdown

#TODO:
	# with https://developer.github.com/v3/activity/feeds/
	# get personal feed from github
		# http://www.pythonforbeginners.com/feedparser/using-feedparser-in-python
	# get tumblr feed and twitter via rss too
		# http://deltaspooky.tumblr.com/rss
	# use cute icons next to those posts, make the background a different color probably
	# also make sure it only grabs the feed every once in a while by saving a feed timestamp and when its up getting the new one (once every 5 mins?)
	# parse markdown to html for posts

	# allow for posts to be made in simple markdown, either write parser or grab one
		# https://pythonhosted.org/Markdown/reference.html

# helper methods

def render(name, dict=None):
	f = open('templates/'+name, 'r')
	data = f.read()
	f.close()
	temp = jinja2.Template(data)
	return temp.render(dict = dict)
	
def checkRSS():
	# check stored timestamp, grab new feeds from github and tumblr
	# should get called every time a page is loaded
	pass

@route('/static/<filename:path>')
def static(filename):
	return static_file(filename, root='static')

	
# acutal routes

@route('/')
def index():
	dict = {}
	dict["posts"] = []
	
	return render('base.html', dict = dict)
	
@route('/tagged/<tag>')
def tagged(tag):
	dict = {}
	dict["posts"] = []
	
	return render('tagged.html', dict = dict)
	
@route('/post/<id:int>')
def post(id):
	dict = {}
	dict["posts"] = []
	
	return render('post.html', dict = dict)

	
if __name__ == "__main__":
	# run as test server
	run(host='localhost', port=8080)
