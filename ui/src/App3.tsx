import React, { useRef, useEffect } from 'react';

export type B = boolean
export type U = number
export type I = number
export type F = number
export type S = string
export type D = Date

type Output = {
  t: 0
  content: S
}
type Input = {
  t: 1
  caption: S
  value: S
}
type IO = Input | Output

export enum SocketEventT {
  Connect,
  Disconnect,
  Message,
  Error,
}

export type SocketEvent = {
  t: SocketEventT.Connect
} | {
  t: SocketEventT.Disconnect, retry: U
} | {
  t: SocketEventT.Error, error: any
} | {
  t: SocketEventT.Message, message: IO
}
const
  connectEvent: SocketEvent = { t: SocketEventT.Connect }

type SocketEventHandler = (e: SocketEvent) => void

type SendSocketData = (data: any) => void

const
  toSocketAddress = (path: S): S => {
    const
      { protocol, host } = window.location,
      p = protocol === 'https:' ? 'wss' : 'ws'
    return p + "://" + host + path
  }
export const
  connect = (address: S, handle: SocketEventHandler): SendSocketData => {
    let
      _socket: WebSocket | null = null,
      _backoff = 1

    const
      disconnect = () => {
        if (_socket) _socket.close()
      },
      reconnect = (address: S) => {
        const retry = () => reconnect(address)
        const socket = new WebSocket(address)
        socket.onopen = () => {
          _socket = socket
          handle(connectEvent)
          _backoff = 1
          // const hash = window.location.hash
          // socket.send(`+ ${slug} ${hash.charAt(0) === '#' ? hash.substr(1) : hash}`) // protocol: t<sep>addr<sep>data
        }
        socket.onclose = (e) => {
          if (e.code === 1013) { // try again later
            return
          }
          _socket = null
          _backoff *= 2
          if (_backoff > 16) _backoff = 16
          handle({ t: SocketEventT.Disconnect, retry: _backoff })
          window.setTimeout(retry, _backoff * 1000)
        }
        socket.onmessage = (e) => {
          if (!e.data) return
          if (!e.data.length) return
          for (const line of e.data.split('\n')) {
            try {
              const msg = JSON.parse(line) as IO
            } catch (error) {
              console.error(error)
              handle({ t: SocketEventT.Error, error })
            }
          }
        }
        socket.onerror = (error) => {
          console.error(error)
          handle({ t: SocketEventT.Error, error })
        }
      }

    reconnect(toSocketAddress(address))

    return (data: any) => {
      if (_socket) _socket.send(JSON.stringify(data ?? {}))
    }
  }

export const App = () => {
  let send: SendSocketData | null = null
  useEffect(() => {
    if (!send) {
      send = connect(window.location.pathname + 'in', (e) => {
        console.log('got event', e)
      })
    }
  })
  return <div>Hello!</div>
}