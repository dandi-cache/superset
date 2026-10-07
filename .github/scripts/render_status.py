"""Render the status table in README.md from each registered cache's published branches.

For every cache in `.gitmodules` this reads, without downloading anything it does not need:

- the number of entries it publishes, by counting the lines of the compressed JSON Lines on `dist`;
- the size of that compressed bundle, from the `dist` tree;
- when its data last changed, from the head commit of `derivatives`;
- for each upstream cache it reads, when the version it last computed from was published, from the
  `sourcedata/` subdataset pins on `derivatives`. A cache whose source is the archive itself pins
  none, and shows a dash;
- its largest file on either branch, against GitHub's 100 MiB limit for one file. A push carrying a
  file past it is refused, so every file past `WARNING_FRACTION` of it is reported as an
  annotation, and as the `size-warnings` step output the workflow sends an email for.

Only the standard library and `git` are used, so the workflow needs no environment of its own. The
table is written between the two markers below and nothing else in the README is touched.
"""

import datetime
import gzip
import os
import pathlib
import subprocess
import sys
import tempfile

START = "<!-- status:start -->"
END = "<!-- status:end -->"
ROOT = pathlib.Path(__file__).resolve().parents[2]

#: GitHub refuses any file over 100 MiB, and a cache pushes only after a run's work is done.
GITHUB_FILE_LIMIT_BYTES = 100 * 1024 * 1024
#: Past this fraction a file is reported. At the largest caches' growth, about 2 MB a day, that
#: leaves a week or more to declare the output in `split` in its `cache.toml`.
WARNING_FRACTION = 0.8

#: Every file past `WARNING_FRACTION` of the limit, as one line each, collected while rendering.
SIZE_WARNINGS: list[str] = []


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


def largest_file(name: str, branch: str, tree: list[tuple[str, str, str, str]]) -> tuple[int, str]:
    """The largest file on one branch, recording a warning when it is near GitHub's limit."""
    size, path = max(((int(size), path) for kind, _, size, path in tree if kind == "blob"), default=(0, ""))
    if size > WARNING_FRACTION * GITHUB_FILE_LIMIT_BYTES:
        state = "past" if size > GITHUB_FILE_LIMIT_BYTES else "approaching"
        warning = (
            f"{name}: {branch}:{path} is {size / 1e6:.1f} MB, {size / GITHUB_FILE_LIMIT_BYTES:.0%} of GitHub's "
            f"100 MiB limit for one file; it is {state} the size at which every push is refused."
        )
        print(f"::warning title=File size near GitHub's limit::{warning}")
        SIZE_WARNINGS.append(warning)
    return size, path


def headroom(size: int) -> str:
    """A file's size against the limit, flagged once it is past the warning fraction."""
    fraction = size / GITHUB_FILE_LIMIT_BYTES
    flag = " 🛑" if fraction > 1 else " ⚠️" if fraction > WARNING_FRACTION else ""
    return f"{human_size(size)} ({fraction:.0%}){flag}"


def row(name: str, remotes: Remotes) -> str:
    link = f"[{name}](https://github.com/dandi-cache/{name})"
    remote = remotes[name]
    try:
        remote.fetch("derivatives", "dist")
    except subprocess.CalledProcessError as error:
        print(f"::warning::{name}: cannot read its data branches: {error.stderr.decode().strip()}")
        return f"| {link} | unavailable | | | | |"

    dist_tree = remote.tree("refs/remotes/origin/dist")
    largest_file(name, "dist", dist_tree)
    bundles = [
        (sha, int(size))
        for kind, sha, size, path in dist_tree
        if kind == "blob" and path.endswith(".jsonl.gz") and not pathlib.PurePath(path).name.startswith("testing")
    ]
    entries = sum(len(gzip.decompress(remote.blob(sha)).splitlines()) for sha, _ in bundles)
    size = sum(size for _, size in bundles)

    derivatives = git("rev-parse", "refs/remotes/origin/derivatives", cwd=remote.directory)
    updated = remote.committed_at(derivatives)

    derivatives_tree = remote.tree(derivatives)
    largest, _ = largest_file(name, "derivatives", derivatives_tree)

    sources = []
    for kind, sha, _, path in derivatives_tree:
        if kind != "commit" or not path.startswith("sourcedata/"):
            continue
        upstream = pathlib.PurePath(path).name
        try:
            remotes[upstream].fetch(sha)
            sources.append(f"{upstream}: {when(remotes[upstream].committed_at(sha))}")
        except subprocess.CalledProcessError:
            sources.append(f"{upstream}: unavailable")
    source_cell = "<br>".join(sources) if sources else "—"

    return f"| {link} | {entries:,} | {human_size(size)} | {headroom(largest)} | {when(updated)} | {source_cell} |"


def render() -> str:
    lines = [
        START,
        "| Cache | Entries | Compressed size | Largest file on `derivatives` (of 100 MiB) | Last updated (UTC) | Source data as of (UTC) |",
        "| --- | ---: | ---: | ---: | --- | --- |",
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

    output_path = os.environ.get("GITHUB_OUTPUT")
    if SIZE_WARNINGS and output_path:
        with open(output_path, mode="a") as output:
            output.write("size-warnings<<SIZE_WARNINGS_END\n")
            output.writelines(f"{warning}\n" for warning in SIZE_WARNINGS)
            output.write("SIZE_WARNINGS_END\n")


if __name__ == "__main__":
    main()
