# AWS Shield

## General Info

* Service that protects CloudFront (default, for free) and Route 53 services with basic features. 
* Advanced features has CloudFront, Route 53, ELB, EC2, EIP, ... 
* Safeguards web application running on AWS with always-on detection and automatic inline mitigations 
* Helps to minimize application downtime and latency 
* Free service that protects all AWS customers on Elastic Load Balancing (ELB), Amazon CloudFront and Route 53.
* closely related to WAF
* two tiers:
  * standard: no cost
  * advanced
    * Always-on 
    * Protects against SYN/UDP floods, Reflection attacks, and other layers 3/4 attacks 
    * flow based monitoring of network traffic and active application monitoring to provide near real-time notification of DDoS attacks. 
    * DDoS response team (DRT) 24x7 to manage and mitigate application layer DDoS attacks 
    * Protects AWS bill against higher fees due to Elastic Load Balancing (ELB), CloudFront and Route 53 usage spikes during DDoS attacks. 
    * $3000 per month and 1 year commitment

Remember
* basic, free, enabled by default on cloudfront
* anything else, we need shield advanced