# EmuTOS plugin for ROM Hub

> Part of **[Cartridge](https://github.com/BlizzHacker/rom-hub/blob/master/BRAND.md)** by MoveWeight — a **[ROMarr](https://github.com/BlizzHacker/romarr)** / ROM Hub plugin. Unofficial; not affiliated with RomM, Gaseous or Retrom.

Implements the RPP v1 `firmware` capability: **EmuTOS**, a free operating
system for Atari ST computers, downloaded into the Hub's configured
firmware directory and — where the library server can hold firmware —
filed there too.

Nothing here is a dump of an Atari TOS ROM, and nothing here is a patched
one. EmuTOS is written from scratch and published under the **GPL v2**,
which permits redistribution outright.

| Capability | Source | Does |
|---|---|---|
| `firmware` | `sourceforge.net/projects/emutos/…/emutos-<size>-1.4.zip` | names a zip; the **Hub** fetches it and keeps the one declared image |

## Install

    rom-hub plugin install emutos
    rom-hub firmware list emutos
    rom-hub firmware install emutos emutos-512k

Files land in `$ROM_HUB_HOME/var/firmware/emutos/`, or wherever
`ROM_HUB_FIRMWARE_DIR` points — point it at the directory Hatari or
Steem already reads and there is nothing to copy afterwards. That is the
Hub's decision, not this plugin's: a plugin returns a filename and never
a path.

## What it offers

| `firmware` | Platform | Licence | Image | Size |
|---|---|---|---|---|
| `emutos-512k` | `atari-st` | GPL-2.0-only | `etos512us.img` | 524,288 |
| `emutos-256k` | `atari-st` | GPL-2.0-only | `etos256us.img` | 262,144 |
| `emutos-192k` | `atari-st` | GPL-2.0-only | `etos192us.img` | 196,608 |

The image name varies by `language`; the sizes do not.

**Which one do you want?** It is a hardware question, not a software one.
An original ST's ROM sockets hold 192 KB. 256 KB suits machines with
larger sockets. **512 KB is the full build and the right answer for an
emulator**, which has no sockets to run out of. All three are the same
release of the same operating system.

Each build is a separate 2–4 MB archive carrying all 19 languages plus
documentation, and an install keeps exactly one image out of it. That
ratio is the reason members are declared at all.

## Licence, and where it was read

**GPL v2.** `emutos-512k-1.4/doc/license.txt`, inside the archive this
plugin installs, is the GNU General Public License version 2 verbatim.

Worth stating plainly: **GitHub reports `emutos/emutos` as having no
detected licence.** That is a metadata artefact, not a licensing problem
— the licence ships in the archive and in the source tree. This is the
same shape of trap `open-bios` documented for SameBoy, which GitHub
reports as `NOASSERTION` because of a carve-out in its `LICENSE` text.
A badge is not evidence; the file is.

## What is deliberately not here

`emutos-aranym-1.4.zip` is published beside the three builds above and is
not offered. It is a build for one specific emulator's virtual machine
rather than for Atari ST hardware, so filing it under `atari-st` would
describe it wrongly — and this plugin does not guess platforms.

## Config

| Key | Type | Default | Meaning |
|---|---|---|---|
| `language` | `str` | `"us"` | which language build to install |

Known values: `ca`, `cz`, `de`, `es`, `fi`, `fr`, `gr`, `hu`, `it`, `nl`,
`no`, `pl`, `ro`, `ru`, `se`, `sg`, `tr`, `uk`, `us`.

The value becomes part of a **member name inside the archive**, so it is
checked against the table in `emutos/catalogue.py` before it is used and
never interpolated raw. An unknown language is refused by name, at
`firmware list`, before an install can pick it up.

No credentials. The host is public and unauthenticated, and this plugin
sends nothing at all — it makes no request of its own. The Hub makes one
GET per install.

## Network

`sourceforge.net`, `downloads.sourceforge.net`, `*.dl.sourceforge.net`.

The wildcard is not laziness. A SourceForge download redirects twice and
**the final hop is a mirror chosen per request**: `cfhcable`,
`pilotfiber` and `gigenet` have all been observed as the final host for
identical URLs. There is no enumerable set of hosts to write down.

It is also as narrow as it can be — `netpolicy.url_allowed` treats a `*.`
prefix as one or more leading labels and never the bare domain, so this
grants `<mirror>.dl.sourceforge.net` and grants neither `sourceforge.net`
itself nor a lookalike like `dl.sourceforge.net.example.com`.

## Platforms

`emutos/platforms.py` maps this plugin's system names to library platform
slugs by exact match, with **no fallback**.

| System | Platform slug |
|---|---|
| Atari ST | `atari-st` |

`atari-st` was read off the four plugins in this repository that already
use it — `hasheous`, `libretro-database`, `libretro-thumbnails`,
`retroachievements` — rather than chosen.

All three ROM sizes map to that one slug, because they are not three
platforms: they are one operating system built for three ROM socket
capacities on the same family of machines.

## Terms

Redistributable by its own project's licence, stated above with the
evidence beside it. The Hub cannot verify any of this — a dumped TOS and
a reimplemented one look identical on the wire — so it is a rule about
what this catalogue may contain, enforced by review of
`emutos/catalogue.py`.

## Licence

MIT (this plugin's own code). The firmware it installs is GPL-2.0-only,
carried by the EmuTOS project and printed by `rom-hub firmware list`.
