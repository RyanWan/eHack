import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EmotionOptions,EntitiesOptions, KeywordsOptions

file = open("review.txt","r")
text = file.read()
file.close()

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='9e8bc323-edf3-4168-9a3d-34836e2c441d',
  password='NyDxwI1puwiW',
  version='2017-02-27')

response = natural_language_understanding.analyze(
text=text,
  features=Features(
    entities=EntitiesOptions(
      emotion=True,
      sentiment=True,
      limit=2),
    keywords=KeywordsOptions(
      emotion=True,
      sentiment=True,
      limit=2)))

print(json.dumps(response, indent=2))
