# Amazon Lex

## General info
* billed as the inner workings of Alexa
* natural language chatbot engine
* a bot is built around intents
    * utterances invoke intents ("I want to order a pizza")
    * lambda functions are invoked to fulfill the intent
    * slots specify extra information needed by the intent (pizza size, toppings, crust type, when to deliver, ...)
* can deploy to AWS mobile SDK, Facebook Messenger, Slack and Twilio

=> not as smart as it sounds since we need to think about the questions/answers and put the configuration ourselves

Amazon Lex is a service for building conversational interfaces into applications using voice and text. 
Amazon Lex uses automatic speech recognition (ASR) for converting speech to text, and natural language understanding (NLU) 
to recognize the intent of the text, enabling us to build applications with lifelike conversational interactions (e.g. chatbots).

same technology that powers Alexa, chatbots. It is voice enabled or text and handles

* automatic speech recognition (ASR)
* natural language understanding (NLU): listen to what we say or what we type and try to understand

service for building conversational interfaces into any application using voice and text (chatbots, ...)

advanced deep learning functionalities of automatic speech recognition (ASR) for converting speech to text and natural
language understanding to recognize the intent of the text, to enable us to build apps with highly engaging user experiences and lifelike
conversational interactions.

The service is not available everywhere, only the main region (Ireland, N Virginia, Sydney, Oregon)

## Creation in console
Easy to create a custom bot, just give it a name, choose the output voice (can be none which will be text).
We configure a session timeout (5 minutes, ...), IAM role and if the bot is subject to Children's Online Privacy Protection Act (COPPA).

Once it is created, we want to create an intent to help the service know what it should expect.3
We can help the detection with sample utterances (I would like to book a flight). We can also define "Slots" which will be looked
for by the chatbot:

* name: teaType
* slot type: lots of predefined type such as airlines, animal, artist, city, books, colors, ...
* prompt: the text that will be displayed 

If we created a sample utterances, the slots will be checked against that utterances to reply the prompt message.

* I am making a cup of tea.
* I am making a cup of {teaType} tea. => this is the slot that will be triggered
* I would like a {teaType} tea about now

Based on the utterances, AWS will learn similarity and accept them as well so we don't have to specify everything.

We then define the responses that will be picked randomly: I hope you enjoy your {teaType} tea!

Finally, we build it, test it and publish.

We can also trigger lambdas that will do some actions such as calling services.

## Use cases
* create a chatbot that triages customer support requests directly on the product page of a website
* create an automated receptionist that directs people as they enter a building
* provide an interactive voice interface to an application

## Resources
FAQ: https://aws.amazon.com/lex/faqs/

