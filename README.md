# toml_tools, Tomli and Tomli-W for Python 2 and Iron Python

v1.1.1 - fit for purpose!  Passes 52 of Hukkin's unittest tests, in Python 2 and Iron Python 2.7

v1.0.0 is a complete overhaul - toml_tools is now based on tomli and tomli-w.  Note, unlike toml_tools v0, toml and tomlkit, toml_tools v1 and tomli require files to be opened in bytes mode ('rb').


# Parent Project number (1/2)'s Readme File (Tomli)

> A lil' TOML parser

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Intro](#intro)
- [Installation](#installation)
- [Usage](#usage)
  - [Parse a TOML string](#parse-a-toml-string)
  - [Parse a TOML file](#parse-a-toml-file)
  - [Handle invalid TOML](#handle-invalid-toml)
  - [Construct `decimal.Decimal`s from TOML floats](#construct-decimaldecimals-from-toml-floats)
  - [Building a `tomli`/`tomllib` compatibility layer](#building-a-tomlitomllib-compatibility-layer)
- [FAQ](#faq)
  - [Why this parser?](#why-this-parser)
  - [Is comment preserving round-trip parsing supported?](#is-comment-preserving-round-trip-parsing-supported)
  - [Is there a `dumps`, `write` or `encode` function?](#is-there-a-dumps-write-or-encode-function)
  - [How do TOML types map into Python types?](#how-do-toml-types-map-into-python-types)
- [Performance](#performance)

<!-- mdformat-toc end -->

## Intro<a name="intro"></a>

Tomli is a Python library for parsing [TOML](https://toml.io).
It is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0).

A version of Tomli, the `tomllib` module,
was added to the standard library in Python 3.11
via [PEP 680](https://www.python.org/dev/peps/pep-0680/).
Tomli continues to provide a backport on PyPI for Python versions
where the standard library module is not available
and that have not yet reached their end-of-life.

## Installation<a name="installation"></a>

```bash
pip install tomli
```

## Usage<a name="usage"></a>

### Parse a TOML string<a name="parse-a-toml-string"></a>

```python
import tomli

toml_str = """
[[players]]
name = "Lehtinen"
number = 26

[[players]]
name = "Numminen"
number = 27
"""

toml_dict = tomli.loads(toml_str)
assert toml_dict == {
    "players": [{"name": "Lehtinen", "number": 26}, {"name": "Numminen", "number": 27}]
}
```

### Parse a TOML file<a name="parse-a-toml-file"></a>

```python
import tomli

with open("path_to_file/conf.toml", "rb") as f:
    toml_dict = tomli.load(f)
```

The file must be opened in binary mode (with the `"rb"` flag).
Binary mode will enforce decoding the file as UTF-8 with universal newlines disabled,
both of which are required to correctly parse TOML.

### Handle invalid TOML<a name="handle-invalid-toml"></a>

```python
import tomli

try:
    toml_dict = tomli.loads("]] this is invalid TOML [[")
except tomli.TOMLDecodeError:
    print("Yep, definitely not valid.")
```

Note that error messages are considered informational only.
They should not be assumed to stay constant across Tomli versions.

### Construct `decimal.Decimal`s from TOML floats<a name="construct-decimaldecimals-from-toml-floats"></a>

```python
from decimal import Decimal
import tomli

toml_dict = tomli.loads("precision-matters = 0.982492", parse_float=Decimal)
assert isinstance(toml_dict["precision-matters"], Decimal)
assert toml_dict["precision-matters"] == Decimal("0.982492")
```

Note that `decimal.Decimal` can be replaced with another callable that converts a TOML float from string to a Python type.
The `decimal.Decimal` is, however, a practical choice for use cases where float inaccuracies can not be tolerated.

Illegal types are `dict` and `list`, and their subtypes.
A `ValueError` will be raised if `parse_float` produces illegal types.

### Building a `tomli`/`tomllib` compatibility layer<a name="building-a-tomlitomllib-compatibility-layer"></a>

Python versions 3.11+ ship with a version of Tomli:
the `tomllib` standard library module.
To build code that uses the standard library if available,
but still works seamlessly with Python 3.6+,
do the following.

Instead of a hard Tomli dependency, use the following
[dependency specifier](https://packaging.python.org/en/latest/specifications/dependency-specifiers/)
to only require Tomli when the standard library module is not available:

```
tomli >= 1.1.0 ; python_version < "3.11"
```

Then, in your code, import a TOML parser using the following fallback mechanism:

```python
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

tomllib.loads("['This parses fine with Python 3.6+']")
```

## FAQ<a name="faq"></a>

### Why this parser?<a name="why-this-parser"></a>

- it's lil'
- pure Python with zero dependencies
- the fastest pure Python parser [\*](#performance):
  16x as fast as [tomlkit](https://pypi.org/project/tomlkit/),
  2.3x as fast as [toml](https://pypi.org/project/toml/)
- outputs [basic data types](#how-do-toml-types-map-into-python-types) only
- 100% spec compliant: passes all tests in
  [BurntSushi/toml-test](https://github.com/BurntSushi/toml-test)
  test suite
- thoroughly tested: 100% branch coverage

### Is comment preserving round-trip parsing supported?<a name="is-comment-preserving-round-trip-parsing-supported"></a>

No.

The `tomli.loads` function returns a plain `dict` that is populated with builtin types and types from the standard library only.
Preserving comments requires a custom type to be returned so will not be supported,
at least not by the `tomli.loads` and `tomli.load` functions.

Look into [TOML Kit](https://github.com/sdispater/tomlkit) if preservation of style is what you need.

### Is there a `dumps`, `write` or `encode` function?<a name="is-there-a-dumps-write-or-encode-function"></a>

[Tomli-W](https://github.com/hukkin/tomli-w) is the write-only counterpart of Tomli, providing `dump` and `dumps` functions.

The core library does not include write capability, as most TOML use cases are read-only, and Tomli intends to be minimal.

### How do TOML types map into Python types?<a name="how-do-toml-types-map-into-python-types"></a>

| TOML type        | Python type         | Details                                                      |
| ---------------- | ------------------- | ------------------------------------------------------------ |
| Document Root    | `dict`              |                                                              |
| Key              | `str`               |                                                              |
| String           | `str`               |                                                              |
| Integer          | `int`               |                                                              |
| Float            | `float`             |                                                              |
| Boolean          | `bool`              |                                                              |
| Offset Date-Time | `datetime.datetime` | `tzinfo` attribute set to an instance of `datetime.timezone` |
| Local Date-Time  | `datetime.datetime` | `tzinfo` attribute set to `None`                             |
| Local Date       | `datetime.date`     |                                                              |
| Local Time       | `datetime.time`     |                                                              |
| Array            | `list`              |                                                              |
| Table            | `dict`              |                                                              |
| Inline Table     | `dict`              |                                                              |

## Performance<a name="performance"></a>

The `benchmark/` folder in this repository contains a performance benchmark for comparing the various Python TOML parsers.
The benchmark can be run with `tox -e benchmark-pypi`.
Running the benchmark on my personal computer output the following:

```console
foo@bar:~/dev/tomli$ tox -e benchmark-pypi
benchmark-pypi installed: attrs==21.4.0,click==8.0.3,pytomlpp==1.0.10,qtoml==0.3.1,rtoml==0.7.1,toml==0.10.2,tomli==2.0.1,tomlkit==0.9.2
benchmark-pypi run-test-pre: PYTHONHASHSEED='3088452573'
benchmark-pypi run-test: commands[0] | python -c 'import datetime; print(datetime.date.today())'
2022-02-09
benchmark-pypi run-test: commands[1] | python --version
Python 3.8.10
benchmark-pypi run-test: commands[2] | python benchmark/run.py
Parsing data.toml 5000 times:
------------------------------------------------------
    parser |  exec time | performance (more is better)
-----------+------------+-----------------------------
     rtoml |    0.891 s | baseline (100%)
  pytomlpp |    0.969 s | 91.90%
     tomli |        4 s | 22.25%
      toml |     9.01 s | 9.88%
     qtoml |     11.1 s | 8.05%
   tomlkit |       63 s | 1.41%
```

The parsers are ordered from fastest to slowest, using the fastest parser as baseline.
Tomli performed the best out of all pure Python TOML parsers,
losing only to pytomlpp (wraps C++) and rtoml (wraps Rust).

# Iron-Tomli-W

A fork of Tomli-W for Iron Python 2

- **Reluctant Iron Python 2 user**: [James Parrott](https://github.com/JamesParrott)
- **Version**: 1.0.0
- **Date**: 25 April, 2023
 - **License**: [MIT](https://github.com/GeospatialPython/pyshp/blob/master/LICENSE.TXT)
 - 
## Installation<a name="installation"></a>

For the time being, manually copy `_write.py` and `__init__.py` into a folder called `iron-tomli-w` into a path (and append that to sys.path if it's not already there)

# Parent Project number (2/2)'s Readme File (Iron-Tomli-W)

A fork of Tomli-W for Iron Python 2

- **Reluctant Iron Python 2 user**: [James Parrott](https://github.com/JamesParrott)
- **Version**: 1.0.0
- **Date**: 25 April, 2023
 - **License**: [MIT](https://github.com/GeospatialPython/pyshp/blob/master/LICENSE.TXT)
 - 
## Installation<a name="installation"></a>

For the time being, manually copy `_write.py` and `__init__.py` into a folder called `iron-tomli-w` into a path (and append that to sys.path if it's not already there)

# Tomli-W

> A lil' TOML writer

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Intro](#intro)
- [Installation](#installation)
- [Usage](#usage)
  - [Write to string](#write-to-string)
  - [Write to file](#write-to-file)
- [FAQ](#faq)
  - [Does Tomli-W sort the document?](#does-tomli-w-sort-the-document)
  - [Does Tomli-W support writing documents with comments or custom whitespace?](#does-tomli-w-support-writing-documents-with-comments-or-custom-whitespace)
  - [Why does Tomli-W not write a multi-line string if the string value contains newlines?](#why-does-tomli-w-not-write-a-multi-line-string-if-the-string-value-contains-newlines)
  - [Is Tomli-W output guaranteed to be valid TOML?](#is-tomli-w-output-guaranteed-to-be-valid-toml)

<!-- mdformat-toc end -->

## Intro<a name="intro"></a>

Tomli-W is a Python library for writing [TOML](https://toml.io).
It is a write-only counterpart to [Tomli](https://github.com/hukkin/tomli),
which is a read-only TOML parser.
Tomli-W is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0).

## Usage<a name="usage"></a>

### Write to string<a name="write-to-string"></a>

```python
import tomli_w

doc = {"table": {"nested": {}, "val3": 3}, "val2": 2, "val1": 1}
expected_toml = """\
val2 = 2
val1 = 1

[table]
val3 = 3

[table.nested]
"""
assert tomli_w.dumps(doc) == expected_toml
```

### Write to file<a name="write-to-file"></a>

```python
import tomli_w

doc = {"one": 1, "two": 2, "pi": 3}
with open("path_to_file/conf.toml", "wb") as f:
    tomli_w.dump(doc, f)
```

## FAQ<a name="faq"></a>

### Does Tomli-W sort the document?<a name="does-tomli-w-sort-the-document"></a>

No, but it respects sort order of the input data,
so one could sort the content of the `dict` (recursively) before calling `tomli_w.dumps`.

### Does Tomli-W support writing documents with comments or custom whitespace?<a name="does-tomli-w-support-writing-documents-with-comments-or-custom-whitespace"></a>

No.

### Why does Tomli-W not write a multi-line string if the string value contains newlines?<a name="why-does-tomli-w-not-write-a-multi-line-string-if-the-string-value-contains-newlines"></a>

This default was chosen to achieve lossless parse/write round-trips.

TOML strings can contain newlines where exact bytes matter, e.g.

```toml
s = "here's a newline\r\n"
```

TOML strings also can contain newlines where exact byte representation is not relevant, e.g.

```toml
s = """here's a newline
"""
```

A parse/write round-trip that converts the former example to the latter does not preserve the original newline byte sequence.
This is why Tomli-W avoids writing multi-line strings.

A keyword argument is provided for users who do not need newline bytes to be preserved:

```python
import tomli_w

doc = {"s": "here's a newline\r\n"}
expected_toml = '''\
s = """
here's a newline
"""
'''
assert tomli_w.dumps(doc, multiline_strings=True) == expected_toml
```

### Is Tomli-W output guaranteed to be valid TOML?<a name="is-tomli-w-output-guaranteed-to-be-valid-toml"></a>

No.
If there's a chance that your input data is bad and you need output validation,
parse the output string once with `tomli.loads`.
If the parse is successful (does not raise `tomli.TOMLDecodeError`) then the string is valid TOML.
