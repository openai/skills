# Phaxio Reference

## Auth

The v1 CLI uses environment variables:

- `PHAXIO_API_KEY`
- `PHAXIO_API_SECRET`

The helper sends these as request auth on every API call.

## Auth model

Use Phaxio as the default v1 provider because API key + secret auth is a good fit for a headless CLI:

- no browser login
- no token refresh flow
- no local credential cache
- easy CI or automation support through environment variables

For future providers, choose auth in this order:

1. API key + secret for single-account automation.
2. OAuth client credentials for service-to-service org setups.
3. OAuth auth code or JWT for delegated user access.

Avoid storing provider secrets in repo config files. If a local config file is added later, keep only non-secret defaults there and continue reading credentials from environment variables.

## Endpoints

Base URL:

- `https://api.phaxio.com/v2`

Implemented endpoints:

- `POST /faxes`
- `GET /faxes/{id}`
- `GET /faxes/{id}/file`

## Send behavior

The CLI sends a multipart request with:

- `to`: destination fax number
- `file`: local PDF
- `cover_page`: optional cover page text
- `callback_url`: optional webhook callback URL

## Notes

- Destination numbers should use E.164 format.
- `--wait` polls `GET /faxes/{id}` until the fax reaches a terminal state or times out.
- The provider adapter is intentionally isolated in `scripts/fax_cli.py` so additional providers can be added without changing the command surface.
