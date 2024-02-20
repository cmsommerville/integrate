from .crud import (
    ns_crud,
    ns_crud_benefit,
    ns_crud_product,
    ns_crud_provision,
    ns_ref,
    ns_selection,
)
from .dropdowns import ns_dd
from .getters import ns_getters

NAMESPACES = [
    {"namespace": ns_ref, "path": "/ref"},
    {"namespace": ns_crud, "path": "/config"},
    {"namespace": ns_crud_product, "path": "/config/product/<int:product_id>"},
    {"namespace": ns_crud_benefit, "path": "/config/benefit/<int:benefit_id>"},
    {"namespace": ns_crud_provision, "path": "/config/provision/<int:provision_id>"},
    {"namespace": ns_selection, "path": "/selection"},
    {"namespace": ns_dd, "path": "/dd"},
    {"namespace": ns_getters, "path": "/data"},
]
