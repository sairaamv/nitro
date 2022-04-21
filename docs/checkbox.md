# Checkbox



## Basic

Set `mode='check'` to show a checkbox.


```py
keep_signed_in = view(box('Keep me signed in', mode='check'))
view(f'Keep me signed in: {keep_signed_in}.')
```


![Screenshot](assets/screenshots/checkbox_basic.png)


## Value

Set `value=True` to pre-select the checkbox.

The mode setting `mode='check'` is implied, and can be elided.


```py
keep_signed_in = view(box('Keep me signed in', value=True))
view(f'Keep me signed in: {keep_signed_in}.')
```


![Screenshot](assets/screenshots/checkbox_value.png)
