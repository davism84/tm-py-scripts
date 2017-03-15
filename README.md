# tm-py-scripts
transmart ETL python scripts

# For transmart

**1. Generate config file**

`$ python cfgen.py -transmart -tab data-2.tsv -o data-2.cfg `

**2. Adding Patients**

`$ python ../patgen.py -b -p MYTEST data-2.tsv`
- import the patients into the database at this point before step 4

**3. Building an Ontology**

`$ python ../oncgen.py -b -p MYTEST data-2.cfg data-2.tsv`

**4. Generate Observations**
* this needs to have the patients preloaded

`$ python ../obsgen.py -b -p MYTEST -k concepts_dim.sql-keys.tsv data-2.tsv`


## **_Postgres SQL for loading data_**

_These use the Postgres **COPY** command for loading bulk data which is much faster_
- COPY i2b2demodata.patient_dimension
(sex_cd,age_in_years_num,race_cd,update_date,download_date,import_date,sourcesystem_cd)
FROM '/home/transmart/transmart-data/imports/patient_dim.csv'
(FORMAT csv, HEADER true);

- copy i2b2demodata.concept_dimension
(concept_cd,concept_path,name_char,update_date,download_date,import_date,sourcesystem_cd)
FROM '/home/transmart/transmart-data/imports/concepts_dim.csv'
(FORMAT csv, HEADER true);

- copy i2b2metadata.i2b2
(c_hlevel, c_fullname,c_name,c_visualattributes,c_synonym_cd,c_facttablecolumn,c_tablename,c_columnname,c_dimcode,c_tooltip,update_date,download_date,import_date,sourcesystem_cd,c_basecode,c_operator,c_columndatatype,c_comment	,m_applied_path,c_metadataxml)
FROM '/home/transmart/transmart-data/imports/i2b2.csv'
(FORMAT csv, HEADER true);

- copy i2b2demodata.observation_fact
(encounter_num,patient_num,concept_cd,start_date,modifier_cd,valtype_cd,tval_char,nval_num,import_date,valueflag_cd,provider_id,location_cd,instance_num,sourcesystem_cd)
FROM '/home/transmart/transmart-data/imports/observation_facts.csv'
(FORMAT csv, HEADER true);

**To add counts to concept tree**

select tm_cz.i2b2_create_concept_counts('\Public Studies\TEST58\', null);

** To secure a study**

I2B2_SECURE_STUDY
