---
name: create-github-pr
description: Review a Git branch, verify its commits and diff, push it, and open a focused GitHub pull request. Use when asked to create, open, submit, or publish a pull request or PR from the current repository.
---

# create github pr

Open one focused pull request from the current branch. Preserve unrelated changes and follow the repository's instructions and pull request template.

## inspect

- Read the repository instructions and contribution conventions.
- Inspect the current branch, worktree status, remotes, upstream, and existing pull requests for the branch.
- Determine the intended base from the request or repository default.
- Fetch the relevant remote, then review the commits and complete diff from the merge base through `HEAD`.
- Stop if the branch includes unrelated commits or the intended base is unclear.

## prepare

- Ensure all changes intended for the pull request are committed. Keep unrelated worktree changes out of the commits.
- Run checks appropriate to the changed behavior and repository guidance.
- Review the final diff for accidental, generated, sensitive, or unrelated content.
- Do not bypass hooks, rewrite published history, or force-push unless explicitly requested.

## write

Follow the repository's title and body conventions. When it does not define a format, use:

```text
<emoji> <type>(<scope>): <summary>
<emoji> <type>: <summary>
```

Use a short, specific title with lowercase, imperative wording and no trailing punctuation. Include a scope only when it adds clarity. Common types are `docs`, `feat`, `fix`, `refactor`, `chore`, and `style`.

Write a concise body:

```markdown
## summary

- <what changed and why>

## checks

- <validation performed>
```

Mention meaningful risks or follow-up work without inventing details. Use the repository's pull request template when one exists.

## publish

- Push the current branch to the appropriate remote and set its upstream when needed.
- Open a ready pull request unless the user requests a draft or the work is explicitly incomplete.
- Set the intended base and head explicitly when repository or remote ambiguity exists.
- If a pull request already exists for the branch, return it instead of creating a duplicate.
- Verify the resulting pull request's URL, title, base, head, and state.
- Report the URL, checks run, and any remaining uncommitted changes.
