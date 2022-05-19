# Amazon Comprehend

## General info
Amazon Comprehend is a machine learning-powered service using natural language processing (NLP) to make it easy to find insights and relationships in text.

* input social media, emails, web pages, documents, transcripts, medical records (Comprehend Medical)
* extract key phrases, entities, sentiment, language, syntax topics and document classifications
* can train on our data

NLP service and text analytics, find insights and relationships in unstructured data

* can identify the language of the text
* extracts key phrases, places, people, brands or events
* understands how positive or negative the text is
* analyzes text using tokenization and parts of speech
* automatically organizes a collection of text files by topic

We can also use AutoML capabilities in Comprehend to build a custom set of entities or text classification models that are tailored uniquel

## Features
* keyp hrase extraction: find what a document is actually about. Returns key phrases and confidence
* sentiment analysis: find if it is negative/neutral/positive document + confidence
* syntax analysis: look at each word and detects verbs, nouns, adjectives, punctuation, ...
* entity recognition: is it talking about organization, time, person, value, ...
* medical named entity and relationship extraction (NERe): get info on unstructured medical notes
* custom entities: specify entities related to our business and find them in text
* language detection: used by amazon translate (the auto detect language), returns language and confidence
* custom classification: we train custom classification on our existing data (document has topic X, document 2 has topic Y, ...); train for future classification
* topic modeling: bring topics out of the model
* multiple language support

We can do real time analysis or offline

For real time analysis, we get

* entities detected in the text (person, organization, date, ...)
* key phrases
* language detection
* sentiment: neutral/negative/positive
* syntax

## Amazon Comprehend Medical

extract complex medical information from unstructured text

The service can identify medical information, such as
medical conditions, medications, dosages, strengths, and frequencies from a variety of
sources like doctor’s notes, clinical trial reports, and patient health records. 

can also identify the relationship among the extracted medication and test, treatment and procedure information for easier analysis
=> example: identify particular dosage, strength and frequency related to a specific medication from unstructured clinical notes

protects data privacy

## Use cases
* perform customer sentiment analysis on inbound messages to support the system
* create a system to label unstructured (clinical) data to assist in research and analysis
* determine the topics from transcribed audio recordings of company meetings

## Resources

FAQ: https://aws.amazon.com/comprehend/faqs/