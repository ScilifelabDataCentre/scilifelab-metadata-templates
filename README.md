# SciLifeLab Metadata Templates

This repository stores metadata templates in use at SciLifeLab, organized according to data type. 

## General template structure

A template has a _title_, a _description_ and a _semantic version_ number, as well as well as a list of associated attribute fields. Each _attribute field_ needs to have:
- title
- description
- type
- list of controlled vocabulary terms if applicable
- level of requirement/cardinality (mandatory vs optional)
- end_repository_alias (if applicable; can be multiple if multiple relevant end repositories are considered)
- reference_ontology (if exists)

In addition to data type specific fields capturing the technical metadata itself, all templates include additional organizational metadata such as 
- SciLifeLab infrastructure platform and unit
- Unit internal project ID(s)
- Associated order ID
- Experimental Sample IDs (as assigned by the unit, 1 exp sample = 1 data file (pair))
- Associated Sample IDs (as shared by the researcher with the unit)


A row entry for an individual sample would then be

| <data_type_specific_field1> |...| <data_type_specific_fieldM> | <data_file_name_R1> |...|<data_file_name_RP>| <orga_meta_field1>|...| <orga_meta_fieldN> |
| --------------------------- | - | --------------------------- | ------------------- | - | ----------------- | ----------------- | - | ------------------ |


Templates are provided as _.tsv_, _.json_ and _.xlsx_. The _.json_ and _.xlsx_ files include controlled vocabulary terms where available. 

## Specific templates available

| Title | Description | Link |
| ----- | ----------- | ---- |
| SciLifeLab Genomics Technical Metadata Template | This template aims to capture technical metadata for genomics data produced at the Genomics platform, compatible with submission requirements from ENA and ArrayExpress. | [genomics/README.md](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/README.md) | 
