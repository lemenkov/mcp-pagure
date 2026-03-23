"""Pagure API client."""

import os
from typing import Optional, List, Dict, Any
import httpx
from .models import PagureProject, PagurePullRequest, PagureCommit


class PagureClient:
    """Client for interacting with Pagure API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        """Initialize Pagure client.

        Args:
            base_url: Pagure instance URL (default: https://src.fedoraproject.org)
            api_token: Pagure API token (from env PAGURE_API_TOKEN if not provided)
        """
        self.base_url = (base_url or os.getenv("PAGURE_BASE_URL",
                         "https://src.fedoraproject.org")).rstrip("/")
        self.api_token = api_token or os.getenv("PAGURE_API_TOKEN")
        self.api_base = f"{self.base_url}/api/0"

        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"token {self.api_token}"
        return headers

    async def list_projects(
        self,
        namespace: Optional[str] = "rpms",
        pattern: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """List projects/packages.

        Args:
            namespace: Project namespace (rpms, container, modules, etc.)
            pattern: Search pattern for project name
            page: Page number
            per_page: Results per page

        Returns:
            Dict with projects list and pagination info
        """
        params = {
            "namespace": namespace,
            "page": page,
            "per_page": per_page,
        }
        if pattern:
            params["pattern"] = pattern

        response = await self.client.get(
            f"{self.api_base}/projects",
            params=params,
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_project(
        self,
        project: str,
        namespace: str = "rpms",
    ) -> PagureProject:
        """Get project information.

        Args:
            project: Project name
            namespace: Project namespace

        Returns:
            PagureProject model
        """
        response = await self.client.get(
            f"{self.api_base}/{namespace}/{project}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        data = response.json()
        return PagureProject(**data)

    async def fork_project(
        self,
        project: str,
        namespace: str = "rpms",
    ) -> Dict[str, Any]:
        """Fork a project to your namespace.

        Args:
            project: Project name
            namespace: Project namespace

        Returns:
            Fork creation result
        """
        response = await self.client.post(
            f"{self.api_base}/fork",
            json={"repo": project, "namespace": namespace},
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_file(
        self,
        project: str,
        filename: str,
        branch: str = "rawhide",
        namespace: str = "rpms",
    ) -> str:
        """Get file content from repository.

        Args:
            project: Project name
            filename: File path
            branch: Branch name
            namespace: Project namespace

        Returns:
            File content as string
        """
        response = await self.client.get(
            f"{self.base_url}/{namespace}/{project}/raw/{branch}/f/{filename}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.text

    async def list_branches(
        self,
        project: str,
        namespace: str = "rpms",
    ) -> List[str]:
        """List repository branches.

        Args:
            project: Project name
            namespace: Project namespace

        Returns:
            List of branch names
        """
        response = await self.client.get(
            f"{self.api_base}/{namespace}/{project}/git/branches",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        data = response.json()
        return data.get("branches", [])

    async def list_pull_requests(
        self,
        project: str,
        namespace: str = "rpms",
        status: str = "Open",
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """List pull requests.

        Args:
            project: Project name
            namespace: Project namespace
            status: PR status (Open, Merged, Closed, all)
            page: Page number
            per_page: Results per page

        Returns:
            Dict with PRs and pagination info
        """
        params = {
            "status": status,
            "page": page,
            "per_page": per_page,
        }

        response = await self.client.get(
            f"{self.api_base}/{namespace}/{project}/pull-requests",
            params=params,
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_pull_request(
        self,
        project: str,
        pr_id: int,
        namespace: str = "rpms",
    ) -> PagurePullRequest:
        """Get pull request details.

        Args:
            project: Project name
            pr_id: Pull request ID
            namespace: Project namespace

        Returns:
            PagurePullRequest model
        """
        response = await self.client.get(
            f"{self.api_base}/{namespace}/{project}/pull-request/{pr_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        data = response.json()
        return PagurePullRequest(**data)

    async def comment_on_pr(
        self,
        project: str,
        pr_id: int,
        comment: str,
        namespace: str = "rpms",
    ) -> Dict[str, Any]:
        """Add a comment to a pull request.

        Args:
            project: Project name
            pr_id: Pull request ID
            comment: Comment text
            namespace: Project namespace

        Returns:
            Comment creation result
        """
        response = await self.client.post(
            f"{self.api_base}/{namespace}/{project}/pull-request/{pr_id}/comment",
            json={"comment": comment},
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def merge_pull_request(
        self,
        project: str,
        pr_id: int,
        namespace: str = "rpms",
    ) -> Dict[str, Any]:
        """Merge a pull request.

        Args:
            project: Project name
            pr_id: Pull request ID
            namespace: Project namespace

        Returns:
            Merge result
        """
        response = await self.client.post(
            f"{self.api_base}/{namespace}/{project}/pull-request/{pr_id}/merge",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def close_pull_request(
        self,
        project: str,
        pr_id: int,
        namespace: str = "rpms",
    ) -> Dict[str, Any]:
        """Close a pull request without merging.

        Args:
            project: Project name
            pr_id: Pull request ID
            namespace: Project namespace

        Returns:
            Close result
        """
        response = await self.client.post(
            f"{self.api_base}/{namespace}/{project}/pull-request/{pr_id}/close",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_commit(
        self,
        project: str,
        commit_hash: str,
        namespace: str = "rpms",
    ) -> Dict[str, Any]:
        """Get commit details.

        Args:
            project: Project name
            commit_hash: Commit hash
            namespace: Project namespace

        Returns:
            Commit details
        """
        response = await self.client.get(
            f"{self.api_base}/{namespace}/{project}/c/{commit_hash}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()
