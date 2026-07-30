"""What this plugin offers, and the evidence for each entry.

Every claim below was checked against the archives themselves on
2026-07-30 -- downloaded, opened, and read -- rather than against a wiki.

## The rule

**Clean-room and openly licensed, or it is not here.** EmuTOS is a
free operating system for Atari ST computers, written from scratch. It
is not a dump of an Atari TOS ROM, and it is not a patched one.

## The licence, read out of the archive

`emutos-512k-1.4/doc/license.txt`, inside the archive this plugin
installs, is the **GNU General Public License version 2** verbatim.
Redistribution is permitted, which is the whole question for a plugin
that installs binaries, and it was answered from the archive being
installed rather than from a badge -- GitHub reports `emutos/emutos` as
having no detected licence at all, which is a metadata artefact and not
a licensing problem.

## Three builds, one operating system

EmuTOS publishes the same release at three ROM sizes, and they are for
different hardware rather than for different machines:

    emutos-192k-1.4.zip   2,260,230 bytes   19 x 196,608
    emutos-256k-1.4.zip   2,933,355 bytes   19 x 262,144
    emutos-512k-1.4.zip   3,708,741 bytes   19 x 524,288

An original ST's ROM sockets hold 192 KB. 512 KB is the full build, and
the right answer for an emulator, which has no sockets to run out of.
All three carry the same 19 languages.

## What is not here

`emutos-aranym-1.4.zip` is published beside them and is not offered. It
is a build for one specific emulator's virtual machine rather than for
Atari ST hardware, so filing it under `atari-st` would describe it
wrongly -- and this plugin does not guess platforms.

## Why the catalogue is static

`list()` makes no network request, for the reasons `open_bios/catalogue`
gives: firmware is bytes an emulator *executes*, so an operator should
get the release this plugin says it verified.
"""

from dataclasses import dataclass

#: The release this plugin was verified against.
EMUTOS_VERSION = "1.4"

#: The directory the release sits in. It happens to equal the version for
#: EmuTOS, and it is still a separate constant: C-BIOS files release
#: `0.29a` under `0.29`, and deriving one from the other there produced a
#: 404 that only an end-to-end install caught. Two facts, two names.
EMUTOS_DIR = "1.4"

_BASE = "https://sourceforge.net/projects/emutos/files/emutos"

#: Languages every build ships, as the suffix on the image name. Read out
#: of the archives: all three carry exactly these 19.
#:
#: A language is operator configuration that becomes part of a **member
#: name**, so it is checked against this table before use and never
#: interpolated raw.
LANGUAGES: dict[str, str] = {
    "ca": "Catalan",
    "cz": "Czech",
    "de": "German",
    "es": "Spanish",
    "fi": "Finnish",
    "fr": "French",
    "gr": "Greek",
    "hu": "Hungarian",
    "it": "Italian",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "ro": "Romanian",
    "ru": "Russian",
    "se": "Swedish",
    "sg": "Swiss German",
    "tr": "Turkish",
    "uk": "English (UK)",
    "us": "English (US)",
}

DEFAULT_LANGUAGE = "us"


@dataclass(frozen=True)
class Source:
    """One installable firmware item, before it becomes a FirmwareArtifact."""

    firmware_id: str
    name: str
    #: This plugin's system name. `platforms.platform_for` turns it into a
    #: library platform slug, or refuses.
    system: str
    description: str
    #: The ROM size this build targets, as it appears in both the archive
    #: name and the image name -- "512k", "256k", "192k".
    size: str
    #: Size of the zip, measured. Reported before the request goes out.
    archive_bytes: int
    #: Size of one unpacked image, measured. All 19 are identical.
    image_bytes: int

    @property
    def archive_filename(self) -> str:
        return f"emutos-{self.size}-{EMUTOS_VERSION}.zip"

    @property
    def url(self) -> str:
        return f"{_BASE}/{EMUTOS_DIR}/{self.archive_filename}/download"

    def member(self, language: str) -> str:
        """The image member for this build in `language`.

        `language` has already been checked against `LANGUAGES` by the
        caller -- this does not validate, so that one place does.
        """
        return f"etos{self.size.rstrip('k')}{language}.img"


SOURCES: tuple[Source, ...] = (
    Source(
        firmware_id="emutos-512k",
        name="EmuTOS 512 KB",
        system="Atari ST",
        description=(
            "The full build. The right one for an emulator, which has no "
            "ROM sockets to run out of, and for later hardware."
        ),
        size="512k",
        archive_bytes=3708741,
        image_bytes=524288,
    ),
    Source(
        firmware_id="emutos-256k",
        name="EmuTOS 256 KB",
        system="Atari ST",
        description=(
            "For machines whose ROM sockets hold 256 KB. Same release, "
            "built smaller."
        ),
        size="256k",
        archive_bytes=2933355,
        image_bytes=262144,
    ),
    Source(
        firmware_id="emutos-192k",
        name="EmuTOS 192 KB",
        system="Atari ST",
        description=(
            "For an original ST, whose ROM sockets hold 192 KB. The "
            "smallest build, and the most constrained."
        ),
        size="192k",
        archive_bytes=2260230,
        image_bytes=196608,
    ),
)


def find(firmware_id: str) -> Source:
    """The source with this id, or `KeyError` naming what is here.

    `plan()` looks an item up rather than trusting the artifact handed
    back to it: that artifact left this process, and believing its fields
    would mean building a member name out of a value that made a round
    trip through somewhere else.
    """
    for source in SOURCES:
        if source.firmware_id == firmware_id:
            return source
    known = ", ".join(s.firmware_id for s in SOURCES)
    raise KeyError(f"no firmware {firmware_id!r} here; this plugin has {known}")
