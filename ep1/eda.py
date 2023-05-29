# imports
import ibis

import polars as pl
import seaborn as sns

import plotly.io as pio
import plotly.express as px
import ibis.selectors as s
import matplotlib.pyplot as plt

from imdb_project import *
from imdb_project.assets.bronze import *
from imdb_project.assets.silver import *
from imdb_project.assets.gold import *

# options
## ibis config
ibis.options.interactive = True

## matplotlib config
plt.style.use("dark_background")

## seaborn config
sns.set(style="darkgrid")
sns.set(rc={"figure.figsize": (12, 10)})

## plotly config
pio.templates.default = "plotly_dark"

# assets
## bronze
binb = bronze_imdb_name_basics()
bita = bronze_imdb_title_akas()
bitb = bronze_imdb_title_basics()
bitc = bronze_imdb_title_crew()
bite = bronze_imdb_title_episode()
bitp = bronze_imdb_title_principals()
bitr = bronze_imdb_title_ratings()

## silver
sinb = silver_imdb_name_basics(binb)
sita = silver_imdb_title_akas(bita)
sitb = silver_imdb_title_basics(bitb)
sitc = silver_imdb_title_crew(bitc)
site = silver_imdb_title_episode(bite)
sitp = silver_imdb_title_principals(bitp)
sitr = silver_imdb_title_ratings(bitr)

## gold
gir = gold_imdb_ratings(sitb, sitr)
