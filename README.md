# BrandBastion Assessment

Task: Create an agent that interfaces with the requester trough a chat interface.
The agent should appear to the user to be a friendly analyst that specializes in reading data-heavy reports and extracting insights regarding the social media activity on a media brand space.

# Overview

## Agent Structure

The backend implements a multi-agent AI system for social media analytics:

1. **Agent Layer** (`agents/`): Specialized AI agents for different analytical tasks
2. **API Layer** (`api/`): FastAPI REST endpoints for frontend communication
3. **Memory Layer** (`memory/`): Conversation history and knowledge management
4. **Workflow Layer** (`workflow/`): Steps for agent interactions and analysis
5. **orchestrator** (`orchestrator.py`): Implementation of the workflow. Defines step order and other runtime configurations
6. **config** (`config.py`): Evnironment variables configuration
7. **server** (`server.py`): entrypoint for the backend application

## Agent Stack

This agent uses [Agno](https://docs.agno.com/introduction) as the main framework for Agentic APIs. It uses [FastAPI](https://fastapi.tiangolo.com) underneath the package to serve the application. It relies on [Pydantic](https://docs.pydantic.dev/latest/) to ensure the data structures used are coherent. It stores conversation through SQLite using [sqlalchemy](http://www.sqlalchemy.org). The models used for this demo are OpenAI's `gpt-4o-mini` and `gpt-4o` and `sentence-transformers/all-MiniLM-L6-v2` from HuggingFace for history data embedding.

## Considerations

- I had to modify the frontend template app to include a upload feature. This was unexpected in the development of this challenge because I thought the template had one, the "click to upload" feature is not properly working and I had no time to fix it.
- The chat history is not properly working, althrough I have configured it. I am not sure if it is a misconfiguration or it is needed to change the implementation.

## Documentation assets

[project structure](./docs/PROJECT_STRUCTURE.md)

## Writeup

**Q:** Please provide a write up with an explanation of your decisions. For example, how did you decide to store your context, how does the decision graph of your agent look like (and why you chose it that way), what tools did you chose to code yourself and what components did you leave to the LLM (and why) etc.
**A:** I'll begin with the architecture. I structured the project this way to make it easier to locate and update components as development progresses. The design takes inspiration from clean architecture but is tailored specifically for AI agent development. The agent consists of a [workflow](https://docs.agno.com/workflows_2/overview) with three steps:

- `check_query_subject`: Addresses the subject of the conversation ensuring it is related to data analysis. It also enhances the problem to solve by formulating a possible plan to gather data in the files attached to be used in the next step.
- `gather_data_from_context`: This step parses the files to find relevant data to answer the query. It uses two different approaches for each type of file: If its pdf it sends to the model API with the file attached to perform the OCR. However, if it is a text file, the contents are parsed and appended into the context for extraction in a regular model call.
- `generate_report`: Compiles the data from previous steps to best answer the query. In this step also it can return for clarification in case the data is not sufficient to generate the report.

I went with these three steps because I wanted more control over file parsing, especially when dealing with text, and also to use AI to cut down the context by picking out the relevant parts of the data early on. This way, I could also catch and handle edge cases without much prompt engineering—for example, when the query isn’t really about data analysis. I left the LLM to do what it’s best at, like pattern recognition and OCR (gather_data_from_context), figuring out intent (check_query_subject), and generating content (generate_report), while I kept control of the overall workflow and how the Agent runs things.

the main flow of the decision tree is as: query -> `check_query_subject` -> `gather_data_from_context` -> `generate_report` -> result
edge cases by step (excluding error steps):

1) `check_query_subject`
- Step to redirect to the user if the subject is other than data analysis

2) `gather_data_from_context`
- Step to redirect to the user if no files are provided

3) `generate_report`
- Step to redirect to the user if not relevant data was found.

**Q:** Write a few lines on how you would handle scale on this problem. If instead of a 200 comments sample you had a 2000000 comments database for the analysis in question, how would you handle that? If you had 500 concurrent users? Etc
**A:** in this case I would need to use batch processing to avoid token limit issues in conjunction with embedding to store the context. The file processing task can also be broken into subtasks to concurrently gather information on files.

**Q:** Write a few lines on how you would deploy this solution in a cloud architecture. How would you handle state, latency, race conditions, etc?
**A:** I would run this on a virtual server/container manager (such as EC2/Kubernetes) so it can provide multiple instances of the service so it can handle load and scale horizontally. I would separate (if possible) the heavy processing part of files, such as the OCR task to a separate cluster and use an event based approach, like a message queue, to avoid race conditions. This system would also need heavy monitoring metrics to identify possible bottlenecks and optimizations to the production environment. A persistent storage with embeddings can be used as a first-layer cache to return previous answered queries in order to improve latency. The I/Os would also need optimization such as a connection pooling to reduce delays in reading/writing data.

**Q:** Write a few lines on how you would handle grounding and hallucination prevention/mitigation for this problem.
**A:** setting the temperature to 0 in the data gathering step and applying some prompt engineering to make the agent not create fictional or false information reduces significantly the analysis hallucination.

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

OBS: the post for the backend must be 7777 or else it wont connect to the frontend!

## running the frontend

The frontend is a modified template for AI Agents. The base template is found at: https://github.com/agno-agi/agent-ui

1) in another terminal, `$ cd ui/agent-ui`.

2) install the dependencies: `$ npm install`

3) run the client: `$ npm run dev`

4) the app is in `localhost:3000`

5) all tests can be done through the interface. There is no need to change the input, it can be uploaded alongside the prompt.

