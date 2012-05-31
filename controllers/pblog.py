#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
import md5
import random
from config import settings

T_ARTICLE = 'article'
T_COMMENT = 'comment'
T_MSG = 'msg'
T_USER = 'user'

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
      if len(query)==0 and page != 0:
        return render.error()
      count = int(db.query("select count(*) from " + T_ARTICLE)[0]["count(*)"])
      ne = pre = 0
      maxpage = count / 5
      
      if maxpage % 5 != 0:
        maxpage += 1

      if page > 0:
        pre = page

      if page+1 < maxpage:
        ne = page + 2
      return render.index(query, ne, pre)
    except:
      print 'expcetion when getting page from url,page=%d' % page
      return render.error()

class Post:
  def GET(self):
    try:
      post_id = int(web.input(id = '0').id)
      myVar = dict(id=post_id)
      if post_id == 0:
        return render.error()
      post = db.select(T_ARTICLE,myVar, where="id=$id",limit = 1)
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
      return render.post(post[0], pre_post_id, ne_post_id)
    except:
      print 'exception when getting post'
      return render.error()

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
      posts = db.select(T_ARTICLE, limit = "%d,5"%(page * 5), where="tag like '%"+tag_filted+"%'", order="date DESC")
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
      return render.error()
