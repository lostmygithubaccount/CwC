# imports
import ibis

from dagster import Definitions

## local imports
from .jobs import jobs
from .assets import assets
from .resources import resources

# config
# backend = "polars" # issues with conversions
backend = "duckdb"
ibis.set_backend(backend)

defs = Definitions(
    assets=assets,
    resources=resources,
    jobs=jobs,
)
