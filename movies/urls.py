from django.urls import path
from movies import views as movie_views  # Importer directement les vues du module movies
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', movie_views.index, name='index'),  # Utiliser movie_views.index si c'est dans le module movies
    path('signup/', movie_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("movies/", movie_views.MovieListView.as_view(), name="movies_list"),
    path("movies/create/", movie_views.MovieCreateView.as_view(), name="create_movie"),
    path("movies/<int:pk>/update/", movie_views.MovieUpdateView.as_view(), name="update_movie"),
    path('movies/delete/', movie_views.MovieDeleteListView.as_view(), name='delete_movie'),
    path('profile/', movie_views.profile_view, name='profile'),
]