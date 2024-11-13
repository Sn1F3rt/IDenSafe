# IDenSafe - A Decentralized Identity Management Application

[![ci/gh-actions/ruff](https://github.com/Sn1F3rt/IDenSafe/actions/workflows/ruff.yml/badge.svg)](https://github.com/Sn1F3rt/IDenSafe/actions/workflows/ruff.yml)
[![License](https://img.shields.io/github/license/Sn1F3rt/BlogChain)](LICENSE)


## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
  - [Development](#development)
  - [Production](#production)
- [License](#license)

## About

BlogChain is a proof-of-concept blockchain-based identity management system for KYC. It is built on the [Ethereum](https://ethereum.org/en/) blockchain. It implements the [Sign-In with Ethereum](https://login.xyz/) authentication protocol, natively in Python using the [siwe-py](https://pypi.org/project/siwe/) library. On the core, it is built using the [Flask](https://flask.palletsprojects.com/) web framework. Database management is done using [SQLAlchemy](https://www.sqlalchemy.org/). 

It supports Ethereum based user authentication, setting username, verifying KYC and enabling attributes which can be requested.

## Prerequisites

- Git
- Python 3.10 or higher
- MariaDB/MySQL database
- [Ganache](https://www.trufflesuite.com/ganache) or any other Ethereum testnet

## Installation

1. Install [`uv`](https://docs.astral.sh/uv/) > https://docs.astral.sh/uv/getting-started/installation/

2. Clone the repository

   ```shell
    git clone https://github.com/Sn1F3rt/IDenSafe.git
   ```
   
3. Switch to the project directory

   ```shell
    cd IDenSafe
   ```
   
4. Create a virtual environment

   ```shell
   uv venv
   ```
   or if you have `make` installed

   ```shell
   make env
   ```
   
5. Install dependencies

   ```shell
    uv sync --no-dev --extra prod
   ```
   or if you have `make` installed

   ```shell
   make prod
   ```

## Configuration

Copy the [`config.example.py`](config.example.py) file to `config.py` and:

- update the `SECRET_KEY` variable with a 32-bit hexadecimal string.
- update the `DB_*` variables with your database credentials.
- update the `WEB3_PROVIDER` variable with the URL of your Ethereum node.

## Running

### Development

```shell
uv run launcher.py # or make
```

or if you have `make` installed

```shell
make activate
make
```

The API server will be running at `http://localhost:5000`.

### Production

```shell
source .venv/bin/activate # or make activate
gunicorn --bind 0.0.0.0:5000 launcher:app
```


or if you want to enable SSL support

```shell
source .venv/bin/activate
gunicorn --certfile cert.pem --keyfile key.pem --bind 0.0.0.0:5000 launcher:app
```

The API server will be running at `http://localhost:5000`. The certificate and key files are required for SSL support.

## License

[GNU General Public License v3.0](LICENSE)

Copyright &copy; 2024 [Sayan "Sn1F3rt" Bhattacharyya](https://sn1f3rt.dev)
