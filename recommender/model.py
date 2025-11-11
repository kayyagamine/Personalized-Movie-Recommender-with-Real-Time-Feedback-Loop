import pandas as pd
import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, csv_path, omdb_api_key):
        self.movies = pd.read_csv(csv_path, encoding='latin1')
        self.movies.dropna(subset=['title'], inplace=True)
        self.omdb_api_key = omdb_api_key

        # Process and cache available genres and languages
        self._process_genres_and_languages()

    def _process_genres_and_languages(self):
        """Process and extract unique genres and languages from the dataset"""
        all_genres = []
        for genre_str in self.movies['genre'].dropna():
            genres = re.split(r'[,;|/]', str(genre_str))
            for genre in genres:
                cleaned_genre = genre.strip()
                if cleaned_genre and cleaned_genre.lower() not in ['n/a', 'na', '']:
                    all_genres.append(cleaned_genre)

        self.available_genres = sorted(list(set(all_genres)))

        all_languages = []
        for lang_str in self.movies['language'].dropna():
            languages = re.split(r'[,;|/]', str(lang_str))
            for lang in languages:
                cleaned_lang = lang.strip()
                if cleaned_lang and cleaned_lang.lower() not in ['n/a', 'na', '']:
                    all_languages.append(cleaned_lang)

        self.available_languages = sorted(list(set(all_languages)))

    def get_available_genres(self):
        return ['All'] + self.available_genres

    def get_available_languages(self):
        return ['All'] + self.available_languages

    def get_genre_counts(self):
        genre_counts = {}
        for genre in self.available_genres:
            count = self.movies['genre'].str.contains(genre, case=False, na=False).sum()
            genre_counts[genre] = count
        return genre_counts

    def get_language_counts(self):
        lang_counts = {}
        for lang in self.available_languages:
            count = self.movies['language'].str.contains(lang, case=False, na=False).sum()
            lang_counts[lang] = count
        return lang_counts

    def fetch_poster(self, title):
        url = f"http://www.omdbapi.com/?t={title}&apikey={self.omdb_api_key}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if 'Poster' in data and data['Poster'] != 'N/A':
                return data['Poster']
        except Exception as e:
            print(f"Error fetching poster for {title}: {e}")
        return None

    def recommend(self, genre=None, language=None, min_rating=5, max_results=20):
        df = self.movies.copy()
        if genre and genre != 'All':
            df = df[df['genre'].str.contains(genre, case=False, na=False)]
        if language and language != 'All':
            df = df[df['language'].str.contains(language, case=False, na=False)]
        df = df[df['rating'] >= min_rating]
        df = df.sort_values(by='rating', ascending=False)
        df = df.head(max_results)
        if len(df) <= 10:
            df['poster'] = df['title'].apply(self.fetch_poster)
        else:
            df['poster'] = None
        return df[['title', 'genre', 'language', 'rating', 'director', 'cast', 'num_ratings', 'poster']]

    def get_movie_stats(self):
        stats = {
            'total_movies': len(self.movies),
            'unique_genres': len(self.available_genres),
            'unique_languages': len(self.available_languages),
            'avg_rating': self.movies['rating'].mean(),
            'rating_range': (self.movies['rating'].min(), self.movies['rating'].max())
        }
        return stats

    def search_movies(self, query, search_in=['title', 'director', 'cast']):
        df = self.movies.copy()
        mask = pd.Series([False] * len(df))
        for column in search_in:
            if column in df.columns:
                mask |= df[column].str.contains(query, case=False, na=False)
        results = df[mask].sort_values(by='rating', ascending=False)
        return results[['title', 'genre', 'language', 'rating', 'director', 'cast', 'num_ratings']]

    def ml_search_movies(self, genre=None, language=None, min_rating=5, top_n=10):
        df = self.movies.copy()
        df = df[df['rating'] >= min_rating]
        df = df.dropna(subset=['genre', 'language'])
        df['combined_features'] = df['genre'].astype(str) + ' ' + df['language'].astype(str)

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df['combined_features'])

        input_features = (genre if genre else '') + ' ' + (language if language else '')
        input_vector = vectorizer.transform([input_features])

        cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()
        df['similarity'] = cosine_sim
        df = df.sort_values(by=['similarity', 'rating'], ascending=False)
        result = df.head(top_n)
        result['poster'] = None
        return result[['title', 'genre', 'language', 'rating', 'director', 'cast', 'num_ratings', 'poster']].reset_index(drop=True)
