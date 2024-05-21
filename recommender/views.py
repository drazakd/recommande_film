from django.shortcuts import render
from django.http import HttpResponse
import pickle
from django.contrib import messages

# Charger les modèles
new_df = pickle.load(open('models/movie_list.pkl', 'rb'))
similarity = pickle.load(open('models/similarite.pkl', 'rb'))
# movies_genres = pickle.load(open('models/movies_genres.pkl', 'rb'))


def home(request):
    return render(request, 'recommander/home.html')


# def recommend(request):
#     if request.method == 'POST':
#         movie = request.POST.get('movie')
#         genre = request.POST.get('genre')
#         keywords = request.POST.get('keywords')
#
#         recommendations = get_recommendations(movie, genre, keywords)
#         return render(request, 'recommander/recommend.html', {'recommendations': recommendations, 'movie': movie})
#     return HttpResponse("Please use the form to get recommendations.")


# def get_recommendations(movie, genre=None, keywords=None):
#     indices = set(new_df.index)
#
#     # Filtrer par genre
#     if genre:
#         genre_indices = movies_genres[movies_genres['genres'].str.contains(genre, case=False)].index
#         indices = indices.intersection(set(genre_indices))
#
#     # Filtrer par mots-clés
#     if keywords:
#         keyword_indices = movies_genres[movies_genres['tags'].str.contains(keywords, case=False)].index
#         indices = indices.intersection(set(keyword_indices))
#
#     # Trouver les distances de similarité
#     movie_index = new_df[new_df['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[movie_index])), key=lambda x: x[1], reverse=True)
#
#     # Récupérer les recommandations
#     recommended_movies = []
#     for i, dist in distances[1:]:
#         if i in indices:
#             recommended_movies.append(new_df.iloc[i]['title'])
#             if len(recommended_movies) == 5:
#                 break
#
#     return recommended_movies

def recommend(request):
    if request.method == 'POST':
        movie = request.POST.get('movie')

        # Vérifiez si le film existe dans le DataFrame
        if movie not in new_df['title'].values:
            messages.error(request, "Le film que vous avez saisi n'est pas dans la base de données.")
            return render(request, 'recommander/home.html')

        recommendations = get_recommendations(movie)
        return render(request, 'recommander/recommend.html', {'recommendations': recommendations, 'movie': movie})
    return HttpResponse("Please use the form to get recommendations.")


def get_recommendations(movie):
    # Vérifiez si le film existe dans le DataFrame
    if movie not in new_df['title'].values:
        return []

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for i, dist in distances[1:6]:  # Limiter les recommandations aux 5 premiers films
        recommended_movies.append(new_df.iloc[i]['title'])

    return recommended_movies

