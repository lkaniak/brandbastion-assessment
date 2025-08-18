# BrandBastion Assessment

Task: Create an agent that interfaces with the requester trough a chat interface.
The agent should appear to the user to be a friendly analyst that specializes in reading data-heavy reports and extracting insights regarding the social media activity on a media brand space.

# Overview

## Documentation assets

## Writeup

# Development

## running the backend

This project uses [Agno](https://docs.agno.com/introduction) for AI Agent workflow. Steps for installation:

1) configure and export the variables in `.env.development` as `.env`. ([direnv](https://github.com/direnv/direnv) is highly recommended)

2) install the dependencies ([uv](https://docs.astral.sh/uv/) is highly recommended)

- using `uv`:

in this folder:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install project dependencies
uv sync

# install dev dependencies
uv sync --group dev
```

3) run the backend

with the `.venv` activated:

```bash

python -m src.server

```

## running the frontend

The frontend is a template for AI Agents. The template is found at: https://github.com/agno-agi/agent-ui

1) in another terminal, `$ cd ui/agent-ui`.

2) install the dependencies: `$ npm install`

3) run the client: `$ npm run dev`

4) the app is in `localhost:3000`

