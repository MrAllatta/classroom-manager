# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## 3. Prepare Input Directory

```bash
mkdir -p handoffs results deliverables tmp
```

## 4. Add a Task

Copy the example task:
```bash
cp example_task.json handoffs/task-CURRDES-0001.json
```

Or create your own with format:
```json
{
  "task_id": "ROLE-XXXX",
  "goal": "Task description",
  "deliverables": ["output.md"]
}
```

## 5. Run Executor

**One-time execution:**
```bash
python executor.py --no-watch
```

**Watch mode (continuous):**
```bash
python executor.py
```

## 6. Check Results

Execution metadata:
```bash
cat results/result-CURRDES-0001.json
```

Generated content:
```bash
cat deliverables/outline.md
```

## Model Routing Reference

| Task ID Prefix | Model Used | Cost |
|---|---|---|
| CURRDES-* | claude-sonnet-4-5 | Higher (complex) |
| PLAN-* | claude-haiku-3-5 | Lower (efficient) |
| ASSESS-* | claude-sonnet-4-5 | Higher (nuanced) |
| COMMS-* | claude-haiku-3-5 | Lower (templates) |

## Customization

**Change models:**
Edit `MODEL_MAP` in executor.py

**Adjust response length:**
Change `max_tokens=4096` in execute_task()

**Add system prompt:**
Add `system=` parameter to messages.create() call

**Change timeout:**
Set `timeout_seconds` field in task JSON

## Troubleshooting

| Issue | Solution |
|---|---|
| `ANTHROPIC_API_KEY not set` | Run `export ANTHROPIC_API_KEY="..."` |
| `anthropic not found` | Run `pip install -r requirements.txt` |
| Task times out | Increase `timeout_seconds` in task JSON |
| No deliverable created | Check `deliverables_dir` permissions |

For detailed docs, see `SETUP.md` and `IMPLEMENTATION_SUMMARY.md`
