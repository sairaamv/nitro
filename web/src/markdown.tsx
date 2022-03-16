import React from 'react';
import styled from 'styled-components';
import { micromark, Options } from 'micromark';
import { gfm, gfmHtml } from 'micromark-extension-gfm'
import { B, S, U } from './core';
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const opts: Options = {
  allowDangerousHtml: false,
  extensions: [gfm()],
  htmlExtensions: [gfmHtml()]
}

export const Markdown = styled.div`
/* Don't add margins before/after first/last paragraph */
&>p:first-child {
  margin-top: 0;
}
&>p:last-child {
  margin-bottom: 0;
}
&>p:only-child {
  margin: 0;
}

/* resets */

h1, h2, h3, h4, h5, h6, p, blockquote, pre {
  box-sizing: border-box;
  margin: 0;
  font-size: 1rem;
  line-height: 1.5rem;
  font-weight: 400;
}
img {
  max-width: 100%;
  display: block;
}

/* customizations */

h1 {
  font-weight: 200;
  font-size: 3rem;
  line-height: 3.3rem;
  margin-bottom: 0.5rem;
}
h2 {
  font-weight: 300;
  font-size: 2rem;
  line-height: 2.5rem;
  margin-bottom: 0.5rem;
}
h3 {
  font-size: 1.44rem;
  line-height: 2rem;
  font-weight: 400;
  margin-bottom: 0.25rem;
  color: #333;
}
h4 {
  font-size: 1.2rem;
  line-height: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}
h5 {
  font-size: 1rem;
  line-height: 1.75rem;
  font-weight: 700;
  text-transform: uppercase;
  font-feature-settings: 'smcp';
  color: #333;
}
h6 {
  font-size: 0.92rem;
  line-height: 1.25rem;
  margin-bottom: 1rem;
}
p, ul, ol {
  font-size: 1.2rem;
  line-height: 1.75rem;
  margin-bottom: 1rem;
  color: #242424;
}
strong {
  font-weight: 600;
}
ul {
  list-style: none;
  padding-left: 2rem;
  text-indent: -1rem;
}
ul>li:before {
  content: "—";
  text-indent: -1rem;
  margin-right: .5rem;
}
ol ol, ul ol {
  list-style-type: lower-roman;
}
ul ul ol, ul ol ol, ol ul ol, ol ol ol {
  list-style-type: lower-alpha;
}
/* Workaround: Markdown renderer adds superfluous p inside ol's li.*/
ol li p { 
  margin: 0;
}
blockquote {
  padding: 0 1em;
  border-left: 0.25em solid #ddd;
}
blockquote p {
  color: #555; 
}
.footnotes {
  h2 {
    font-size: 1rem;
    line-height: 1.75rem;
    font-weight: 700;
    text-transform: uppercase;
    font-feature-settings: 'smcp';
  }
  ol li, ol li p {
    font-size: 1rem;
  }
}
p code, li code, blockquote code {
  padding: 0.2em 0.4em;
  font-size: 85%;
  margin: 0;
  background-color: #eee;
}
pre {
  padding: 1rem;
  overflow: auto;
  margin-bottom: 1rem;
  background-color: #eee;
}

/* Source: https://github.com/micromark/micromark-extension-gfm-footnote */

/* Style the footnotes section. */
.footnotes {
  font-size: smaller;
  color: #8b949e;
  border-top: 1px solid #30363d;
}

/* Hide the section label for visual users. */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  word-wrap: normal;
  border: 0;
}

/* Place [ and ] around footnote calls. */
[data-footnote-ref]::before {
  content: '[';
}

[data-footnote-ref]::after {
  content: ']';
}
`

const getIndentation = (rx: RegExp, lines: S[]): U => {
  const indents: U[] = []
  for (const line of lines) {
    const m = line.match(rx)
    if (!m) return 0
    indents.push(m[0].length)
  }
  return Math.min(...indents)
}
const getSpaceIndentation = (lines: S[]): U => getIndentation(/^ +/, lines)
const getTabIndentation = (lines: S[]): U => getIndentation(/^\t+/, lines)
const dedent = (s: S): S => {
  let lines = s.split(/\r?\n/)
  const n = lines.length
  if (n > 0) {
    lines = lines.slice(
      lines[0].trim().length === 0 ? 1 : 0,
      lines[n - 1].trim().length === 0 ? n - 1 : n
    )
  }
  const indent = getSpaceIndentation(lines) || getTabIndentation(lines)
  return indent === 0
    ? s
    : lines.map(line => line.substring(indent)).join('\n')
}
export const
  highlight = (html: S) => html
    .replaceAll(/<code class="language-(.+?)">(.+?)<\/code>/gms, (_, language, code) => {
      return hljs.highlight(code, { language }).value
    }),
  isFootnoteLink = (s: S) => s.startsWith('user-content'), // gfm-footnote default
  markdown = (text: S): [S, B] => {
    let hasLinks = false
    const md = highlight(micromark(dedent(text), opts))
      // Change <a href="#foo"> to <a data-jump="foo" href>
      // Exclude footnote references.
      // We need the links to be rendered as such, but not affect the address bar.
      .replaceAll(/href="#(.+?)"/g, (all, ref) => {
        if (isFootnoteLink(ref)) return all
        hasLinks = true
        return `data-jump="${ref}" href`
      })
    return [md, hasLinks]
  }
