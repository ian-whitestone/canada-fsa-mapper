CREATE TABLE fsa_polys (
  fsa varchar(3) PRIMARY KEY,
  province varchar(100),
  poly_str text,
  poly geography(POLYGON,4326),
  center_text text,
  center geography(POINT,4326)
)
;


CREATE TABLE fsa_multi_polys (
  fsa varchar(3) PRIMARY KEY,
  province varchar(100),
  multi_poly_str text,
  multi_poly geography(MULTIPOLYGON,4326),
  center_text text,
  center geography(POINT,4326)
)
;


-- run after inserting poly_strs
UPDATE fsa_polys
SET poly = ST_GeomFromText(poly_str)
;

UPDATE fsa_polys
SET center_text = ST_AsText(ST_Centroid(poly_str))
;

UPDATE fsa_polys
SET center = ST_GeomFromText(center_text)
;

UPDATE fsa_multi_polys
SET multi_poly = ST_GeomFromText(multi_poly_str)
;

UPDATE fsa_multi_polys
SET center_text = ST_AsText(ST_Centroid(multi_poly_str))
;

UPDATE fsa_multi_polys
SET center = ST_GeomFromText(center_text)
;

-- table for web viz
CREATE TABLE all_fsa AS (
  SELECT fsa, province, ST_AsGeoJSON(ST_ForceRHR(poly::geometry)) AS geom, ST_AsGeoJSON(center) AS center
  FROM fsa_polys
  UNION ALL
  SELECT fsa, province, ST_AsGeoJSON(ST_ForceRHR(multi_poly::geometry)) AS geom, ST_AsGeoJSON(center) AS center
  FROM fsa_multi_polys
)
;

-- create GTA subset
insert into all_fsa
select fsa, 'GTA' as province, geom, center
from all_fsa
where substring(fsa,1,1) in ('M','L')
and province='Ontario'

CREATE TABLE all_fsa_geom AS (
  SELECT fsa, province, poly::geometry AS geom, ST_AsGeoJSON(center) AS center
  FROM fsa_polys
  UNION ALL
  SELECT fsa, province, multi_poly::geometry AS geom, ST_AsGeoJSON(center) AS center
  FROM fsa_multi_polys
)
;
