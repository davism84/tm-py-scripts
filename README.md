# For transmart

**1. Generate config file**

$ python ..\..\tm-py-scripts\cfgen.py -d breast -transmart -tab data-151.tsv -o data.cfg

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

**_NEED TO run this for PUBLIC study_**
- select tm_cz.i2b2_create_security_for_trial('<study_id>', 'N', 0);

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
-- this is IMPORTANT to at least set security AFTER loading PATIENT_DIMENSION, the Grid feature JOINs with the PATIENT_TRIAL table to display the demographics info

select tm_cz.I2B2_SECURE_STUDY('<trial name-UPPERCASE>', 0);    -- trial name must be in UPPERCASE! this will make the STUDY completely secure, not PUBLIC (use individual SQL below to make PUBLIC, )

- select tm_cz.i2b2_create_security_for_trial('PvtRegistry', 'Y', 0);  -- study_id, <secured? y/n>, <jobid>
- select tm_cz.i2b2_load_security_data(0);	-- onnly run this if it's a SECURE study

1 adds a concept_cd = 'SECURITY' record to OBSERVATION_FACT 
2 adds patients to patient_trial with secure_obj_token

REM this command should work for the above two commands but there is a syntax error somewhere 


** REMOVE a study
select tm_cz.i2b2_backout_trial('CancerRegistry', '\Public Studies\CancerRegistry\', -1);