#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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


# Total Percentages of Python Versions
graph = vincent.StackedArea((df / df.sum(axis=1)).ix[:, "3.2":])
graph.legend(title="")
graph.axes["y"].format = "%"
graph.to_json(JSON_FILE)


print("Created {}".format(JSON_FILE))
