CREATE VIEW [dbo].[vw_selection_rate_table_factors] AS 
WITH 
SELECTED_BENEFITS_RATE_TABLE AS (
SELECT 
    SB.selection_benefit_id, 
    SB.selection_plan_id, 
    SB.config_benefit_variation_state_id, 
    CBVS.config_benefit_id, 
    SB.selection_value, 
    RT.*
FROM selection_benefit AS SB 
INNER JOIN config_benefit_variation_state CBVS ON 
    SB.config_benefit_variation_state_id = CBVS.config_benefit_variation_state_id
INNER JOIN config_rate_table RT ON 
    CBVS.config_rate_table_set_id = RT.config_rate_table_set_id
), 

RATE_TABLE_TO_CONFIGURED_FACTOR_SETS AS (
SELECT 
    RT.selection_benefit_id, 
    RT.selection_plan_id, 
    RT.config_benefit_id, 
    RT.config_rate_table_id, 
    RT.config_rate_table_set_id, 
    CBP.config_provision_id , 
    SF.config_factor_set_id, 
    (CASE WHEN FS.vary_by_rating_age = 1 THEN RT.rating_age ELSE -1 END) as rate_table_age_value, 
    (CASE WHEN FS.vary_by_rating_attr1 = 1 THEN RT.rating_attr_id1 ELSE -1 END) as rating_attr_id1, 
    (CASE WHEN FS.vary_by_rating_attr2 = 1 THEN RT.rating_attr_id2 ELSE -1 END) as rating_attr_id2,
    (CASE WHEN FS.vary_by_rating_attr3 = 1 THEN RT.rating_attr_id3 ELSE -1 END) as rating_attr_id3,
    (CASE WHEN FS.vary_by_rating_attr4 = 1 THEN RT.rating_attr_id4 ELSE -1 END) as rating_attr_id4,
    (CASE WHEN FS.vary_by_rating_attr5 = 1 THEN RT.rating_attr_id5 ELSE -1 END) as rating_attr_id5,
    (CASE WHEN FS.vary_by_rating_attr6 = 1 THEN RT.rating_attr_id6 ELSE -1 END) as rating_attr_id6 
FROM SELECTED_BENEFITS_RATE_TABLE RT 
INNER JOIN config_benefit_provision CBP ON 
    RT.config_benefit_id = CBP.config_benefit_id
INNER JOIN config_provision_state PS ON 
    CBP.config_provision_id = PS.config_provision_id
INNER JOIN selection_provision SP ON 
    PS.config_provision_state_id = SP.config_provision_state_id AND 
    RT.selection_plan_id = SP.selection_plan_id 
INNER JOIN selection_factor AS SF ON 
    SP.selection_provision_id = SF.selection_provision_id
INNER JOIN config_factor_set AS FS ON 
    SF.config_factor_set_id = FS.config_factor_set_id
)

SELECT 
    RT.selection_benefit_id, 
    RT.selection_plan_id, 
    RT.config_rate_table_id, 
    ROUND(EXP(SUM(LOG(COALESCE(F.selection_factor_value, 1)))),5) AS factor_value
FROM RATE_TABLE_TO_CONFIGURED_FACTOR_SETS AS RT 
LEFT JOIN selection_factor AS F ON 
    RT.config_factor_set_id = F.config_factor_set_id AND 
    RT.rate_table_age_value = F.selection_rate_table_age_value AND 
    RT.rating_attr_id1 = F.selection_rating_attr_id1 AND 
    RT.rating_attr_id2 = F.selection_rating_attr_id2 AND 
    RT.rating_attr_id3 = F.selection_rating_attr_id3 AND 
    RT.rating_attr_id4 = F.selection_rating_attr_id4 AND 
    RT.rating_attr_id5 = F.selection_rating_attr_id5 AND 
    RT.rating_attr_id6 = F.selection_rating_attr_id6
GROUP BY RT.selection_benefit_id, RT.selection_plan_id, RT.config_rate_table_id



