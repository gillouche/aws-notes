# Amazon Translate

## General info
Amazon Translate is a neural machine, text translation service for language translation.
Neural machine translation is a form of language translation automation that uses deep learning models to deliver more 
accurate and more natural sounding translation than traditional statistical and rule-based translation algorithms.

neural machine translation service that delivers fast, high quality and affordable language translation

deliver more accurate and more natural sounding translation than traditional statistical and rule based translation algorithms

can localize content (websites, applications) for international users and easily translate large volumes of text efficiently

The translation can be done

* batch
* real time: very similar to google translate

The main page for Amazon translate is the metrics page where we see the successful request count, throttled ones, ...

## Custom terminology
to help the translation 

* brand names
* character names
* model names
* other unique content is translated exactly the way we need it

The input file can be CSV or Translation Memory eXchange (TMX) -> appropriate for proper names, brand names, etc

For CSV, the first column is the text, the other columns are the translations (columns header are the language code en, fr, ...)

TMX file has this format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
 <header
    creationtool="XYZTool" creationtoolversion="0"
    datatype="PlainText" segtype="sentence"
    adminlang="en-us" srclang="en"
    o-tmf="test"/>
 <body>
   <tu>
     <tuv xml:lang="en">
       <seg>Amazon</seg>
     </tuv>
     <tuv xml:lang="fr">
       <seg>Amazon</seg>
     </tuv>
     <tuv xml:lang="de">
       <seg>Amazon</seg>
     </tuv>
     <tuv xml:lang="es">
       <seg>Amazon</seg>
     </tuv>
   </tu>   
 </body>
</tmx>
```

## API
```python
import boto3

def lambda_handler(event, context):
    translate = boto3.client('translate')

    response = translate.translate_text(
        Text='my text',
        SourceLanguageCode = 'en',
        TargetLanguageCode = 'fr'       
    )

    return {
        'statusCode': 200,
        'body': response['TranslatedText']
    }
```

## Use cases
* enhance an online customer chat application to translate conversations in real time
* batch translate documents within a multilingual company
* create a news publishing solution to convert posted stories to multiple languages

## Resources

FAQ:  https://aws.amazon.com/translate/faqs/