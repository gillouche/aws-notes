# AWS CodeGuru

## General Info
Amazon CodeGuru provides intelligent recommendations to improve code quality and identify an application’s most expensive lines of code.

You can integrate CodeGuru into existing software development workflows to automate code reviews.

CodeGuru continuously monitors an application’s performance in production.

Provides recommendations and on how to improve code quality, application performance, and reduce overall cost.

Secrets detection: hardcoded in code repositories, config files, API keys, passwords, SSH keys, access token, ...

Helps code quality

## Security detection
CodeGuru can detect many security issues such as:

* OWASP Top 10: checks for top web application security risks such as broken access control, injection, and data integrity failures 
* AWS API security best practices: check API security for Amazon Elastic Compute Cloud and AWS Key Management Service 
* AWS security best practices (AWS crypto is implemented to Amazon’s standards): apply Amazon’s internal security expertise to your code 
* Java crypto library best practices: check if Javax.Crypto.Cipher is initialized and called correctly 
* Python crypto library best practices: check if correct versions of Python hashing and cryptography algorithms are used 
* Secure web applications: check app-related security issues, such as LDAP injections 
* Sensitive information leaks: check for any leakage of personal or sensitive information (example: logging AWS account credentials in plain text)
* Input validation: checks for malformed or malicious data from untrusted sources