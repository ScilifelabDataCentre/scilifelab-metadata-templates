# SciLifeLab Genomics Technical Metadata Template

The _SciLifeLab Genomics Technical Metadata Template_ is a data-type specific template, collecting __technical metadata for genomics data produced at the Genomics platform__. As such, it fulfills submission requirements from the main recipient repository _ENA_ ([European Nucleotide Archive](https://www.ebi.ac.uk/ena/)). 

In addition, the template includes SciLifeLab specific [organisational metadata fields](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/organisational_metadata_fields.yml) relevant for data provenance for the researcher as well as other metadata consumers at SciLifeLab. These can be omitted when submitting to public end repositories, such as ENA. 

## Contact
For __general questions__ about the _SciLifeLab Genomics Technical Metadata Template_, please contact data-management@scilifelab.se. 

For __specific questions regarding filled-in metadata files received as part of a data delivery from NGI__ as the data-producing unit, please contact support@ngisweden.se. 

## Contributors
The genomics template has been developed in collaboration between the Genomics Platform, NBIS and SciLifeLab Data Centre. The following people have contributed with their expertise (ordered by affiliation):
- Johannes Alneberg, NGI
- Anandashankar Anil, NGI
- Sara Ekberg, NGI
- Adrien Coulier, NGI
- Jonas Kjellin, NGI
- Sonja Mathias, SciLifeLab Data Centre
- Rickard Hammarén, SciLifeLab Data Centre
- Yvonne Kallberg, NBIS
- Niclas Jareborg, NBIS


## Formats 
The genomics template can be downloaded in the following __formats__:

- A [_genomics_technical_metadata.json_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata.json) listing all required metadata fields with their attribute descriptors and controlled vocabularies fetched from ENA where applicable, for reference. 
- A [ _genomics_technical_metadata.tsv_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata.tsv) containing only the field names as a header row, to be filled in with the information for individual runs (1 (single or paired) run per row). 
- A [_genomics_template_schema.json_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_template_schema.json) __schema__ against which a filled-in _.tsv_ can be validated to ensure that it complies with the template. 

## Example files
In addition, there are two __example__ files available that show how a filled-in _.tsv_ could look:
- [example_data/example-genomics_technical_metadata_bam.tsv](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/example_data/example-genomics_technical_metadata_bam.tsv): an example for a HiFi data experiment with a single .bam file.
- [example_data/example-genomics_technical_metadata_fastq.tsv](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/example_data/example-genomics_technical_metadata_fastq.tsv): an example for HiC and RNAseq data experiments with paired fastq files. 

## Validation
Last but not least, there exists a __validation__ script that can be used to validate a filled-in _.tsv_ against the template schema, [scripts/validate_json_schema.py](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/scripts/validate_json_schema.py). It can be passed a multi-row tsv to validate against the template schema as follows
```
python validate_json_schema.py path/to/your/tsv/file.tsv
```
Optionally, the schema can be specified using `python validate_json_schema.py path/to/your.tsv --schema path/to/schema.json` with the default being set as `../genomics_template_schema.json`. 

## Regarding data submissions to public end repositories (ENA)

The main recipient repositories for genomic data are [European Nucleotide Archive](https://www.ebi.ac.uk/ena/) (ENA) and [ArrayExpress](https://www.ebi.ac.uk/biostudies/arrayexpress). Note that the nucleotide sequencing data submitted to ArrayExpress is forwarded (by them via brokering) to ENA. The SciLifeLab Genomics Technical Metadata Template is designed to be compatible with the metadata requirements for data submissions to ENA. 

For an interactive submission of the technical metadata via its Webin Submissions Portal, ENA requires a single _.tsv_ file containing the technical fields listed as parts of the template below (curated from ENA.experiment and ENA.run object metadata). 

Specific notes on the collected metadata fields: 
- ENA submissions distinguish between submission of single read and paired reads. Some fields are only relevant if handling paired reads data stored as a pair of fastq files (`insert_size`, `reverse_file_name`, `reverse_file_md5`). In this case the file name path stored in `file_name` and the MD5 checksum stored in `file_md5` correspond to the ENA fields `forward_file_name` and `forward_file_md5`. 
    - The value of the field `library_layout` is set to distinguish between the `SINGLE` and `PAIRED` reads cases.
- The field `library_name` is populated by the data producing unit with the same value as the `experimental_sample_id` field and is required to be unique per file (pair). 
- The ENA fields `design_description`(not listed below) and `library_construction_protocol` cover largely the same information and are seen as redundant of each other. We decide to populate (only) `library_construction_protocol` for the SciLifeLab genomics template. 
- We programmatically fetch the controlled vocabularies accepted by ENA for the following fields
    - `instrument_model`
    - `library_source`
    - `library_selection`
    - `library_strategy`
    - `library_layout`
    - `file_type`


## List of collected metadata fields
<!-- START OF OVERVIEW TABLE -->
| Field Name | Requirement | Description | Controlled vocabulary |
| ---------- | ---------- | ------------ | ---------- |
| study_alias | mandatory_for_data_submitter | Accession number of the study (PRJEBxxxxxx), e.g. from the Studies report in the ENA Webin Portal.  |  
| sample_alias | mandatory_for_data_submitter | Accession number of the sample (SAMEAxxxxxx or ERSxxxxxx) that the sequencing was made on, from the Samples report in the ENA Webin Portal.  |  
| instrument_model | mandatory_for_data_producer | Model of the sequencing instrument.  | 454 GS, 454 GS 20, 454 GS FLX, 454 GS FLX Titanium, 454 GS FLX+, 454 GS Junior, AB 310 Genetic Analyzer, AB 3130 Genetic Analyzer, AB 3130xL Genetic Analyzer, AB 3500 Genetic Analyzer, AB 3500xL Genetic Analyzer, AB 3730 Genetic Analyzer, AB 3730xL Genetic Analyzer, AB 5500 Genetic Analyzer, AB 5500xl Genetic Analyzer, AB 5500xl-W Genetic Analysis System, AB SOLiD 3 Plus System, AB SOLiD 4 System, AB SOLiD 4hq System, AB SOLiD PI System, AB SOLiD System, AB SOLiD System 2.0, AB SOLiD System 3.0, AVITI 24, BGISEQ-50, BGISEQ-500, Complete Genomics, DNBSEQ-G400, DNBSEQ-G400 FAST, DNBSEQ-G50, DNBSEQ-G800, DNBSEQ-T10x4RS, DNBSEQ-T7, Element AVITI, FASTASeq 300, GENIUS, GS111, Genapsys Sequencer, GenoCare 1600, GenoLab M, GridION, Helicos HeliScope, HiSeq X Five, HiSeq X Ten, Illumina Genome Analyzer, Illumina Genome Analyzer II, Illumina Genome Analyzer IIx, Illumina HiScanSQ, Illumina HiSeq 1000, Illumina HiSeq 1500, Illumina HiSeq 2000, Illumina HiSeq 2500, Illumina HiSeq 3000, Illumina HiSeq 4000, Illumina HiSeq X, Illumina MiSeq, Illumina MiniSeq, Illumina NovaSeq 6000, Illumina NovaSeq X, Illumina NovaSeq X Plus, Illumina iSeq 100, Ion GeneStudio S5, Ion GeneStudio S5 Plus, Ion GeneStudio S5 Prime, Ion Torrent Genexus, Ion Torrent PGM, Ion Torrent Proton, Ion Torrent S5, Ion Torrent S5 XL, MGISEQ-2000RS, MinION, NextSeq 1000, NextSeq 2000, NextSeq 500, NextSeq 550, Onso, PacBio RS, PacBio RS II, PromethION, Revio, Sentosa SQ301, Sequel, Sequel II, Sequel IIe, Tapestri, UG 100, Vega, unspecified 
| library_name | mandatory_for_data_producer | The data producer's name for this library. Can be modified by submitter if desired. Should be unique per file (pair).  |  
| library_source | mandatory_for_data_producer | Specifies the type of source material that is being sequenced.  | GENOMIC, GENOMIC SINGLE CELL, TRANSCRIPTOMIC, TRANSCRIPTOMIC SINGLE CELL, METAGENOMIC, METATRANSCRIPTOMIC, SYNTHETIC, VIRAL RNA, OTHER 
| library_selection | mandatory_for_data_producer | Method used to enrich the target in the sequence library preparation.  | RANDOM, PCR, RANDOM PCR, RT-PCR, HMPR, MF, repeat fractionation, size fractionation, MSLL, cDNA, cDNA_randomPriming, cDNA_oligo_dT, PolyA, Oligo-dT, Inverse rRNA, Inverse rRNA selection, ChIP, ChIP-Seq, MNase, DNase, Hybrid Selection, Reduced Representation, Restriction Digest, 5-methylcytidine antibody, MBD2 protein methyl-CpG binding domain, CAGE, RACE, MDA, padlock probes capture method, other, unspecified 
| library_strategy | mandatory_for_data_producer | Sequencing technique used for this library.  | WGS, WGA, WXS, RNA-Seq, ssRNA-seq, snRNA-seq, miRNA-Seq, ncRNA-Seq, FL-cDNA, EST, Hi-C, ATAC-seq, WCS, RAD-Seq, CLONE, POOLCLONE, AMPLICON, CLONEEND, FINISHING, ChIP-Seq, MNase-Seq, DNase-Hypersensitivity, Bisulfite-Seq, CTS, MRE-Seq, MeDIP-Seq, MBD-Seq, Tn-Seq, VALIDATION, FAIRE-seq, SELEX, RIP-Seq, ChIA-PET, Synthetic-Long-Read, Targeted-Capture, Tethered Chromatin Conformation Capture, NOMe-Seq, ChM-Seq, GBS, Ribo-Seq, OTHER 
| library_layout | mandatory_for_data_producer | Specifies whether to expect single or paired configuration of reads.  | SINGLE, PAIRED 
| insert_size | mandatory_for_data_producer_if_paired_reads | The average size of the fragments that are being sequenced, not the length of the reads. The value recorded here represents the ideal insert size that the protocol aims to achieve.  |  
| library_construction_protocol | mandatory_for_data_producer | Free form text describing the protocol by which the sequencing library was constructed. Can be extended by submitter if necessary.  |  
| file_type | mandatory_for_data_producer | The run data file model.  | sra, srf, sff, fastq, fasta, tab, 454_native, 454_native_seq, 454_native_qual, Helicos_native, Illumina_native, Illumina_native_seq, Illumina_native_prb, Illumina_native_int, Illumina_native_qseq, Illumina_native_scarf, SOLiD_native, SOLiD_native_csfasta, SOLiD_native_qual, PacBio_HDF5, bam, cram, CompleteGenomics_native, OxfordNanopore_native 
| file_name | mandatory_for_data_producer | The name or relative pathname of a (forward) run data file.  If handling paired fastq files put the forward run data file name here.  |  
| file_md5 | mandatory_for_data_producer | The MD5 checksum of the (forward) file. If handling paired fastq files put the MD5 checksum of the forward run data file here.  |  
| reverse_file_name | mandatory_for_data_producer_if_paired_reads | The name or relative pathname of a run data file. This field is only used for paired fastq files.  |  
| reverse_file_md5 | mandatory_for_data_producer_if_paired_reads | The MD5 checksum of the reverse file. This field is used only for paired fastq files.  |  
| scilifelab_unit | mandatory_for_data_producer | SciLifeLab infrastructure unit that generated the associated data and metadata. May specify node within unit if applicable.  | National Genomics Infrastructure (NGI), NGI Stockholm, NGI Uppsala (SNP&SEQ Technology Platform), NGI Uppsala (Uppsala Genome Center), Ancient DNA 
| unit_internal_project_id | mandatory_for_data_producer | Project ID as assigned by the unit.  |  
| order_id | optional_for_data_producer | Order ID associated with the data and metadata delivery, if applicable.  |  
| experimental_sample_id | mandatory_for_data_producer | Experimental Sample IDs as assigned by the unit, 1 exp sample = 1 data file (pair).  |  
| associated_sample_id | mandatory_for_data_producer | Associated sample ID as shared by the researcher with the unit.  |  
| metadata_file_creation_date | mandatory_for_data_producer | Date of creation of the metadata file.  |  
| template_name | mandatory_for_data_producer | Name of the SciLifeLab metadata template used to collect the metadata.  |  
| template_version | mandatory_for_data_producer | Version of the metadata template used to collect the metadata.  |  
<!-- END OF OVERVIEW TABLE -->
