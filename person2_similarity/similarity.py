
import numpy as np
import pandas as pd
from pathlib import Path


def _common(a, b):
    """Keep only movies rated by both users."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    mask = ~np.isnan(a) & ~np.isnan(b)
    return a[mask], b[mask]


def cosine_similarity(a, b):
    """Calculate cosine similarity between two users."""
    a, b = _common(a, b)

    if len(a) == 0:
        return np.nan

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return np.nan

    return float(np.dot(a, b) / denominator)


def euclidean_distance(a, b):
    """Calculate Euclidean distance between two users."""
    a, b = _common(a, b)

    if len(a) == 0:
        return np.nan

    return float(np.linalg.norm(a - b))


def inner_product(a, b):
    """Calculate the inner product of two users' ratings."""
    a, b = _common(a, b)

    if len(a) == 0:
        return np.nan

    return float(np.dot(a, b))


def angle_degrees(a, b):
    """Calculate the angle between two users' rating vectors."""
    a, b = _common(a, b)

    if len(a) == 0:
        return np.nan

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return np.nan

    cosine = np.dot(a, b) / denominator
    cosine = np.clip(cosine, -1.0, 1.0)

    return float(np.degrees(np.arccos(cosine)))


def similarity_matrix(ratings_df, method=cosine_similarity):
    """Create a user-by-user similarity matrix."""
    users = ratings_df.index
    result = pd.DataFrame(
        index=users,
        columns=users,
        dtype=float
    )

    for u in users:
        for v in users:
            result.loc[u, v] = method(
                ratings_df.loc[u].values,
                ratings_df.loc[v].values
            )

    return result


if __name__ == "__main__":
    # Find the project folder regardless of the current terminal folder
    project_folder = Path(__file__).resolve().parent.parent
    matrix_path = project_folder / "person1_data" / "ratings_matrix.csv"
    output_path = Path(__file__).resolve().parent / "user_similarity.csv"

    if not matrix_path.exists():
        print("ERROR: ratings_matrix.csv was not found.")
        print("Expected location:", matrix_path)
        raise SystemExit(1)

    ratings = pd.read_csv(matrix_path, index_col=0)

    # Use 20 users for the initial test
    sample = ratings.iloc[:20]

    similarities = similarity_matrix(sample)
    distances = similarity_matrix(sample, euclidean_distance)
    products = similarity_matrix(sample, inner_product)
    angles = similarity_matrix(sample, angle_degrees)

    # Save the results in the person2_similarity folder
    similarities.to_csv(output_path)
    distances.to_csv(output_path.parent / "user_distances.csv")
    products.to_csv(output_path.parent / "user_inner_products.csv")
    angles.to_csv(output_path.parent / "user_angles.csv")

    print("User comparison completed successfully!")
    print("Users tested:", len(sample))
    print("Similarity matrix shape:", similarities.shape)
    print("Files saved in:", output_path.parent)
    print("\nCosine similarity preview:")
    print(similarities.iloc[:5, :5])
