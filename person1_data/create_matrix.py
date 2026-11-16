import pandas as pd

# Load ratings
ratings = pd.read_csv(
    "person1_data/cleaned_ratings.csv"
)

# Create user-movie ratings matrix
ratings_matrix = ratings.pivot(
    index="UserID",
    columns="MovieID",
    values="Rating"
)

# Save matrix
ratings_matrix.to_csv(
    "person1_data/ratings_matrix.csv"
)

print("RATINGS MATRIX CREATED SUCCESSFULLY!")

print("Number of users:", ratings_matrix.shape[0])
print("Number of movies:", ratings_matrix.shape[1])

print("\nFirst 5 rows:")
print(ratings_matrix.head())