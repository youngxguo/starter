# skills

- keep each skill in `skills/<skill-name>`.
- keep `SKILL.md` concise and put trigger conditions in its description.
- add scripts, references, or assets only when the workflow needs them.
- keep `agents/openai.yaml` aligned with the skill.
- validate every changed skill with the skill creator's `quick_validate.py`.

## installing

- use `python3 install.py` to link every skill for Codex and Claude.
- keep installation idempotent and refuse to replace paths the repo does not own.
- add or update installer tests when installation behavior changes.
