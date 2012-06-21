#! /usr/bin/env python
# -*- coding: utf-8 -*-

import web

web.config.debug = True
db = web.database(dbn='mysql', db='blog',user='root',pw='root')
render = web.template.render('tpls/',base="layout")
post_content = web.template.render('tpls/')
admin_render = web.template.render('tpls/admin-tpls')
config = web.storage(
    email = 'ddk.tsang@gmail.com',
    site_name = 'pBlog',
    static = '/static',
    description='A Simple Python Blog',
    author='ddk',
)
image_upload_dir = r"/home/ddk/opensource/python/webpy-blog/static/upload/imgs/"
file_upload_dir = r"/home/ddk/opensource/python/webpy-blog/static/upload/"
web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = post_content
