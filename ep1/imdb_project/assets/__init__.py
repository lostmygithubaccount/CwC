# imports
from dagster import load_assets_from_modules

## local imports
from . import bronze, silver, gold

from .constants import *

# load assets
bronze_assets = load_assets_from_modules([bronze], group_name=BRONZE)
silver_assets = load_assets_from_modules([silver], group_name=SILVER)
gold_assets = load_assets_from_modules([gold], group_name=GOLD)

assets = [*bronze_assets, *silver_assets, *gold_assets]
