# Amazon Lightsail

## General Info

Virtual Private Server service, single instance, not in a VPC/subnet (at least we don't have access).

EC2 T2 instances type with less features but cheaper. Less configuration available (disk size, ...)

Can pre-configure it for several applications:

* wordprocess
* Node.js
* LAMP stack
* Gitlab etc

OS supported:

* Amazon Linux
* Debian
* FreeBSD
* OpenSUSE
* Ubuntu
* Windows Server 2012 R2
* Windows Server 2016

We have a few choice to make such as Availability Zone, platform (Linux or Windows) and a blue print which can be an app+os or just the OS. The only app for windows is SQL server.

## Use case

we want one EC2 running all the time that is much simpler to manage and use (less configuration overall)

## Billing

pay per month, similar to an offer in a datacenter with different price for CPU, RAM, disk space, data transfer, ...
