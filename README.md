# aws-notes
Notes about AWS cloud for the certifications.

Notes are messy, contain duplicates and way too much content, so it is a mistake to read them.

Source:

* [Acloud.guru](https://acloudguru.com)
* [LinuxAcademy (dead)](www.linuxacademy.com)
* [DevOps pro](https://www.udemy.com/course/aws-certified-devops-engineer-professional-hands-on/learn/lecture/16349474?start=0)
* [Architect pro](https://www.udemy.com/course/aws-certified-solutions-architect-professional-training/learn/lecture/25490046?start=1#overview)
* [Data analytics specialty](https://www.udemy.com/course/aws-data-analytics/learn/lecture/14150621?start=0#overview)
* [Machine Learning specialty](https://www.udemy.com/course/aws-machine-learning/learn/lecture/16368832?start=0)

## Requirements
* python3
* pandoc
* xelatex
* bash

## Build
First generate the index of the services 

```bash
python3 generate_index.py
```

This creates a build directory with some markdown files:

* build/archi.md
* build/big_data.md
* build/complete.md
* build/devops.md
* build/ML.md
* index.md

The index.md is a document with link to the different services in the repository.

Then execute the script create_pdf.sh script to generate the PDF from these markdowns in the output directory.

```bash
bash create_pdf.sh
```

## Certifications

* DevOps pro
* Archi pro
* Machine Learning specialty
* Data analytics specialty
* Developer associate
* SysOps associate
