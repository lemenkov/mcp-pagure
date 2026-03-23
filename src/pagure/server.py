"""Main MCP server for Pagure integration."""

import os
import argparse
from typing import Optional
from fastmcp import FastMCP
from .client import PagureClient


# Initialize FastMCP server
mcp = FastMCP("Pagure MCP Server")

# Global client instance
pagure_client: Optional[PagureClient] = None


def get_client() -> PagureClient:
    """Get or create the Pagure client."""
    global pagure_client
    if pagure_client is None:
        pagure_client = PagureClient()
    return pagure_client


@mcp.tool()
async def list_projects(
    namespace: str = "rpms",
    pattern: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """List Pagure projects/packages.

    Args:
        namespace: Project namespace (rpms, container, modules, etc.)
        pattern: Search pattern for project name
        page: Page number (default: 1)
        per_page: Results per page (default: 20)

    Returns:
        JSON string with project list and pagination info
    """
    client = get_client()
    result = await client.list_projects(namespace, pattern, page, per_page)

    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_project_info(
    project: str,
    namespace: str = "rpms",
) -> str:
    """Get detailed information about a Pagure project.

    Args:
        project: Project name (e.g., 'python3', 'kernel')
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with project details
    """
    client = get_client()
    result = await client.get_project(project, namespace)

    return result.model_dump_json(indent=2)


@mcp.tool()
async def fork_project(
    project: str,
    namespace: str = "rpms",
) -> str:
    """Fork a Pagure project to your namespace.

    Args:
        project: Project name to fork
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with fork creation result
    """
    client = get_client()
    result = await client.fork_project(project, namespace)

    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_file(
    project: str,
    filename: str,
    branch: str = "rawhide",
    namespace: str = "rpms",
) -> str:
    """Get file content from a Pagure repository.

    Args:
        project: Project name
        filename: File path (e.g., 'python3.spec', 'sources')
        branch: Branch name (default: rawhide)
        namespace: Project namespace (default: rpms)

    Returns:
        File content as string
    """
    client = get_client()
    content = await client.get_file(project, filename, branch, namespace)

    return content


@mcp.tool()
async def list_branches(
    project: str,
    namespace: str = "rpms",
) -> str:
    """List all branches in a Pagure repository.

    Args:
        project: Project name
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with list of branch names
    """
    client = get_client()
    branches = await client.list_branches(project, namespace)

    import json
    return json.dumps({"branches": branches}, indent=2)


@mcp.tool()
async def list_pull_requests(
    project: str,
    namespace: str = "rpms",
    status: str = "Open",
    page: int = 1,
    per_page: int = 20,
) -> str:
    """List pull requests for a Pagure project.

    Args:
        project: Project name
        namespace: Project namespace (default: rpms)
        status: PR status - Open, Merged, Closed, or all (default: Open)
        page: Page number (default: 1)
        per_page: Results per page (default: 20)

    Returns:
        JSON string with PR list and pagination info
    """
    client = get_client()
    result = await client.list_pull_requests(project, namespace, status, page, per_page)

    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_pull_request(
    project: str,
    pr_id: int,
    namespace: str = "rpms",
) -> str:
    """Get detailed information about a specific pull request.

    Args:
        project: Project name
        pr_id: Pull request ID number
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with PR details including comments
    """
    client = get_client()
    result = await client.get_pull_request(project, pr_id, namespace)

    return result.model_dump_json(indent=2)


@mcp.tool()
async def comment_on_pr(
    project: str,
    pr_id: int,
    comment: str,
    namespace: str = "rpms",
) -> str:
    """Add a comment to a pull request.

    Args:
        project: Project name
        pr_id: Pull request ID number
        comment: Comment text to add
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with comment creation result
    """
    client = get_client()
    result = await client.comment_on_pr(project, pr_id, comment, namespace)

    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def merge_pull_request(
    project: str,
    pr_id: int,
    namespace: str = "rpms",
) -> str:
    """Merge an approved pull request.

    Args:
        project: Project name
        pr_id: Pull request ID number to merge
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with merge result
    """
    client = get_client()
    result = await client.merge_pull_request(project, pr_id, namespace)

    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def close_pull_request(
    project: str,
    pr_id: int,
    namespace: str = "rpms",
) -> str:
    """Close a pull request without merging.

    Args:
        project: Project name
        pr_id: Pull request ID number to close
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with close result
    """
    client = get_client()
    result = await client.close_pull_request(project, pr_id, namespace)

    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_commit(
    project: str,
    commit_hash: str,
    namespace: str = "rpms",
) -> str:
    """Get detailed information about a specific commit.

    Args:
        project: Project name
        commit_hash: Commit hash (full or short)
        namespace: Project namespace (default: rpms)

    Returns:
        JSON string with commit details
    """
    client = get_client()
    result = await client.get_commit(project, commit_hash, namespace)

    import json
    return json.dumps(result, indent=2)


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Pagure MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to in HTTP mode (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8805,
        help="Port to bind to in HTTP mode (default: 8805)"
    )

    args = parser.parse_args()

    # Verify environment variables
    if not os.getenv("PAGURE_API_TOKEN"):
        print("Warning: PAGURE_API_TOKEN environment variable not set")
        print("Set it with: export PAGURE_API_TOKEN='your-token-here'")

    # Run the server
    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(transport="http", host=args.host, port=args.port, path="/mcp")


if __name__ == "__main__":
    main()
