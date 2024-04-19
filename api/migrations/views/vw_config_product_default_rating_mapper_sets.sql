CREATE VIEW [dbo].[vw_config_product_default_rating_mapper_sets] AS 
WITH
unpivot_product_rating_collections AS (
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
) AS U
)

SELECT  
    U.config_product_id, 
    U.rating_mapper_collection_id AS config_rating_mapper_collection_id, 
    (CASE 
        WHEN U.collection_number = 'rating_mapper_collection_id1' THEN 'selection_rating_mapper_set_id1'
        WHEN U.collection_number = 'rating_mapper_collection_id2' THEN 'selection_rating_mapper_set_id2'
        WHEN U.collection_number = 'rating_mapper_collection_id3' THEN 'selection_rating_mapper_set_id3'
        WHEN U.collection_number = 'rating_mapper_collection_id4' THEN 'selection_rating_mapper_set_id4'
        WHEN U.collection_number = 'rating_mapper_collection_id5' THEN 'selection_rating_mapper_set_id5'
        WHEN U.collection_number = 'rating_mapper_collection_id6' THEN 'selection_rating_mapper_set_id6'
    END) AS selection_rating_mapper_set_type, 
    COALESCE(
        RMC.default_config_rating_mapper_set_id, 
        (
            SELECT MIN(config_rating_mapper_set_id) 
            FROM config_rating_mapper_set AS S 
            WHERE S.config_rating_mapper_collection_id = U.rating_mapper_collection_id
        )
    ) AS default_config_rating_mapper_set_id
FROM unpivot_product_rating_collections AS U
INNER JOIN config_rating_mapper_collection AS RMC ON 
    U.rating_mapper_collection_id = RMC.config_rating_mapper_collection_id
