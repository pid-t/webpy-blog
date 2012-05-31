#!/usr/bin/env python
# coding: utf-8
import web
from config.admin_url import admin_urls

admin_app = web.application(admin_urls, locals())

pre_fix = 'controllers.pblog.'

urls = (
  '/(.*)/', pre_fix + 'Redirect',
  '/',  pre_fix + 'Index',
  '/post', pre_fix + 'Post',
  '/tag', pre_fix + 'Tag',
  '/about',pre_fix + 'About',
  '/admin',admin_app, 
)
