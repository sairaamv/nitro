import { DatePicker as FDatePicker } from '@fluentui/react';
import React from 'react';
import { dateToString, toDate } from './core';
import { BoxProps, make } from './ui';


export const DatePicker = make(({ context, box }: BoxProps) => {
  const
    { index, value } = box,
    defaultDate = toDate(value) ?? new Date(),
    defaultValue = dateToString(defaultDate),
    onSelectDate = (d?: Date | null) => {
      console.log('in select', d)
      context.capture(index, dateToString(d ?? defaultDate))
    },
    render = () => {
      const
        { text, placeholder, value, min, max, required } = box,
        date = toDate(value),
        minDate = toDate(min),
        maxDate = toDate(max)

      // TODO firstDayOfWeek, firstWeekOfYear customization
      // TODO pass strings for localization
      return (
        <FDatePicker
          label={text}
          value={date}
          minDate={minDate}
          maxDate={maxDate}
          placeholder={placeholder}
          onSelectDate={onSelectDate}
          isRequired={required}
          highlightSelectedMonth
          showGoToToday
        />
      )
    }

  context.capture(index, defaultValue)

  return { render }
})