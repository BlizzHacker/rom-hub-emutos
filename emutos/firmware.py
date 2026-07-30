"""emutos `firmware`: one archive per build, and one image out of it.

    catalogue.SOURCES -> FirmwareArtifact[]
    FirmwareArtifact  -> FetchPlan -> the HOST downloads and unpacks

The plugin never fetches anything. It names a URL and the **host** fetches
it, after checking that URL against this plugin's `network` allowlist and
re-checking every redirect hop -- which matters here, because a
SourceForge download ends on a mirror chosen per request.

Each build is a separate 2-4 MB archive that yields exactly **one** 192,
256 or 512 KB image. That ratio is the point of declaring members: the
archive carries all 19 languages plus documentation, and the operator
asked for one image in one language.
"""

from rom_hub_sdk import FetchFile, FetchPlan, FirmwareArtifact, FirmwareProvider

from . import catalogue
from .platforms import NeedsMapping, platform_for  # noqa: F401


class ConfigError(Exception):
    """A config value this plugin will not build a member name out of."""


class UnknownFirmware(Exception):
    """No such item in this plugin's catalogue."""


class Firmware(FirmwareProvider):
    def list(self) -> list[FirmwareArtifact]:
        # Read here as well as in `plan()` so a bad language is reported
        # by `firmware list`, before an operator picks something and finds
        # out during an install.
        language = self._language()
        return [self._artifact(source, language) for source in catalogue.SOURCES]

    def plan(self, firmware: FirmwareArtifact) -> FetchPlan:
        try:
            source = catalogue.find(firmware.firmware_id)
        except KeyError as exc:
            raise UnknownFirmware(str(exc)) from None
        # Validated even though it is not used to build this plan: an
        # install should not proceed on a config the catalogue would have
        # refused.
        self._language()

        return FetchPlan(
            files=[
                FetchFile(
                    url=source.url,
                    filename=source.archive_filename,
                    size_bytes=source.archive_bytes,
                )
            ],
            # The host reads the artifact's platform for a firmware
            # install, not this one; FetchPlan requires the field, so it
            # is set to the same value rather than to a placeholder.
            platform=platform_for(source.system),
        )

    # -- building the catalogue -------------------------------------------

    def _artifact(self, source, language: str) -> FirmwareArtifact:
        return FirmwareArtifact(
            firmware_id=source.firmware_id,
            name=source.name,
            # Raises "needs mapping" naming the system rather than
            # guessing one.
            platform=platform_for(source.system),
            # Stated, not derived. GitHub reports emutos/emutos as having
            # no detected licence; the archive ships GPL v2 verbatim at
            # doc/license.txt. See `catalogue.py`.
            license="GPL-2.0-only",
            version=catalogue.EMUTOS_VERSION,
            description=(
                f"{source.description} Language: "
                f"{catalogue.LANGUAGES[language]}. "
                f"{source.image_bytes:,} bytes. "
                f"Source: https://emutos.sourceforge.io/"
            ),
            archive="zip",
            members=[source.member(language)],
        )

    # -- configuration -----------------------------------------------------

    def _language(self) -> str:
        raw = str(
            self.ctx.config.get("language") or catalogue.DEFAULT_LANGUAGE
        ).strip().lower()
        if raw in catalogue.LANGUAGES:
            return raw
        known = ", ".join(sorted(catalogue.LANGUAGES))
        raise ConfigError(
            f"language {raw!r} is not one EmuTOS ships. It becomes part of "
            f"an image name inside the archive, so it is checked against "
            f"the table rather than interpolated: known languages are "
            f"{known}."
        )
