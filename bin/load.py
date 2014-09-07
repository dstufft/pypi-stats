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

import pandas
import sqlalchemy


engine = sqlalchemy.create_engine(os.environ["STATS_DB"])


print("Loading Data...")

data_frames = {}

data_frames["python_version"] = pandas.read_sql_query(
    """ SELECT *
        FROM crosstab(
            '
                SELECT
                    download_time::date,
                    array_to_string(python_version[0:2], ''.'')
                        AS python_version,
                    COUNT(*)
                FROM (
                    SELECT download_time,
                           string_to_array(python_version, ''.'')
                               AS python_version
                    FROM downloads
                    WHERE installer_type = ''pip''
                      AND installer_version != ''''
                      AND python_version SIMILAR TO
                        ''(2.6|2.7|3.2|3.3|3.4).%%''
                ) as s
                GROUP BY download_time::date,
                         array_to_string(python_version[0:2], ''.'')
                ORDER BY 1, 2;
            ',
            '
                SELECT unnest(ARRAY[
                    ''2.6'', ''2.7'', ''3.2'', ''3.3'', ''3.4''
                ])
            '
        )
        AS ct(
            date timestamp,
            "2.6" int, "2.7" int, "3.2" int, "3.3" int, "3.4" int
        )
    """,
    engine,
    index_col="date",
)

data_frames["python_type"] = pandas.read_sql_query(
    """ SELECT *
        FROM crosstab(
            '
                SELECT download_time::date, python_type, COUNT(*)
                FROM (
                    SELECT download_time, python_type
                    FROM downloads
                    WHERE installer_type = ''pip''
                      AND installer_version != ''''
                      AND python_type IN (''cpython'', ''pypy'', ''jython'')
                ) as s
                GROUP BY download_time::date, python_type
                ORDER BY 1, 2;
            ',
            '
                SELECT unnest(ARRAY[''cpython'', ''pypy'', ''jython''])
            '
        )
        AS ct(date timestamp, "CPython" int, "PyPy" int, "Jython" int)
    """,
    engine,
    index_col="date",
)

print("Data Loaded.")

filename = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "data.pkl")
)

if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))

with open(filename, "wb") as fp:
    pickle.dump(data_frames, fp)
