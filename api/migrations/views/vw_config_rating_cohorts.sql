CREATE VIEW [dbo].[vw_config_rating_cohorts] AS 
WITH 
product AS (
SELECT U.config_product_id, U.collection_number, U.rating_mapper_collection_id
FROM (
    SELECT 
        config_product_id, 
        rating_mapper_collection_id1, 
        rating_mapper_collection_id2, 
        rating_mapper_collection_id3, 
        rating_mapper_collection_id4, 
        rating_mapper_collection_id5, 
        rating_mapper_collection_id6
    FROM config_product
) AS P
UNPIVOT (rating_mapper_collection_id FOR collection_number IN (
        rating_mapper_collection_id1, 
        rating_mapper_collection_id2, 
        rating_mapper_collection_id3, 
        rating_mapper_collection_id4, 
        rating_mapper_collection_id5, 
        rating_mapper_collection_id6
    )
) AS U), 

rating_age_detail AS (
SELECT DISTINCT P.config_product_id, AD.rate_table_age_value
FROM config_product P 
INNER JOIN config_age_distribution_detail AD ON 
    P.age_distribution_set_id = AD.config_age_distribution_set_id
), 

mapper_detail AS (
SELECT
    P.config_product_id, 
    collection_number, 
    S.config_rating_mapper_collection_id, 
    M.config_rating_mapper_set_id, 
    M.rate_table_attribute_detail_id, 
    M.output_attribute_detail_id, 
    R.config_attr_detail_code AS rate_table_attribute_detail_code, 
    O.config_attr_detail_code AS output_attribute_detail_code, 
    M.weight
FROM config_rating_mapper_detail AS M
INNER JOIN config_rating_mapper_set S ON 
    M.config_rating_mapper_set_id = S.config_rating_mapper_set_id
INNER JOIN product AS P ON 
    S.config_rating_mapper_collection_id = P.rating_mapper_collection_id
INNER JOIN config_attr_detail AS R ON 
    M.rate_table_attribute_detail_id = R.config_attr_detail_id
INNER JOIN config_attr_detail AS O ON 
    M.output_attribute_detail_id = O.config_attr_detail_id
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
SELECT DISTINCT
    C1.config_product_id, 
    COALESCE(A.rate_table_age_value, -1) AS rate_table_age_value, 
    COALESCE(C1.rate_table_attribute_detail_id, -1)  AS rate_table_attribute_detail_id1, 
    COALESCE(C2.rate_table_attribute_detail_id, -1)  AS rate_table_attribute_detail_id2, 
    COALESCE(C3.rate_table_attribute_detail_id, -1)  AS rate_table_attribute_detail_id3, 
    COALESCE(C4.rate_table_attribute_detail_id, -1)  AS rate_table_attribute_detail_id4, 
    COALESCE(C5.rate_table_attribute_detail_id, -1)  AS rate_table_attribute_detail_id5, 
    COALESCE(C6.rate_table_attribute_detail_id, -1)  AS rate_table_attribute_detail_id6
FROM collection1 AS C1
LEFT JOIN collection2 AS C2 ON C1.config_product_id = C2.config_product_id
LEFT JOIN collection3 AS C3 ON C1.config_product_id = C3.config_product_id
LEFT JOIN collection4 AS C4 ON C1.config_product_id = C4.config_product_id
LEFT JOIN collection5 AS C5 ON C1.config_product_id = C5.config_product_id
LEFT JOIN collection6 AS C6 ON C1.config_product_id = C6.config_product_id
LEFT JOIN rating_age_detail AS A ON C1.config_product_id = A.config_product_id
)

SELECT X.*, HASHBYTES('MD5', CONCAT_WS('#', config_product_id, rate_table_age_value, 
    rate_table_attribute_detail_id1, rate_table_attribute_detail_id2, rate_table_attribute_detail_id3, 
    rate_table_attribute_detail_id4, rate_table_attribute_detail_id5, rate_table_attribute_detail_id6)
    ) AS row_hash
FROM census AS X 
