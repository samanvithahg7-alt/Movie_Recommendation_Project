
# Movie Recommendation Project

## Project Overview

This project uses mathematical concepts such as norms, Euclidean distance, inner products, and angles to compare users' movie preferences and build a movie recommendation system.

The project uses the **MovieLens 1M dataset**.

## Project Team

- **Person 1 – Dataset Preparation:** Loads, checks, cleans, and organizes the data.
- **Person 2 – User Similarity:** Compares users using mathematical similarity measures.
- **Person 3 – Movie Recommendations:** Develops the recommendation approach.
- **Person 4 – Integration:** Combines the separate parts into the final project.

## Dataset

The `dataset/ml-1m/` folder contains:

- `ratings.dat` – User IDs, movie IDs, ratings, and timestamps.
- `movies.dat` – Movie IDs, titles, and genres.
- `users.dat` – User information supplied with the dataset.

Ratings are on a scale from **1 to 5**.

## Person 1: Data Preparation

Person 1 is responsible for preparing the dataset for the rest of the team.

Tasks completed:

1. Loaded the ratings and movie metadata files.
2. Checked for missing values and duplicate ratings.
3. Checked rating values and movie metadata.
4. Saved the prepared data as CSV files.
5. Created a user–movie ratings matrix.
6. Created a separate movie information file.
7. Generated a dataset summary.

## Prepared Data Files

| File | Description |
|---|---|
| `cleaned_ratings.csv` | Ratings data after validation checks |
| `movies_metadata.csv` | Movie metadata in CSV format |
| `ratings_matrix.csv` | Users as rows and movies as columns |
| `movie_information.csv` | Movie information for the team |
| `data_summary.txt` | Dataset statistics |

**Important:** Blank cells (`NaN`) in the ratings matrix mean that a user has not rated that movie. They are not zero ratings.

## Dataset Summary

- Total ratings: **1,000,209**
- Total users: **6,040**
- Movies in metadata: **3,883**
- Movies with at least one rating: **3,706**
- Minimum rating: **1**
- Maximum rating: **5**
- Average rating: **3.58**

The data checks found no missing values in the loaded ratings or movie metadata, no duplicate user–movie rating pairs, and no ratings outside the 1–5 range.

## Requirements

- Python 3
- pandas
- NumPy
- Matplotlib

Install the required packages:

```powershell
python -m pip install pandas numpy matplotlib
```

## Running Person 1's Scripts

Open the project folder in VS Code and run these commands from the project root:

```powershell
python person1_data\check_dataset.py
python person1_data\data_cleaning.py
python person1_data\create_matrix.py
python person1_data\create_movie_data.py
python person1_data\data_summary.py
```

Run each command separately and check the terminal for errors.

## Team Handoff

Person 1 should share the prepared CSV files and `data_summary.txt` with the rest of the team.

The `ratings_matrix.csv` file is the main input for user-similarity calculations.

## Notes

- Keep the original dataset files unchanged.
- Store generated files in `person1_data/`.
- Do not treat missing ratings as zero.
- Document any changes to the data preparation process.
