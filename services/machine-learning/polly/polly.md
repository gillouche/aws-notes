# Amazon Polly

## General info

service that turns text into lifelike speech (Text to speech TTS), create apps that talk (polly = parrot)

advanced deep learning technologies to synthesize speech that sounds like a human voice

consistent fast response time required to support real time interactive dialog

we can cache and save Polly's speech audio to replay offline and redistribute

send text to API and receive standard audio file (MP3) or play it directly

## Options
includes 47 lifelike voices spread across 24 languages

## Data input
supports UTF-8 input, plain (ASCII) text or SSML

The data input can either be text or Speech Synthesis Markup Language (SSML) that allows us to be more specific
on how we want a specific text to be pronounce. Speech Synthesis Markup Language (SSML) is an XML-based markup language used with speech synthesis applications. 
SSML is a recommendation of the W3C's voice browser working group.

SSML gives control over

* emphasis
* pronounciation
* breathing
* whispering
* speech rate
* pitch
* pauses

```html
<speak>What do you think of this course?<amazon:effect name="whispered">I think it is great.</amazon:effect></speak>
```

Speech Marks can encode when sentence/word starts and ends in the audio stream -> useful for lip-synching animation (like animated character)

## Customizations
supports customizations with custom lexicons (specific terminology, ..) that we can upload to AWS

* customize pronouciation of specific words & phrases
* ex: "World Wide Web Consortium" instead of W3C

"you can modify speech by uploading an applying lexicons, which provide a mapping between words, their written representations,
and their pronounciations suitable for use in speech synthesis. You can apply up to five lexicons per language in the console.
These lexicons are applied in a top-down order where the first entry in the list has precedence over all the other entries."

## Use cases
* create accessibility tools to read web content
* provide automatically generated announcements via a public address (PA) systsem
* create automated voice response (AVR) solution for a telephony systems (including Amazon Connect)
    * transcribe what is said on the phone (Amazon Transcribe?)
    * analyze
    * prepare response
    * use polly to say it

Not only useful to read stuff but to also talk to people

## Billing

pay per the number of characters we convert to speech

## Resources

FAQ: https://aws.amazon.com/polly/faqs/
