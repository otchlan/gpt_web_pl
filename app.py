from flask import Flask, render_template, request, url_for, flash, redirect
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

session_sec__key = os.urandom(24).hex()

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = session_sec__key

messages = [
    {'title': 'Message one',
     'content': 'Messaage one content'},
    {'title': 'Message two',
     'content': 'Messaage two content'}
]
""" WPROWADZANIE ZE STRONY """
@app.route('/cr/', methods=('GET', 'POST'))
def cr():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cos = request.form['cos']

        if not title:
            flash('Title is required')
        elif not content:
            flash('Contetnt is required')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))
    return render_template('dane_do_back.html')

#ppt = " mam na imie Technologia"
ppt = " inaczej"

@app.route("/test_dl")
def deepl_in(text=ppt):
    #return {"message": "Hello World"}
    translator = deepl.Translator(DEEPL_API_KEY)
    global result_deepl
    result_deepl = translator.translate_text(text, source_lang='PL', target_lang='EN-US')
    result_deepl = result_deepl.text

    return render_template('index.html', content=result_deepl)


@app.route("/rose")
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
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        #presecne_penalty=0.3
    )
    return render_template('index.html', content=res)
"""
TO DO
- zobacz to na temat tego answers
- 
- rozpisac kazda mozliwosc przyjmowania i wlasciwosci promptu
- wywietlanie odpowiedzi tylko a nie calego zwrotu
- no i jakis prompt trzeba zrobic ogarniety do tego zeby marketing ogarnial
- dodac advenced
"""