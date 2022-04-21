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


# # Styling

# ## Background Color
# Set `background=` to apply a background color.
#
# The text color is automatically changed to a contrasting color if not specified.
# A padding is automatically applied if not specified.
def styling_background(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        box(text, background='#e63946'),
        box(text, background='#f1faee'),
        box(text, background='#a8dadc'),
        box(text, background='#457b9d'),
        box(text, background='#1d3557'),
    )


# ## Text Color
# Set `color=` to change the text color.
def styling_color(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        box(text, color='#e63946'),
        box(text, color='#457b9d'),
        box(text, color='#1d3557'),
    )


# ## Border Color
# Set `border=` to add a border.
#
# A padding is automatically applied if not specified.
def styling_border(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        box(text, border='#e63946'),
        box(text, border='#457b9d'),
        box(text, border='#1d3557'),
    )


# ## Align Text
# Set `align=` to `left`, `right`, `center` or `justify` to align text.
def styling_align(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        row(
            box(text, align='left'),
            box(text, align='center'),
            box(text, align='justify'),
            box(text, align='right'),
            gap=20,
        )
    )


# ## Sizing
# Nitro provides extensive control over how items are sized and spaced, using `width`, `height`, `margin`, `padding`,
# and `gap`.
#
# These parameters can be specified as either integers or strings.
#
# - Integers are interpreted as pixels, e.g. `42` and `'42px'` have the same effect.
# - Strings must be a number followed by one of the units listed below (e.g. `'42px'`, `'42in'`, `'42mm'`, etc.
#   - Absolute units:
#     - `px`: One pixel (1/96th of an inch).
#     - `cm`: One centimeter.
#     - `mm`: One millimeter.
#     - `in`: One inch (96px).
#     - `pc`: One pica (12pt or 1/6th of an inch).
#     - `pt`: One point (1/72nd of an inch).
#   - Relative units:
#     - `%`: A percentage of the container's size.
#     - `vh`: 1% of the viewport height.
#     - `vw`: 1% of the viewport width.
#     - `vmin`: The smaller of `vw` and `vh`.
#     - `vmax`: The larger of `vw` and `vh`.
#     - `ex`: The x-height of the font of the element.
#     - `em`: The font size of the element.
#     - `rem`: The font size of the page.

def styling_size(view: View):
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    view(
        box(text, width=200, background='#eee'),  # interpreted as '200px'
        box(text, width='250px', background='#eee'),
        box(text, width='3in', background='#eee'),
        box(text, width='50%', background='#eee'),
        box(text, height='1in', background='#eee'),
        box(text, width='250px', height='100px', background='#eee'),
    )


# ## Margin
# Set `margin=` to add a margin around each item.
#
# Top, right, bottom, left margins can be controlled independently, and are specified
# as `'top right bottom left'` strings.
#
# - `'x'` is shorthand for `'x x x x'`.
# - `'x y'` is shorthand for `'x y x y'`.
# - `'x y z'` is shorthand for `'x y z y'`.
def styling_margin(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    boxes = [
        # Uniform 20px margin
        box(text, margin='20px', background='#eee'),
        # Same as '20px'
        box(text, margin=20, background='#eee'),
        # 0px top and bottom, 100px right and left margin
        box(text, margin='0px 100px', background='#eee'),
        # 0px top, 100px right and left, 30px bottom margin
        box(text, margin='0px 100px 30px', background='#eee'),
        # 0px top, 100px right, 30px bottom, 200px left margin
        box(text, margin='0px 100px 30px 200px', background='#eee'),
    ]
    view(col(*[row(b, border='#000', padding=0) for b in boxes]))


# ## Padding
# Set `padding=` to control the padding (inset) inside each item.
#
# Top, right, bottom, left paddings can be controlled independently, and are specified
# as `'top right bottom left'` strings.
#
# - `'x'` is shorthand for `'x x x x'`.
# - `'x y'` is shorthand for `'x y x y'`.
# - `'x y z'` is shorthand for `'x y z y'`.
def styling_padding(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        col(
            # Uniform 20px padding
            box(text, padding='20px', background='#eee'),
            # Same as '20px'
            box(text, padding=20, background='#eee'),
            # 0px top and bottom, 100px right and left padding
            box(text, padding='0px 100px', background='#eee'),
            # 0px top, 100px right and left, 30px bottom padding
            box(text, padding='0px 100px 30px', background='#eee'),
            # 0px top, 100px right, 30px bottom, 200px left padding
            box(text, padding='0px 100px 30px 200px', background='#eee'),
        )
    )
