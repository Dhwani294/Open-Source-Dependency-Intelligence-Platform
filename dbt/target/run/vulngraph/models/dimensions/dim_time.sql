
  
    

    create or replace table `erudite-river-423507-n3`.`vulngraph`.`dim_time`
      
    
    

    
    OPTIONS()
    as (
      

WITH dates AS (

    SELECT day AS date
    FROM UNNEST(
        GENERATE_DATE_ARRAY(
            DATE('2020-01-01'),
            DATE('2035-12-31')
        )
    ) AS day

)

SELECT
    CAST(FORMAT_DATE('%Y%m%d', date) AS INT64) AS date_id,
    date,
    EXTRACT(WEEK FROM date) AS week,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(YEAR FROM date) AS year
FROM dates
    );
  