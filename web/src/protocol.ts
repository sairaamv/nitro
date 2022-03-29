import React from "react"
import { S, N, B, U, V, Pair, Triple, I } from "./core"

export enum MsgType {
  Error = 1,
  Join,
  Leave,
  Abort,
  Resume,
  Request,
  Response,
  Watch,
  Event,
  Input,
  Insert,
  Update,
  Remove,
  Conf,
  Switch,
}

export type Msg = {
  t: MsgType.Error
  e: S
} | {
  t: MsgType.Join
  d: any // XXX formalize
} | {
  t: MsgType.Insert
  d: Input
  p?: I
} | {
  t: MsgType.Update
  d: Input
  p?: I
} | {
  t: MsgType.Remove
  d: Input
} | {
  t: MsgType.Input,
  d: Array<V | V[] | null>
} | {
  t: MsgType.Conf,
  d: Conf
} | {
  t: MsgType.Switch,
  d: V
}

export type Conf = {
  title?: S,
  caption?: S,
  menu?: Option[]
  nav?: Option[]
}

export enum WidgetT {
  Box = 1,
  Option,
}

export type InputMode = 'md' | 'button' | 'menu' | 'radio' | 'check' | 'text' | 'range' | 'number' | 'time' | 'date' | 'day' | 'week' | 'month' | 'tag' | 'color' | 'rating'

export type Input = {
  t: WidgetT.Box
  xid: S
  index: I // -1 = don't capture
  text?: S
  name?: S
  mode?: InputMode
  value?: V | Pair<V>
  options: Option[]
  items?: Input[]
  row?: B
  tile?: S
  cross_tile?: S
  wrap?: S
  gap?: S
  align?: S // CSS text-align
  width?: S | [S] | Pair<S> | Triple<S> // CSS width / [min] / [min, max] / [min, max, initial]
  height?: S | [S] | Pair<S> | Triple<S> // CSS height / [min] / [min, max] / [min, max, initial]
  margin?: S // CSS margin
  padding?: S // CSS padding
  border?: S // CSS border 1px solid ~
  color?: S  // CSS color
  background?: S // CSS background
  grow?: U // CSS flex-grow
  shrink?: U // CSS flex-shrink
  basis?: S // CSS flex-basis
  icon?: S
  min?: V
  max?: V
  step?: N
  precision?: U
  range?: [V, V] | [N, N, N] | [N, N, N, U]
  mask?: S
  prefix?: S
  suffix?: S
  // format?: S // TODO: displayed-value format string for spinbutton, slider
  placeholder?: S
  error?: S
  lines?: U
  multiple?: B
  required?: B
  password?: B
  editable?: B
}

export type Option = {
  t: WidgetT.Option
  value: V
  text?: S
  icon?: S
  caption?: S
  selected?: B
  options?: Option[]
}
