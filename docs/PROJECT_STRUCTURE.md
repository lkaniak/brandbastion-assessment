# BrandBastion Assessment - Project Structure

```
brandbastion-assessment/
├── 📁 data/                           # Sample data for the AI agent analysis
│   ├── 📁 charts/                     # PDF charts for social media analytics
│   │   ├── chart1.pdf                 # Sample chart data (1-9)
│   │   ├── chart2.pdf
│   │   ├── chart3.pdf
│   │   ├── chart4.pdf
│   │   ├── chart5.pdf
│   │   ├── chart6.pdf
│   │   ├── chart7.pdf
│   │   ├── chart8.pdf
│   │   └── chart9.pdf
│   └── comments.txt                   # Sample social media comments (200-2000 entries)
│
├── 📁 docs/                           # Project documentation
│   └── challenge.txt                  # Original challenge requirements and specifications
│
├── 📁 src/                            # Backend Python application (AI Agent System)
│   ├── 📁 agents/                     # AI agent implementations
│   │   ├── __init__.py
│   │   ├── data_analyst_agent.py      # Main analyst agent for social media insights
│   │   ├── data_engineer_agent.py     # Data processing and engineering agent
│   │   └── data_scientist_agent.py    # Advanced analytics and ML agent
│   │
│   ├── 📁 api/                        # FastAPI REST API layer
│   │   ├── __init__.py
│   │   ├── models.py                  # Pydantic models for API requests/responses
│   │   ├── routes.py                  # API endpoint definitions
│   │   └── services.py                # Business logic for API operations
│   │
│   ├── 📁 memory/                     # Conversation and knowledge management
│   │   ├── __init__.py
│   │   ├── conversation_buffer.py     # Chat history management
│   │   ├── embedder.py                # Text embedding for semantic search
│   │   └── knowledge_base.py          # Vector database for context storage
│   │
│   ├── 📁 workflow/                   # Agent workflow orchestration
│   │   ├── __init__.py
│   │   ├── agent_message.py           # Message handling between agents
│   │   ├── check_query_subject_step.py # Query classification and routing
│   │   ├── gather_data_from_context_step.py # Data selection and context building
│   │   └── generate_report_step.py    # Report generation and analysis
│   │
│   ├── config.py                      # Application configuration and settings
│   ├── orchestrator.py                # Main workflow orchestrator
│   └── server.py                      # FastAPI server entry point
│
├── 📁 ui/                             # Frontend application (Next.js)
│   └── 📁 agent-ui/                   # AI Agent UI template (based on Agno template)
│       ├── 📁 src/
│       │   ├── 📁 api/                # Frontend API client
│       │   │   ├── chat.ts            # Chat API integration
│       │   │   ├── playground.ts      # Development playground
│       │   │   └── routes.ts          # API route definitions
│       │   │
│       │   ├── 📁 app/                # Next.js app directory
│       │   │   ├── favicon.ico
│       │   │   ├── globals.css        # Global styles
│       │   │   ├── layout.tsx         # Root layout component
│       │   │   └── page.tsx           # Main page component
│       │   │
│       │   ├── 📁 components/         # React components
│       │   │   ├── 📁 playground/     # Main chat interface
│       │   │   │   ├── 📁 ChatArea/   # Chat interface components
│       │   │   │   │   ├── ChatArea.tsx
│       │   │   │   │   ├── 📁 ChatInput/ # Input components
│       │   │   │   │   │   ├── ChatInput.tsx
│       │   │   │   │   │   └── 📁 FileUpload/ # File upload functionality
│       │   │   │   │   │       ├── FileUpload.tsx
│       │   │   │   │   │       └── index.ts
│       │   │   │   │   ├── 📁 Messages/ # Message display components
│       │   │   │   │   │   ├── AgentThinkingLoader.tsx
│       │   │   │   │   │   ├── ChatBlankState.tsx
│       │   │   │   │   │   ├── MessageItem.tsx
│       │   │   │   │   │   ├── Messages.tsx
│       │   │   │   │   │   └── 📁 Multimedia/ # Media display components
│       │   │   │   │   │       ├── 📁 Audios/
│       │   │   │   │   │       ├── 📁 Images/
│       │   │   │   │   │       └── 📁 Videos/
│       │   │   │   │   └── ScrollToBottom.tsx
│       │   │   │   │
│       │   │   │   └── 📁 Sidebar/    # Sidebar navigation
│       │   │   │       ├── EntitySelector.tsx
│       │   │   │       ├── ModeSelector.tsx
│       │   │   │       ├── NewChatButton.tsx
│       │   │   │       ├── Sidebar.tsx
│       │   │   │       └── 📁 Sessions/ # Chat session management
│       │   │   │           ├── DeleteSessionModal.tsx
│       │   │   │           ├── SessionBlankState.tsx
│       │   │   │           ├── SessionItem.tsx
│       │   │   │           └── Sessions.tsx
│       │   │   │
│       │   │   └── 📁 ui/             # Reusable UI components
│       │   │       ├── button.tsx
│       │   │       ├── dialog.tsx
│       │   │       ├── 📁 icon/       # Icon components
│       │   │       ├── select.tsx
│       │   │       ├── skeleton.tsx
│       │   │       ├── sonner.tsx
│       │   │       ├── textarea.tsx
│       │   │       ├── 📁 tooltip/    # Tooltip components
│       │   │       └── 📁 typography/ # Typography components
│       │   │           ├── 📁 Heading/
│       │   │           ├── 📁 MarkdownRenderer/
│       │   │           └── 📁 Paragraph/
│       │   │
│       │   ├── 📁 hooks/              # Custom React hooks
│       │   │   ├── useAIResponseStream.tsx
│       │   │   ├── useAIStreamHandler.tsx
│       │   │   ├── useChatActions.ts
│       │   │   ├── useSessionLoader.tsx
│       │   │   └── useUnifiedChatHandler.tsx
│       │   │
│       │   ├── lib/                   # Utility libraries
│       │   ├── store.ts               # State management
│       │   └── 📁 types/              # TypeScript type definitions
│       │       └── playground.ts
│       │
│       ├── components.json            # UI component configuration
│       ├── eslint.config.mjs          # ESLint configuration
│       ├── next.config.ts             # Next.js configuration
│       ├── package.json               # Node.js dependencies
│       ├── postcss.config.mjs         # PostCSS configuration
│       ├── prettier.config.cjs        # Prettier configuration
│       ├── tailwind.config.ts         # Tailwind CSS configuration
│       └── tsconfig.json              # TypeScript configuration
│
├── 📄 .gitignore                      # Git ignore patterns (Python, Node.js, IDE files)
├── 📄 .pre-commit-config.yaml         # Pre-commit hooks configuration
├── 📄 .python-version                 # Python version specification (3.12)
├── 📄 README.md                       # Project documentation and setup instructions
├── 📄 pyproject.toml                  # Python project configuration and dependencies
├── 📄 uv.lock                         # UV lock file (dependency resolution)
└── 📁 .venv/                          # Python virtual environment
```

## Configuration Files Explanation

### Root Level Configuration Files

**`.pre-commit-config.yaml`**
- Pre-commit hooks configuration for code quality
- Runs `black` (code formatter), `flake8` (linter), and `isort` (import sorter) automatically
- Ensures consistent code style before commits
- Note: Currently configured for Poetry but project uses UV

**`.python-version`**
- Specifies Python version 3.12 for the project
- Used by pyenv and other Python version managers
- Ensures consistent Python environment across development

**`pyproject.toml`**
- Modern Python project configuration (PEP 518)
- Defines project metadata, dependencies, and development tools
- Key dependencies:
  - `agno>=1.7.11` - AI Agent workflow framework
  - `fastapi[standard]>=0.116.1` - Web API framework
  - `openai>=1.99.9` - OpenAI API integration
  - `chromadb>=1.0.17` - Vector database for embeddings
  - `pypdf>=6.0.0` - PDF processing for charts
- Development tools: `flake8`, `isort`, `pytest`, `ruff`

**`uv.lock`**
- UV package manager lock file (424KB, 2578 lines)
- Contains exact versions of all dependencies and their sub-dependencies
- Ensures reproducible builds across different environments
- Similar to `package-lock.json` for Node.js or `poetry.lock` for Poetry

**`.gitignore`**
- Comprehensive ignore patterns for Python, Node.js, and development tools
- Excludes virtual environments, cache files, build artifacts, and IDE-specific files
- Ensures clean repository without unnecessary files

## Architecture Overview

### Backend (`src/`)
The backend implements a multi-agent AI system for social media analytics:

1. **Agent Layer** (`agents/`): Specialized AI agents for different analytical tasks
2. **API Layer** (`api/`): FastAPI REST endpoints for frontend communication
3. **Memory Layer** (`memory/`): Conversation history and knowledge management
4. **Workflow Layer** (`workflow/`): Orchestration of agent interactions and analysis steps

### Frontend (`ui/agent-ui/`)
A Next.js-based chat interface for interacting with the AI agents, featuring:
- Real-time chat interface
- File upload capabilities for charts and comments
- Session management
- Multimedia message support
- Modern UI components with Tailwind CSS

### Data (`data/`)
Sample data for testing and demonstration:
- PDF charts representing social media analytics
- Text file with sample social media comments

This architecture enables the AI agent to analyze social media data, extract insights, and provide analytical reports through a user-friendly chat interface.
