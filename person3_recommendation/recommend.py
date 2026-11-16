"""
Person 3 - Movie Recommendation

Input:
    person1_data/ratings_matrix.csv
    person1_data/movies_metadata.csv

Output:
    person3_recommendation/recommendations_user_<ID>.csv

Run from the project root:
    python person3_recommendation/recommend.py
"""

from pathlib import Path
import numpy as np
import pandas as pd


def cosine_similarity_common(a, b, min_common=2):
    """Cosine similarity calculated only over movies both users rated."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    common = np.isfinite(a) & np.isfinite(b)

    if int(common.sum()) < min_common:
        return 0.0

    a_common = a[common]
    b_common = b[common]
    denominator = np.linalg.norm(a_common) * np.linalg.norm(b_common)

    if denominator == 0:
        return 0.0

    return float(np.dot(a_common, b_common) / denominator)


def recommend_movies(
    ratings_df,
    user_id,
    movie_metadata=None,
    top_n=10,
    n_neighbors=30,
    min_common=2,
):
    """
    Recommend movies using ratings from similar users.

    Parameters
    ----------
    ratings_df : pandas.DataFrame
        Users as rows, movie IDs as columns; unrated cells are NaN.
    user_id : int or str
        User ID present in ratings_df.index.
    movie_metadata : pandas.DataFrame, optional
        Metadata with MovieID and Title columns.
    top_n : int
        Number of recommendations to return.
    n_neighbors : int
        Maximum number of similar users used for predictions.
    min_common : int
        Minimum number of co-rated movies for similarity calculation.

    Returns
    -------
    pandas.DataFrame
        MovieID, Title (if metadata supplied), PredictedRating, NeighborsUsed.
    """
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    ratings = ratings_df.copy()
    ratings.index = ratings.index.astype(str)
    ratings.columns = ratings.columns.astype(str)
    target_id = str(user_id)

    if target_id not in ratings.index:
        raise ValueError(
            f"User ID {target_id!r} is not in the ratings matrix. "
            f"Example valid IDs: {', '.join(ratings.index[:10])}"
        )

    target = ratings.loc[target_id].to_numpy(dtype=float)
    neighbor_scores = []

    # Find users with similar tastes.
    for other_id, row in ratings.iterrows():
        if other_id == target_id:
            continue

        other = row.to_numpy(dtype=float)
        score = cosine_similarity_common(target, other, min_common=min_common)

        # Only positive similarity contributes to a recommendation.
        if score > 0:
            neighbor_scores.append((other_id, score))

    neighbor_scores.sort(key=lambda item: item[1], reverse=True)
    neighbor_scores = neighbor_scores[:n_neighbors]

    if not neighbor_scores:
        raise ValueError(
            "No suitable similar users were found. Try a different user ID."
        )

    weighted_totals = np.zeros(ratings.shape[1], dtype=float)
    similarity_totals = np.zeros(ratings.shape[1], dtype=float)
    neighbor_counts = np.zeros(ratings.shape[1], dtype=int)

    for neighbor_id, similarity in neighbor_scores:
        neighbor_ratings = ratings.loc[neighbor_id].to_numpy(dtype=float)
        rated_mask = np.isfinite(neighbor_ratings)

        weighted_totals[rated_mask] += (
            neighbor_ratings[rated_mask] * similarity
        )
        similarity_totals[rated_mask] += similarity
        neighbor_counts[rated_mask] += 1

    # Weighted mean of neighbors' ratings is the predicted rating.
    predicted = np.full(ratings.shape[1], np.nan, dtype=float)
    can_predict = similarity_totals > 0
    predicted[can_predict] = (
        weighted_totals[can_predict] / similarity_totals[can_predict]
    )

    # Never recommend a movie the target user has already rated.
    already_rated = np.isfinite(target)
    predicted[already_rated] = np.nan

    candidate_indices = np.flatnonzero(np.isfinite(predicted))
    if len(candidate_indices) == 0:
        raise ValueError("No unrated movies could be predicted for this user.")

    best_indices = candidate_indices[
        np.argsort(predicted[candidate_indices])[::-1][:top_n]
    ]

    results = pd.DataFrame({
        "MovieID": ratings.columns[best_indices],
        "PredictedRating": np.round(predicted[best_indices], 3),
        "NeighborsUsed": neighbor_counts[best_indices],
    })

    if movie_metadata is not None:
        metadata = movie_metadata.copy()
        if "MovieID" in metadata.columns:
            metadata["MovieID"] = metadata["MovieID"].astype(str)
            columns = ["MovieID"]
            if "Title" in metadata.columns:
                columns.append("Title")
            if "Genres" in metadata.columns:
                columns.append("Genres")
            results = results.merge(
                metadata[columns].drop_duplicates("MovieID"),
                on="MovieID",
                how="left",
            )
            preferred = ["MovieID", "Title", "Genres", "PredictedRating", "NeighborsUsed"]
            results = results[[c for c in preferred if c in results.columns]]

    return results.reset_index(drop=True)


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "person1_data"
    output_dir = Path(__file__).resolve().parent

    ratings_path = data_dir / "ratings_matrix.csv"
    metadata_path = data_dir / "movies_metadata.csv"

    if not ratings_path.exists():
        raise FileNotFoundError(
            f"Ratings matrix not found: {ratings_path}\n"
            "Make sure Person 1's prepared data is in person1_data."
        )

    ratings = pd.read_csv(ratings_path, index_col=0)
    metadata = None

    if metadata_path.exists():
        metadata = pd.read_csv(metadata_path, encoding="latin-1")

    print("Person 3 - Movie Recommendation")
    print(f"Users available: {len(ratings.index)}")
    print("Enter a user ID from the ratings matrix (for example, 1).")
    user_id = input("User ID: ").strip()

    try:
        recommendations = recommend_movies(
            ratings,
            user_id,
            movie_metadata=metadata,
            top_n=10,
            n_neighbors=30,
        )
    except ValueError as exc:
        print(f"Could not generate recommendations: {exc}")
        return

    output_path = output_dir / f"recommendations_user_{user_id}.csv"
    recommendations.to_csv(output_path, index=False)

    print("\nTop recommendations:")
    print(recommendations.to_string(index=False))
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
