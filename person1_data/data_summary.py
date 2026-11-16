import pandas as pd
import os

print("CREATING DATA SUMMARY...")

ratings = pd.read_csv("person1_data/cleaned_ratings.csv")
movies = pd.read_csv("person1_data/movies_metadata.csv")
matrix = pd.read_csv("person1_data/ratings_matrix.csv", index_col=0)

summary = f"""
MOVIE RECOMMENDATION PROJECT
PERSON 1: DATASET SUMMARY

Total ratings: {len(ratings)}
Total users: {ratings['UserID'].nunique()}
Total movies in metadata: {len(movies)}
Movies rated: {matrix.shape[1]}
Minimum rating: {ratings['Rating'].min()}
Maximum rating: {ratings['Rating'].max()}
Average rating: {ratings['Rating'].mean():.2f}
"""

os.makedirs("person1_data", exist_ok=True)

with open("person1_data/data_summary.txt", "w") as file:
    file.write(summary)

print("Data summary created successfully!")
print(summary)