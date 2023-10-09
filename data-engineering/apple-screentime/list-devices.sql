SELECT
    date(ZLASTSEENDATE+978307200,'UNIXEPOCH', 'LOCALTIME') as "LAST_SEEN_DATE",
    ZMODEL,ZDEVICEID,ZRAPPORTID,ZVERSION
FROM
    ZSYNCPEER
ORDER BY
    LAST_SEEN_DATE desc;
