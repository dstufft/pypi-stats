#!/usr/bin/env python
import os
import os.path
import pickle

import vincent


DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data")
)

DATA_FILE = os.path.join(DATA_DIR, "data.pkl")

JOB_NAME = os.path.splitext(os.path.basename(__file__))[0][5:]

JSON_FILE = os.path.join(DATA_DIR, "{}.json".format(JOB_NAME))


# Load data
with open(DATA_FILE, "rb") as fp:
    data_frames = pickle.load(fp)


# We want a particular stored DataFrame
df = data_frames["python_version"]


# Adjust the data to fix some problems
df = df.resample("W")  # TODO: Should we do this by mean or max?
df = df.fillna(0)


# Relative Download Counts of Python Versions
graph = vincent.Line(df)
graph.legend(title="")
graph.axes["y"].format = "s"
graph.to_json(JSON_FILE)


print("Created {}".format(JSON_FILE))
