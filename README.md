# 🎬 Movie Recommender System

A content-based movie recommendation system built with Streamlit and powered by the TMDB 5000 dataset. Uses cosine similarity to find movies similar to your selection.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **Smart Recommendations**: Content-based filtering using cosine similarity
- **Rich Movie Details**: Fetches real-time data from TMDB API including ratings, genres, runtime, and synopsis
- **Modern UI**: Clean, responsive design with smooth animations
- **Mobile Friendly**: Fully responsive layout that works on all devices
- **Fast Performance**: Pre-computed similarity matrix for instant recommendations

## 🚀 Live Demo

[View Live Demo](#) <!-- Add your deployment link here -->

## 📸 Screenshots

<!-- Add screenshots of your app here -->

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **ML Libraries**: scikit-learn, pandas, numpy
- **API**: TMDB (The Movie Database)
- **Deployment**: Streamlit Cloud / Heroku

## 📋 Prerequisites

- Python 3.8 or higher
- TMDB API Key ([Get one here](https://www.themoviedb.org/settings/api))

## 🔧 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/movie-recommender-system.git
cd movie-recommender-system
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add your TMDB API key
   - Open `app.py`
   - Replace the API_KEY value with your own key

5. Run the application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
movie-recommender-system/
├── app.py                      # Main Streamlit application
├── models/
│   └── movie_list.pkl         # Preprocessed movie data
├── similarity.pkl             # Pre-computed similarity matrix
├── tmdb_5000_movies.csv       # Raw movie dataset
├── tmdb_5000_credits.csv      # Movie credits dataset
├── main.ipynb                 # Data preprocessing notebook
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku deployment config
├── DEPLOYMENT.md              # Deployment instructions
└── README.md                  # Project documentation
```

## 🎯 How It Works

1. **Data Preprocessing**: Movie metadata is processed and vectorized using TF-IDF
2. **Similarity Calculation**: Cosine similarity is computed between all movies
3. **Recommendation**: When you select a movie, the system finds the top 5 most similar movies
4. **Details Fetching**: Real-time movie details are fetched from TMDB API

## 🌐 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Navneet Mallick**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for providing the movie database API
- Dataset from [Kaggle TMDB 5000 Movie Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
- Built with [Streamlit](https://streamlit.io/)

## 📊 Dataset

The project uses the TMDB 5000 Movie Dataset which includes:
- 4,803 movies
- Movie metadata (genres, keywords, cast, crew)
- User ratings and popularity metrics

## 🔮 Future Enhancements

- [ ] Add user authentication
- [ ] Implement collaborative filtering
- [ ] Add movie trailers
- [ ] Create watchlist functionality
- [ ] Add movie search with filters
- [ ] Implement A/B testing for recommendations

---

⭐ Star this repo if you found it helpful!
