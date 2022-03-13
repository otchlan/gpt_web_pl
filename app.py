from flask import Flask, render_template, request
import deepl, os, openai
from dotenv import load_dotenv


""" Pobieranie kluczy API """
load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORG = os.getenv('OPENAI_ORG')

""" Inicjalizacja OpenAI """
openai.organization = OPENAI_ORG
openai.api_key = OPENAI_API_KEY

app = Flask(__name__, template_folder='templates')

#ppt = " mam na imie Technologia"
ppt = " inaczej"

"""
@app.post("/input/")
async def input_text(text: str = Form(...)):
    return {"text": text}
"""


@app.route("/test")
def deepl_in(text=ppt):
    #return {"message": "Hello World"}
    translator = deepl.Translator(DEEPL_API_KEY)
    global result_deepl
    result_deepl = translator.translate_text(text, source_lang='PL', target_lang='EN-US')
    result_deepl = result_deepl.text


    return render_template('index.html', content=result_deepl)


@app.route("/")
def index(text=ppt):
    translator = deepl.Translator(DEEPL_API_KEY)
    result_deepl = translator.translate_text(text, source_lang='PL', target_lang='EN-US')
    result_deepl = result_deepl.text

    #res = openai.Engine.retrieve('text-davinci-001')
    res = openai.Completion.create(
        engine='text-davinci-001',
        prompt=result_deepl, #dane podawane do API OPENAI
        temperature=0.7,
            # The temperature controls how much randomness is in the output
            # https://algowriting.medium.com/gpt-3-temperature-setting-101-41200ff0d0be
        max_tokens=10,
        top_p=1,
        frequency_penalty=0,
        # presecne_penalty=0.3
    )
    return render_template('index.html', content=res)
"""
TO DO
- zobacz to na temat tego answers
- 
- wywietlanie odpowiedzi tylko a nie calego zwrotu
- no i jakis prompt trzeba zrobic ogarniety do tego zeby marketing ogarnial
- dodac advenced
"""