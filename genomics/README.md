# SciLifeLab Genomics Technical Metadata Template
The main recipient repositories for genomic data are [European Nucleotide Archive](https://www.ebi.ac.uk/ena/) (ENA) and [ArrayExpress](https://www.ebi.ac.uk/biostudies/arrayexpress). Note that the nucleotide sequencing data submitted to ArrayExpress is forwarded (by them via brokering) to ENA.

For this purpose data type specific templates are created, aiming to capture technical metadata for genomics data produced at the Genomics platform, compatible with submission requirements from ENA and ArrayExpress. In addition, the templates include SciLifeLab specific organisational metadata fields. 

Within a template each template field needs to have:
- Field name
- Level of requirement/cardinality (mandatory vs optional)
- Description
- List of controlled vocabulary terms if applicable

The genomics template can be downloaded in the following formats:
- [Single read _.tsv_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata_single_read.tsv)
- [Paired reads _.tsv_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata_paired_reads.tsv)
- TODO xlsx, includes instructions and CV terms
- TODO json, includes CV terms
  
The _.tsv_ files are split between the cases for single and paired reads to comply with the format and fields required for interactive submission to ENA using the Webin Portal. Note that the organisational metadata fields present at the end of the _.tsv_ should be excluded in a submission to ENA, but are relevant for data provenance for the researcher as well as other metadata consumers at SciLifeLab. 


## Technical metadata required by ENA 

For interactive submission of the technical metadata, ENA requires a single _.tsv_ file containing the fields listed below (merged from ENA.experiment and ENA.run object metadata). 

**Note:**
- Some fields are only relevant if handling single read data (`file_name`, `file_md5`) or paired reads data (`insert_size`, `forward_file_name`, `forward_file_md5`, `reverse_file_name`, `reverse_file_md5`).
- ENA fields `design_description`(not listed below) and `library_construction_protocol` cover largely the same information and are seen as redundant of each other. We decide to populate (only) `library_construction_protocol` for the SciLifeLab genomics template. 


| Field name                    | Cardinality   |  Description     | Controlled vocabulary   |
|:------------------------------|:--------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| (study_alias) | mandatory     | (from study metadata, provided by submitter) Identifies the parent study.    |     |
| (sample_alias) | mandatory     | (from sample metadata, provided by submitter) Identifies the sample the experiment is linked to. |   |
| name  | mandatory     | Name or title of the experiment, short text that can be used to call out experiment records in searches or in displays.  |  |
| library_construction_protocol | optional      | Free form text describing the protocol by which the sequencing library was constructed. (either this or the field design_description should be populated)  |    |
| library_name    | optional      | The submitter's name for this library.    |    |
| library_strategy   | mandatory     | Sequencing technique intended for this library.     | WGS, WGA, WXS, RNA-Seq, ssRNA-seq, snRNA-seq, miRNA-Seq, ncRNA-Seq, FL-cDNA, EST, Hi-C, ATAC-seq, WCS, RAD-Seq, CLONE, POOLCLONE, AMPLICON, CLONEEND, FINISHING, ChIP-Seq, MNase-Seq, DNase-Hypersensitivity, Bisulfite-Seq, CTS, MRE-Seq, MeDIP-Seq, MBD-Seq, Tn-Seq, VALIDATION, FAIRE-seq, SELEX, RIP-Seq, ChIA-PET, Synthetic-Long-Read, Targeted-Capture, Tethered Chromatin Conformation Capture, NOMe-Seq, ChM-Seq, GBS, Ribo-Seq, OTHER   |
| library_source   | mandatory     | The library_source specifies the type of source material that is being sequenced.    | GENOMIC, GENOMIC SINGLE CELL, TRANSCRIPTOMIC, TRANSCRIPTOMIC SINGLE CELL, METAGENOMIC, METATRANSCRIPTOMIC, SYNTHETIC, VIRAL RNA, OTHER |
| library_selection      | mandatory     | Method used to enrich the target in the sequence library preparation.  | RANDOM, PCR, RANDOM PCR, RT-PCR, HMPR, MF, repeat fractionation, size fractionation, MSLL, cDNA, cDNA_randomPriming, cDNA_oligo_dT, PolyA, Oligo-dT, Inverse rRNA, Inverse rRNA selection, ChIP, ChIP-Seq, MNase, DNase, Hybrid Selection, Reduced Representation, Restriction Digest, 5-methylcytidine antibody, MBD2 protein methyl-CpG binding domain, CAGE, RACE, MDA, padlock probes capture method, other, unspecified   |
| library_layout    | optional     | Library_layout specifies whether to expect single, paired, or other configuration of reads. Mandatory if paired reads. | SINGLE, PAIRED, Other  |
| insert_size   | optional      | Insert size for paired reads.      |     |
| instrument_model      | mandatory     | Model of the sequencing instrument.  | 454 GS, 454 GS 20, 454 GS FLX, 454 GS FLX Titanium, 454 GS FLX+, 454 GS Junior, AB 310 Genetic Analyzer, AB 3130 Genetic Analyzer, AB 3130xL Genetic Analyzer, AB 3500 Genetic Analyzer, AB 3500xL Genetic Analyzer, AB 3730 Genetic Analyzer, AB 3730xL Genetic Analyzer, AB 5500 Genetic Analyzer, AB 5500xl Genetic Analyzer, AB 5500xl-W Genetic Analysis System, AB SOLiD 3 Plus System, AB SOLiD 4 System, AB SOLiD 4hq System, AB SOLiD PI System, AB SOLiD System, AB SOLiD System 2.0, AB SOLiD System 3.0, BGISEQ-50, BGISEQ-500, Complete Genomics, DNBSEQ-G400, DNBSEQ-G400 FAST, DNBSEQ-G50, DNBSEQ-T7, Element AVITI, FASTASeq 300, GENIUS, GS111, Genapsys Sequencer, GenoCare 1600, GenoLab M, GridION, Helicos HeliScope, HiSeq X Five, HiSeq X Ten, Illumina Genome Analyzer, Illumina Genome Analyzer II, Illumina Genome Analyzer IIx, Illumina HiScanSQ, Illumina HiSeq 1000, Illumina HiSeq 1500, Illumina HiSeq 2000, Illumina HiSeq 2500, Illumina HiSeq 3000, Illumina HiSeq 4000, Illumina HiSeq X, Illumina MiSeq, Illumina MiniSeq, Illumina NovaSeq 6000, Illumina NovaSeq X, Illumina iSeq 100, Ion GeneStudio S5, Ion GeneStudio S5 Plus, Ion GeneStudio S5 Prime, Ion Torrent Genexus, Ion Torrent PGM, Ion Torrent Proton, Ion Torrent S5, Ion Torrent S5 XL, MGISEQ-2000RS, MinION, NextSeq 1000, NextSeq 2000, NextSeq 500, NextSeq 550, Onso, PacBio RS, PacBio RS II, PromethION, Revio, Sentosa SQ301, Sequel, Sequel II, Sequel IIe, Tapestri, UG 100, unspecified |
| file_name  | mandatory  | The name or relative pathname of a run data file. The field is used for all file types except paired fastq files.  |   | 
|  file_md5 | mandatory  | The MD5 checksum of the file. This field is mandatory if submitter do not use the Webin File Uploader or upload the checksum using a .md5 file. The field is used for all file types except paired fastq files.   |   | 
| forward_file_name  | mandatory  | The name or relative pathname of forward run data file. The field is only used for paired fastq files.  |   | 
|  forward_file_md5 | mandatory  | The MD5 checksum of the file. This field is mandatory if submitter do not use the Webin File Uploader or upload the checksum using a .md5 file. The field is only used for paired fastq files.  |   |
| reverse_file_name  | mandatory  | The name or relative pathname of reverse run data file. The field is only used for paired fastq files.  |   | 
|  reverse_file_md5 | mandatory  | The MD5 checksum of the reverse file. This field is mandatory if submitter do not use the Webin File Uploader or upload the checksum using a .md5 file. The field is only used for paired fastq files.   |   |
| file_format | mandatory    | Format of the sequence file(s). | bam, cram, fastq, PacBio_HDF5, OxfordNanopore_native |

## How to generate the template files

The template files (tsv, TODO: json and xlsx) are generated by the script [create_genomics_template.py](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/create_genomics_template.py) by merging the relevant ENA required fields (generated and stored in [ENA_experiment_metadata_fields](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/tree/main/genomics/ENA_experiment_metadata_fields)) with the SciLifeLab organisational metadata fields specified in [../organisation_metadata_fields.yml](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/organisational_metadata_fields.yml).

Within the folder [ENA_experiment_metadata_fields](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/tree/main/genomics/ENA_experiment_metadata_fields) the script [pull_ENA_exp_run_templates.py](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/ENA_experiment_metadata_fields/pull_ENA_exp_run_templates.py) fetches the ENA experiment and run metadata templates as specified in [ENA_target_metadata_fields.html](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/ENA_experiment_metadata_fields/ENA_target_metadata_fields.yml) from ENA's _xsd_ schema files stored at https://github.com/enasequence/webin-xml/tree/master/src/main/resources/uk/ac/ebi/ena/sra/schema. This script is based on the script [template_updater.py](https://github.com/ELIXIR-Belgium/ENA-metadata-templates/blob/main/scripts/template_updater.py), copyright @ Elixir Belgium and licensed under the MIT license.

To regenerate, execute the following steps. 
Install dependencies
```
pip install -r requirements.txt
```
If necessary, re-fetch ENA required fields 
```
cd ENA_experiment_metadata_fields
python pull_ENA_exp_run_templates.py
```
Recreate templates from `genomics` folder
```
python create_genomics_template.py
```


