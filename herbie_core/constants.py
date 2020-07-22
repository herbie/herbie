class StatusConstants:
    STATUS = "status"
    STATUS_OK = "ok"
    STATUS_ERROR = "error"


class ValidatorResponseConstants:
    RESPONSE_KEY = "response"
    ERROR_MESSAGE = "error_message"
    VALIDATE_KEY = "validation_error"
    REQUIRED_KEY = "required"
    ADDITIONAL_PROPERTIES = "additionalProperties"


class ControllerConstants:
    DELETE_ALL_VERSIONS_MESSAGE = "entity with key {} deleted from all versions"
    DELETE_ALL_VERSIONS_MESSAGE_NOT_FOUND = "entity with key {} not found"
    DELETE_FROM_VERSION_MESSAGE = "entity with key {} deleted from version {}"
    DELETE_FROM_VERSION_MESSAGE_NOT_FOUND = "entity with key {} and version {} not found"
    SAVE_MESSAGE = "entity with key {} created in version {}"
    UPDATE_MESSAGE = "entity with key {} updated in version {}"
    BUSINESS_ENTITY_NOT_EXIST = "business entity {} does not exist"
    VERSION_NOT_EXIST = "version {} does not exist"
    VERSION_MISSING = "Version is missing"
    KEY = "key"
    PAYLOAD = "payload"
    VERSION = "version"
    UNAUTHORIZED = "unauthorized"
    DELETE = "delete"
    ADD = "add"
    CHANGE = "change"
    VIEW = "view"


class CommandsConstants:
    FIRST_PAGE = 1
    BUSINESS_ENTITY = "business_entity"
    CHUNK_SIZE = "chunk_size"
    FULL_EXPORT = "full_export"


class GroupConstants:
    BUSINESS_ENTITIES_VIEW_GROUP = "business_entities_view_group"


class MessageActionConstants:
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
