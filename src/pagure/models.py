"""Pydantic models for Pagure API responses."""

from typing import Optional, List
from pydantic import BaseModel, Field


class PagureUser(BaseModel):
    """Pagure user model."""
    name: str
    fullname: Optional[str] = None
    url_path: Optional[str] = None


class PagureProject(BaseModel):
    """Pagure project model."""
    id: int
    name: str
    namespace: Optional[str] = None
    description: Optional[str] = None
    fullname: str
    url_path: str
    access_users: dict = Field(default_factory=dict)
    access_groups: dict = Field(default_factory=dict)
    date_created: Optional[str] = None
    date_modified: Optional[str] = None


class PagurePullRequest(BaseModel):
    """Pagure pull request model."""
    id: int
    uid: str
    title: str
    status: str  # Open, Merged, Closed
    branch: str
    branch_from: str
    project: dict
    repo_from: Optional[dict] = None
    user: dict
    assignee: Optional[dict] = None
    date_created: str
    updated_on: str
    commit_start: Optional[str] = None
    commit_stop: Optional[str] = None
    comments: List[dict] = Field(default_factory=list)


class PagureCommit(BaseModel):
    """Pagure commit model."""
    hash: str
    author: str
    committer: str
    commit_time: int
    message: str
    parents: List[str] = Field(default_factory=list)
