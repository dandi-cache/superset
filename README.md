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
datalad get -n caches/content-id-to-unique-dandiset-path
```

Or fetch everything at once:

```shell
datalad get -n -r .
```

Some caches publish their data on dedicated branches (see the listing below); after `datalad get`, check out the relevant branch inside the subdataset, e.g.:

```shell
git -C caches/content-id-to-unique-dandiset-path checkout min
```

To refresh previously retrieved caches to their latest state:

```shell
datalad update --how merge -r
```

## Listing

| Cache | Description | Data branches | Status |
| --- | --- | --- | --- |
| [content-id-to-dandiset-paths](https://github.com/dandi-cache/content-id-to-dandiset-paths) | Maps content ID relationship to current Dandiset paths. | `main` | Active |
| [content-id-to-unique-dandiset-path](https://github.com/dandi-cache/content-id-to-unique-dandiset-path) | A subset of `content-id-to-dandiset-paths` which have been identified to have only a single correspondence. | `min` | Active |
| [content-id-to-usage-dandiset-path](https://github.com/dandi-cache/content-id-to-usage-dandiset-path) | Adaptation of `content-id-to-unique-dandiset-path` for temporarily resolving all remaining content links to some Dandiset. | `min` | Active |
| [usage-dandiset-path-to-asset-size](https://github.com/dandi-cache/usage-dandiset-path-to-asset-size) | Map each asset in usage-dandiset-path to its size in bytes. | `main` | Active |
| [qualifying-aind-content-ids](https://github.com/dandi-cache/qualifying-aind-content-ids) | A subset of `content-id-to-nwb-files` which have been identified to qualify for the AIND ephys pipeline. | `derivatives`, `dist` | Active |
| [dandi-validations](https://github.com/dandi-cache/dandi-validations) | Derivative dataset of validation outputs for all published Dandiset versions. | `main` | Active |
| [content-id-to-dandiset-paths-old](https://github.com/dandi-cache/content-id-to-dandiset-paths-old) | A cache of the content ID relationship to current Dandiset paths. | `min` | Superseded by `content-id-to-dandiset-paths` |

Also of interest: [cache-template](https://github.com/dandi-cache/cache-template) — a common template with suggested structure, layout, and mechanisms for a typical DANDI Cache (not a data cache itself, so not registered as a subdataset).

Check the `README` in each repository for cache-specific usage instructions.

## Staying current

The subdataset registrations in this superdataset are pinned to specific commits, as is standard for DataLad superdatasets. A scheduled workflow ([`update-listing.yml`](./.github/workflows/update-listing.yml)) advances those pins to the latest state of each cache once a day, so a fresh `datalad clone` (or `datalad update`) always resolves to recent data.
