import pickle
import difflib
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent


def load_data(file_name):
    with (BASE_DIR / file_name).open("rb") as f:
        return pickle.load(f)


def recommend_movies(movie_name: str, top_n: int = 5):
    movies = load_data("movies_list.pkl")
    similarity_scores = load_data("cosine_matrix.pkl")

    movie_titles = [title for _, title in movies]
    if not movie_titles:
        return []

    normalized_name = movie_name.strip().lower()
    title_lookup = {title.lower(): title for title in movie_titles}

    if normalized_name in title_lookup:
        target_title = title_lookup[normalized_name]
    else:
        matches = difflib.get_close_matches(
            normalized_name,
            [title.lower() for title in movie_titles],
            n=1,
            cutoff=0.6,
        )
        if not matches:
            return []
        target_title = next(title for title in movie_titles if title.lower() == matches[0])

    movie_index = movie_titles.index(target_title)
    similar_movies_indices = similarity_scores[movie_index].argsort()[-(top_n + 1):-1][::-1]
    recommended_movies = [movie_titles[i] for i in similar_movies_indices if i != movie_index]

    return recommended_movies[:top_n]


if __name__ == "__main__":
    movie_name = input("Enter a movie name: ").strip()
    recommendations = recommend_movies(movie_name)
    if recommendations:
        print("Recommended movies:")
        for movie in recommendations:
            print(movie)
    else:
        print("No recommendations found.")