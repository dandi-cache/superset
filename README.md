# DANDI Cache: Master Listing

This repository is the master listing of all [DANDI Cache](https://github.com/dandi-cache) repositories — a living collection of up-to-date pre-computed mappings commonly used by developers working with the [DANDI Archive](https://dandiarchive.org/).

It is also a [DataLad](https://www.datalad.org/) superdataset: every cache is registered as a subdataset under [`caches/`](./caches), so the entire collection can be retrieved immediately with a couple of commands.

## Retrieval with DataLad

Install the whole collection (lightweight — subdatasets are not downloaded until requested):

```shell
datalad clone https://github.com/dandi-cache/superset dandi-cache
cd dandi-cache
```

Fetch a single cache:

```shell
datalad get -n caches/content-id-to-usage-dandiset-path
```

Or fetch everything at once:

```shell
datalad get -n -r .
```

Every cache publishes its data on dedicated branches rather than on `main`, which carries only the code that produces it. After `datalad get`, check out the branch you want inside the subdataset:

```shell
git -C caches/content-id-to-usage-dandiset-path checkout derivatives
```

`derivatives` holds the cache as newline-delimited JSON; `dist` holds the same content compressed. The subdataset pins below track each cache's `main`, so they follow the code rather than the data — the data on `derivatives` and `dist` is advanced by each cache's own scheduled update, independently of this listing.

To refresh previously retrieved caches to their latest state:

```shell
datalad update --how merge -r
```

## Listing

Every cache below publishes to the same two data branches, `derivatives` and `dist`, and every one is active.

| Cache | Description |
| --- | --- |
| [content-id-to-dandiset-paths](https://github.com/dandi-cache/content-id-to-dandiset-paths) | For each content ID, every Dandiset and path within it where an asset with that content has been seen. Accumulated over time. |
| [content-id-to-nwb-file](https://github.com/dandi-cache/content-id-to-nwb-file) | The NWB subset of `content-id-to-usage-dandiset-path`: one `(Dandiset ID, asset path)` pair per content ID, kept when the asset path is an NWB file. |
| [content-id-to-usage-dandiset-path](https://github.com/dandi-cache/content-id-to-usage-dandiset-path) | A single `(Dandiset ID, asset path)` per content ID, resolved heuristically from the multi-valued entries of `content-id-to-dandiset-paths`. |
| [content-id-to-valid-nwb-file](https://github.com/dandi-cache/content-id-to-valid-nwb-file) | NWB validity per content ID, from streaming each asset in `content-id-to-nwb-file` through the NWB Inspector at the `CRITICAL` threshold. |
| [dandiset-id-to-number-of-assets](https://github.com/dandi-cache/dandiset-id-to-number-of-assets) | The number of assets in each Dandiset's `draft` version. |
| [dandiset-id-to-title](https://github.com/dandi-cache/dandiset-id-to-title) | Each Dandiset's current title, from its `draft` version metadata. |
| [dandiset-id-to-total-size](https://github.com/dandi-cache/dandiset-id-to-total-size) | The total size in bytes of the assets attributed to each Dandiset. |
| [qualifying-aind-content-ids](https://github.com/dandi-cache/qualifying-aind-content-ids) | For each content ID qualifying for `qualifying-lfp-content-ids`, whether it also qualifies for the stricter AIND ephys pipeline. |
| [qualifying-lfp-content-ids](https://github.com/dandi-cache/qualifying-lfp-content-ids) | NWB content IDs holding at least one `ElectricalSeries` in `acquisition` sampled above 10 kHz. |
| [usage-dandiset-path-to-asset-size](https://github.com/dandi-cache/usage-dandiset-path-to-asset-size) | The size in bytes of each asset in `content-id-to-usage-dandiset-path`. |
| [valid-nwb-file-to-chunk-stats](https://github.com/dandi-cache/valid-nwb-file-to-chunk-stats) | A summary of each valid NWB file's HDF5 data layout — how its datasets are chunked and compressed — for estimating what it costs to stream. |
| [valid-nwb-file-to-cophenetic-index](https://github.com/dandi-cache/valid-nwb-file-to-cophenetic-index) | The total cophenetic index of each valid HDF5 NWB file's internal object hierarchy. |
| [valid-nwb-file-to-number-of-datasets](https://github.com/dandi-cache/valid-nwb-file-to-number-of-datasets) | The number of datasets inside each valid NWB file. |
| [valid-nwb-file-to-number-of-groups](https://github.com/dandi-cache/valid-nwb-file-to-number-of-groups) | The number of groups inside each valid NWB file. |
| [valid-nwb-file-to-out-degrees](https://github.com/dandi-cache/valid-nwb-file-to-out-degrees) | Out-degree statistics of each valid HDF5 NWB file's internal object hierarchy. |
| [valid-nwb-file-to-sackin-index](https://github.com/dandi-cache/valid-nwb-file-to-sackin-index) | The normalized Sackin index of each valid NWB file's internal object hierarchy. |

## Status

How large each cache is and how fresh, read from its published branches each time this listing is refreshed.
*Entries* counts the lines of the cache's JSON Lines on `dist`, and *Compressed size* is that bundle's size.
*Last updated* is the most recent change to `derivatives`; a run that found nothing new changes nothing, so it does not move.
*Source data as of* is when each upstream cache had published the version this cache last computed from, so a gap between it and that upstream's own *Last updated* is how far this cache is behind; a dash means the cache reads the archive directly.

<!-- status:start -->
| Cache | Entries | Compressed size | Largest file on `derivatives` (of 100 MiB) | Last updated (UTC) | Source data as of (UTC) |
| --- | ---: | ---: | ---: | --- | --- |
| [content-id-to-dandiset-paths](https://github.com/dandi-cache/content-id-to-dandiset-paths) | 583,255 | 25.4 MB | 7.5 MB (7%) | 2026-10-09 05:55 | — |
| [content-id-to-nwb-file](https://github.com/dandi-cache/content-id-to-nwb-file) | 232,210 | 9.7 MB | 29.0 MB (28%) | 2026-10-09 07:20 | content-id-to-usage-dandiset-path: 2026-10-09 06:39 |
| [content-id-to-usage-dandiset-path](https://github.com/dandi-cache/content-id-to-usage-dandiset-path) | 593,396 | 25.1 MB | 10.7 MB (10%) | 2026-10-09 06:39 | content-id-to-dandiset-paths: 2026-10-09 05:55 |
| [content-id-to-valid-nwb-file](https://github.com/dandi-cache/content-id-to-valid-nwb-file) | 427,269 | 16.6 MB | 80.0 MB (76%) | 2026-10-09 09:38 | content-id-to-nwb-file: 2026-10-08 19:15 |
| [dandiset-id-to-number-of-assets](https://github.com/dandi-cache/dandiset-id-to-number-of-assets) | 2,223 | 6.8 KB | 31.3 KB (0%) | 2026-10-09 06:08 | — |
| [dandiset-id-to-title](https://github.com/dandi-cache/dandiset-id-to-title) | 2,223 | 28.3 KB | 78.2 KB (0%) | 2026-10-09 06:00 | — |
| [dandiset-id-to-total-size](https://github.com/dandi-cache/dandiset-id-to-total-size) | 657 | 6.0 KB | 15.4 KB (0%) | 2026-10-09 08:02 | content-id-to-usage-dandiset-path: 2026-10-09 06:39<br>usage-dandiset-path-to-asset-size: 2026-10-09 07:28 |
| [qualifying-aind-content-ids](https://github.com/dandi-cache/qualifying-aind-content-ids) | 2,386 | 52.9 KB | 678.1 KB (1%) | 2026-10-09 07:22 | content-id-to-usage-dandiset-path: 2026-10-09 06:39<br>content-id-to-valid-nwb-file: 2026-10-09 06:26<br>qualifying-lfp-content-ids: 2026-10-09 01:23 |
| [qualifying-lfp-content-ids](https://github.com/dandi-cache/qualifying-lfp-content-ids) | 130,859 | 2.7 MB | 24.6 MB (23%) | 2026-10-09 01:23 | content-id-to-nwb-file: 2026-10-08 19:15<br>content-id-to-valid-nwb-file: 2026-10-08 23:36 |
| [usage-dandiset-path-to-asset-size](https://github.com/dandi-cache/usage-dandiset-path-to-asset-size) | 579,175 | 14.4 MB | 28.9 MB (28%) | 2026-10-09 07:28 | content-id-to-usage-dandiset-path: 2026-10-09 06:39 |
| [valid-nwb-file-to-chunk-stats](https://github.com/dandi-cache/valid-nwb-file-to-chunk-stats) | 97,334 | 3.2 MB | 22.9 MB (22%) | 2026-10-09 11:04 | content-id-to-valid-nwb-file: 2026-10-09 06:26 |
| [valid-nwb-file-to-cophenetic-index](https://github.com/dandi-cache/valid-nwb-file-to-cophenetic-index) | 132,684 | 3.0 MB | 6.2 MB (6%) | 2026-10-09 05:38 | content-id-to-valid-nwb-file: 2026-10-09 01:42 |
| [valid-nwb-file-to-number-of-datasets](https://github.com/dandi-cache/valid-nwb-file-to-number-of-datasets) | 108,585 | 2.4 MB | 4.9 MB (5%) | 2026-10-09 10:28 | content-id-to-valid-nwb-file: 2026-10-09 06:26 |
| [valid-nwb-file-to-number-of-groups](https://github.com/dandi-cache/valid-nwb-file-to-number-of-groups) | 110,236 | 2.5 MB | 5.0 MB (5%) | 2026-10-09 11:16 | content-id-to-valid-nwb-file: 2026-10-09 06:26 |
| [valid-nwb-file-to-out-degrees](https://github.com/dandi-cache/valid-nwb-file-to-out-degrees) | 132,684 | 4.3 MB | 25.8 MB (25%) | 2026-10-09 04:14 | content-id-to-valid-nwb-file: 2026-10-09 01:42 |
| [valid-nwb-file-to-sackin-index](https://github.com/dandi-cache/valid-nwb-file-to-sackin-index) | 110,086 | 2.8 MB | 6.9 MB (7%) | 2026-10-09 12:05 | content-id-to-valid-nwb-file: 2026-10-09 09:38 |

Generated 2026-10-09 12:06 UTC.
<!-- status:end -->

Also of interest: [cache-template](https://github.com/dandi-cache/cache-template), the common template with standardized structure, layout, and mechanisms for a typical DANDI Cache; [dandi-cache-utils](https://github.com/dandi-cache/dandi-cache-utils), the shared library and container base image every cache is built on; and [dandi-cache-action](https://github.com/dandi-cache/dandi-cache-action), the composite actions that build those images and run the updates. None of the three is a data cache, so none is registered as a subdataset.

Check the `README` in each repository for cache-specific usage instructions.

## Staying current

The subdataset registrations in this superdataset are pinned to specific commits, as is standard for DataLad superdatasets. A scheduled workflow ([`update-listing.yml`](./.github/workflows/update-listing.yml)) advances those pins to the latest state of each cache once a day, so a fresh `datalad clone` (or `datalad update`) always resolves to recent data.
The same run regenerates the [status table](#status) through [`render_status.py`](./.github/scripts/render_status.py).

A cache whose remote cannot be reached — deleted, renamed, or made private — does not stop the others from advancing, but it does fail the run and send mail, so the listing cannot quietly freeze.
