SELECT
    date(ZOBJECT.ZSTARTDATE+978307200,'UNIXEPOCH', 'LOCALTIME') as "DATE",
    round(sum(ZOBJECT.ZENDDATE-ZOBJECT.ZSTARTDATE) / 3600.0, 3 ) as "TOTAL_USAGE_PER_DAY_IN_HOURS"
FROM
    ZOBJECT 
WHERE
    --ZSTREAMNAME = "/app/usage"
    --and
    -- only in the past, don't care about today's summary since today isn't over yet
    DATE < date('now')
GROUP BY
    DATE
ORDER BY
    DATE DESC;
