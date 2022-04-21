# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from h2o_nitro import View, box, row, col, option, lorem


# # Tag Picker

# ## Basic
# Set `mode='tag'` to display a tag picker. `multiple=True` is implied.
def tag_picker_basic(view: View):
    tags = view(box(
        'Choose some tags',
        mode='tag',
        options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {tags}.')


# ## Value
# Set `value=` to pre-select options having those values.
def tag_picker_value(view: View):
    tags = view(box(
        'Choose some tags',
        mode='tag',
        value=['yellow', 'red'],
        options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {tags}.')


# ## Selected
# Set `selected=True` to pre-select one or more options.
def tag_picker_selected(view: View):
    tags = view(box('Choose some tags', mode='tag', options=[
        option('violet', 'Violet'),
        option('indigo', 'Indigo'),
        option('blue', 'Blue'),
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]))
    view(f'You chose {tags}.')
