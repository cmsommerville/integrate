CREATE PROCEDURE [dbo].[selection_rate_engine] (@selection_plan_id INT) AS 
SET NOCOUNT OFF; 

WITH 
selection_rating_mapper_details AS (
SELECT S.selection_plan_id, S.selection_rating_mapper_set_type, D.*
FROM selection_rating_mapper_detail AS D 
INNER JOIN selection_rating_mapper_set AS S ON 
    D.selection_rating_mapper_set_id = S.selection_rating_mapper_set_id 
WHERE S.selection_plan_id = @selection_plan_id
), 

rating_weights AS (
SELECT 
    SP.selection_plan_id, 
    AB.selection_age_band_id, 
    AB.age_band_lower, 
    AB.age_band_upper, 
    AGE.rate_table_age_value, 

    RMS1.rate_table_attribute_detail_id AS rate_table_attribute_detail_id1, 
    RMS2.rate_table_attribute_detail_id AS rate_table_attribute_detail_id2, 
    RMS3.rate_table_attribute_detail_id AS rate_table_attribute_detail_id3, 
    RMS4.rate_table_attribute_detail_id AS rate_table_attribute_detail_id4, 
    RMS5.rate_table_attribute_detail_id AS rate_table_attribute_detail_id5, 
    RMS6.rate_table_attribute_detail_id AS rate_table_attribute_detail_id6, 

    RMS1.output_attribute_detail_id AS output_attribute_detail_id1, 
    RMS2.output_attribute_detail_id AS output_attribute_detail_id2, 
    RMS3.output_attribute_detail_id AS output_attribute_detail_id3, 
    RMS4.output_attribute_detail_id AS output_attribute_detail_id4, 
    RMS5.output_attribute_detail_id AS output_attribute_detail_id5, 
    RMS6.output_attribute_detail_id AS output_attribute_detail_id6, 

    SUM(COALESCE(AGE.weight, 1) * COALESCE(RMS1.weight, 1) * COALESCE(RMS2.weight, 1) * COALESCE(RMS3.weight, 1) * 
    COALESCE(RMS4.weight, 1) * COALESCE(RMS5.weight, 1) * COALESCE(RMS6.weight, 1)) AS rating_weight
FROM selection_plan AS SP
INNER JOIN config_product AS PROD ON 
    SP.config_product_id = PROD.config_product_id
LEFT JOIN config_age_distribution_detail AGE ON 
    PROD.age_distribution_set_id = AGE.config_age_distribution_set_id 
LEFT JOIN selection_rating_mapper_details RMS1 ON 
    SP.selection_plan_id = RMS1.selection_plan_id AND 
    RMS1.selection_rating_mapper_set_type = 'selection_rating_mapper_set_id1'
LEFT JOIN selection_rating_mapper_details RMS2 ON 
    SP.selection_plan_id = RMS2.selection_plan_id AND 
    RMS2.selection_rating_mapper_set_type = 'selection_rating_mapper_set_id2'
LEFT JOIN selection_rating_mapper_details RMS3 ON 
    SP.selection_plan_id = RMS3.selection_plan_id AND 
    RMS3.selection_rating_mapper_set_type = 'selection_rating_mapper_set_id3'
LEFT JOIN selection_rating_mapper_details RMS4 ON 
    SP.selection_plan_id = RMS4.selection_plan_id AND 
    RMS4.selection_rating_mapper_set_type = 'selection_rating_mapper_set_id4'
LEFT JOIN selection_rating_mapper_details RMS5 ON 
    SP.selection_plan_id = RMS5.selection_plan_id AND 
    RMS5.selection_rating_mapper_set_type = 'selection_rating_mapper_set_id5'
LEFT JOIN selection_rating_mapper_details RMS6 ON 
    SP.selection_plan_id = RMS6.selection_plan_id AND 
    RMS6.selection_rating_mapper_set_type = 'selection_rating_mapper_set_id6'
LEFT JOIN selection_age_band AB ON 
    SP.selection_plan_id = AB.selection_plan_id AND 
    COALESCE(AGE.age_value, 999) BETWEEN AB.age_band_lower AND AB.age_band_upper
WHERE SP.selection_plan_id = @selection_plan_id
GROUP BY 
    SP.selection_plan_id, 
    AB.selection_age_band_id, 
    AB.age_band_lower, 
    AB.age_band_upper, 
    AGE.rate_table_age_value, 

    RMS1.rate_table_attribute_detail_id,
    RMS2.rate_table_attribute_detail_id,
    RMS3.rate_table_attribute_detail_id,
    RMS4.rate_table_attribute_detail_id,
    RMS5.rate_table_attribute_detail_id,
    RMS6.rate_table_attribute_detail_id,

    RMS1.output_attribute_detail_id,
    RMS2.output_attribute_detail_id,
    RMS3.output_attribute_detail_id, 
    RMS4.output_attribute_detail_id,
    RMS5.output_attribute_detail_id, 
    RMS6.output_attribute_detail_id
), 

benefit_duration_factors AS (
SELECT 
    BD.selection_benefit_id, EXP(SUM(LOG(BD.selection_factor))) AS benefit_duration_factor
FROM selection_benefit_duration AS BD 
INNER JOIN selection_benefit AS B ON 
    BD.selection_benefit_id = B.selection_benefit_id
WHERE B.selection_plan_id = @selection_plan_id
GROUP BY BD.selection_benefit_id
), 

rating_engine AS (
SELECT 
    SB.selection_benefit_id, 
    SB.selection_plan_id, 
    SB.config_benefit_variation_state_id, 
    CBVS.config_benefit_id, 
    SB.selection_value, 
    W.selection_age_band_id, 
    W.age_band_lower, 
    W.age_band_upper, 
    W.output_attribute_detail_id1, 
    W.output_attribute_detail_id2, 
    W.output_attribute_detail_id3, 
    W.output_attribute_detail_id4, 
    W.output_attribute_detail_id5, 
    W.output_attribute_detail_id6, 
    W.rating_weight, 
    COALESCE(F.factor_value, 1) AS factor_value, 
    rate_per_unit, 
    ROUND(COALESCE(F.factor_value, 1) * COALESCE(BDF.benefit_duration_factor, 1) * 
    RT.rate_per_unit * FREQ.ref_attr_value * 
        SB.selection_value / (0.0 + RT.rate_unit_value), 5) AS rate
FROM selection_benefit AS SB 
INNER JOIN selection_plan AS SP ON 
    SB.selection_plan_id = SP.selection_plan_id 
INNER JOIN config_benefit_variation_state CBVS ON 
    SB.config_benefit_variation_state_id = CBVS.config_benefit_variation_state_id
INNER JOIN config_rate_table RT ON 
    CBVS.config_rate_table_set_id = RT.config_rate_table_set_id
INNER JOIN rating_weights W ON 
    SP.selection_plan_id = W.selection_plan_id AND 
    COALESCE(RT.rating_age, 999) = COALESCE(W.rate_table_age_value, 999) AND 
    COALESCE(RT.rating_attr_id1, -1) = COALESCE(W.rate_table_attribute_detail_id1, -1) AND 
    COALESCE(RT.rating_attr_id2, -1) = COALESCE(W.rate_table_attribute_detail_id2, -1) AND 
    COALESCE(RT.rating_attr_id3, -1) = COALESCE(W.rate_table_attribute_detail_id3, -1) AND 
    COALESCE(RT.rating_attr_id4, -1) = COALESCE(W.rate_table_attribute_detail_id4, -1) AND 
    COALESCE(RT.rating_attr_id5, -1) = COALESCE(W.rate_table_attribute_detail_id5, -1) AND 
    COALESCE(RT.rating_attr_id6, -1) = COALESCE(W.rate_table_attribute_detail_id6, -1) 
INNER JOIN ref_master FREQ ON 
    RT.rate_frequency_id = FREQ.ref_id
LEFT JOIN vw_selection_rate_table_factors F ON 
    SB.selection_benefit_id = F.selection_benefit_id AND 
    RT.config_rate_table_id = F.config_rate_table_id
LEFT JOIN benefit_duration_factors AS BDF ON 
    SB.selection_benefit_id = BDF.selection_benefit_id
WHERE SB.selection_plan_id = @selection_plan_id
), 

rates AS (
SELECT 
    selection_benefit_id, 
    selection_plan_id, 
    selection_age_band_id, 
    output_attribute_detail_id1, output_attribute_detail_id2, output_attribute_detail_id3, 
    output_attribute_detail_id4, output_attribute_detail_id5, output_attribute_detail_id6, 
    ROUND(SUM(rating_weight * rate) / SUM(rating_weight), 5) AS rate_value
FROM rating_engine 
GROUP BY 
    selection_benefit_id, 
    selection_plan_id, 
    selection_age_band_id, 
    output_attribute_detail_id1, output_attribute_detail_id2, output_attribute_detail_id3, 
    output_attribute_detail_id4, output_attribute_detail_id5, output_attribute_detail_id6
)

SELECT 
    R.*, HASHBYTES('MD5', CONCAT_WS('#', 
        selection_benefit_id, selection_plan_id, selection_age_band_id, output_attribute_detail_id1, 
        output_attribute_detail_id2, output_attribute_detail_id3, output_attribute_detail_id4, 
        output_attribute_detail_id5, output_attribute_detail_id6, rate_value
    )) AS row_hash
INTO #selection_benefit_rate
FROM rates AS R 
; 


    BEGIN TRANSACTION T1; 
        DELETE R 
        FROM selection_benefit_rate AS R 
        LEFT JOIN #selection_benefit_rate AS N ON 
            R.selection_benefit_id = N.selection_benefit_id AND 
            R.selection_plan_id = N.selection_plan_id AND 
            R.row_hash = N.row_hash 
        WHERE 
            R.selection_plan_id = @selection_plan_id AND 
            N.selection_benefit_id IS NULL
        ; 

        INSERT INTO selection_benefit_rate (
            selection_benefit_id, selection_plan_id, selection_age_band_id, output_attribute_detail_id1, 
            output_attribute_detail_id2, output_attribute_detail_id3, output_attribute_detail_id4, 
            output_attribute_detail_id5, output_attribute_detail_id6, rate_value, row_hash, 
            created_dts, updated_dts, updated_by
        )
        SELECT 
            N.selection_benefit_id, N.selection_plan_id, N.selection_age_band_id, N.output_attribute_detail_id1, 
            N.output_attribute_detail_id2, N.output_attribute_detail_id3, N.output_attribute_detail_id4, 
            N.output_attribute_detail_id5, N.output_attribute_detail_id6, N.rate_value, N.row_hash, 
            GETDATE() AS created_dts, 
            GETDATE() AS updated_dts, 
            'selection_rate_engine' AS updated_by
        FROM #selection_benefit_rate AS N
        LEFT JOIN selection_benefit_rate AS R ON 
            R.selection_benefit_id = N.selection_benefit_id AND 
            R.selection_plan_id = N.selection_plan_id AND 
            R.row_hash = N.row_hash 
        WHERE 
            R.selection_benefit_id IS NULL
        ;

    COMMIT TRANSACTION T1;
    
