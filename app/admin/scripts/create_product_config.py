import numpy as np
import datetime
import json

STATES = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
]


def fn_benefit_amounts():
    minval = float(np.random.choice([0, 50, 100, 250, 500, 1000, 5000, 10000, 50000]))
    maxval = 2 * minval
    stepval = 25
    if minval == 0:
        maxval = 1000

    defaultval = minval + maxval / 2
    return {
        "min_value": minval,
        "max_value": maxval,
        "step_value": stepval,
        "default_value": defaultval,
    }


def fn_benefit_durations():
    return [
        {
            "config_benefit_duration_set_code": "annual_payments",
            "config_benefit_duration_set_label": "Number of Payments per Year",
            "duration_items": [
                {
                    "config_benefit_duration_detail_code": f"{i+1}",
                    "config_benefit_duration_detail_label": f"{i+1} / year",
                    "config_benefit_duration_factor": round(
                        np.random.normal(0.7 + i / 10, 0.03), 5
                    ),
                    "acl": [
                        {"auth_role_code": "uw800"},
                        {"auth_role_code": "uw900"},
                        {"auth_role_code": "uw1000"},
                    ],
                }
                for i in range(5)
            ],
        }
    ]


def fn_states(key_prefix):
    return [
        {
            f"{key_prefix}_state_code": state,
            f"{key_prefix}_state_effective_date": str(datetime.date(2022, 1, 1)),
            f"{key_prefix}_state_expiration_date": str(datetime.date(9999, 12, 31)),
        }
        for state in STATES
    ]


def fn_rate_tables(n=500):
    return [
        {
            "config_rate_table_set_label": "Standard Rates",
            "config_benefit_code": f"bnft{i:03}",
            "rating_mapper_collection_label1": "Standard Relationship Mappers",
            "rates": [
                {
                    "rating_attr_code1": "EE",
                    "rate_per_unit": round(np.random.normal(150, 10), 4),
                    "rate_frequency_code": "1pp",
                    "rate_unit_value": 100,
                },
                {
                    "rating_attr_code1": "SP",
                    "rate_per_unit": round(np.random.normal(100, 10), 4),
                    "rate_frequency_code": "1pp",
                    "rate_unit_value": 100,
                },
                {
                    "rating_attr_code1": "CH",
                    "rate_per_unit": round(np.random.normal(150, 20), 4),
                    "rate_frequency_code": "1pp",
                    "rate_unit_value": 100,
                },
            ],
        }
        for i in range(n)
    ]


def fn_factors(data_type):
    if data_type == "number":
        return [
            {
                "factor_priority": 1,
                "factor_rules": [
                    {
                        "comparison_attr_name": "selection_value",
                        "comparison_operator_symbol": "<",
                        "comparison_attr_value": "1000",
                        "comparison_attr_data_type_code": data_type,
                    },
                ],
                "factor_values": [
                    {"factor_value": round(np.random.normal(1, 0.05), 3)}
                ],
            },
            {
                "factor_priority": 2,
                "vary_by_rating_attr1": True,
                "factor_rules": [
                    {
                        "comparison_attr_name": "selection_value",
                        "comparison_operator_symbol": ">=",
                        "comparison_attr_value": "1000",
                        "comparison_attr_data_type_code": data_type,
                    },
                    {
                        "comparison_attr_name": "selection_value",
                        "comparison_operator_symbol": "<",
                        "comparison_attr_value": "5000",
                        "comparison_attr_data_type_code": data_type,
                    },
                ],
                "factor_values": [
                    {
                        "rating_attr_code1": "EE",
                        "factor_value": round(np.random.normal(1, 0.05), 3),
                    },
                    {
                        "rating_attr_code1": "SP",
                        "factor_value": round(np.random.normal(1, 0.05), 3),
                    },
                    {
                        "rating_attr_code1": "CH",
                        "factor_value": round(np.random.normal(1, 0.05), 3),
                    },
                ],
            },
        ]
    elif data_type == "string":
        return [
            {
                "factor_priority": 1,
                "factor_rules": [
                    {
                        "comparison_attr_name": "selection_value",
                        "comparison_operator_symbol": "=",
                        "comparison_attr_value": "A",
                        "comparison_attr_data_type_code": data_type,
                    },
                ],
                "factor_values": [
                    {"factor_value": round(np.random.normal(1, 0.05), 3)}
                ],
            },
            {
                "factor_priority": 2,
                "vary_by_rating_attr1": True,
                "factor_rules": [
                    {
                        "comparison_attr_name": "selection_value",
                        "comparison_operator_symbol": "=",
                        "comparison_attr_value": "B",
                        "comparison_attr_data_type_code": data_type,
                    },
                ],
                "factor_values": [
                    {
                        "rating_attr_code1": "EE",
                        "factor_value": round(np.random.normal(1, 0.05), 3),
                    },
                    {
                        "rating_attr_code1": "SP",
                        "factor_value": round(np.random.normal(1, 0.05), 3),
                    },
                    {
                        "rating_attr_code1": "CH",
                        "factor_value": round(np.random.normal(1, 0.05), 3),
                    },
                ],
            },
        ]
    return [
        {
            "factor_priority": 1,
            "factor_rules": [
                {
                    "comparison_attr_name": "selection_value",
                    "comparison_operator_symbol": "=",
                    "comparison_attr_value": "true",
                    "comparison_attr_data_type_code": data_type,
                },
            ],
            "factor_values": [{"factor_value": round(np.random.normal(1, 0.05), 3)}],
        },
    ]


def fn_provision_single(i):
    data_type = np.random.choice(["number", "string", "boolean"], p=[0.7, 0.2, 0.1])
    return {
        "config_provision_code": f"prov{i:03}",
        "config_provision_label": f"Provision {i:03}",
        "config_provision_data_type_code": data_type,
        "config_provision_description": f"Provision {i:03}",
        "states": fn_states("config_provision"),
        "factors": fn_factors(data_type),
        "benefit_provisions": {
            "exclude": [f"bnft{j:03}" for j in range(500) if (j + 1) % (75 + i) == 0]
        },
    }


def fn_benefit_variation_states():
    return [
        {
            "config_benefit_variation_state_code": state,
            "config_benefit_variation_state_effective_date": str(
                datetime.date(2022, 1, 1)
            ),
            "config_benefit_variation_state_expiration_date": str(
                datetime.date(9999, 12, 31)
            ),
            "config_rate_table_set_label": "Standard Rates",
        }
        for state in STATES
    ]


def fn_benefit_variations(product_variation_code: str, n=500):
    return [
        {
            "config_benefit_code": f"bnft{i:03}",
            "config_product_variation_code": product_variation_code,
            "states": fn_benefit_variation_states(),
        }
        for i in range(n)
    ]


def fn_benefits(n=500):
    return [
        {
            "config_benefit_code": f"bnft{i:03}",
            "config_benefit_label": f"Benefit {i:03}",
            "config_rate_group_code": "FLAT",
            "benefit_auth": [
                {
                    "priority": (i_auth + 1) * 10,
                    **fn_benefit_amounts(),
                    "acl": [{"auth_role_code": f"uw{(i_auth + 8) * 100}"}],
                }
                for i_auth in range(3)
            ],
            "unit_type_code": "dollars",
            "config_benefit_description": f"Benefit {i:03}",
            "duration_sets": fn_benefit_durations() if (i + 1) % 9 == 0 else [],
        }
        for i in range(n)
    ]


def fn_provisions(n=20):
    return [fn_provision_single(i) for i in range(n)]


def fn_product_variations():
    return [
        {
            "config_product_variation_code": "base",
            "config_product_variation_label": "Base Accident",
            "states": fn_states("config_product_variation"),
        }
    ]


def fn_rate_groups():
    return [
        {
            "config_rate_group_code": "APU",
            "config_rate_group_label": "Annual Rate per $1000",
            "unit_value": 1000,
            "apply_discretionary_factor": True,
        },
        {
            "config_rate_group_code": "FLAT",
            "config_rate_group_label": "Flat Rate",
            "unit_value": 1,
            "apply_discretionary_factor": False,
        },
    ]


def fn_product():
    n_benefits = 500
    return {
        "config_product_code": "AC70000",
        "config_product_label": "Accident Series 70000",
        "config_product_effective_date": "2022-01-01",
        "config_product_expiration_date": "9999-12-31",
        "product_issue_date": "2021-01-01",
        "master_product_code": "AC",
        "form_code": "70000",
        "age_rating_strategy_code": "none",
        "age_distribution_set_label": None,
        "rating_mapper_collection_label1": "Standard Relationship Mappers",
        "rating_mapper_collection_label2": None,
        "rating_mapper_collection_label3": None,
        "rating_mapper_collection_label4": None,
        "rating_mapper_collection_label5": None,
        "rating_mapper_collection_label6": None,
        "allow_employer_paid": True,
        "voluntary_census_strategy_code": "required",
        "employer_paid_census_strategy_code": "required",
        "states": fn_states("config_product"),
        "product_variations": fn_product_variations(),
        "rate_groups": fn_rate_groups(),
        "benefits": fn_benefits(n=n_benefits),
        "provisions": fn_provisions(),
        "rate_tables": fn_rate_tables(n=n_benefits),
        "benefit_variations": fn_benefit_variations("base", n=n_benefits),
    }


if __name__ == "__main__":
    data = fn_product()
    with open("work/product_config.json", "w") as f:
        json.dump(data, f)
