from flask import Flask, render_template, request, redirect, url_for
from recommender import MovieRecommender, FeedbackManager
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "kay"  # Required for flashing messages

# Initialize recommender and feedback manager
recommender = MovieRecommender("data/movies data.csv", 
                              omdb_api_key="379b0c39")
feedback_manager = FeedbackManager(
    "data/movies data.csv",
    feedback_excel_path="data/feedbackdata.csv"
)

@app.route("/", methods=["GET", "POST"])
def index():
    movies = []
    selected_genre = "All"
    selected_language = "All"
    min_rating = 5
    
    # Get available options from the recommender
    available_genres = recommender.get_available_genres()
    available_languages = recommender.get_available_languages()
    
    # Get dataset statistics
    stats = recommender.get_movie_stats()
    
    if request.method == "POST":
        # Get form data
        selected_genre = request.form.get("genre", "All")
        selected_language = request.form.get("language", "All")
        min_rating = float(request.form.get("min_rating", 5))
        max_results = int(request.form.get("max_results", 20))
        
        # Get recommendations based on selected criteria
        df = recommender.recommend(
            genre=selected_genre if selected_genre != "All" else None,
            language=selected_language if selected_language != "All" else None,
            min_rating=min_rating,
            max_results=max_results
        )
        
        # Convert to dictionary for template
        movies = df.to_dict(orient="records")
    
    return render_template("index.html", 
                         movies=movies,
                         available_genres=available_genres,
                         available_languages=available_languages,
                         selected_genre=selected_genre,
                         selected_language=selected_language,
                         min_rating=min_rating,
                         stats=stats)

@app.route("/search", methods=["GET", "POST"])
def search():
    movies = []
    search_query = ""
    is_similar_result = False  # Flag to distinguish result type
    
    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        if search_query:
            # Convert titles to lowercase for match check
            lower_titles = recommender.movies['title'].str.lower()
            
            if search_query.lower() in lower_titles.values:
                # Use ML model to get similar movies
                df = recommender.recommend_similar(search_query, top_n=10)
                is_similar_result = True
            else:
                # Default keyword search
                df = recommender.search_movies(search_query)
            
            movies = df.to_dict(orient="records")
    
    return render_template(
        "search.html", 
        movies=movies,
        search_query=search_query,
        is_similar_result=is_similar_result
    )

@app.route("/stats")
def stats():
    """Display dataset statistics"""
    movie_stats = recommender.get_movie_stats()
    genre_counts = recommender.get_genre_counts()
    language_counts = recommender.get_language_counts()
    
    return render_template("stats.html",
                         stats=movie_stats,
                         genre_counts=genre_counts,
                         language_counts=language_counts)

@app.route("/feedback", methods=["POST"])
def feedback():
    movie_id_str = request.form.get("movie_id", "")
    rating_str = request.form.get("rating", "")
    
    if not movie_id_str or not rating_str:
        flash("Missing feedback data.", "error")
        return redirect(url_for("index"))
    
    try:
        movie_id = int(movie_id_str)
        rating = float(rating_str)
    except ValueError:
        flash("Invalid input. Please submit a valid movie ID and rating.", "error")
        return redirect(url_for("index"))
    
    feedback_manager.update_rating(movie_id, rating)
    flash("Thanks! Your feedback has been recorded.", "success")
    return redirect(url_for("index"))

@app.route("/process-feedback")
def process_feedback_excel():
    feedback_manager.update_all_from_feedback()
    flash("Feedback processed successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
