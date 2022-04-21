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

import { BaseSlots, createTheme, getColorFromString, hsl2rgb, hsv2hex, hsv2hsl, IColor, isDark, loadTheme, Theme, ThemeGenerator, themeRulesStandardCreator } from '@fluentui/react';
import { Dict, S, U } from './core';

export type Scheme = {
  primaryFont: S
  monospaceFont: S
  primaryColorName: S
  primaryColor: S
  foregroundColor: S
  backgroundColor: S
}

export const defaultScheme: Scheme = {
  primaryFont: 'inherit',
  monospaceFont: 'inherit',
  primaryColor: '#5a64f0',
  primaryColorName: 'indigo',
  foregroundColor: '#3e3f4a',
  backgroundColor: '#ffffff',
}

const
  hueNames = [
    'lava',
    'orange',
    'amber',
    'yellow',
    'lime',
    'mint',
    'green',
    'teal',
    'cyan',
    'sky',
    'blue',
    'indigo',
    'purple',
    'violet',
    'pink',
    'red',
  ],
  makeSwatches = (names: S[], colors: S[], startAt: S): [S, S][] => {
    const
      startIndex = hueNames.indexOf(startAt),
      k = startIndex < 0 ? 0 : startIndex,
      n = names.length
    return colors.map((color, i) => ([names[(k + i) % n], color]))
  },
  cycleHues = (color: S, n: U) => {
    const
      c = getColorFromString(color) ?? getColorFromString(defaultScheme.primaryColor)!,
      hsl = hsv2hsl(c.h, c.s, c.v),
      h = hsl.h,
      s = Math.round(hsl.s),
      l = Math.round(hsl.l),
      dh = 360 / n,
      hues = new Array<S>(n)
    for (let i = 0; i < n; i++) {
      hues[i] = `hsl(${Math.floor(h + dh * i) % 360}, ${s}%, ${l}%)`
    }
    return hues
  },
  generateHues = (scheme: Scheme) => {
    const
      { primaryColor, primaryColorName } = scheme,
      hues = cycleHues(primaryColor, hueNames.length),
      swatches = makeSwatches(hueNames, hues, primaryColorName)
    return swatches
  },
  generateTheme = (scheme: Scheme) => {
    //
    // Adapted from https://github.com/microsoft/fluentui/blob/master/apps/theming-designer/src/components/ThemingDesigner.tsx
    //
    const
      foregroundColor = getColorFromString(scheme.foregroundColor)!,
      backgroundColor = getColorFromString(scheme.backgroundColor)!,
      primaryColor = getColorFromString(scheme.primaryColor)!,
      slots: [BaseSlots, IColor][] = [
        [BaseSlots.primaryColor, primaryColor],
        [BaseSlots.foregroundColor, foregroundColor],
        [BaseSlots.backgroundColor, backgroundColor]
      ],
      rules = themeRulesStandardCreator(),
      currentIsDark = isDark(rules[BaseSlots[BaseSlots.backgroundColor]].color!)

    ThemeGenerator.insureSlots(rules, currentIsDark)
    for (const [slot, color] of slots) {
      ThemeGenerator.setSlot(rules[BaseSlots[slot]], color, currentIsDark, true, true)
    }

    const
      palette: Dict<S> = ThemeGenerator.getThemeAsJson(rules),
      theme = createTheme({
        defaultFontStyle: {
          fontFamily: 'inherit',
        },
        palette,
        isInverted: isDark(rules[BaseSlots[BaseSlots.backgroundColor]].color!),
      })
    return theme
  },
  defineSwatches = (swatches: [S, S][]) => {
    const
      root = document.querySelector(':root') as HTMLElement,
      s = root.style
    for (const [name, color] of swatches) {
      s.setProperty(`--${name}`, `${color}`)
    }
  },
  hyphenCase = (s: S) => s.replace(/[A-Z]/g, x => '-' + x.toLowerCase()),
  dict2Swatches = (colors: Dict<S>, prefix: S) => {
    const swatches: [S, S][] = []
    for (const k in colors) {
      swatches.push([prefix + hyphenCase(k), colors[k]])
    }
    return swatches
  },
  extractSwatches = (theme: Theme) => {
    const
      {
        black,
        white,
        accent,

        themeDarker,
        themeDark,
        themeDarkAlt,
        themePrimary,
        themeSecondary,
        themeTertiary,
        themeLight,
        themeLighter,
        themeLighterAlt,

        neutralDark,
        neutralPrimary,
        neutralPrimaryAlt,
        neutralSecondary,
        neutralSecondaryAlt,
        neutralTertiary,
        neutralTertiaryAlt,
        neutralQuaternary,
        neutralQuaternaryAlt,
        neutralLight,
        neutralLighter,
        neutralLighterAlt,

      } = theme.palette,

      colors: Dict<S> = {
        'foreground': black,
        'background': white,
        accent,

        'accentDarker': themeDarker,
        'accentDark': themeDark,
        'accentDarkAlt': themeDarkAlt,
        'accentPrimary': themePrimary,
        'accentSecondary': themeSecondary,
        'accentTertiary': themeTertiary,
        'accentLight': themeLight,
        'accentLighter': themeLighter,
        'accentLighterAlt': themeLighterAlt,

        neutralDark,
        neutralPrimary,
        neutralPrimaryAlt,
        neutralSecondary,
        neutralSecondaryAlt,
        neutralTertiary,
        neutralTertiaryAlt,
        neutralQuaternary,
        neutralQuaternaryAlt,
        neutralLight,
        neutralLighter,
        neutralLighterAlt,
      }

    return dict2Swatches(colors, '')
  }

export const loadScheme = (scheme: Scheme) => {
  defineSwatches(generateHues(scheme))

  const theme = generateTheme(scheme)
  defineSwatches(extractSwatches(theme))

  loadTheme(theme)
}
