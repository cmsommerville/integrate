from . import crud
from .dropdowns import ns_dd
from .getters import ns_getters
from .diagnostics import ns_diagnostics

NAMESPACES = [
    {"namespace": crud.ns_ref, "path": "/ref"},
    {"namespace": crud.ns_base, "path": "/config"},
    {"namespace": crud.ns_product, "path": "/config/product/<int:parent_id>"},
    {"namespace": crud.ns_benefit, "path": "/config/benefit/<int:parent_id>"},
    {
        "namespace": crud.ns_benefit_duration,
        "path": "/config/bnftdur/<int:benefit_duration_set_id>",
    },
    {"namespace": crud.ns_coverage, "path": "/config/coverage/<int:parent_id>"},
    {"namespace": crud.ns_plan_design, "path": "/config/design/<int:parent_id>"},
    {"namespace": crud.ns_provision, "path": "/config/provision/<int:parent_id>"},
    {"namespace": crud.ns_variation, "path": "/config/variation/<int:parent_id>"},
    {
        "namespace": crud.ns_variation_state,
        "path": "/config/varstate/<int:parent_id>",
    },
    {"namespace": crud.ns_selection_base, "path": "/selection"},
    {
        "namespace": crud.ns_selection_benefit,
        "path": "/selection/benefit/<int:parent_id>",
    },
    {"namespace": crud.ns_selection_plan, "path": "/selection/plan/<int:parent_id>"},
    {"namespace": ns_dd, "path": "/dd"},
    {"namespace": ns_getters, "path": "/data"},
    {"namespace": ns_diagnostics, "path": "/diag"},
]
