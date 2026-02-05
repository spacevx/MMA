import pygame
from pygame import Surface

from paths import assetsPath

keysPath = assetsPath / "tiles" / "keyboard"

_cache: dict[str, Surface] = {}
_scaledCache: dict[tuple[str, int], Surface] = {}

_NAME_MAP: dict[int, str] = {
    pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e",
    pygame.K_f: "f", pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j",
    pygame.K_k: "k", pygame.K_l: "l", pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o",
    pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r", pygame.K_s: "s", pygame.K_t: "t",
    pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", pygame.K_y: "y",
    pygame.K_z: "z",

    pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4",
    pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9",

    pygame.K_UP: "arrow_up", pygame.K_DOWN: "arrow_down",
    pygame.K_LEFT: "arrow_left", pygame.K_RIGHT: "arrow_right",

    pygame.K_SPACE: "space", pygame.K_RETURN: "return", pygame.K_ESCAPE: "escape",
    pygame.K_TAB: "tab", pygame.K_BACKSPACE: "backspace", pygame.K_DELETE: "delete",
    pygame.K_INSERT: "insert", pygame.K_HOME: "home", pygame.K_END: "end",
    pygame.K_PAGEUP: "page_up", pygame.K_PAGEDOWN: "page_down",

    pygame.K_LSHIFT: "shift", pygame.K_RSHIFT: "shift",
    pygame.K_LCTRL: "ctrl", pygame.K_RCTRL: "ctrl",
    pygame.K_LALT: "alt", pygame.K_RALT: "alt",
    pygame.K_CAPSLOCK: "capslock",

    pygame.K_F1: "f1", pygame.K_F2: "f2", pygame.K_F3: "f3", pygame.K_F4: "f4",
    pygame.K_F5: "f5", pygame.K_F6: "f6", pygame.K_F7: "f7", pygame.K_F8: "f8",
    pygame.K_F9: "f9", pygame.K_F10: "f10", pygame.K_F11: "f11", pygame.K_F12: "f12",

    pygame.K_MINUS: "minus", pygame.K_EQUALS: "equals", pygame.K_PERIOD: "period",
    pygame.K_COMMA: "comma", pygame.K_SEMICOLON: "semicolon",
    pygame.K_SLASH: "slash_forward", pygame.K_BACKSLASH: "slash_back",
    pygame.K_LEFTBRACKET: "bracket_open", pygame.K_RIGHTBRACKET: "bracket_close",
    pygame.K_QUOTE: "quote", pygame.K_BACKQUOTE: "tilde",
    pygame.K_KP_ENTER: "numpad_enter", pygame.K_NUMLOCKCLEAR: "numlock",
    pygame.K_PRINTSCREEN: "printscreen",
}


def _loadIcon(name: str) -> Surface | None:
    if name in _cache:
        return _cache[name]

    path = keysPath / f"keyboard_{name}.png"
    if not path.exists():
        return None

    surf = pygame.image.load(str(path)).convert_alpha()
    _cache[name] = surf
    return surf


def getKeyIcon(key: int, size: int = 32) -> Surface | None:
    name = _NAME_MAP.get(key)
    if name is None:
        return None

    cacheKey = (name, size)
    if cacheKey in _scaledCache:
        return _scaledCache[cacheKey]

    base = _loadIcon(name)
    if base is None:
        return None

    scaled = pygame.transform.smoothscale(base, (size, size))
    _scaledCache[cacheKey] = scaled
    return scaled


def hasIcon(key: int) -> bool:
    return key in _NAME_MAP


def clearCache() -> None:
    _cache.clear()
    _scaledCache.clear()
