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
| Cache | Entries | Compressed size | Last updated (UTC) | Source data as of (UTC) |
| --- | ---: | ---: | --- | --- |
| [content-id-to-dandiset-paths](https://github.com/dandi-cache/content-id-to-dandiset-paths) | 542,756 | 23.8 MB | 2026-10-04 05:40 | — |
| [content-id-to-nwb-file](https://github.com/dandi-cache/content-id-to-nwb-file) | 231,510 | 9.7 MB | 2026-10-04 06:47 | content-id-to-usage-dandiset-path: 2026-10-04 06:21 |
| [content-id-to-usage-dandiset-path](https://github.com/dandi-cache/content-id-to-usage-dandiset-path) | 552,907 | 23.5 MB | 2026-10-04 06:21 | content-id-to-dandiset-paths: 2026-10-04 05:40 |
| [content-id-to-valid-nwb-file](https://github.com/dandi-cache/content-id-to-valid-nwb-file) | 246,485 | 9.7 MB | 2026-10-04 10:28 | content-id-to-nwb-file: 2026-10-04 06:47 |
| [dandiset-id-to-number-of-assets](https://github.com/dandi-cache/dandiset-id-to-number-of-assets) | 2,215 | 6.7 KB | 2026-10-04 05:51 | — |
| [dandiset-id-to-title](https://github.com/dandi-cache/dandiset-id-to-title) | 2,215 | 28.3 KB | 2026-10-04 05:43 | — |
| [dandiset-id-to-total-size](https://github.com/dandi-cache/dandiset-id-to-total-size) | 653 | 5.9 KB | 2026-10-04 07:26 | content-id-to-usage-dandiset-path: 2026-10-04 06:21<br>usage-dandiset-path-to-asset-size: 2026-10-04 07:01 |
| [qualifying-aind-content-ids](https://github.com/dandi-cache/qualifying-aind-content-ids) | 1,298 | 29.1 KB | 2026-10-04 06:25 | content-id-to-usage-dandiset-path: 2026-10-04 06:21<br>content-id-to-valid-nwb-file: 2026-10-04 03:34<br>qualifying-lfp-content-ids: 2026-10-04 00:47 |
| [qualifying-lfp-content-ids](https://github.com/dandi-cache/qualifying-lfp-content-ids) | 77,262 | 1.6 MB | 2026-10-04 08:35 | content-id-to-nwb-file: 2026-10-04 06:47<br>content-id-to-valid-nwb-file: 2026-10-04 03:34 |
| [usage-dandiset-path-to-asset-size](https://github.com/dandi-cache/usage-dandiset-path-to-asset-size) | 538,695 | 13.5 MB | 2026-10-04 07:01 | content-id-to-usage-dandiset-path: 2026-10-04 06:21 |
| [valid-nwb-file-to-chunk-stats](https://github.com/dandi-cache/valid-nwb-file-to-chunk-stats) | 68,334 | 2.3 MB | 2026-10-04 06:13 | content-id-to-valid-nwb-file: 2026-10-04 03:34 |
| [valid-nwb-file-to-cophenetic-index](https://github.com/dandi-cache/valid-nwb-file-to-cophenetic-index) | 77,235 | 1.8 MB | 2026-10-04 10:56 | content-id-to-valid-nwb-file: 2026-10-04 03:34 |
| [valid-nwb-file-to-number-of-datasets](https://github.com/dandi-cache/valid-nwb-file-to-number-of-datasets) | 71,085 | 1.6 MB | 2026-10-04 08:28 | content-id-to-valid-nwb-file: 2026-10-04 03:34 |
| [valid-nwb-file-to-number-of-groups](https://github.com/dandi-cache/valid-nwb-file-to-number-of-groups) | 72,436 | 1.6 MB | 2026-10-04 08:58 | content-id-to-valid-nwb-file: 2026-10-04 03:34 |
| [valid-nwb-file-to-out-degrees](https://github.com/dandi-cache/valid-nwb-file-to-out-degrees) | 77,235 | 2.5 MB | 2026-10-04 09:36 | content-id-to-valid-nwb-file: 2026-10-04 03:34 |
| [valid-nwb-file-to-sackin-index](https://github.com/dandi-cache/valid-nwb-file-to-sackin-index) | 71,086 | 1.8 MB | 2026-10-04 10:19 | content-id-to-valid-nwb-file: 2026-10-04 03:34 |

Generated 2026-10-04 11:15 UTC.
<!-- status:end -->

Also of interest: [cache-template](https://github.com/dandi-cache/cache-template), the common template with standardized structure, layout, and mechanisms for a typical DANDI Cache; [dandi-cache-utils](https://github.com/dandi-cache/dandi-cache-utils), the shared library and container base image every cache is built on; and [dandi-cache-action](https://github.com/dandi-cache/dandi-cache-action), the composite actions that build those images and run the updates. None of the three is a data cache, so none is registered as a subdataset.

Check the `README` in each repository for cache-specific usage instructions.

## Staying current

The subdataset registrations in this superdataset are pinned to specific commits, as is standard for DataLad superdatasets. A scheduled workflow ([`update-listing.yml`](./.github/workflows/update-listing.yml)) advances those pins to the latest state of each cache once a day, so a fresh `datalad clone` (or `datalad update`) always resolves to recent data.
The same run regenerates the [status table](#status) through [`render_status.py`](./.github/scripts/render_status.py).

A cache whose remote cannot be reached — deleted, renamed, or made private — does not stop the others from advancing, but it does fail the run and send mail, so the listing cannot quietly freeze.
