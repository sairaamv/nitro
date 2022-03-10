from typing import Optional, Tuple, List, Dict, Union, Callable, Set
import msgpack
from enum import IntEnum


class _MsgType(IntEnum):
    Error = 1
    Join = 2
    Leave = 3
    Abort = 4
    Resume = 5
    Request = 6
    Response = 7
    Watch = 8
    Event = 9
    Input = 10
    Insert = 11
    Update = 12
    Remove = 13


class _WidgetT(IntEnum):
    Input = 1
    Option = 2


_primitive = (bool, int, float, str)
Primitive = Union[bool, int, float, str]


class RemoteError(Exception):
    pass


class ProtocolError(Exception):
    pass


def _marshal(d: dict):
    return msgpack.packb(d)


def _unmarshal(b) -> dict:
    return msgpack.unpackb(b)


def _dump(x):  # recursive
    if isinstance(x, (tuple, list, set)):
        return [_dump(e) for e in x]
    if callable(getattr(x, 'dump', None)):
        return x.dump()
    return x


def _clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


N = Union[int, float]
V = Union[N, str]


class Option:
    def __init__(
            self,
            value: V,
            text: Optional[str] = None,
            icon: Optional[str] = None,
            caption: Optional[str] = None,
            selected: Optional[bool] = None,
            options: Optional['Options'] = None,
    ):
        self.value = value
        self.text = text
        self.icon = icon
        self.caption = caption
        self.selected = selected
        self.options = options

    def dump(self) -> dict:
        d = dict(
            t=_WidgetT.Option,
            value=self.value,
            text=self.text,
            icon=self.icon,
            caption=self.caption,
            selected=self.selected,
            options=_dump(self.options),
        )
        return _clean(d)


option = Option

OptionPair = Tuple[V, str]
Options = Union[
    str,
    Tuple[Primitive, ...],
    List[Primitive],
    Set[Primitive],
    Dict[Primitive, V],
    Tuple[Option, ...],
    List[Option],
    Set[Option],
    Tuple[OptionPair, ...],
    List[OptionPair],
    Set[OptionPair],
]

Item = Union['Input', str]
Items = Union[List[Item], Tuple[Item, ...]]
Range = Union[
    Tuple[V, V],
    Tuple[N, N],
    Tuple[N, N, N],
    Tuple[N, N, N, int],
    List[V],
]
Value = Union[
    V,
    Tuple[V, V],
    List[V],
]


class Input:
    def __init__(
            self,
            text: Optional[str] = None,
            name: Optional[str] = None,
            mode: Optional[str] = None,
            icon: Optional[str] = None,
            value: Optional[Value] = None,
            min: Optional[V] = None,
            max: Optional[V] = None,
            step: Optional[N] = None,
            precision: Optional[int] = None,
            range: Optional[Range] = None,
            mask: Optional[str] = None,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
            placeholder: Optional[str] = None,
            error: Optional[str] = None,
            lines: Optional[int] = None,
            multiple: Optional[bool] = None,
            required: Optional[bool] = None,
            password: Optional[bool] = None,
            editable: Optional[bool] = None,
            options: Optional[Options] = None,
            items: Optional[Items] = None,
            inline: Optional[bool] = None,
            size: Optional[V] = None,
            align: Optional[str] = None,
    ):
        self.text = text
        self.name = name
        self.mode = mode
        self.icon = icon
        self.value = value
        self.min = min
        self.max = max
        self.step = step
        self.precision = precision
        self.range = range
        self.mask = mask
        self.prefix = prefix
        self.suffix = suffix
        self.placeholder = placeholder
        self.error = error
        self.lines = lines
        self.multiple = multiple
        self.required = required
        self.password = password
        self.editable = editable
        self.options = options
        self.items = items
        self.inline = inline
        self.size = size
        self.align = align

    def dump(self) -> dict:
        d = dict(
            t=_WidgetT.Input,
            text=self.text,
            name=self.name,
            mode=self.mode,
            icon=self.icon,
            value=self.value,
            min=self.min,
            max=self.max,
            step=self.step,
            precision=self.precision,
            range=self.range,
            mask=self.mask,
            prefix=self.prefix,
            suffix=self.suffix,
            placeholder=self.placeholder,
            error=self.error,
            lines=self.lines,
            multiple=self.multiple,
            required=self.required,
            password=self.password,
            editable=self.editable,
            options=_dump(self.options),
            items=_dump(self.items),
            inline=self.inline,
            size=self.size,
            align=self.align,
        )
        return _clean(d)


def input(
        content: Optional[Union[str, Items]] = None,
        name: Optional[str] = None,
        mode: Optional[str] = None,
        icon: Optional[str] = None,
        value: Optional[Value] = None,
        min: Optional[V] = None,
        max: Optional[V] = None,
        step: Optional[N] = None,
        precision: Optional[int] = None,
        range: Optional[Range] = None,
        mask: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        placeholder: Optional[str] = None,
        error: Optional[str] = None,
        lines: Optional[int] = None,
        multiple: Optional[bool] = None,
        required: Optional[bool] = None,
        password: Optional[bool] = None,
        editable: Optional[bool] = None,
        options: Optional[Options] = None,
        inline: Optional[bool] = None,
        size: Optional[V] = None,
        align: Optional[str] = None,
) -> Input:
    text, items = (None, content) if isinstance(content, (tuple, list)) else (content, None)
    return Input(
        text,
        name,
        mode,
        icon,
        value,
        min,
        max,
        step,
        precision,
        range,
        mask,
        prefix,
        suffix,
        placeholder,
        error,
        lines,
        multiple,
        required,
        password,
        editable,
        options,
        items,
        inline,
        size,
        align,
    )


class UI:
    def __init__(self, send: Callable, recv: Callable, handle: Callable):
        self._send = send
        self._recv = recv
        self._handle = handle

    def run(self):
        self._read(_MsgType.Join)  # XXX handle join
        while True:
            self._handle(self)

    def _read(self, expected: int):
        msg = _unmarshal(self._recv())
        if isinstance(msg, dict):
            t = msg.get('t')
            if t == _MsgType.Error:
                code = msg.get('c')
                raise RemoteError(f'code {code}')
            if (expected > -1) and t != expected:
                raise ProtocolError(f'unexpected message: want {expected}, got {t}')
            if t == _MsgType.Input:
                d = msg.get('d')
                n = len(d)
                if n == 0:
                    return
                elif n == 1:
                    return d[0]
                else:
                    return tuple(d)
            if t == _MsgType.Join:
                d = msg.get('d')
                return d
            raise ProtocolError(f'unknown message type {t}')
        raise ProtocolError(f'unknown message format: want dict, got {type(msg)}')

    def _write(self):
        pass

    def __call__(
            self,
            content: Optional[Union[str, Items]] = None,
            position: Optional[int] = None,
            insert: Optional[bool] = False,
            name: Optional[str] = None,
            mode: Optional[str] = None,
            icon: Optional[str] = None,
            value: Optional[Value] = None,
            min: Optional[V] = None,
            max: Optional[V] = None,
            step: Optional[N] = None,
            precision: Optional[int] = None,
            range: Optional[Range] = None,
            mask: Optional[str] = None,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
            placeholder: Optional[str] = None,
            error: Optional[str] = None,
            lines: Optional[int] = None,
            multiple: Optional[bool] = None,
            required: Optional[bool] = None,
            password: Optional[bool] = None,
            editable: Optional[bool] = None,
            options: Optional[Options] = None,
            inline: Optional[bool] = None,
            size: Optional[V] = None,
            align: Optional[str] = None,
    ):
        d = input(
            content,
            name,
            mode,
            icon,
            value,
            min,
            max,
            step,
            precision,
            range,
            mask,
            prefix,
            suffix,
            placeholder,
            error,
            lines,
            multiple,
            required,
            password,
            editable,
            options,
            inline,
            size,
            align,
        ).dump()
        msg = dict(t=_MsgType.Insert if insert else _MsgType.Update, d=d)
        if position is not None:
            msg['p'] = position
        self._send(_marshal(msg))
        return self._read(_MsgType.Input)