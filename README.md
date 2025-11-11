# 🎬 Personalized Movie Recommender with Real-Time Feedback Loop

A **Python + Flask** based movie recommendation system that uses **TF-IDF** and **Cosine Similarity** to suggest movies similar to a given title.  
It dynamically fetches posters using the **OMDb API** and includes a **real-time feedback loop**, allowing users to rate movies and refine recommendations interactively.  
The project is containerized with **Docker** and integrated with **GitHub Actions CI/CD** for automated builds and deployments.

---

## 🧠 Overview

This project demonstrates a lightweight **content-based recommender system**.  
It reads movie metadata, computes TF-IDF vectors for movie plots, and calculates cosine similarity between movies to find related titles.  
User feedback (ratings) is captured in real time and logged into a CSV file (`feedbackdata.csv`), which helps the system refine recommendations dynamically.  
Movie posters and metadata are retrieved from the **OMDb API**.

---

## ⚙️ Features

- 🔍 **Content-based filtering** using TF-IDF and Cosine Similarity  
- 💬 **Real-time feedback loop** with user ratings stored in CSV  
- 🎞️ **Dynamic movie posters** via OMDb API integration  
- 🧠 **Adaptive recommendations** that improve over time  
- 🐳 **Dockerized** for cross-platform deployment  
- ⚡ **CI/CD** setup with GitHub Actions

---

## 🧰 Tech Stack

| Category | Tools |
|-----------|--------|
| **Language** | Python 3.x |
| **Framework** | Flask |
| **Libraries** | Pandas, Scikit-learn, Requests, Joblib |
| **API** | OMDb API |
| **DevOps** | Docker, GitHub Actions |
| **Storage** | CSV (for feedback and movie data) |

---

## 📁 Project Structure

```bash
Personalized-Movie-Recommender-with-Real-Time-Feedback-Loop/
│
├── app.py                     # Flask application entry point
├── Dockerfile                 # Container setup for deployment
├── requirements.txt           # Python dependencies
├── .dockerignore              # Files and folders ignored by Docker
│
├── data/                      # Data storage directory
│   ├── movies data.csv        # Movie metadata dataset
│   └── feedbackdata.csv       # User ratings and feedback log
│
├── recommender/               # Core recommender engine
│   ├── model.py               # TF-IDF + Cosine Similarity logic
│   ├── feedback.py            # Handles feedback logging and updates
│   └── __init__.py            # Package initializer
│
├── static/                    # Frontend assets
│   └── style.css              # CSS styling for the web app
│
└── templates/                 # HTML templates for Flask
    └── index.html             # Main web interface
```

## 🚀 How to Run Locally

# 1️⃣ Clone the repository
git clone https://github.com/<your-username>/Personalized-Movie-Recommender-with-Real-Time-Feedback-Loop.git
cd Personalized-Movie-Recommender-with-Real-Time-Feedback-Loop

# 2️⃣ Install Dependencies
pip install -r requirements.txt

# 3️⃣ Run the Flask App
python app.py

# Visit the app in your browser:
# http://localhost:5000

## 🐳 Run with Docker

docker build -t movie-recommender .
docker run -p 5000:5000 movie-recommender

## 🧪 Usage

1. Open the app in your browser
2. Enter a movie title in the search bar
3. View top similar movies with posters and metadata
4. Rate movies from 1–5 stars
5. Ratings are stored in data/feedbackdata.csv and used to refine recommendations

## 🧩 Model Explanation

TF-IDF Vectorization:
  Converts movie plots into numerical feature vectors.

Cosine Similarity:
  Calculates similarity between movies based on TF-IDF vectors.

Feedback Integration:
  Updates recommendation relevance based on user ratings saved in feedbackdata.csv.

## 🔁 Real-Time Feedback Flow

1. User rates a movie in the Flask web app.
2. Rating is stored in data/feedbackdata.csv.
3. The recommender reads this feedback and adjusts recommendations dynamically.
4. Users get updated, more personalized suggestions.

## 💻 Example Dependencies

Flask
pandas
scikit-learn
requests
joblib

## 🧱 System Architecture

User
  ↓
Flask Web App (app.py)
  ↓
Recommender Engine (TF-IDF + Cosine Similarity)
  ↓
OMDb API → Fetch movie posters
  ↓
Feedback Module (feedback.py) → feedbackdata.csv
  ↺
Recommendations updated dynamically

## ⚡ CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.
Each push to 'main' triggers:
  - Dependency installation
  - Code linting and testing
  - Docker image build
  - Optional deployment workflow

## 🧾 License

This project is licensed under the MIT License — see the LICENSE file for details.

## 👨‍💻 Author

Kumaraswamy G
🎓 BMS College of Engineering, Bengaluru
📧 kumaraswamy.ai23@bmsce.ac.in
💡 AIML Engineering Student passionate about Recommender Systems & MLOps

## 🚀 Future Enhancements

- Add collaborative filtering for hybrid recommendations
- Use PostgreSQL/Redis for scalable feedback storage
- Integrate user authentication and session management
- Deploy via Kubernetes for distributed scalability

## ⭐ Contributing

Contributions, feature requests, and issues are welcome!
Fork this repository, make your improvements, and submit a pull request.

"Great recommendations come from good feedback — this system learns from you in real time."

