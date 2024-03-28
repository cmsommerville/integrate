from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ACLSchema(Schema):
    auth_role_code = fields.Str(validate=validate.Length(max=30))


class ProductStateSchema(Schema):
    config_product_state_code = fields.Str(validate=validate.Length(equal=2))
    config_product_state_effective_date = fields.Str()
    config_product_state_expiration_date = fields.Str()


class ProductVariationStateSchema(Schema):
    config_product_variation_state_code = fields.Str(validate=validate.Length(equal=2))
    config_product_variation_state_effective_date = fields.Str()
    config_product_variation_state_expiration_date = fields.Str()
    default_config_age_band_set_label = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )


class BenefitVariationStateSchema(Schema):
    config_benefit_variation_state_code = fields.Str(validate=validate.Length(equal=2))
    config_rate_table_set_label = fields.Str(validate=validate.Length(max=100))
    config_benefit_variation_state_effective_date = fields.Str()
    config_benefit_variation_state_expiration_date = fields.Str()


class BenefitVariationSchema(Schema):
    config_benefit_code = fields.Str(validate=validate.Length(max=30))
    config_product_variation_code = fields.Str(validate=validate.Length(max=30))
    states = fields.Nested(BenefitVariationStateSchema, many=True)


class ProvisionStateSchema(Schema):
    config_provision_state_code = fields.Str(validate=validate.Length(equal=2))
    config_provision_state_effective_date = fields.Str()
    config_provision_state_expiration_date = fields.Str()


class ProductVariationSchema(Schema):
    config_product_variation_code = fields.Str(validate=validate.Length(max=30))
    config_product_variation_label = fields.Str(validate=validate.Length(max=100))
    states = fields.Nested(ProductVariationStateSchema, many=True)


class RateGroupSchema(Schema):
    config_rate_group_code = fields.Str(validate=validate.Length(max=30))
    config_rate_group_label = fields.Str(validate=validate.Length(max=100))
    unit_value = fields.Float()
    apply_discretionary_factor = fields.Bool()


class RateTableDetailSchema(Schema):
    rating_attr_code1 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code2 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code3 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code4 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code5 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code6 = fields.Str(validate=validate.Length(max=30), required=False)
    rate_per_unit = fields.Float()
    rate_frequency_code = fields.Str(validate=validate.Length(max=30))
    rate_unit_value = fields.Float()


class RateTableSetSchema(Schema):
    config_benefit_code = fields.Str(validate=validate.Length(max=30))
    config_rate_table_set_label = fields.Str(validate=validate.Length(max=100))
    rating_mapper_collection_label1 = fields.Str(
        validate=validate.Length(max=100), required=False
    )
    rating_mapper_collection_label2 = fields.Str(
        validate=validate.Length(max=100), required=False
    )
    rating_mapper_collection_label3 = fields.Str(
        validate=validate.Length(max=100), required=False
    )
    rating_mapper_collection_label4 = fields.Str(
        validate=validate.Length(max=100), required=False
    )
    rating_mapper_collection_label5 = fields.Str(
        validate=validate.Length(max=100), required=False
    )
    rating_mapper_collection_label6 = fields.Str(
        validate=validate.Length(max=100), required=False
    )
    rates = fields.Nested(RateTableDetailSchema, many=True)

    @validates_schema
    def validate_set_and_detail(self, data, **kwargs):
        """
        Validate that if the rate table set varies by a rating mapper collection,
        then rates must be specified for that attribute.
        """
        for i in range(1, 7):
            if data.get(f"rating_mapper_collection_label{i}") is not None:
                detail_contains_code = all(
                    [
                        rate.get(f"rating_attr_code{i}") is not None
                        for rate in data["rates"]
                    ]
                )
                if not detail_contains_code:
                    raise ValidationError(
                        f"Rate table set varies by attribute {i}, but no rate table details available by attribute {i}."
                    )


class BenefitDurationDetailSchema(Schema):
    config_benefit_duration_detail_code = fields.Str(validate=validate.Length(max=30))
    config_benefit_duration_detail_label = fields.Str(validate=validate.Length(max=100))
    config_benefit_duration_factor = fields.Float()
    is_restricted = fields.Bool(default=False)
    acl = fields.Nested(ACLSchema, many=True)


class BenefitDurationSetSchema(Schema):
    config_benefit_duration_set_code = fields.Str(validate=validate.Length(max=30))
    config_benefit_duration_set_label = fields.Str(validate=validate.Length(max=100))
    duration_items = fields.Nested(BenefitDurationDetailSchema, many=True)


class BenefitAuthSchema(Schema):
    priority = fields.Int()
    min_value = fields.Float()
    max_value = fields.Float()
    step_value = fields.Float()
    default_value = fields.Float()
    acl = fields.Nested(ACLSchema, many=True)


class BenefitSchema(Schema):
    config_benefit_code = fields.Str(validate=validate.Length(max=30))
    config_coverage_code = fields.Str(validate=validate.Length(max=30))
    config_benefit_label = fields.Str(validate=validate.Length(max=100))
    config_rate_group_code = fields.Str(validate=validate.Length(max=30))
    unit_type_code = fields.Str(validate=validate.Length(max=30))
    config_benefit_description = fields.Str(validate=validate.Length(max=1000))
    duration_sets = fields.Nested(BenefitDurationSetSchema, many=True, allow_none=True)
    benefit_auth = fields.Nested(BenefitAuthSchema, many=True)


class BenefitProvisionSchema(Schema):
    exclude = fields.List(fields.Str())


class FactorRuleSchema(Schema):
    comparison_attr_name = fields.Str(validate=validate.Length(max=300))
    comparison_operator_symbol = fields.Str(validate=validate.Length(max=30))
    comparison_attr_value = fields.Str(validate=validate.Length(max=100))
    comparison_attr_data_type_code = fields.Str(validate=validate.Length(max=30))


class FactorValueSchema(Schema):
    rating_attr_code1 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code2 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code3 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code4 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code5 = fields.Str(validate=validate.Length(max=30), required=False)
    rating_attr_code6 = fields.Str(validate=validate.Length(max=30), required=False)
    factor_value = fields.Float()


class FactorSetSchema(Schema):
    factor_priority = fields.Int()
    vary_by_rating_attr1 = fields.Bool(required=False)
    vary_by_rating_attr2 = fields.Bool(required=False)
    vary_by_rating_attr3 = fields.Bool(required=False)
    vary_by_rating_attr4 = fields.Bool(required=False)
    vary_by_rating_attr5 = fields.Bool(required=False)
    vary_by_rating_attr6 = fields.Bool(required=False)
    factor_rules = fields.Nested(FactorRuleSchema, many=True)
    factor_values = fields.Nested(FactorValueSchema, many=True)

    @validates_schema
    def validate_rating_attrs(self, data, **kwargs):
        """
        Validate that the vary_by flags and the factor value rating attributes are consistent with one another.
        """
        for i in range(1, 7):
            vary_by_attr = data.get(f"vary_by_rating_attr{i}", False)
            values_vary = all(
                [
                    val.get(f"rating_attr_code{i}") is not None
                    for val in data["factor_values"]
                ]
            )

            if vary_by_attr and not values_vary:
                raise ValidationError(
                    f"Factor set varies by rating attribute {i}, but factor values do not."
                )

            if not vary_by_attr and values_vary:
                raise ValidationError(
                    f"Factor set does not vary by rating attribute {i}, but factor values do."
                )


class CoverageSchema(Schema):
    config_coverage_code = fields.Str(validate=validate.Length(max=30))
    config_coverage_label = fields.Str(validate=validate.Length(max=100))
    config_coverage_description = fields.Str(validate=validate.Length(max=1000))


class ProvisionSchema(Schema):
    config_provision_code = fields.Str(validate=validate.Length(max=30))
    config_provision_label = fields.Str(validate=validate.Length(max=100))
    config_provision_data_type_code = fields.Str(validate=validate.Length(max=30))
    config_dropdown_set_label = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )
    config_provision_description = fields.Str(validate=validate.Length(max=1000))
    states = fields.Nested(ProvisionStateSchema, many=True)
    factors = fields.Nested(FactorSetSchema, many=True)
    benefit_provisions = fields.Nested(BenefitProvisionSchema)


class ProductLoaderSchema(Schema):
    config_product_code = fields.Str(validate=validate.Length(max=30))
    config_product_label = fields.Str(validate=validate.Length(max=100))
    config_product_effective_date = fields.Str()
    config_product_expiration_date = fields.Str()
    product_issue_date = fields.Str()
    master_product_code = fields.Str(validate=validate.Length(max=30))
    form_code = fields.Str(validate=validate.Length(max=30))
    age_rating_strategy_code = fields.Str(validate=validate.Length(max=30))
    age_distribution_set_label = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    rating_mapper_collection_label1 = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    rating_mapper_collection_label2 = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    rating_mapper_collection_label3 = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    rating_mapper_collection_label4 = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    rating_mapper_collection_label5 = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    rating_mapper_collection_label6 = fields.Str(
        validate=validate.Length(max=100), allow_none=True, required=False
    )
    allow_employer_paid = fields.Bool()
    voluntary_census_strategy_code = fields.Str(validate=validate.Length(max=30))
    employer_paid_census_strategy_code = fields.Str(validate=validate.Length(max=30))
    states = fields.Nested(ProductStateSchema, many=True)
    rate_groups = fields.Nested(RateGroupSchema, many=True)
    product_variations = fields.Nested(ProductVariationSchema, many=True)
    coverages = fields.Nested(CoverageSchema, many=True)
    benefits = fields.Nested(BenefitSchema, many=True)
    provisions = fields.Nested(ProvisionSchema, many=True)
    rate_tables = fields.Nested(RateTableSetSchema, many=True)
    benefit_variations = fields.Nested(BenefitVariationSchema, many=True)

    @validates_schema
    def validate_rate_groups(self, data, **kwargs):
        """
        Validate that if the rate groups assigned to each benefit are defined on the product
        """
        configured_rate_groups = [
            rg["config_rate_group_code"] for rg in data["rate_groups"]
        ]
        benefit_rate_groups_valid = all(
            [
                b["config_rate_group_code"] in configured_rate_groups
                for b in data["benefits"]
            ]
        )
        if not benefit_rate_groups_valid:
            raise ValidationError(
                "Cannot configure rate groups on benefits unless those rate groups are defined on the product"
            )

    @validates_schema
    def validate_rating_mappers(self, data, **kwargs):
        """
        Validate that the product's rating mappers are consistent with the benefit rate tables and factor sets.
        """
        for i in range(1, 7):
            product_vary_by_mapper = (
                data.get(f"rating_mapper_collection_label{i}") is not None
            )
            if product_vary_by_mapper:
                # ensure that all rate tables vary by this mapper
                rate_tables_vary_by_mapper = all(
                    [
                        rt.get(f"rating_mapper_collection_label{i}") is not None
                        for rt in data["rate_tables"]
                    ]
                )
                if not rate_tables_vary_by_mapper:
                    raise ValidationError(
                        f"Invalid configuration. Product varies by rating mapper collection {i}, but rate tables do not."
                    )
            else:
                # ensure that none of the factors vary by this mapper
                factor_sets_vary_by_mapper = any(
                    [
                        any(
                            [
                                fs.get(f"vary_by_rating_attr{i}") is not None
                                for fs in p["factors"]
                            ]
                        )
                        for p in data["provisions"]
                    ]
                )
                if factor_sets_vary_by_mapper:
                    raise ValidationError(
                        f"Invalid configuration. Product does not vary by rating mapper collection {i}, but factor sets do."
                    )

    @validates_schema
    def validate_rate_tables(self, data, **kwargs):
        """
        Validate that if the rate tables have valid benefit definitions
        """
        configured_benefit_codes = [b["config_benefit_code"] for b in data["benefits"]]

        all_valid_rate_table_benefit_codes = all(
            [
                rt["config_benefit_code"] in configured_benefit_codes
                for rt in data["rate_tables"]
            ]
        )
        if not all_valid_rate_table_benefit_codes:
            raise ValidationError(
                "Cannot configure rate tables for benefits unless those benefits are defined on the product"
            )

    @validates_schema
    def validate_benefit_variations(self, data, **kwargs):
        configured_variation_codes = [
            b["config_product_variation_code"] for b in data["product_variations"]
        ]
        configured_benefit_codes = [b["config_benefit_code"] for b in data["benefits"]]
        configured_rate_tables = {
            (
                b["config_rate_table_set_label"],
                b["config_benefit_code"],
            )
            for b in data["rate_tables"]
        }

        all_valid_benefit_variation__variation_codes = all(
            [
                bv["config_product_variation_code"] in configured_variation_codes
                for bv in data["benefit_variations"]
            ]
        )
        if not all_valid_benefit_variation__variation_codes:
            raise ValidationError(
                "Cannot configure benefit variations unless those product variations have been defined on the product"
            )

        all_valid_benefit_variation__benefit_codes = all(
            [
                bv["config_benefit_code"] in configured_benefit_codes
                for bv in data["benefit_variations"]
            ]
        )
        if not all_valid_benefit_variation__benefit_codes:
            raise ValidationError(
                "Cannot configure benefit variations unless those benefits have been defined on the product"
            )

        all_valid_benefit_variation__rate_tables = True
        for bv in data["benefit_variations"]:
            bnft = bv["config_benefit_code"]
            all_valid_benefit_variation__rate_tables = (
                all_valid_benefit_variation__rate_tables
                & all(
                    [
                        (
                            bvs["config_rate_table_set_label"],
                            bnft,
                        )
                        in configured_rate_tables
                        for bvs in bv["states"]
                    ]
                )
            )
            if not all_valid_benefit_variation__rate_tables:
                raise ValidationError(
                    "Cannot assign rate tables to benefit variation states unless those rate tables have been defined"
                )
