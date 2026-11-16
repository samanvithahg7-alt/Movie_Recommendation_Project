# Person 3 - Movie Recommendation

## Files added
- `recommend.py`: user-based collaborative-filtering recommendation code.

## Input files
Person 3 reads these prepared files from `person1_data/`:
- `ratings_matrix.csv` (users are rows, movies are columns; blank/NaN means unrated)
- `movies_metadata.csv` (includes MovieID, Title, and Genres)

## Run
From the `Movie_Recommendation_Project` root folder:

```powershell
python person3_recommendation\recommend.py
```

Enter a valid user ID when prompted (for example, `1`).

## Output
The script saves `recommendations_user_<ID>.csv` inside this folder. The output contains recommended movie IDs, titles and genres (when metadata is available), predicted ratings, and the number of neighbors who rated each movie.

## For Person 4 - integration handoff
Person 4 can import the reusable function:

```python
from person3_recommendation.recommend import recommend_movies

recommendations = recommend_movies(
    ratings_df,
    user_id=1,
    movie_metadata=movies_metadata_df,
    top_n=10,
)
```

`ratings_df` should be loaded from `person1_data/ratings_matrix.csv` using `pd.read_csv(..., index_col=0)`. `movie_metadata_df` should be loaded from `person1_data/movies_metadata.csv`.

The function returns a pandas DataFrame and does not require the saved Person 2 20-user sample CSV. It calculates similarities from the ratings matrix directly.
