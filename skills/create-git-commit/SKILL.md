---
name: create-git-commit
description: Review current Git changes, select a coherent scope, stage it, write a clear lowercase commit message, and create the commit. Use when asked to commit current changes, make a Git commit, checkpoint work, or turn worktree changes into a commit.
---

# create git commit

Create one focused commit from the current worktree. Preserve unrelated changes and do not push unless explicitly requested.

## inspect

- Read the repository instructions and commit conventions.
- Inspect the branch, status, staged diff, unstaged diff, and relevant untracked files.
- Identify the changes covered by the request. If unrelated changes make the intended scope unclear, ask before staging them.

## verify

- Run checks appropriate to the selected changes and repository guidance.
- Review the selected diff for accidental, generated, sensitive, or unrelated content.
- Do not discard, rewrite, or hide changes outside the commit scope.

## stage

- Stage only the files or hunks that belong in the commit.
- Avoid broad staging commands when the worktree contains unrelated changes.
- Review the staged diff before committing.

## write

Follow the repository's commit format. When it does not define one, use one of these title forms:

```text
<emoji> <type>(<scope>): <summary>
<emoji> <type>: <summary>
```

Use these defaults:

- `📝 docs` for documentation
- `✨ feat` for new behavior
- `🐛 fix` for corrected behavior
- `♻️ refactor` for internal restructuring
- `🔧 chore` for maintenance
- `🎨 style` for formatting-only changes

- Write the title and body in lowercase, except where exact capitalization is required for names or identifiers.
- Use imperative style and omit trailing punctuation from the title.
- Keep the title short and specific, and include a scope only when it adds useful context.
- Add a body only when the reason, tradeoff, or important context is not clear from the title.

## commit

- Create the commit without bypassing hooks.
- If a hook or commit fails, diagnose it and keep any fix within the requested scope.
- Verify the resulting commit and report its hash, title, checks run, and any remaining uncommitted changes.
