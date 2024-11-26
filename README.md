# SciLifeLab Metadata Templates

This repository stores metadata templates in use at SciLifeLab. 

Templates will be organized according to data type. In addition to data type specific fields capturing the technical metadata itself, all templates should capture general organizational metadata such as 
- SciLifeLab infrastructure platform and unit
- Unit internal project ID(s)
- Associated order ID
- Experimental Sample IDs (as assigned by the unit, 1 exp sample = 1 data file (pair))
- Associated Sample IDs (as shared by the researcher with the unit)

A template has
- name
- description/applicability
- version

Within a template each template field needs to have:
- name
- description
- type
- list of controlled vocabulary terms if applicable
- level of requirement (mandatory vs optional)

In addition data type specific fields also need
- end_repository_alias (can be multiple if multiple relevant end repositories are considered)
- reference_ontology (if exists)

A row entry for an individual sample would then be

| UUID  | <orga_meta_field1>|...| <orga_meta_fieldN> |<data_type_specific_field1>|...| <data_type_specific_fieldM> | <data_file_name_R1> |...|<data_file_name_RP>|
| ----- | ----------------- | - | ------------------ | ------------------------- | - | --------------------------- | ------------------- | -- | ---------------- |


Templates are provided as INSERT FILE FORMAT HERE.

Open question:

- suitable file format? How to provide controlled vocabularies? machine readable vs humanly readable and usable

## A SciLifeLab Genomics Technical Metadata Template

For now the focus is on a template capturing technical metadata for genomics data produced at the Genomics platform. The template should be compatible with submission requirements from ENA and ArrayExpress. 


Open question: do we need a "single cell"-specific template?
