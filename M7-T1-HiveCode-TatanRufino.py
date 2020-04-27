
------M7 - T1 - HIVE-------

Tatan Rufino

---------------------------

LINUX CONSOLE:

---------------------------

hive

use m7;

CREATE TABLE contracts_tmp(
codigo_mes int,
provincia string,
municipio string,
total_contratos int,
contratos_hombres int,
contratos_mujeres int
 ) COMMENT 'Contratos por municipio'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\;'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE; 

LOAD DATA LOCAL INPATH '/warehouse/m7/U1/data/Contratos_por_municipio.csv' INTO TABLE m7.contracts_tmp;

CREATE TABLE contracts AS 
SELECT
IF(provincia like '%VILA','ÁVILA',provincia) AS provincia,
contratos_mujeres,
contratos_hombres
FROM contracts_tmp;

SELECT * FROM contracts;

CREATE TABLE provinces_regions(
Comunidad_autonoma string,
Provincia string
 ) COMMENT 'Provincias por region'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\;'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE; 

LOAD DATA LOCAL INPATH '/warehouse/m7/U1/data/Comunidades_y_provincias.csv' INTO TABLE m7.provinces_regions;

SELECT * FROM provinces_regions;

//HACEMOS EL INNER JOIN

CREATE TABLE Region_contracts AS 
SELECT provinces_regions.Comunidad_Autonoma AS comunidad_autonoma, 
sum(contracts.contratos_mujeres) AS contratos_mujeres, 
sum(contracts.contratos_hombres) AS contratos_hombres 
FROM provinces_regions
WHERE sum(contracts.contratos_mujeres) > sum(contracts.contratos_hombres)
INNER JOIN contracts ON 
provinces_regions.Provincia = contracts.provincia 
GROUP BY provinces_regions.Comunidad_Autonoma;

SELECT * FROM region_contracts WHERE contratos_mujeres > contratos_hombres;


SELECT provinces_regions.Comunidad_Autonoma AS comunidad_autonoma, 
sum(contracts.contratos_mujeres) AS contratos_mujeres, 
sum(contracts.contratos_hombres) AS contratos_hombres 
FROM provinces_regions 
INNER JOIN contracts ON 
provinces_regions.Provincia = contracts.provincia 
GROUP BY provinces_regions.Comunidad_Autonoma
WHERE contracts.contratos_mujeres > contracts.contratos_hombres;
