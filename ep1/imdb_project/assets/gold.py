# imports
from dagster import asset

## local imports
from . import functions as f


# assets
@asset
def gold_imdb_ratings(silver_imdb_title_basics, silver_imdb_title_ratings):
    """
    Joined titles, ratings, and TODO more.
    """
    t = silver_imdb_title_basics.join(silver_imdb_title_ratings, "tconst", how="left")
    t = t.relabel({"tconst_x": "tconst"}).drop("tconst_y")
    return t
