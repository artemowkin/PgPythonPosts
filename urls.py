import views


urlpatterns = {
	'/': views.homepage,
	'/login/': views.login,
	'/logout/': views.logout,
	'/signup/': views.signup,
	'/posts/': views.posts,
	'/posts/create/': views.create_post,
}