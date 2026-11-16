import pandas as pd
import os

print("CHECKING MOVIELENS DATASET")

ratings_path = "dataset/ml-1m/ratings.dat"
movies_path = "dataset/ml-1m/movies.dat"

if os.path.exists(ratings_path) and os.path.exists(movies_path):
    print("Dataset files found!")

    ratings = pd.read_csv(
        ratings_path,
        sep="::",
        engine="python",
        names=["UserID", "MovieID", "Rating", "Timestamp"],
        encoding="latin-1"
    )

    movies = pd.read_csv(
        movies_path,
        sep="::",
        engine="python",
        names=["MovieID", "Title", "Genres"],
        encoding="latin-1"
    )

    print("\nDataset loaded successfully!")
    print("Total ratings:", len(ratings))
    print("Total movies:", len(movies))

    print("\nFirst 5 ratings:")
    print(ratings.head())

    print("\nFirst 5 movies:")
    print(movies.head())

else:
    print("Dataset files not found. Check the folder location.")