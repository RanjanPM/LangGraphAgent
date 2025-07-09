# LangGraph Agent Project

## Prerequisites

- **Python 3.10+** (Recommended: 3.11 or later)
- **VS Code** (with Python extension)
- **Git**
- **uv** (ultra-fast Python package manager)

## Setup Instructions

### 1. Install Python
- Download and install Python from [python.org](https://www.python.org/downloads/).
- Ensure Python is added to your PATH.

### 2. Install VS Code
- Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/).
- Install the Python extension from the VS Code marketplace.

### 3. Install uv (Python package manager)
- Open PowerShell and run:
  ```powershell
  iwr https://astral.sh/uv/install.ps1 -useb | iex
  $env:Path = "C:\Users\<YourUsername>\.local\bin;$env:Path"
  ```
- Replace `<YourUsername>` with your Windows username.

### 4. Set up a Virtual Environment in VS Code
- Open the project folder in VS Code.
- Open the command palette (Ctrl+Shift+P) and run:
  - `Python: Create Environment` (choose `venv`)
- Or manually in terminal:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

### 5. Install Project Dependencies
- With your virtual environment activated, run:
  ```powershell
  uv pip install langgraph langchain langsmith notebook python-dotenv
  ```

### 6. API Keys Setup
Create a `.env` file in the project root with the following keys:
```env
GOOGLE_API_KEY=
COLLECT_API_KEY=
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT='https://api.smith.langchain.com'
LANGSMITH_API_KEY=
LANGSMITH_PROJECT='LangGraphAgent'
OPENAI_API_KEY=
```

#### How to obtain API Keys:
- **Gemini 2.5 (Google Generative AI):**
  - Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new API key.
  - Paste it as `GOOGLE_API_KEY` in your `.env` file.
- **Collect API (for gas prices):**
  - Sign up at [Collect API](https://www.collectapi.com/) and subscribe to the "Gas Price" API.
  - Copy your API key and set it as `COLLECT_API_KEY`.
- **LangSmith (for tracing):**
  - Sign up at [LangSmith](https://smith.langchain.com/).
  - Go to your account settings and generate an API key.
  - Set it as `LANGSMITH_API_KEY`.
  - Optionally, set your project name as `LANGSMITH_PROJECT`.
- **OpenAI (optional):**
  - Get your API key from [OpenAI](https://platform.openai.com/account/api-keys) and set as `OPENAI_API_KEY`.

### 7. Running the Project
- Open a terminal in VS Code.
- Activate your virtual environment:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- Start Jupyter Notebook:
  ```powershell
  uv pip install notebook
  jupyter notebook
  ```
- Open and run the provided notebooks (e.g., `4_tool_call.ipynb`, `7_langsmith_tracing.ipynb`).

### 8. GitHub
- All code and notebooks are version controlled in this repository.
- Sensitive data (API keys) are excluded via `.gitignore`.

## Notes
- Never commit your `.env` file with real API keys to the repository.
- For more details, see the documentation for [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [LangSmith](https://smith.langchain.com/).