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

DATA_FILE = os.path.join(DATA_DIR, "python-impl.pkl")

JOB_NAME = os.path.splitext(os.path.basename(__file__))[0][5:]

JSON_FILE = os.path.join(DATA_DIR, "{}.json".format(JOB_NAME))


with open(DATA_FILE, "rb") as fp:
    df = pickle.load(fp)


df = df.resample("W", how="sum")
df.fillna(0, inplace=True)

# Total Percentages of Python Versions
graph = vincent.StackedArea(df / df.sum(axis=1))
graph.colors("Paired")
graph.legend(title="")
graph.axes["y"].format = "%"
graph.scales["y"].domain_max = 1.0
graph.to_json(JSON_FILE)
