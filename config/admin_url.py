import web
admin_prefix = 'controllers.blogAdmin.'
admin_urls = (
  '/login', admin_prefix + 'Login',
  '/logout',admin_prefix + 'Logout',
  '/index', admin_prefix + 'Index',
  '/edit_post', admin_prefix + "EditPost",
  '/add_post', admin_prefix + "AddPost",
  '/uploadImage', admin_prefix + "UploadImage",
  '/updatePost', admin_prefix + "UpdatePost",
  '/del_post', admin_prefix + "DeletePost",
)
