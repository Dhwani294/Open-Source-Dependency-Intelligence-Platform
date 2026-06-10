CREATE TABLE IF NOT EXISTS `vulngraph.dim_time`
(
    date_id INT64 NOT NULL,

    date DATE NOT NULL,

    week INT64,
    month INT64,
    quarter INT64,
    year INT64
)
PARTITION BY date;