#! /usr/bin/env python
# -*- coding:utf-8 -*-

import web
import md5
import random
import json
from config import settings

db = settings.db
adminRender = settings.admin_render
T_USER = 'user'
T_ARTICLE = 'article'
salt = '&A102ad@#)'

class Login:
  ''' login logic '''

  def GET(self):
    if web.ctx.session.id == 1:
      raise web.seeother('/index')
    return adminRender.login()
  
  def POST(self):
    user_data = web.input()
    username = user_data.get('username','')
    password = user_data.get('password','')
    if username=='' or password=='':
      return adminRender.login_error()
    data = db.select(T_USER, where=('user="'+username+'"'))
    if (len(data) ==0):
      return adminRender.login_error()
    password += salt
    password = md5.new(password).hexdigest()
    if password != data[0].password:
      return adminRender.login_error()
    seed = random.randint(0,100000)
    web.ctx.session.hash = md5.new((username + password + str(seed))).hexdigest()
    web.ctx.session.id = 1
    web.ctx.session.seed = seed
    raise web.seeother('/index')

class Logout:
  '''logout logic '''

  def GET(self):
    web.ctx.session.id = 0
    web.ctx.session.seed = 0
    web.ctx.session.hash = ''
    raise web.seeother('/login')

class Index:
  ''' going to admin index logic '''
  def GET(self):
    if web.ctx.session.id!=1:
      return adminRender.login()
    try:
      page = int(web.input(p = '1').p) -1;
      query = db.select(T_ARTICLE,what='id,title,date',limit='%d,5'%(page*5),order='date DESC')
      if len(query)==0 and page !=0:
        return adminRender.error()
      count = int(db.query('select count(*) from ' + T_ARTICLE)[0]["count(*)"])
      ne = pre = 0
      maxpage = count / 5
      if maxpage % 5 != 0:
        maxpage += 1
      if page > 0:
        pre = page
      if page + 1 < maxpage:
        ne = page + 2
      return adminRender.posts(query, ne, pre, page+1, maxpage)
    except:
      return adminRender.error()
    return adminRender.posts()

class AddPost:
  '''add post login '''
  def GET(self):
    if web.ctx.session.id != 1:
      return adminRender.login()
    return adminRender.post_edit(0,'','','')

class UploadImage:
  ''' upload and save the images '''
  def POST(self):
    files = web.input(imgFile={})
    imgDomain = '/static/upload/imgs/'
    saveDir = '/home/ddk/opensource/python/pblog/static/upload/imgs/'
    web.header('Content-Type','application/json')
    if 'imgFile' in files:
      print 'upload image via post method'
      filePath = files.imgFile.filename.replace('\\','/')
      filename = filePath.split('/')[-1]
      savePath = saveDir + filename
      fout = open(savePath,'w')
      fout.write(files.imgFile.file.read())
      fout.close()
      successJson = dict(error=0,url=(imgDomain + filename))
      return json.dumps(successJson)
    else:
      errorJson = dict(error=1,message='上出失败!')
      return json.dumps(errorJson)

class EditPost:
  ''' going to edit post logic '''
  
  def GET(self):
    post_id = int(web.input(id='-1').id)
    if post_id == -1:
      return adminRender.error()
    myVar = dict(id=post_id)
    posts = db.select(T_ARTICLE, myVar, where="id=$id", limit = 1)
    if len(posts) == 0:
      return adminRender.error()
    post = posts[0]
    return adminRender.post_edit(post.id, post.title,post.tag, post.content)

class UpdatePost:
  ''' update post logic'''
  def POST(self):
    data = web.input(id='0', title='',content='',tag='')
    post_id = int(data.id)
    isNewPost = False
    if post_id == 0:
      isNewPost = True
    atitle = data.title
    text = data.content
    post_tag = data.tag
    if isNewPost:
      db.insert(T_ARTICLE,id=0,date=web.SQLLiteral("NOW()"),usrid=web.ctx.session.id,comment=0,title=atitle,content=text,tag = post_tag)
    else:
      db.update(T_ARTICLE,where='id=$post_id', vars = {'post_id':post_id},title=atitle,content=text,tag = post_tag)
    raise web.seeother('/index')

class DeletePost:
  '''Delete post login '''
  def GET(self):
    post_id = int(web.input(id='0').id);
    if post_id == 0:
      adminRender.error()
    db.delete(T_ARTICLE, where='id=$post_id', vars={'post_id':post_id})
    raise web.seeother('/index')