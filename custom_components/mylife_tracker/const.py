"""Constants for the MyLife Tracker integration."""

DOMAIN = "mylife_tracker"

CONF_API_KEY = "api_key"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 300
MIN_SCAN_INTERVAL = 60

API_STATUS_PATH = "/api/ha/status"
API_PUSH_PATH = "/api/ha/push"

ATTR_EXPIRED_DOCS = "expired_docs"
ATTR_WARNING_DOCS = "warning_docs"
ATTR_UNPAID_BILLS = "unpaid_bills"
ATTR_UNPAID_EXTRA_COSTS = "unpaid_extra_costs"
ATTR_LAST_UPDATED = "last_updated"
ATTR_DOCS_BADGE_COUNT = "docs_badge_count"
ATTR_PAYMENTS_BADGE_COUNT = "payments_badge_count"
ATTR_HOUSEHOLD_LABELS = "household_labels"
ATTR_USER_LABELS = "user_labels"
ATTR_EDUCATION = "education"
ATTR_EDU_STUDENTS = "students"
ATTR_EDU_LAST_WEEK_GRADES = "last_week_grades"
ATTR_EDU_NEXT_WEEK_HOMEWORK = "next_week_homework"
ATTR_EDU_TIMETABLE_WEEK = "timetable_week"
ATTR_EDU_LAST_WEEK_RANGE = "last_week_range"
ATTR_EDU_NEXT_WEEK_RANGE = "next_week_range"
ATTR_EDU_TIMETABLE_WEEK_RANGE = "timetable_week_range"
ATTR_EDU_LAST_SYNC_AT = "last_sync_at"

SERVICE_REFRESH = "refresh"
