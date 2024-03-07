# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name='lco',
    version='0.0.1',
    py_modules=['lco'],
    author_email="looker-content-observer@google.com",
    install_requires=[
        "click>=8.0",
        "PyYAML>=5.1",
        "looker-sdk>=23.0.0",
        "pandas>2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'lco = lco:cli',
        ],
    },
)