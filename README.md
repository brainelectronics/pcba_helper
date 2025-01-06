# PCBA Helper

[![Downloads](https://pepy.tech/badge/pcba-helper)](https://pepy.tech/project/pcba-helper)
![Release](https://img.shields.io/github/v/release/brainelectronics/pcba_helper?include_prereleases&color=success)
![Python](https://img.shields.io/badge/Python-3.9%20|%203.10%20|%203.11-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/brainelectronics/pcba_helper/branch/main/graph/badge.svg)](https://app.codecov.io/github/brainelectronics/pcba_helper)

Generate a deployment folder with all required files for easy PCBA

---------------

## General

Generate a (secured) deployment folder with all required files for easy PCBA

<!-- MarkdownTOC -->

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Contributing](#contributing)
  - [Setup](#setup)
  - [Testing](#testing)
  - [Changelog](#changelog)
- [Credits](#credits)

<!-- /MarkdownTOC -->

## Installation

```bash
[<PYTHON> -m] pip[3] install [--user] [--upgrade] pcba_helper
```

## Usage

Create a login secured deployment folder from the KiCAD project at
`examples/KiCAD`. The folder is named `deploy` and placed in the
`examples/KiCAD` folder. The [iBOM file][ref-ibom] is expected relative to the
KiCAD project folder.

```bash
generate-deployments examples/KiCAD \
  --output examples/KiCAD/deploy \
  --ibom-file ibom/ibom.html \
  --username "John" \
  --password "secret" \
  -vvvv
```

The parameter `--public` is optional and creates pure HTML files which can be
accessed without passing any login page, parameter values of `username` and
`password` are ignored.

## Example

The `docker-compose.yml` generates the PDF from the KiCAD schematic, creates
the `deploy` folder and fires up an Apache server with PHP at the fixed IP
address [`172.42.0.2`](http://172.42.0.2).

```bash
[PUBLIC=1] docker compose up --build
docker compose down
[sudo] rm -rf examples/KiCAD/deploy
```

## Contributing

### Setup

For active development you need to have `poetry` and `pre-commit` installed

```bash
python3 -m pip install --upgrade --user poetry pre-commit
git clone https://github.com/brainelectronics/pcba_helper.git
cd pcba_helper
pre-commit install
poetry install
```

### Testing

```bash
# run all tests
poetry run coverage run -m pytest -v

# run only one specific tests
poetry run coverage run -m pytest -v -k "test_read_save"
```

Generate the coverage files with

```bash
python create_report_dirs.py
coverage html
```

The coverage report is placed at `reports/coverage/html/index.html`

### Changelog

The changelog format is based on [Keep a Changelog][ref-keep-a-changelog], and
this project adheres to [Semantic Versioning][ref-semantic-versioning].

Please add a changelog snippet, see below, for every PR you contribute. The
changes are categorised into:

- `bugfixes` fix an issue which can be used out of the box without any further
changes required by the user. Be aware that in some cases bugfixes can be
breaking changes.
- `features` is used to indicate a backwards compatible change providing
improved or extended functionalitiy. This does, as `bugfixes`, in any case
not require any changes by the user to keep the system running after upgrading.
- `breaking` creates a breaking, non backwards compatible change which
requires the user to perform additional tasks, adopt his currently running
code or in general can't be used as is anymore.

The scope of a change shall either be:
- `internal` if no new deployment is required for this change, like updates in
the documentation for example
- `external` or `all` if this change affects the public API of this package or
requires a new tag and deployment for any other reason

The changelog entry shall be short but meaningful and can of course contain
links and references to other issues or PRs. New lines are only allowed for a
new bulletpoint entry. Usage examples or other code snippets should be placed
in the code documentation, README or the docs folder.

The name of the snippet shall be `<ISSUE_ID.md>`

```bash
[poetry run] changelog-generator \
    create .snippets/1.md
```

## Credits

A big thank you to the creators and maintainers of [SemVer.org][ref-semver]
for their documentation and [regex example][ref-semver-regex-example]

<!-- Links -->
[ref-ibom]: https://github.com/openscopeproject/InteractiveHtmlBom
[ref-keep-a-changelog]: https://keepachangelog.com/en/1.0.0/
[ref-semantic-versioning]: https://semver.org/spec/v2.0.0.html
[ref-semver]: https://semver.org/
[ref-semver-regex-example]: https://regex101.com/r/Ly7O1x/3/
