# Amazon Simple Email Service (SES)

## General Info

Used to send an emails like a newsletter. This is different than SNS which sends an email to a topic where people are subscribed to.

=> SNS sends notifications to a topic while SES is used to send marketing notification and transactional emails. 

It is needed to confirm the subscription to SES by email (prevents spam) or we cannot use SES to send email to the address.

The email that is verified is used to send the email: myemail@gmail.com via awazonses.com

SES is meant for sending high volume email efficiently and securely. We can send email **without recipient's consent**.

SNS is meant as a channel pub/sub service. The end-user **must first subscribe** and approve that subscription through email before amazon delivers emails from the subscribed channel to the end user.
