# Hanashiai - Core

[![Version](https://img.shields.io/badge/version-0.4.0-brightgreen.svg)](https://github.com/VesnaBrucoms/hanashiai-core)
[![Build Status](https://travis-ci.org/VesnaBrucoms/hanashiai-core.svg?branch=master)](https://travis-ci.org/VesnaBrucoms/hanashiai-core)

The core functionality for interacting with Reddit for Hanashiai.

## Install

Hanashiai - Core can be found on PyPi:

```
pip install hanashiai-core
```

## Testing

Any tests run locally will need to build the testing image:

```
docker build -f Dockerfile-tests -t hanashiai-core .
```

### Unit Tests

The unit tests are run for every build. If you want to run them locally, run the following:

```
docker run --rm hanashiai-core pytest /opt/tests/unit_tests/
```

### Ad-hoc Scripts

Other one off testing scripts can be found under `/opt/tests/misc/`, e.g.:

```
docker run --rm hanashiai-core python /opt/tests/misc/search_test.py
```

## License

[MIT](LICENSE) (c) Trevalyan Stevens