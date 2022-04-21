// Copyright 2022 H2O.ai, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { Dropdown as FDropdown, IDropdownOption } from '@fluentui/react';
import React from 'react';
import { selectedOf, toDropdownOption, toGroupedDropdownOptions } from './options';
import { BoxProps, make } from './ui';

// TODO support icons on items. See "Customized Dropdown" Fluent example.
export const Dropdown = make(({ context, box }: BoxProps) => {
  const
    { index, text, placeholder, error, required, options } = box,
    selected = selectedOf(box),
    hasGroups = options.some(c => c.options?.length ? true : false),
    items: IDropdownOption[] = hasGroups ? toGroupedDropdownOptions(options) : options.map(toDropdownOption),
    selectedKey = selected ? selected.value : undefined,
    onChange = (_?: React.FormEvent<HTMLElement>, option?: IDropdownOption) => {
      if (option) context.capture(index, option.key)
    },
    render = () => {
      return (
        <FDropdown
          label={text}
          placeholder={placeholder}
          options={items}
          defaultSelectedKey={selectedKey}
          errorMessage={error}
          required={required ? true : false}
          onChange={onChange}
        />
      )
    }

  if (selected) context.capture(index, selected.value)

  return { render }
})