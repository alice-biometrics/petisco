name: pypi

on:
  release:
    types: [published]

jobs:
  get-version:
    uses: alice-biometrics/actions/.github/workflows/get-version.yml@v1.44
    with:
      type: release
