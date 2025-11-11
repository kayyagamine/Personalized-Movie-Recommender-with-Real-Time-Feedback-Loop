import pandas as pd

class FeedbackManager:
    def __init__(self, csv_path, feedback_excel_path):
        self.csv_path = csv_path
        self.feedback_excel_path = feedback_excel_path
        self.movies = pd.read_csv(csv_path, encoding='latin1')

        # Normalize column names to avoid mismatch due to spaces or case
        self.movies.columns = self.movies.columns.str.strip().str.lower()

    def update_rating(self, movie_id, user_rating):
        idx_list = self.movies.index[self.movies['movie_id'] == movie_id].tolist()
        if not idx_list:
            print(f"Movie ID {movie_id} not found.")
            return

        idx = idx_list[0]

        # Update rating
        self.movies.at[idx, 'rating'] = user_rating

        # Optional: also increase num_ratings by 1
        if 'num_ratings' in self.movies.columns:
            self.movies.at[idx, 'num_ratings'] += 1

        # Save immediately
        self.movies.to_csv(self.csv_path, index=False)
        print(f"Updated movie_id {movie_id} with new rating {user_rating}.")

    def update_all_from_feedback(self):
        try:
            feedback_df = pd.read_csv(self.feedback_excel_path)
        except Exception as e:
            print(f"[ERROR] Could not read feedback file: {e}")
            return

        print(f"Processing {len(feedback_df)} feedback entries...")

        for _, row in feedback_df.iterrows():
            try:
                movie_id = int(row['movie_id'])
                rating = float(row['rating'])
                self.update_rating(movie_id, rating)
            except Exception as e:
                print(f"Error processing row {row}: {e}")

        print("Movie CSV updated.")

        # Clear feedback file
        pd.DataFrame(columns=["movie_id", "rating"]).to_csv(self.feedback_excel_path, index=False)
        print("Feedback file cleared.")
