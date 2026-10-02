"""Render the status table in README.md from each registered cache's published branches.

For every cache in `.gitmodules` this reads, without downloading anything it does not need:

- the number of entries it publishes, by counting the lines of the compressed JSON Lines on `dist`;
- the size of that compressed bundle, from the `dist` tree;
- when its data last changed, from the head commit of `derivatives`;
- for each upstream cache it reads, when the version it last computed from was published, from the
  `sourcedata/` subdataset pins on `derivatives`. A cache whose source is the archive itself pins
  none, and shows a dash.

Only the standard library and `git` are used, so the workflow needs no environment of its own. The
table is written between the two markers below and nothing else in the README is touched.
"""

import datetime
import gzip
import pathlib
import subprocess
import sys
import tempfile

START = "<!-- status:start -->"
END = "<!-- status:end -->"
ROOT = pathlib.Path(__file__).resolve().parents[2]


def git(*arguments: str, cwd: pathlib.Path | None = None, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *arguments], cwd=cwd, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode().strip()


def caches() -> list[str]:
    """Each registered cache's name, in listing order."""
    paths = git("config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=ROOT)
    return sorted(pathlib.PurePath(line.split()[1]).name for line in paths.splitlines())


class Remote:
    """A blobless, shallow, bare copy of one cache: trees and commits only, blobs on demand."""

    def __init__(self, url: str, directory: pathlib.Path) -> None:
        self.directory = directory
        git("init", "--quiet", "--bare", str(directory))
        git("remote", "add", "origin", url, cwd=directory)
        git("config", "remote.origin.promisor", "true", cwd=directory)
        git("config", "remote.origin.partialclonefilter", "blob:none", cwd=directory)

    def fetch(self, *references: str) -> None:
        git("fetch", "--quiet", "--depth=1", "--filter=blob:none", "origin", *references, cwd=self.directory)

    def committed_at(self, revision: str) -> datetime.datetime:
        stamp = git("show", "--no-patch", "--format=%cI", revision, cwd=self.directory)
        return datetime.datetime.fromisoformat(stamp).astimezone(datetime.UTC)

    def tree(self, revision: str) -> list[tuple[str, str, str, str]]:
        """`(type, object, size, path)` for every entry under `revision`."""
        listing = git("ls-tree", "-r", "-l", revision, cwd=self.directory)
        rows = []
        for line in listing.splitlines():
            metadata, path = line.split("\t", 1)
            _, kind, sha, size = metadata.split()
            rows.append((kind, sha, size, path))
        return rows

    def blob(self, sha: str) -> bytes:
        return git("cat-file", "blob", sha, cwd=self.directory, binary=True)


def human_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1000 or unit == "GB":
            return f"{size:,} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1000
    raise AssertionError


def when(moment: datetime.datetime) -> str:
    return moment.strftime("%Y-%m-%d %H:%M")


class Remotes(dict):
    """One local copy per cache, shared between its own row and the rows of caches reading it."""

    def __init__(self, scratch: pathlib.Path) -> None:
        super().__init__()
        self.scratch = scratch

    def __missing__(self, name: str) -> Remote:
        self[name] = Remote(f"https://github.com/dandi-cache/{name}.git", self.scratch / name)
        return self[name]


def row(name: str, remotes: Remotes) -> str:
    link = f"[{name}](https://github.com/dandi-cache/{name})"
    remote = remotes[name]
    try:
        remote.fetch("derivatives", "dist")
    except subprocess.CalledProcessError as error:
        print(f"::warning::{name}: cannot read its data branches: {error.stderr.decode().strip()}")
        return f"| {link} | unavailable | | | |"

    bundles = [
        (sha, int(size))
        for kind, sha, size, path in remote.tree("refs/remotes/origin/dist")
        if kind == "blob" and path.endswith(".jsonl.gz") and not pathlib.PurePath(path).name.startswith("testing")
    ]
    entries = sum(len(gzip.decompress(remote.blob(sha)).splitlines()) for sha, _ in bundles)
    size = sum(size for _, size in bundles)

    derivatives = git("rev-parse", "refs/remotes/origin/derivatives", cwd=remote.directory)
    updated = remote.committed_at(derivatives)

    sources = []
    for kind, sha, _, path in remote.tree(derivatives):
        if kind != "commit" or not path.startswith("sourcedata/"):
            continue
        upstream = pathlib.PurePath(path).name
        try:
            remotes[upstream].fetch(sha)
            sources.append(f"{upstream}: {when(remotes[upstream].committed_at(sha))}")
        except subprocess.CalledProcessError:
            sources.append(f"{upstream}: unavailable")
    source_cell = "<br>".join(sources) if sources else "—"

    return f"| {link} | {entries:,} | {human_size(size)} | {when(updated)} | {source_cell} |"


def render() -> str:
    lines = [
        START,
        "| Cache | Entries | Compressed size | Last updated (UTC) | Source data as of (UTC) |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    with tempfile.TemporaryDirectory() as scratch:
        remotes = Remotes(pathlib.Path(scratch))
        for name in caches():
            lines.append(row(name, remotes))
    now = datetime.datetime.now(datetime.UTC)
    lines += ["", f"Generated {when(now)} UTC.", END]
    return "\n".join(lines)


def main() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text()
    if START not in text or END not in text:
        sys.exit(f"README.md must contain {START} and {END}.")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    readme.write_text(before + render() + after)


if __name__ == "__main__":
    main()
