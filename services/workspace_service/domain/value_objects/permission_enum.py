from enum import Enum

class EPermission(str, Enum):
    # Workspace
    WORKSPACE_EDIT = "workspace:edit"
    WORKSPACE_DELETE = "workspace:delete"
    WORKSPACE_API_KEY_MANAGE = "workspace:api_key_manage"

    # Members
    MEMBER_INVITE = "member:invite"
    MEMBER_REMOVE = "member:remove"
    MEMBER_ROLE_CHANGE = "member:role_change"
    MEMBER_VIEW = "member:view"

    # Event Schemas
    SCHEMA_CREATE = "schema:create"
    SCHEMA_EDIT = "schema:edit"
    SCHEMA_DELETE = "schema:delete"
    SCHEMA_READ = "schema:read"

    # Pipelines
    PIPELINE_CREATE = "pipeline:create"
    PIPELINE_EDIT = "pipeline:edit"
    PIPELINE_DELETE = "pipeline:delete"
    PIPELINE_READ = "pipeline:read"

    # Dashboards
    DASHBOARD_CREATE = "dashboard:create"
    DASHBOARD_EDIT_OWN = "dashboard:edit_own"
    DASHBOARD_EDIT_ANY = "dashboard:edit_any"
    DASHBOARD_DELETE_OWN = "dashboard:delete_own"
    DASHBOARD_DELETE_ANY = "dashboard:delete_any"
    DASHBOARD_READ = "dashboard:read"
    DASHBOARD_SHARE = "dashboard:share"

    # Widgets
    WIDGET_CREATE = "widget:create"
    WIDGET_EDIT = "widget:edit"
    WIDGET_DELETE = "widget:delete"

    # Analytics / Data
    ANALYTICS_QUERY = "analytics:query"
    ANALYTICS_EXPORT = "analytics:export"

    # Annotations
    ANNOTATION_CREATE = "annotation:create"
    ANNOTATION_DELETE_OWN = "annotation:delete_own"
    ANNOTATION_DELETE_ANY = "annotation:delete_any"

    # Event Inspector
    INSPECTOR_READ = "inspector:read"
