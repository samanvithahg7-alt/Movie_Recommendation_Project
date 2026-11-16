import pandas as pd

# Load movie information
movies = pd.read_csv(
    "person1_data/movies_metadata.csv"
)

# Display movie information
print("MOVIE INFORMATION")

print("\nTotal movies:", len(movies))

print("\nFirst 10 movies:")
print(movies.head(10))

# Save movie information
movies.to_csv(
    "person1_data/movie_information.csv",
    index=False
)

print("\nMovie information saved successfully!")