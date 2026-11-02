---
name: github-integration
description: Use the session's enabled GitHub connector or web-project-scoped GitHub credentials through the correct CLI entry point, preserving repository scope and the user's existing configuration.
---

# GitHub Integration

Select the first matching mode below from current session context: `github_enabled`, `github_repos`, `device_only_execution_enabled`, `long_sandbox_execution`, `github_token_source`, and `github_connector_errored`. When `github_repos` is provided, it identifies the repositories the user explicitly selected for this task.

## Enabled connector on Device-only or Long Sandbox

Use this mode when `github_enabled=true` and either `device_only_execution_enabled=true` or `long_sandbox_execution=true`.

Plain `gh ...` retains the user's existing GitHub CLI configuration. When choosing the enabled GitHub connector, use its entry point:

```sh
"$MANUS_CONFIG_HOME/connectors/github/gh" <args...>
```

In PowerShell:

```powershell
& "$env:MANUS_CONFIG_HOME\connectors\github\gh.cmd" <args...>
```

Before first use, check whether `gh` is installed. If missing, install GitHub CLI on the user's computer using an available system package manager or an official native release. Report the exact error if installation fails.

Do not run `gh auth login` or change the user's global Git or GitHub CLI configuration.

Clone through the connector with `"$MANUS_CONFIG_HOME/connectors/github/gh" repo clone <repo-name>` or the equivalent PowerShell entry point. When creating repositories, use `--private` by default to protect user privacy.

## Preconfigured connector CLI

Otherwise, use this mode when `github_enabled=true` and `github_token_source="connector"`.

The GitHub CLI is preconfigured and logged into the user's account. Use `gh` through `exec` for GitHub operations instead of the browser. Clone with `gh repo clone <repo-name>`. When creating repositories, use `--private` by default to protect user privacy.

## Web-project-scoped CLI

Otherwise, use this mode when both Device-only and Long Sandbox execution are false and `github_token_source="webdev"`.

The authenticated `gh` CLI can access only the web project's exported GitHub repository.

For operations on any other repository:

- If `github_connector_errored=true`, explain that the connector is expired or revoked and ask the user to reconnect it in connector settings.
- Otherwise, suggest enabling the GitHub connector.

Review provenance: [all three original branches](references/original-block.txt).
