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

Also of interest: [cache-template](https://github.com/dandi-cache/cache-template), the common template with standardized structure, layout, and mechanisms for a typical DANDI Cache; [dandi-cache-utils](https://github.com/dandi-cache/dandi-cache-utils), the shared library and container base image every cache is built on; and [dandi-cache-action](https://github.com/dandi-cache/dandi-cache-action), the composite actions that build those images and run the updates. None of the three is a data cache, so none is registered as a subdataset.

Check the `README` in each repository for cache-specific usage instructions.

## Staying current

The subdataset registrations in this superdataset are pinned to specific commits, as is standard for DataLad superdatasets. A scheduled workflow ([`update-listing.yml`](./.github/workflows/update-listing.yml)) advances those pins to the latest state of each cache once a day, so a fresh `datalad clone` (or `datalad update`) always resolves to recent data.

A cache whose remote cannot be reached — deleted, renamed, or made private — does not stop the others from advancing, but it does fail the run and send mail, so the listing cannot quietly freeze.
