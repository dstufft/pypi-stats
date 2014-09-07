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


DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data")
)

DATA_FILE = os.path.join(DATA_DIR, "data.pkl")

JOB_NAME = os.path.splitext(os.path.basename(__file__))[0][5:]

PICKLE_FILE = os.path.join(DATA_DIR, "{}.pkl".format(JOB_NAME))


engine = sqlalchemy.create_engine(os.environ["STATS_DB"])


df = pandas.read_sql_query(
    """ SELECT *
        FROM crosstab(
            '
                SELECT
                    date_trunc(''day'', download_time),
                    array_to_string(python_version[0:2], ''.'')
                        AS python_version,
                    COUNT(*)
                FROM (
                    SELECT download_time,
                           string_to_array(python_version, ''.'')
                               AS python_version
                    FROM downloads
                    WHERE python_version SIMILAR TO
                        ''(2.6|2.7|3.2|3.3|3.4).%%''
                        OR python_version IN (
                            ''2.6'', ''2.7'', ''3.2'', ''3.3'', ''3.4''
                        )
                ) as s
                GROUP BY date_trunc(''day'', download_time),
                         array_to_string(python_version[0:2], ''.'')
                ORDER BY 1, 2
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


with open(PICKLE_FILE, "wb") as fp:
    pickle.dump(df, fp)
