import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk, messagebox

# Load dataset
df = pd.read_csv("tmdb_5000_movies.csv")
df = df[['title', 'overview']]
df.dropna(inplace=True)

# Vectorize movie overviews using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Map movie titles to indices (case-insensitive)
indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()


# Function to get movie recommendations
def get_recommendations(title, num_recommendations=5):
    idx = indices.get(title.lower())
    if idx is None:
        return ["Movie not found."]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
    movie_indices = [i[0] for i in sim_scores]

    results = []
    for i in movie_indices:
        movie_title = df.iloc[i]['title']
        overview = df.iloc[i]['overview']
        results.append(f"🎬 {movie_title}\n{overview}\n")
    return results


# Function called when "Recommend" button is pressed
def show_recommendations():
    movie = selected_movie.get()
    if not movie.strip():
        messagebox.showwarning("Input Error", "Please select or enter a movie title.")
        return

    num_recs = num_recs_slider.get()
    results = get_recommendations(movie, num_recs)

    if results == ["Movie not found."]:
        result_box.configure(state='normal')
        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END, "❌ Movie not found. Please try again.")
        result_box.configure(state='disabled')
        return

    result_box.configure(state='normal')
    result_box.delete('1.0', tk.END)
    for r in results:
        result_box.insert(tk.END, r + "\n" + "-" * 60 + "\n")
    result_box.configure(state='disabled')


# Initialize main window
root = tk.Tk()
root.title("🎬 Movie Recommender")

# Styling
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 11))

# Widgets
tk.Label(root, text="Enter or Select a Movie:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='w')

selected_movie = tk.StringVar()
movie_list = df['title'].tolist()
movie_combo = ttk.Combobox(root, textvariable=selected_movie, values=movie_list, width=60)
movie_combo.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Recommendations:", font=("Arial", 12)).grid(row=1, column=0, sticky='w', padx=10)
num_recs_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
num_recs_slider.set(5)
num_recs_slider.grid(row=1, column=1, sticky='w', padx=10)

recommend_btn = ttk.Button(root, text="🎥 Recommend", command=show_recommendations)
recommend_btn.grid(row=2, column=0, columnspan=2, pady=10)

tk.Label(root, text="Recommendations:", font=("Arial", 13, "bold")).grid(row=3, column=0, columnspan=2, sticky='w',
                                                                         padx=10)

result_box = tk.Text(root, height=20, width=90, wrap=tk.WORD, font=("Arial", 11))
result_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
result_box.configure(state='disabled')

scrollbar = ttk.Scrollbar(root, command=result_box.yview)
scrollbar.grid(row=4, column=2, sticky='ns')
result_box['yscrollcommand'] = scrollbar.set

root.mainloop()
