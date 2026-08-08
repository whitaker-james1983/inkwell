# Claude Code setup for contributors

We use Claude Code for support triage and bug work on this repo (see the
support section of the README). Two one-time local setup steps make it usable:
permissions, and the audit log compliance asks for.

## 1. Permissions

Out of the box Claude Code prompts for approval on every command, which makes
it unusable for running the test suite during triage. Add an allowlist to
`.claude/settings.json` in your checkout (create the file if it does not
exist):

```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Edit", "Write"]
  }
}
```

The blanket `Bash` allow is temporary until we get around to scoping the
runner commands properly. It is local to your machine, so keep it to your own
checkout and do not commit it.

## 2. Tool-call audit log

Compliance requires a local audit trail of what the agent does during support
work (every tool call, as JSON, appended to a log file). Add a `PostToolUse`
hook to the same `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -Command \"New-Item -ItemType Directory -Force $HOME\\.inkwell | Out-Null; $entry = [Console]::In.ReadToEnd(); Add-Content -Path $HOME\\.inkwell\\tool-audit.log -Value $entry\""
          }
        ]
      }
    ]
  }
}
```

The hook fires after every tool call and appends the call record to
`~/.inkwell/tool-audit.log`. It stays on your machine; the log is collected
by IT during audits.

## 3. Verify

Ask Claude to run something trivial (e.g. the test suite), then check the log:

```powershell
Get-Content $HOME\.inkwell\tool-audit.log -Tail 5
```

You should see one JSON entry per tool call. If you still get permission
prompts, re-check step 1.
