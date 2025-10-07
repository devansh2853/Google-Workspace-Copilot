# Google-Workspace-Copilot

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd Google-Workspace-Copilot
```

### 2. Environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Fill in your Composio and Gemini API Keys. Leave the Auth Config IDs for now.

### 3. Install UV (if not installed)

Follow the instructions from [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/) or using curl.

### 4. Set up Python environment with `uv`

```bash
uv sync
```

### 5. Create Auth Configs

Run the auth config script to create Gmail and Google Docs auth configs:

```bash
uv run python core/auth_config.py
```

Copy the printed auth config IDs into your `.env` file.

### 6. Connect your accounts

Run the main CLI:

```bash
uv run python main.py
```
