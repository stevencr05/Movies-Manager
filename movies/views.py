from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.dateparse import parse_date
from django.utils import timezone
from .models import Movie
from .forms import MovieForm, UserProfileForm, ChangePasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'movies/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movies_list')  # Redirection vers le tableau de bord après l'inscription
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



# Vue pour la liste des tâches
class MovieListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = Movie.objects.filter(user=self.request.user)
        
        # Filtrage par genre
        genre_filter = self.request.GET.get('genre')
        if genre_filter:
            queryset = queryset.filter(genre=genre_filter)
        
        # Filtrage par date de sortie
        year_filter = self.request.GET.get('releaseYear')
        now = timezone.now()
        
        if year_filter == 'this_year':
            start_date = datetime(now.year, 1, 1)
            end_date = datetime(now.year, 12, 31)
            queryset = queryset.filter(releaseYear__range=(start_date, end_date))
        elif year_filter == 'historical':
            start_date = datetime(1900, 1, 1)
            end_date = datetime(2023, 12, 31)
            queryset = queryset.filter(releaseYear__range=(start_date, end_date))
        
        # Fonctionnalité de recherche
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(director__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Movie.objects.values_list('genre', flat=True).distinct()
        return context


# Vue pour la création des films    
class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/create_movie.html'
    success_url = reverse_lazy('movies_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


# Vue pour la mise à jour des films
class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/update_movie.html'
    success_url = reverse_lazy('movies_list')
    
    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)
    
    
# Vue pour la suppression des films
class MovieDeleteListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/delete_movie.html'
    context_object_name = 'movies'

    def get_queryset(self):
        """
        Filtre les films pour ne montrer que ceux appartenant à l'utilisateur connecté.
        """
        return Movie.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Gère la suppression d'un film à partir du formulaire.
        """
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = Movie.objects.filter(id=movie_id, user=self.request.user).first()
            if movie:
                movie.delete()
                messages.success(request, 'Film supprimé avec succès.')
            else:
                messages.error(request, 'Film non trouvé ou vous n\'avez pas les droits nécessaires pour le supprimer.')
        return redirect('delete_movie')
    

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(data=request.POST, user=request.user)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Important to keep the user logged in after changing the password
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = ChangePasswordForm(user=request.user)

    return render(request, 'movies/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
