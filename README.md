# mcp-pagure

MCP server for Pagure integration (src.fedoraproject.org, pagure.io, and other Pagure instances).

## Overview

This MCP server provides tools for interacting with Pagure git forges, including Fedora's package source repository (dist-git) at src.fedoraproject.org.

## Features

- Package/repository browsing and management
- Spec file operations (view, diff)
- Patch management (list, view)
- Pull Request workflow (list, view, comment, merge)
- Git operations (commits, diffs, branches)
- Multi-instance support (src.fedoraproject.org, pagure.io, self-hosted)

## Installation
```bash
pip install mcp-pagure
```

## Configuration

Requires Pagure API token from your Pagure instance:
- src.fedoraproject.org: https://src.fedoraproject.org/settings#nav-api-tab
- pagure.io: https://pagure.io/settings#nav-api-tab
```bash
export PAGURE_API_TOKEN="your-token-here"
export PAGURE_BASE_URL="https://src.fedoraproject.org"  # optional, defaults to src.fp.o
```

## Usage

### Stdio Mode (Local)
```bash
mcp-pagure
```

### HTTP Mode (Remote)
```bash
mcp-pagure --transport http --port 8805
```

### With Claude CLI
```bash
claude mcp add --transport sse \
  --header "Authorization: Bearer $PAGURE_API_TOKEN" \
  pagure https://your-server.com/mcp/pagure
```

## Tools

### Repository Operations
- `list_projects` - Browse available projects/packages
- `get_project_info` - Get project metadata
- `fork_project` - Fork a project to your namespace

### File Operations
- `get_file` - View file content from repo
- `list_branches` - List repository branches
- `list_tags` - List repository tags

### Pull Request Workflow
- `list_pull_requests` - List PRs (open/closed/merged/all)
- `get_pull_request` - View PR details and comments
- `comment_on_pr` - Add review comments
- `merge_pull_request` - Merge approved PR
- `close_pull_request` - Close PR without merging

### Git Operations
- (No Git/commit tools available - Pagure API doesn't support commit listing)

## Development
```bash
git clone https://github.com/lemenkov/mcp-pagure
cd mcp-pagure
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

Apache-2.0

## Author

Peter Lemenkov <lemenkov@gmail.com>
