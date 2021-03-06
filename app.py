import os
import datetime, time
from bottle import route, request, redirect, template, run, static_file, abort
import dataset
import jinja2
import feedparser
import markdown

os.chdir(os.path.dirname(__file__))
templateEnv = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

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
	temp = templateEnv.get_template(name)
	return temp.render(dict = dict)
	
def checkExternalPosts():
	# check stored timestamp, grab new feeds from github and tumblr
	# should get called every time a page is loaded
	pass

@route('/static/<filename:path>')
def static(filename):
	return static_file(filename, root='static')

	
# acutal routes

@route('/')
def index():
	db = dataset.connect('sqlite:///blog.db')
	dict = {}

	dict["posts"] = db["posts"].find(order_by='-timepost')
	
	return render('index.html', dict = dict)
	
@route('/tagged/<tag>')
def tagged(tag):
	db = dataset.connect('sqlite:///blog.db')
	dict = {}
	dict["posts"] = []
	
	return render('tagged.html', dict = dict)
	
@route('/post/<id:int>')
def post(id):
	db = dataset.connect('sqlite:///blog.db')
	dict = {}

	dict["post"] = db["posts"].find_one(id = id)
	
	if dict["post"]:
		return render('post.html', dict = dict)
	else:
		abort(404, "Sorry, could not find that post.")
	
@route('/update', method='GET')
def update():
	dict = {}
	
	return render('update.html', dict = dict)
	
@route('/update', method='POST')
def newUpdate():
	db = dataset.connect('sqlite:///blog.db')
	
	title = request.forms.get('title')
	content = request.forms.get('content')
	tag = request.forms.get('tag')
	password = request.forms.get('password')
	
	if title and content and tag and password:
		if password == "dummy":
			origianlContent = content
			content = markdown.markdown(content)
			db['posts'].insert( {'title': title, 'content': content, 'type': 'blog', 'originalContent': origianlContent, 'tagged': tag, 'timepost': str(time.time()), 'timestamp': str(datetime.datetime.now().strftime("%b %d %Y - %I:%M %p")) } )	
	else:
		print "fail!"
	
	redirect("/")
		
	
if __name__ == "__main__":
	# run as test server
	# db['posts'].insert( {'title': 'welcome to the blog!', 'content': 'hello there friend! welcome to my blog!!', 'type':'blog', 'tagged':'misc', 'timestamp': str(datetime.datetime.now().strftime("%b %d %Y - %I:%M %p")) } )	
	run(host='localhost', port=8080)
