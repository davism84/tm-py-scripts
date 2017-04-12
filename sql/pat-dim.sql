COPY patient_dimension
(sex_cd,age_in_years_num,race_cd,update_date,download_date,import_date,sourcesystem_cd)
FROM '/home/tomcat/patient_dim.csv'
(FORMAT csv, HEADER true);
