import os
import json
from main import run
from dotenv import load_dotenv
load_dotenv()

#Remember upload the file in the "input" folder on "tests" folder
#This "For" read all files in the "input" folder
for file in os.listdir('tests/input/'):
  if file.endswith('.json'):
    #Similar to AWS Lambda - Don't edit!!
    event = json.load(open(f'tests/input/{file}', 'r', encoding='utf-8'))
    context = {}

    #Execute the main function
    response = json.dumps(run(event, context), indent=2)

    #Write a output file of result execution
    f = open(f'tests/output/{file}', 'w', encoding='utf-8')
    f.write(response)
    f.close()

    #Optional print the result on terminal
    #print(response)
