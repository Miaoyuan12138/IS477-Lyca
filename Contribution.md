# Contribution.md

## Caroline Wen's Contributions (Pushed by Caroline Wen)

For this milestone, I focused on building the core technical components of our project.

I completed the full data integration workflow, including cleaning the unemployment dataset, aggregating monthly rates into annual values, selecting and processing the mental-health indicator, and merging both sources by state and year.

I generated the profiling outputs (missingness, coverage, summary tables) and produced the interim processed dataset. 

I also drafted the automation structure (run_all.sh, Snakemake skeleton), and organized the scripts for integration and quality checks. 

Overall, I initialize the technical implementation and ensured the workflow is reproducible for the next phase. (However, the data-acquisition automation is still pending and will be finalized in the next milestone. Also, the data integration logic may be further extended based on future analysis needs.)

## Lydia Li's Contributions (Pushed by Lydia Li)

For this milestone, I focused on documentation, ethics review, and preparing our workflow for reproducibility. I completed the licensing and ethics review for the BLS and CDC datasets and wrote the docs/Ethics.md file covering privacy, bias, and responsible-use issues. I organized the repository structure, added clear notes on data provenance, and drafted the first version of Reproduce.md.

I also created the template for scripts_acquire_data.py and updated metadata and source URL checks for all datasets. Overall, my work strengthened our documentation and ethics foundation and set up the structure needed for an automated, reproducible workflow in the next milestone.