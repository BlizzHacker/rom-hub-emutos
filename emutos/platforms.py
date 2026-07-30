"""This plugin's system names -> a library platform slug.

Exact match, no fallback, for the reason `open_bios/platforms.py` gives:
a ROM under the wrong system is visibly wrong, and a BIOS under the wrong
system is *invisible* -- the emulator goes on reporting it has none.

`atari-st` was **read off this project**, not chosen. Four plugins
already use it -- `hasheous`, `libretro-database`, `libretro-thumbnails`
and `retroachievements` -- and `archive-org` maps two of its own
identifiers onto it. Agreeing costs nothing; disagreeing would file
EmuTOS somewhere no other plugin looks.

## One slug for three ROM sizes, and why that is right

EmuTOS ships 192 KB, 256 KB and 512 KB builds. They are not three
platforms: they are the same operating system built for three ROM socket
capacities on **the same family of machines**. A 192 KB image is what an
original ST's sockets hold; the 512 KB build is the full one used on
later hardware and on emulators that do not care.

So all three map to `atari-st`, and the choice between them is the
operator's hardware question, answered by picking the item -- not a
platform question this table should be inventing an answer to.
"""

#: System, as this plugin's catalogue names it -> library platform slug.
SYSTEM_PLATFORMS: dict[str, str] = {
    "Atari ST": "atari-st",
}


class NeedsMapping(Exception):
    """A system this plugin has no platform slug for."""


def platform_for(system: str) -> str:
    """The library platform slug for `system`, or a refusal naming it."""
    try:
        return SYSTEM_PLATFORMS[system]
    except KeyError:
        known = ", ".join(sorted(SYSTEM_PLATFORMS))
        raise NeedsMapping(
            f"system {system!r} needs mapping: it is not in this plugin's "
            f"system -> platform table, which knows {known}. This plugin "
            f"will not guess a platform for firmware -- a BIOS filed under "
            f"the wrong system is invisible, not visibly wrong."
        ) from None
