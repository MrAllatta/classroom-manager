# Executor Setup & Usage

## Prerequisites

1. **Python 3.9+**
2. **Anthropic API Key** (set as `ANTHROPIC_API_KEY` environment variable)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### API Key

Set your Anthropic API key before running:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Model Routing

Tasks are routed to models based on the role prefix in `task_id`:

| Role Prefix | Model | Use Case |
|---|---|---|
| `CURRDES` | claude-sonnet-4-5 | Complex reasoning, standards knowledge |
| `PLAN` | claude-haiku-3-5 | Structured calendar math, cheap operations |
| `ASSESS` | claude-sonnet-4-5 | Data analysis, nuanced judgment |
| `COMMS` | claude-haiku-3-5 | Templated drafting, cheap operations |
| *other* | claude-haiku-3-5 | Default fallback |

## Usage

### Watch Mode (default)
```bash
python executor.py
```
Polls `handoffs/` directory continuously, processing new tasks as they arrive.

### Run-Once Mode
```bash
python executor.py --no-watch
```
Processes all pending tasks once and exits.

### Custom Directories
```bash
python executor.py \
  --handoffs-dir /path/to/handoffs \
  --results-dir /path/to/results \
  --deliverables-dir /path/to/deliverables
```

### Logging to File
```bash
python executor.py --log-file executor.log
```

## Directory Structure

```
project/
├── handoffs/         # Input: task JSON files (task-ROLE-XXXX.json)
├── results/          # Output: result JSON files
├── deliverables/     # Output: generated content files
└── tmp/              # Internal: atomic write staging area
```

## Task JSON Format

```json
{
  "task_id": "CURRDES-0001",
  "goal": "Create a detailed curriculum outline",
  "deliverables": ["outline.md"],
  "plan": {
    "sections": ["intro", "chapters", "exercises"],
    "target_audience": "advanced learners"
  },
  "constraints": {
    "max_pages": 20,
    "include_references": true
  },
  "timeout_seconds": 600
}
```

**Required fields:**
- `task_id`: Unique task identifier (format: ROLE-XXXX for model routing)
- `goal`: Task description
- `deliverables`: List of output file names

**Optional fields:**
- `plan`: Task planning details (dict/string)
- `constraints`: Task constraints (dict/string)
- `timeout_seconds`: Maximum execution time (default: 600)
- `version`: Task version (default: 1)

## Result JSON Format

**Success:**
```json
{
  "task_id": "CURRDES-0001",
  "status": "done",
  "summary": "Generated 1 deliverable(s) for CURRDES-0001 using claude-sonnet-4-5",
  "deliverables": {
    "outline.md": "/absolute/path/to/outline.md"
  },
  "completed_at": "2026-03-25T21:15:30.123456+00:00",
  "version": 1
}
```

**Failure:**
```json
{
  "task_id": "CURRDES-0001",
  "status": "failed",
  "summary": "Task exceeded timeout",
  "error": "Task did not complete within timeout_seconds",
  "completed_at": "2026-03-25T21:15:30.123456+00:00",
  "version": 1
}
```

## Status Lifecycle

```
queued → running → done (or failed)
```

- **queued**: Task created, not yet started
- **running**: Task is being executed by the LLM
- **done**: Task completed successfully
- **failed**: Task failed (timeout, validation, API error, etc.)

## Implementation Details

### Model Routing

The `get_model_for_task()` function extracts the role prefix from `task_id`:
- Format: `ROLE-XXXX` → extracts `ROLE`
- Looks up model in `MODEL_MAP`
- Falls back to `DEFAULT_MODEL` if not found

### Prompt Building

The `build_prompt()` function creates a structured prompt from:
1. Task ID
2. Goal
3. Plan (optional)
4. Constraints (optional)

### API Integration

- Uses `anthropic.Anthropic` client initialized from `ANTHROPIC_API_KEY`
- Calls `messages.create()` with configurable max_tokens (4096)
- Handles `anthropic.APIError` and general exceptions
- Logs request/response metadata

### Atomic Writes

All JSON writes use atomic patterns:
1. Write to temporary file in `tmp/`
2. Atomic rename to target location
3. Prevents partial writes on process crash

## Troubleshooting

**"ANTHROPIC_API_KEY environment variable not set"**
- Set your API key: `export ANTHROPIC_API_KEY="your-key"`

**"anthropic library not installed"**
- Install dependencies: `pip install -r requirements.txt`

**Task timeouts**
- Increase `timeout_seconds` in task JSON
- Default: 600 seconds (10 minutes)

**Deliverable creation failures**
- Check `deliverables_dir` permissions
- Verify parent directories can be created
- Review error in result JSON `error` field
