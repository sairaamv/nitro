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


# # Basics

# ## Hello World!
# Call `view()` to show something on a page.
def hello_world(view: View):
    view('Hello World!')


# Here, `view()` is comparable to Python's built-in `print()` function,
# and prints its arguments to the web page.

# ## Formatting content
# Strings passed to `view()` are interpreted as
# [Markdown](https://github.github.com/gfm/)
def format_content(view: View):
    view('_Less_ `code` means _less_ **bugs**.')


# ## Show multiline content
# Triple-quote strings to pass multiple lines of markdown.
def format_multiline_content(view: View):
    view('''
    The King said, very gravely:
    - Begin at the beginning,
    - And go on till you come to the end,
    - Then stop.
    ''')


# ## Show items at once
# Pass multiple arguments to `view()` to lay them out top to bottom.
def display_multiple(view: View):
    view(
        'Begin at the beginning,',
        'And go on till you come to the end,',
        'Then stop.',
    )


# ## Show items one at a time
# Call `view()` multiple times to show items one at a time.
#
# The following example steps through three different pages.
def sequence_views(view: View):
    view('Begin at the beginning,')
    view('And go on till you come to the end,')
    view('Then stop.')


# ## Style text
# To style text, put it in a `box()`, and style the box.
#
# `view(text)` is in fact shorthand for `view(box(text))`.
def style_text(view: View):
    view(
        box('Hello World!', color='red', border='red'),
        box('Hello World!', color='white', background='red'),
        box('Hello World!', width='50%', background='#eee'),
    )


# In general, `box()` can be used to create all kinds of content, like text blocks, dropdowns,
# spinboxes, checklists, buttons, calendars, and so on.

# ## Get user input
# Call `box()` with `value=` to create an input field and pass it to `view()`.
#
# When a view contains an input field, the `view()` function returns its input value.
#
def get_input(view: View):
    # Display a textbox and assign the entered value to a variable.
    name = view(box('What is your name?', value='Boaty McBoatface'))
    # Print the entered value.
    view(f'Hello, {name}!')


# Here, `view(box())` behaves similar to Python's built-in `input()` function.
#

# ## Get inputs one at a time
# Call `view()` multiple times to prompt for a sequence of inputs, one at a time.
#
# The following example steps through three different pages.
def sequence_inputs(view: View):
    # Prompt for first name.
    first_name = view(box('First name', value='Boaty'))
    # Prompt for last name.
    last_name = view(box('Last name', value='McBoatface'))
    # Print the entered values.
    view(f'Hello, {first_name} {last_name}!')


# ## Get inputs at once
# Pass multiple boxes to `view()` to prompt for inputs at once.
#
# When a view contains multiple boxes, the `view()` function returns multiple values, in order.
def accept_multiple_inputs(view: View):
    # Prompt for first and last names.
    first_name, last_name = view(
        box('First name', value='Boaty'),
        box('Last name', value='McBoatface'),
    )
    # Print the entered values
    view(f'Hello, {first_name} {last_name}!')


# ## Putting it all together
# Views can be chained together to create sophisticated workflows and wizards.
#
# The example below shows a simple online ordering system.
#
# Observe how it combines `view()` with conditionals and loops, while keeping the code
# simple, concise, and clear.
#
# Notably, if you have built web applications before, notice the absence of callbacks, event handlers,
# web request handlers, routing, etc.
def dunk_your_donuts(view: View):
    # Our menu.
    menu = dict(
        Donut=['Plain', 'Glazed', 'Chocolate'],
        Coffee=['Dark-roast', 'Medium-roast', 'Decaf'],
    )

    # Prompt for items.
    items = view(box(
        'What would you like to order today?',
        options=list(menu.keys()),  # Menu item names.
        multiple=True,  # Allow multiple selections.
    ))

    if len(items) == 0:  # Nothing selected.
        view(f'Nothing to order? Goodbye!')
        return

    # The order summary, which we'll display later.
    summary = ['### Order summary:']

    # Prompt for counts and flavors.
    for item in items:
        count = view(box(f'How many orders of {item} would you like?', value=3))
        for i in range(count):
            flavor = view(box(
                f'Pick a flavor for {item} #{i + 1}',
                options=menu[item],
            ))
            summary.append(f'1. {flavor} {item}')

    summary.append('\nThank you for your order!')

    # Finally, show summary.
    view('\n'.join(summary))

# Building a similar multi-page interactive app with a regular web framework can be
# a fairly complex endeavor, weaving together requests and replies with logic spread across
# multiple functions , but Nitro makes all this delightfully simple!
