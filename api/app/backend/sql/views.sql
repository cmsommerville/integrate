CREATE VIEW vw_config_rating_cohorts AS WITH product AS (
    SELECT U.config_product_id,
        U.collection_number,
        U.rating_mapper_collection_id
    FROM (
            SELECT config_product_id,
                rating_mapper_collection_id1,
                rating_mapper_collection_id2,
                rating_mapper_collection_id3,
                rating_mapper_collection_id4,
                rating_mapper_collection_id5,
                rating_mapper_collection_id6
            FROM config_product
        ) AS P UNPIVOT (
            rating_mapper_collection_id FOR collection_number IN (
                rating_mapper_collection_id1,
                rating_mapper_collection_id2,
                rating_mapper_collection_id3,
                rating_mapper_collection_id4,
                rating_mapper_collection_id5,
                rating_mapper_collection_id6
            )
        ) AS U
),
rating_age_detail AS (
    SELECT DISTINCT P.config_product_id,
        AD.rate_table_age_value
    FROM config_product P
        INNER JOIN config_age_distribution_detail AD ON P.age_distribution_set_id = AD.config_age_distribution_set_id
),
mapper_detail AS (
    SELECT P.config_product_id,
        collection_number,
        S.config_rating_mapper_collection_id,
        M.config_rating_mapper_set_id,
        M.rate_table_attribute_detail_id,
        M.output_attribute_detail_id,
        R.config_attr_detail_code AS rate_table_attribute_detail_code,
        O.config_attr_detail_code AS output_attribute_detail_code,
        M.weight
    FROM config_rating_mapper_detail AS M
        INNER JOIN config_rating_mapper_set S ON M.config_rating_mapper_set_id = S.config_rating_mapper_set_id
        INNER JOIN product AS P ON S.config_rating_mapper_collection_id = P.rating_mapper_collection_id
        INNER JOIN config_attr_detail AS R ON M.rate_table_attribute_detail_id = R.config_attr_detail_id
        INNER JOIN config_attr_detail AS O ON M.output_attribute_detail_id = O.config_attr_detail_id
),
collection1 AS (
    SELECT *
    FROM mapper_detail
    WHERE collection_number = 'rating_mapper_collection_id1'
),
collection2 AS (
    SELECT *
    FROM mapper_detail
    WHERE collection_number = 'rating_mapper_collection_id2'
),
collection3 AS (
    SELECT *
    FROM mapper_detail
    WHERE collection_number = 'rating_mapper_collection_id3'
),
collection4 AS (
    SELECT *
    FROM mapper_detail
    WHERE collection_number = 'rating_mapper_collection_id4'
),
collection5 AS (
    SELECT *
    FROM mapper_detail
    WHERE collection_number = 'rating_mapper_collection_id5'
),
collection6 AS (
    SELECT *
    FROM mapper_detail
    WHERE collection_number = 'rating_mapper_collection_id6'
),
age_band AS (
    SELECT *
    FROM config_age_band_detail
    WHERE config_age_band_set_id = 1
),
census AS (
    SELECT DISTINCT C1.config_product_id,
        COALESCE(A.rate_table_age_value, -1) AS rate_table_age_value,
        COALESCE(C1.rate_table_attribute_detail_id, -1) AS rate_table_attribute_detail_id1,
        COALESCE(C2.rate_table_attribute_detail_id, -1) AS rate_table_attribute_detail_id2,
        COALESCE(C3.rate_table_attribute_detail_id, -1) AS rate_table_attribute_detail_id3,
        COALESCE(C4.rate_table_attribute_detail_id, -1) AS rate_table_attribute_detail_id4,
        COALESCE(C5.rate_table_attribute_detail_id, -1) AS rate_table_attribute_detail_id5,
        COALESCE(C6.rate_table_attribute_detail_id, -1) AS rate_table_attribute_detail_id6
    FROM collection1 AS C1
        LEFT JOIN collection2 AS C2 ON C1.config_product_id = C2.config_product_id
        LEFT JOIN collection3 AS C3 ON C1.config_product_id = C3.config_product_id
        LEFT JOIN collection4 AS C4 ON C1.config_product_id = C4.config_product_id
        LEFT JOIN collection5 AS C5 ON C1.config_product_id = C5.config_product_id
        LEFT JOIN collection6 AS C6 ON C1.config_product_id = C6.config_product_id
        LEFT JOIN rating_age_detail AS A ON C1.config_product_id = A.config_product_id
)
SELECT *
FROM census;
/*  ****************************************************************
 
 SELECTION RATE TABLE FACTORS
 
 **************************************************************** */
CREATE VIEW vw_selection_rate_table_factors AS WITH SELECTED_BENEFITS_RATE_TABLE AS (
    SELECT SB.selection_benefit_id,
        SB.selection_plan_id,
        SB.config_benefit_variation_state_id,
        CBVS.config_benefit_variation_id,
        CBV.config_benefit_id,
        SB.selection_value,
        RT.*
    FROM selection_benefit AS SB
        INNER JOIN config_benefit_variation_state CBVS ON SB.config_benefit_variation_state_id = CBVS.config_benefit_variation_state_id
        INNER JOIN config_benefit_variation CBV ON CBVS.config_benefit_variation_id = CBV.config_benefit_variation_id
        INNER JOIN config_rate_table RT ON CBVS.config_rate_table_set_id = RT.config_rate_table_set_id
),
RATE_TABLE_TO_CONFIGURED_FACTOR_SETS AS (
    SELECT RT.selection_benefit_id,
        RT.selection_plan_id,
        RT.config_benefit_id,
        RT.config_rate_table_id,
        RT.config_rate_table_set_id,
        CBP.config_provision_id,
        SP.config_factor_set_id,
        (
            CASE
                WHEN FS.vary_by_rating_age = 1 THEN RT.rating_age
                ELSE -1
            END
        ) as rate_table_age_value,
        (
            CASE
                WHEN FS.vary_by_rating_attr1 = 1 THEN RT.rating_attr_id1
                ELSE -1
            END
        ) as rating_attr_id1,
        (
            CASE
                WHEN FS.vary_by_rating_attr2 = 1 THEN RT.rating_attr_id2
                ELSE -1
            END
        ) as rating_attr_id2,
        (
            CASE
                WHEN FS.vary_by_rating_attr3 = 1 THEN RT.rating_attr_id3
                ELSE -1
            END
        ) as rating_attr_id3,
        (
            CASE
                WHEN FS.vary_by_rating_attr4 = 1 THEN RT.rating_attr_id4
                ELSE -1
            END
        ) as rating_attr_id4,
        (
            CASE
                WHEN FS.vary_by_rating_attr5 = 1 THEN RT.rating_attr_id5
                ELSE -1
            END
        ) as rating_attr_id5,
        (
            CASE
                WHEN FS.vary_by_rating_attr6 = 1 THEN RT.rating_attr_id6
                ELSE -1
            END
        ) as rating_attr_id6
    FROM SELECTED_BENEFITS_RATE_TABLE RT
        INNER JOIN config_benefit_provision CBP ON RT.config_benefit_id = CBP.config_benefit_id
        INNER JOIN selection_provision SP ON CBP.config_provision_id = SP.config_provision_id
        AND RT.selection_plan_id = SP.selection_plan_id
        INNER JOIN config_factor_set AS FS ON SP.config_factor_set_id = FS.config_factor_set_id
)
SELECT RT.selection_benefit_id,
    RT.selection_plan_id,
    RT.config_rate_table_id,
    ROUND(
        EXP(SUM(LOG(COALESCE(F.selection_factor_value, 1)))),
        5
    ) AS factor_value
FROM RATE_TABLE_TO_CONFIGURED_FACTOR_SETS AS RT
    LEFT JOIN selection_factor AS F ON RT.config_factor_set_id = F.config_factor_set_id
    AND RT.rate_table_age_value = F.selection_rate_table_age_value
    AND RT.rating_attr_id1 = F.selection_rating_attr_id1
    AND RT.rating_attr_id2 = F.selection_rating_attr_id2
    AND RT.rating_attr_id3 = F.selection_rating_attr_id3
    AND RT.rating_attr_id4 = F.selection_rating_attr_id4
    AND RT.rating_attr_id5 = F.selection_rating_attr_id5
    AND RT.rating_attr_id6 = F.selection_rating_attr_id6
GROUP BY RT.selection_benefit_id,
    RT.selection_plan_id,
    RT.config_rate_table_id;