# imports
import ibis

import polars as pl

from ibis import _

# check stuff out
EXCLUDE = ("animals", "melanoma", "muscle", "muscle_raw", "oats", "oats_raw") # TODO: investigate
ex_names = []
ex_lens = []

for mod in dir(ibis.examples):
    if mod.lower() not in EXCLUDE:
        ex_names.append(mod)
        ex_lens.append(getattr(ibis.examples, mod).fetch().count().execute())

df = pl.DataFrame({"name": ex_names, "len": ex_lens})
t = ibis.get_backend().read_in_memory(df.to_arrow())
t.order_by(_.len.desc()).to_csv("out.csv")

