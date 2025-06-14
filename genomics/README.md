# SciLifeLab Genomics Technical Metadata Template
The main recipient repositories for genomic data are [European Nucleotide Archive](https://www.ebi.ac.uk/ena/) (ENA) and [ArrayExpress](https://www.ebi.ac.uk/biostudies/arrayexpress). Note that the nucleotide sequencing data submitted to ArrayExpress is forwarded (by them via brokering) to ENA.

For this purpose data type specific templates are created, aiming to capture technical metadata for genomics data produced at the Genomics platform, compatible with submission requirements from ENA and ArrayExpress. In addition, the templates include SciLifeLab specific [organisational metadata fields](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/organisational_metadata_fields.yml) relevant for data provenance for the researcher as well as other metadata consumers at SciLifeLab. These can be omitted when submitting to ENA. 

The genomics template can be downloaded in the following formats:
- [Single read _.tsv_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata_single_read.tsv)
- [Paired reads _.tsv_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata_paired_reads.tsv)
- [Single read _.json_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata_single_read.json), includes CV terms
- [Paired reads _.json_](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/genomics_technical_metadata_paired_reads.json), includes CV terms


The _.tsv_ files contain only the field names, whereas the _.json_ files include both the high-level template description and version number as well as all attribute field descriptors and the controlled vocabularies fetched from ENA where applicable.

Both the _.tsv_ and _.json_ files are split between the cases for single and paired reads to comply with the format and fields required for interactive submission to ENA using the Webin Portal. 

Within a template each template field needs to have:
- Field name
- Level of requirement/cardinality (mandatory vs optional)
    - `mandatory_for_data_producer`: to be filled in by the data producing facility as far as possible
    - `mandatory_for_data_submitter`: to be filled in by the data submitter, not expected to be known by the data producing facility
- Description
- List of controlled vocabulary terms, if applicable taken from ENA
- Target end repository, thus far interactive submissions to ENA
- Target end repository (field) name
- Target end repository (field) description



### Regarding submissions to ENA

For an interactive submission of the technical metadata via its Webin Submissions Portal, ENA requires a single _.tsv_ file containing the technical fields listed as parts of the templates below (curated from ENA.experiment and ENA.run object metadata). 

Note: 
- ENA submissions distinguish between submission of single read and paired reads. Some fields are only relevant if handling single read data (`file_name`, `file_md5`) or paired reads data (`insert_size`, `forward_file_name`, `forward_file_md5`, `reverse_file_name`, `reverse_file_md5`).
- ENA fields `design_description`(not listed below) and `library_construction_protocol` cover largely the same information and are seen as redundant of each other. We decide to populate (only) `library_construction_protocol` for the SciLifeLab genomics template. 
- We programmatically fetch the controlled vocabularies accepted by ENA for the following fields
    - `instrument_model`
    - `library_source`
    - `library_selection`
    - `library_strategy`
    - `library_layout`
    - `file_type`


## The Genomics technical metadata template for single read data
<!-- START OF SINGLE READ TABLE -->
| Field Name | Requirement | Description | Controlled vocabulary |
| ---------- | ---------- | ------------ | ---------- |
| study_alias | mandatory_for_data_submitter | Accession number of the study (PRJEBxxxxxx), e.g. from the Studies report in the ENA Webin Portal.  |  
| sample_alias | mandatory_for_data_submitter | Accession number of the sample (SAMEAxxxxxx or ERSxxxxxx) that the sequencing where made on, from the Samples report in the ENA Webin Portal, or the sample_alias.  |  
| instrument_model | mandatory_for_data_producer | Model of the sequencing instrument.  | 454 GS, 454 GS 20, 454 GS FLX, 454 GS FLX Titanium, 454 GS FLX+, 454 GS Junior, AB 310 Genetic Analyzer, AB 3130 Genetic Analyzer, AB 3130xL Genetic Analyzer, AB 3500 Genetic Analyzer, AB 3500xL Genetic Analyzer, AB 3730 Genetic Analyzer, AB 3730xL Genetic Analyzer, AB 5500 Genetic Analyzer, AB 5500xl Genetic Analyzer, AB 5500xl-W Genetic Analysis System, AB SOLiD 3 Plus System, AB SOLiD 4 System, AB SOLiD 4hq System, AB SOLiD PI System, AB SOLiD System, AB SOLiD System 2.0, AB SOLiD System 3.0, BGISEQ-50, BGISEQ-500, Complete Genomics, DNBSEQ-G400, DNBSEQ-G400 FAST, DNBSEQ-G50, DNBSEQ-T10x4RS, DNBSEQ-T7, Element AVITI, FASTASeq 300, GENIUS, GS111, Genapsys Sequencer, GenoCare 1600, GenoLab M, GridION, Helicos HeliScope, HiSeq X Five, HiSeq X Ten, Illumina Genome Analyzer, Illumina Genome Analyzer II, Illumina Genome Analyzer IIx, Illumina HiScanSQ, Illumina HiSeq 1000, Illumina HiSeq 1500, Illumina HiSeq 2000, Illumina HiSeq 2500, Illumina HiSeq 3000, Illumina HiSeq 4000, Illumina HiSeq X, Illumina MiSeq, Illumina MiniSeq, Illumina NovaSeq 6000, Illumina NovaSeq X, Illumina NovaSeq X Plus, Illumina iSeq 100, Ion GeneStudio S5, Ion GeneStudio S5 Plus, Ion GeneStudio S5 Prime, Ion Torrent Genexus, Ion Torrent PGM, Ion Torrent Proton, Ion Torrent S5, Ion Torrent S5 XL, MGISEQ-2000RS, MinION, NextSeq 1000, NextSeq 2000, NextSeq 500, NextSeq 550, Onso, PacBio RS, PacBio RS II, PromethION, Revio, Sentosa SQ301, Sequel, Sequel II, Sequel IIe, Tapestri, UG 100, unspecified 
| library_name | mandatory_for_data_producer | The data producer's name for this library. Can be modified by submitter if desired. Should be unique per file (pair).  |  
| library_source | mandatory_for_data_producer | Specifies the type of source material that is being sequenced.  | GENOMIC, GENOMIC SINGLE CELL, TRANSCRIPTOMIC, TRANSCRIPTOMIC SINGLE CELL, METAGENOMIC, METATRANSCRIPTOMIC, SYNTHETIC, VIRAL RNA, OTHER 
| library_selection | mandatory_for_data_producer | Method used to enrich the target in the sequence library preparation.  | RANDOM, PCR, RANDOM PCR, RT-PCR, HMPR, MF, repeat fractionation, size fractionation, MSLL, cDNA, cDNA_randomPriming, cDNA_oligo_dT, PolyA, Oligo-dT, Inverse rRNA, Inverse rRNA selection, ChIP, ChIP-Seq, MNase, DNase, Hybrid Selection, Reduced Representation, Restriction Digest, 5-methylcytidine antibody, MBD2 protein methyl-CpG binding domain, CAGE, RACE, MDA, padlock probes capture method, other, unspecified 
| library_strategy | mandatory_for_data_producer | Sequencing technique used for this library.  | WGS, WGA, WXS, RNA-Seq, ssRNA-seq, snRNA-seq, miRNA-Seq, ncRNA-Seq, FL-cDNA, EST, Hi-C, ATAC-seq, WCS, RAD-Seq, CLONE, POOLCLONE, AMPLICON, CLONEEND, FINISHING, ChIP-Seq, MNase-Seq, DNase-Hypersensitivity, Bisulfite-Seq, CTS, MRE-Seq, MeDIP-Seq, MBD-Seq, Tn-Seq, VALIDATION, FAIRE-seq, SELEX, RIP-Seq, ChIA-PET, Synthetic-Long-Read, Targeted-Capture, Tethered Chromatin Conformation Capture, NOMe-Seq, ChM-Seq, GBS, Ribo-Seq, OTHER 
| library_layout | mandatory_for_data_producer | Specifies whether to expect single, paired, or other configuration of reads.  | SINGLE, PAIRED 
| library_construction_protocol | mandatory_for_data_producer | Free form text describing the protocol by which the sequencing library was constructed. Can be extended by submitter if necessary.  |  
| file_type | mandatory_for_data_producer | The run data file model.  | sra, srf, sff, fastq, fasta, tab, 454_native, 454_native_seq, 454_native_qual, Helicos_native, Illumina_native, Illumina_native_seq, Illumina_native_prb, Illumina_native_int, Illumina_native_qseq, Illumina_native_scarf, SOLiD_native, SOLiD_native_csfasta, SOLiD_native_qual, PacBio_HDF5, bam, cram, CompleteGenomics_native, OxfordNanopore_native 
| file_name | mandatory_for_data_producer | The name or relative pathname of a run data file. This field is used for all file types except paired fastq files.  |  
| file_md5 | mandatory_for_data_producer | The MD5 checksum of the file. This field is used for all file types except paired fastq files.  |  
| scilifelab_unit | mandatory_for_data_producer | SciLifeLab infrastructure unit that generated the associated data and metadata.  | National Genomics Infrastructure, Ancient DNA 
| unit_internal_project_id | mandatory_for_data_producer | Project ID as assigned by the unit.  |  
| order_id | optional_for_data_producer | Order ID associated with the data and metadata delivery, if applicable.  |  
| experimental_sample_id | mandatory_for_data_producer | Experimental Sample IDs as assigned by the unit, 1 exp sample = 1 data file (pair).  |  
| associated_sample_id | optional_for_data_producer | Associated sample ID as shared by the researcher with the unit.  |  
| delivery_date | mandatory_for_data_producer | Date of delivery of metadata and data.  |  
| template_name | mandatory_for_data_producer | Name of the SciLifeLab metadata template used to collect the metadata.  |  
| template_version | mandatory_for_data_producer | Version of the metadata template used to collect the metadata.  |  
<!-- END OF SINGLE READ TABLE -->

## The Genomics technical metadata for paired reads
<!-- START OF PAIRED READS TABLE -->
| Field Name | Requirement | Description | Controlled vocabulary |
| ---------- | ---------- | ------------ | ---------- |
| study_alias | mandatory_for_data_submitter | Accession number of the study (PRJEBxxxxxx), e.g. from the Studies report in the ENA Webin Portal.  |  
| sample_alias | mandatory_for_data_submitter | Accession number of the sample (SAMEAxxxxxx or ERSxxxxxx) that the sequencing where made on, from the Samples report in the ENA Webin Portal, or the sample_alias.  |  
| instrument_model | mandatory_for_data_producer | Model of the sequencing instrument.  | 454 GS, 454 GS 20, 454 GS FLX, 454 GS FLX Titanium, 454 GS FLX+, 454 GS Junior, AB 310 Genetic Analyzer, AB 3130 Genetic Analyzer, AB 3130xL Genetic Analyzer, AB 3500 Genetic Analyzer, AB 3500xL Genetic Analyzer, AB 3730 Genetic Analyzer, AB 3730xL Genetic Analyzer, AB 5500 Genetic Analyzer, AB 5500xl Genetic Analyzer, AB 5500xl-W Genetic Analysis System, AB SOLiD 3 Plus System, AB SOLiD 4 System, AB SOLiD 4hq System, AB SOLiD PI System, AB SOLiD System, AB SOLiD System 2.0, AB SOLiD System 3.0, BGISEQ-50, BGISEQ-500, Complete Genomics, DNBSEQ-G400, DNBSEQ-G400 FAST, DNBSEQ-G50, DNBSEQ-T10x4RS, DNBSEQ-T7, Element AVITI, FASTASeq 300, GENIUS, GS111, Genapsys Sequencer, GenoCare 1600, GenoLab M, GridION, Helicos HeliScope, HiSeq X Five, HiSeq X Ten, Illumina Genome Analyzer, Illumina Genome Analyzer II, Illumina Genome Analyzer IIx, Illumina HiScanSQ, Illumina HiSeq 1000, Illumina HiSeq 1500, Illumina HiSeq 2000, Illumina HiSeq 2500, Illumina HiSeq 3000, Illumina HiSeq 4000, Illumina HiSeq X, Illumina MiSeq, Illumina MiniSeq, Illumina NovaSeq 6000, Illumina NovaSeq X, Illumina NovaSeq X Plus, Illumina iSeq 100, Ion GeneStudio S5, Ion GeneStudio S5 Plus, Ion GeneStudio S5 Prime, Ion Torrent Genexus, Ion Torrent PGM, Ion Torrent Proton, Ion Torrent S5, Ion Torrent S5 XL, MGISEQ-2000RS, MinION, NextSeq 1000, NextSeq 2000, NextSeq 500, NextSeq 550, Onso, PacBio RS, PacBio RS II, PromethION, Revio, Sentosa SQ301, Sequel, Sequel II, Sequel IIe, Tapestri, UG 100, unspecified 
| library_name | mandatory_for_data_producer | The data producer's name for this library. Can be modified by submitter if desired. Should be unique per file (pair).  |  
| library_source | mandatory_for_data_producer | Specifies the type of source material that is being sequenced.  | GENOMIC, GENOMIC SINGLE CELL, TRANSCRIPTOMIC, TRANSCRIPTOMIC SINGLE CELL, METAGENOMIC, METATRANSCRIPTOMIC, SYNTHETIC, VIRAL RNA, OTHER 
| library_selection | mandatory_for_data_producer | Method used to enrich the target in the sequence library preparation.  | RANDOM, PCR, RANDOM PCR, RT-PCR, HMPR, MF, repeat fractionation, size fractionation, MSLL, cDNA, cDNA_randomPriming, cDNA_oligo_dT, PolyA, Oligo-dT, Inverse rRNA, Inverse rRNA selection, ChIP, ChIP-Seq, MNase, DNase, Hybrid Selection, Reduced Representation, Restriction Digest, 5-methylcytidine antibody, MBD2 protein methyl-CpG binding domain, CAGE, RACE, MDA, padlock probes capture method, other, unspecified 
| library_strategy | mandatory_for_data_producer | Sequencing technique used for this library.  | WGS, WGA, WXS, RNA-Seq, ssRNA-seq, snRNA-seq, miRNA-Seq, ncRNA-Seq, FL-cDNA, EST, Hi-C, ATAC-seq, WCS, RAD-Seq, CLONE, POOLCLONE, AMPLICON, CLONEEND, FINISHING, ChIP-Seq, MNase-Seq, DNase-Hypersensitivity, Bisulfite-Seq, CTS, MRE-Seq, MeDIP-Seq, MBD-Seq, Tn-Seq, VALIDATION, FAIRE-seq, SELEX, RIP-Seq, ChIA-PET, Synthetic-Long-Read, Targeted-Capture, Tethered Chromatin Conformation Capture, NOMe-Seq, ChM-Seq, GBS, Ribo-Seq, OTHER 
| library_layout | mandatory_for_data_producer | Specifies whether to expect single, paired, or other configuration of reads.  | SINGLE, PAIRED 
| insert_size | mandatory_for_data_producer | The average size of the fragments that are being sequenced, not the length of the reads.  |  
| library_construction_protocol | mandatory_for_data_producer | Free form text describing the protocol by which the sequencing library was constructed. Can be extended by submitter if necessary.  |  
| file_type | mandatory_for_data_producer | The run data file model.  | sra, srf, sff, fastq, fasta, tab, 454_native, 454_native_seq, 454_native_qual, Helicos_native, Illumina_native, Illumina_native_seq, Illumina_native_prb, Illumina_native_int, Illumina_native_qseq, Illumina_native_scarf, SOLiD_native, SOLiD_native_csfasta, SOLiD_native_qual, PacBio_HDF5, bam, cram, CompleteGenomics_native, OxfordNanopore_native 
| forward_file_name | mandatory_for_data_producer | The name or relative pathname of a run data file. This field is used for paired fastq files.  |  
| forward_file_md5 | mandatory_for_data_producer | The MD5 checksum of the forward file. This field is used for paired fastq files.  |  
| reverse_file_name | mandatory_for_data_producer | The name or relative pathname of a run data file. This field is used for paired fastq files.  |  
| reverse_file_md5 | mandatory_for_data_producer | The MD5 checksum of the reverse file. This field is used for paired fastq files.  |  
| scilifelab_unit | mandatory_for_data_producer | SciLifeLab infrastructure unit that generated the associated data and metadata.  | National Genomics Infrastructure, Ancient DNA 
| unit_internal_project_id | mandatory_for_data_producer | Project ID as assigned by the unit.  |  
| order_id | optional_for_data_producer | Order ID associated with the data and metadata delivery, if applicable.  |  
| experimental_sample_id | mandatory_for_data_producer | Experimental Sample IDs as assigned by the unit, 1 exp sample = 1 data file (pair).  |  
| associated_sample_id | optional_for_data_producer | Associated sample ID as shared by the researcher with the unit.  |  
| delivery_date | mandatory_for_data_producer | Date of delivery of metadata and data.  |  
| template_name | mandatory_for_data_producer | Name of the SciLifeLab metadata template used to collect the metadata.  |  
| template_version | mandatory_for_data_producer | Version of the metadata template used to collect the metadata.  |  
<!-- END OF PAIRED READS TABLE -->

## How to generate the template files

The template files (_.tsv_, _.json_) are generated by the script [scripts/create_genomics_template.py](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/scripts/create_genomics_template.py) by merging the relevant technical fields (stored with controlled vocabularies in [technical_metadata_fields_incl_ENA_CVs.json](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/tree/main/genomics/technical_metadata_fields_incl_ENA_CVs.json)) with the SciLifeLab organisational metadata fields specified in [../organisation_metadata_fields.yml](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/organisational_metadata_fields.yml).

Within the [scripts](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/tree/main/genomics/scripts) folder [update_ENA_controlled_vocabs_.py](https://github.com/ScilifelabDataCentre/scilifelab-metadata-templates/blob/main/genomics/scripts/update_ENA_controlled_vocabs.py) fetches the controlled vocabularies for relevant fields from ENA's _xsd_ schema files stored at https://github.com/enasequence/webin-xml/tree/master/src/main/resources/uk/ac/ebi/ena/sra/schema. This script is based on the script [template_updater.py](https://github.com/ELIXIR-Belgium/ENA-metadata-templates/blob/main/scripts/template_updater.py), copyright @ Elixir Belgium and licensed under the MIT license.

To regenerate, execute the following steps from the `scripts` folder. 
Install dependencies
```
pip install -r requirements.txt
```
If necessary, re-fetch ENA controlled vocabulary terms 
```
python update_ENA_controlled_vocabs.py
```
Recreate templates
```
python create_genomics_template.py
```

