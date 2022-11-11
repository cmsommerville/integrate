from app.auth import ResourcePermissions
from app.auth.tables import TBL_NAMES as AUTH_TBL_NAMES
from app.auth.tables import SCHEMA_NAME as AUTH_SCHEMA_NAME

AUTH_TBL_NAMES = {key: f"{AUTH_SCHEMA_NAME}.{tbl}" for key, tbl in AUTH_TBL_NAMES.items()}

API_ROLE_SUPERUSER = ResourcePermissions(
    get=['superuser'], post=['superuser'], 
    patch=['superuser'], put=['superuser'], delete=['superuser']
)