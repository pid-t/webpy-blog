#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
import md5
import random
import traceback
from config import settings

T_ARTICLE = 'article'
T_COMMENT = 'comment'
T_MSG = 'msg'
T_USER = 'user'
T_TAG = 'tag'

render = settings.render
db = settings.db
reload(sys)
sys.setdefaultencoding("utf-8")

def isAdmin():
  if session.id == 0:
    return False
  data = db.select(usert,where="id="+str(session.id))
  if(len(data) == 0):
    return False
  data = data[0]
  if md5.new((data.user + data.password + str(session.seed)).hexdigest()) == session.hash:
    return True
  else:
    return False

class Redirect:
  def GET(self, path):
    web.seeother('/' + path)

class Index:
  def GET(self):
    try:
      page = int(web.input(p = '1').p) - 1
      query = db.select(T_ARTICLE,limit="%d,5"%(page*5),order="date DESC")
      posts = []
      if len(query)==0 and page != 0:
        return render.error()

      for post in query:
        article = {}
        article['id'] = post.id
        article['date'] = post.date
        article['tags'] = post.tag
        article['title'] = post.title
        article['content'] = post.content
        c_count = int(db.query("select count(*) from " + T_COMMENT + " where articleid = $post_id", vars={"post_id":post.id})[0]["count(*)"])
        article['c_count'] = c_count
        print "post_id=%d,c_count:%d" % (post.id, article['c_count'])
        posts.append(article)

      count = int(db.query("select count(*) from " + T_ARTICLE)[0]["count(*)"])
      ne = pre = 0
      maxpage = count / 5
      
      if maxpage % 5 != 0:
        maxpage += 1

      if page > 0:
        pre = page

      if page+1 < maxpage:
        ne = page + 2
      return render.index(posts, ne, pre)
    except:
      print traceback.format_exc()
      return render.error()

class Post:
  def GET(self):
    try:
      post_id = int(web.input(id = '0').id)
      myVar = dict(id=post_id)
      if post_id == 0:
        return render.error()
      post = db.select(T_ARTICLE,myVar, where="id=$id",limit = 1)
      comments = db.select(T_COMMENT,myVar, where="articleid=$id");
      ne_post = db.select(T_ARTICLE, myVar, where="id > $id",limit = 1)
      pre_post = db.select(T_ARTICLE, myVar, where='id < $id', limit = 1, order='date DESC')
      if len(post) == 0:
        return render.error()
      if len(pre_post) == 0:
        pre_post_id = 0
      else:
        pre_post_id = pre_post[0].id
      if len(ne_post)==0:
        ne_post_id = 0
      else:
        ne_post_id = ne_post[0].id
      return render.post(post[0], pre_post_id, ne_post_id, len(comments), comments)
    except:
      print 'exception when getting post'
      print traceback.format_exc()
      return render.error()
    
  def POST(self):
    user_data = web.input()
    author = user_data.get('author', '')
    email = user_data.get('email', '')
    website = user_data.get('website', '')
    post_id = int(user_data.get('post_id', '-1'))
    content = user_data.get('content', '')
    if post_id == -1:
      return render.error()
    db.insert(T_COMMENT, id=0, date=web.SQLLiteral("NOW()"), homepage=website, email = email, articleid = post_id, content = content, author = author)
    web.seeother('/post?id=' + user_data.get('post_id', ''))

class About:
  def GET(self):
    return render.about()
    
class Tag:
  def GET(self):
    try:
      page = int(web.input(p = '1').p) - 1;
      tag_filted = web.input(key='').key
      if tag_filted == '':
        return render.error()
      query = db.select(T_ARTICLE, limit = "%d,5"%(page * 5), where="tag like '%"+tag_filted+"%'", order="date DESC")
      posts = []
      for post in query:
        article = {}
        article['id'] = post.id
        article['date'] = post.date
        article['tags'] = post.tag
        article['title'] = post.title
        article['content'] = post.content
        c_count = int(db.query("select count(*) from " + T_COMMENT + " where articleid = $post_id", vars={"post_id":post.id})[0]["count(*)"])
        article['c_count'] = c_count
        print "post_id=%d,c_count:%d" % (post.id, article['c_count'])
        posts.append(article)


      count = int(db.query("select count(*) from " + T_ARTICLE + " where tag like '%" + tag_filted +"%'")[0]["count(*)"])
      ne = pre = 0
      maxpage = count / 5
      if maxpage % 5 != 0:
        maxpage += 1
      if page > 0:
        pre = page
      if page+1 < maxpage:
        ne = page + 2
      return render.tag(tag_filted,posts, ne, pre);
    except:
      print traceback.format_exc()
      return render.error()
