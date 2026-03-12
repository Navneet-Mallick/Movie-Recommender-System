# Streamlit Deployment Guide

## Option 1: Deploy to Streamlit Cloud (Recommended)

### Steps:
1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Sign up** with your GitHub account
3. **Click "Deploy an app"** button
4. **Select your repository**: `Navneet-Mallick/Movie-Recommender-System`
5. **Configure**:
   - Main file path: `app.py`
   - Python version: 3.9+
6. **Click Deploy**

### Important: Handle Large Files
Since `models/similarity.pkl` is ~176 MB (too large for Streamlit Cloud):

**Method 1: Upload to Hugging Face (Recommended)**
```bash
pip install huggingface_hub
huggingface-cli login
# Then upload your .pkl files and modify app.py to download them
```

**Method 2: Use Git LFS**
```bash
git lfs install
git lfs track "*.pkl"
git add models/
git commit -m "Add large model files with LFS"
git push origin main
```

---

## Option 2: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

---

## Option 3: Deploy to Heroku / Render / AWS

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy using your preferred platform's CLI

---

## Troubleshooting

**Issue**: Model files not found
- **Solution**: Make sure `models/movie_list.pkl` is in the repo (< 50MB is OK)

**Issue**: Streamlit Cloud times out
- **Solution**: Optimize model loading or use caching with `@st.cache_resource`

**Issue**: API key exposed
- **Solution**: Use Streamlit secrets manager to store your TMDB API key
  1. Create `.streamlit/secrets.toml`:
     ```
     tmdb_api_key = "your_api_key"
     ```
  2. Update app.py:
     ```python
     api_key = st.secrets["tmdb_api_key"]
     ```

---

## Next Steps
1. Fix the large file issue (choose Method 1 or 2 above)
2. Test locally with `streamlit run app.py`
3. Deploy to Streamlit Cloud
