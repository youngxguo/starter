# skills

- keep each skill in `skills/<skill-name>`.
- keep `SKILL.md` concise and put trigger conditions in its description.
- add scripts, references, or assets only when the workflow needs them.
- keep `agents/openai.yaml` aligned with the skill.
- validate every changed skill with the skill creator's `quick_validate.py`.

## distribution

- distribute skills through the Skills Marketplace and its `npx skills` CLI.
- keep `npx skills add . --list` able to discover every skill in the repository.
