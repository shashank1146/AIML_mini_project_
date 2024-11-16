import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load ratings dataset
ratings = pd.read_csv('data/ratings.csv')
movies = pd.read_csv('data/movies.csv')

# Merge datasets
data = pd.merge(ratings, movies, on='movieId')

# Create a pivot table: rows are users, columns are movies, values are ratings
user_movie_matrix = data.pivot_table(index='userId', columns='title', values='rating')

# Fill NaN with 0 (unrated movies)
user_movie_matrix = user_movie_matrix.fillna(0)

# Compute cosine similarity between users
user_similarity = cosine_similarity(user_movie_matrix)

# Function to recommend movies based on user similarity
def collaborative_recommendations(user_id, user_movie_matrix=user_movie_matrix, user_similarity=user_similarity):
    # Get the user's ratings
    user_ratings = user_movie_matrix.loc[user_id]
    
    # Compute the weighted average of other users' ratings
    similar_users = user_similarity[user_id - 1]
    weighted_ratings = np.dot(similar_users, user_movie_matrix) / np.array([np.abs(similar_users).sum()])
    
    # Create a DataFrame for the recommendations
    recommendations = pd.DataFrame(weighted_ratings, index=user_movie_matrix.columns, columns=['score'])
    recommendations = recommendations[~recommendations.index.isin(user_ratings[user_ratings > 0].index)]
    
    # Return top 10 movie recommendations
    return recommendations.sort_values(by='score', ascending=False).head(10)
