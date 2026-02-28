from enum import Enum
from .permission_enum import EPermission


class Role(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EVENT_MANAGER = "event_manager"
    ANALYTICS = "analytics"
    VIEWER = "viewer"


ROLE_PERMISSIONS: dict[Role, set[EPermission]] = {
    Role.OWNER: set(EPermission),  # повний доступ до всього

    Role.ADMIN: {
        # Workspace
        EPermission.WORKSPACE_API_KEY_MANAGE,

        # Members
        EPermission.MEMBER_INVITE,
        EPermission.MEMBER_REMOVE,
        EPermission.MEMBER_ROLE_CHANGE,
        EPermission.MEMBER_VIEW,

        # Event Schemas
        EPermission.SCHEMA_CREATE,
        EPermission.SCHEMA_EDIT,
        EPermission.SCHEMA_DELETE,
        EPermission.SCHEMA_READ,

        # Pipelines
        EPermission.PIPELINE_CREATE,
        EPermission.PIPELINE_EDIT,
        EPermission.PIPELINE_DELETE,
        EPermission.PIPELINE_READ,

        # Dashboards
        EPermission.DASHBOARD_CREATE,
        EPermission.DASHBOARD_EDIT_OWN,
        EPermission.DASHBOARD_EDIT_ANY,
        EPermission.DASHBOARD_DELETE_OWN,
        EPermission.DASHBOARD_DELETE_ANY,
        EPermission.DASHBOARD_READ,
        EPermission.DASHBOARD_SHARE,

        # Widgets
        EPermission.WIDGET_CREATE,
        EPermission.WIDGET_EDIT,
        EPermission.WIDGET_DELETE,

        # Analytics / Data
        EPermission.ANALYTICS_QUERY,
        EPermission.ANALYTICS_EXPORT,

        # Annotations
        EPermission.ANNOTATION_CREATE,
        EPermission.ANNOTATION_DELETE_OWN,
        EPermission.ANNOTATION_DELETE_ANY,

        # Event Inspector
        EPermission.INSPECTOR_READ,
    },

    Role.EVENT_MANAGER: {
        # Members
        EPermission.MEMBER_INVITE,
        EPermission.MEMBER_REMOVE,
        EPermission.MEMBER_ROLE_CHANGE,
        EPermission.MEMBER_VIEW,

        # Event Schemas
        EPermission.SCHEMA_CREATE,
        EPermission.SCHEMA_EDIT,
        EPermission.SCHEMA_DELETE,
        EPermission.SCHEMA_READ,

        # Pipelines
        EPermission.PIPELINE_CREATE,
        EPermission.PIPELINE_EDIT,
        EPermission.PIPELINE_DELETE,
        EPermission.PIPELINE_READ,
    },

    Role.ANALYTICS: {
        # Analytics / Data
        EPermission.ANALYTICS_QUERY,
        EPermission.ANALYTICS_EXPORT,

        # Dashboards
        EPermission.DASHBOARD_READ,
        EPermission.DASHBOARD_CREATE,
        EPermission.DASHBOARD_EDIT_OWN,
        EPermission.DASHBOARD_DELETE_OWN,
        EPermission.DASHBOARD_SHARE,

        # Widgets
        EPermission.WIDGET_CREATE,
        EPermission.WIDGET_EDIT,
        EPermission.WIDGET_DELETE,

        # Annotations
        EPermission.ANNOTATION_CREATE,
        EPermission.ANNOTATION_DELETE_OWN,

        # Event Inspector
        EPermission.INSPECTOR_READ,
    },

    Role.VIEWER: {
        EPermission.MEMBER_VIEW,
        EPermission.SCHEMA_READ,
        EPermission.PIPELINE_READ,
        EPermission.DASHBOARD_READ,
        EPermission.ANALYTICS_QUERY,
        EPermission.INSPECTOR_READ,
    },
}
