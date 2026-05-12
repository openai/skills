# Third-Party Notices

This directory contains vendored browser runtime files used by the local ProjectGraph viewer.

## Markmap

- Packages: `markmap-autoloader`, `markmap-lib`, `markmap-toolbar`, `markmap-view`
- Version: `0.18.12`
- Source: https://www.npmjs.com/package/markmap-lib
- Repository: https://github.com/markmap/markmap
- License: MIT

## D3

- Package: `d3`
- Version: `7.9.0`
- Source: https://www.npmjs.com/package/d3/v/7.9.0
- Repository: https://github.com/d3/d3
- License: ISC

The vendored files are used to keep ProjectGraph viewers local/offline by default. The viewer should not introduce CDN fallback URLs without updating this notice, `VENDOR_MANIFEST.json`, and the release checker.

