import pandas as pd
import os

print("STARTING DATA CLEANING")

# Load ratings
ratings = pd.read_csv(
    "dataset/ml-1m/ratings.dat",
    sep="::",
    engine="python",
    names=["UserID", "MovieID", "Rating", "Timestamp"],
    encoding="latin-1"
)

# Load movies
movies = pd.read_csv(
    "dataset/ml-1m/movies.dat",
    sep="::",
    engine="python",
    names=["MovieID", "Title", "Genres"],
    encoding="latin-1"
)

# Check missing values
print("\nMissing values in ratings:")
print(ratings.isnull().sum())

print("\nMissing values in movies:")
print(movies.isnull().sum())

# Check duplicate ratings
duplicates = ratings.duplicated(
    subset=["UserID", "MovieID"]
).sum()

print("\nDuplicate user-movie ratings:", duplicates)

# Check rating range
print("\nRating range:")
print(ratings["Rating"].min())
print(ratings["Rating"].max())

# Check whether every rated movie exists
missing_movies = (~ratings["MovieID"].isin(movies["MovieID"])).sum()

print("\nRatings with missing movie information:", missing_movies)

# Save cleaned copies
os.makedirs("person1_data", exist_ok=True)

ratings.to_csv(
    "person1_data/cleaned_ratings.csv",
    index=False
)

movies.to_csv(
    "person1_data/movies_metadata.csv",
    index=False
)

print("\nDATA CLEANING CHECK COMPLETED!")