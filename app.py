from flask import Flask, render_template, request, url_for, flash, redirect
import deepl
import os
import openai
import json
from dotenv import load_dotenv


""" Pobieranie kluczy API """
load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORG = os.getenv('OPENAI_ORG')

""" Inicjalizacja OpenAI """
openai.organization = OPENAI_ORG
openai.api_key = OPENAI_API_KEY

session_sec_key = os.urandom(24).hex()

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = session_sec_key

""" Tymczasowy zbir testowy dla wprowadzanych danych z formularza"""
messages = [
    {'title': 'Message one',
     'content': 'Messaage one content'},
    {'title': 'Message two',
     'content': 'Messaage two content'}
]
""" WPROWADZANIE ZE STRONY """
""" https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application """
@app.route('/cr/', methods=('GET', 'POST'))
def cr():
    """Kod ktory uzywany jest do przechwytuwania danych pochodzcych z fontu i przekazuje je na backend"""
    # todo zobaczyc jak podpisac otrzymane dane pod jakies zmienne zeby potem moglybyc przetwarzane dalej
    print(" - dane do back(cr)")
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


# temp_ppt = " mam na imie Technologia"
temp_ppt = " infinity"


@app.route("/dl")  # testy
# TODO co zrobic zeby dzialal source_lang='EN_US' bo wywala blad, a na 'PL' dziala
# def deepl_in(text=temp_ppt, source_lang='EN_US', target_lang='PL'):
def deepl_in(text=temp_ppt, source_lang='PL', target_lang='PL'):
    print(' - deepl_in')
    return render_template('index.html', content=interacting_deepl(text, source_lang, target_lang))


def interacting_deepl(text=temp_ppt, source_lang='PL', target_lang='EN-US'):
    print(' - integrating_deepl')
    translator = deepl.Translator(DEEPL_API_KEY)
    # print('source -- ', source_lang)
    # print('target -- ', target_lang)
    result_deepl = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result_deepl.text


def interacting_model_gpt(engine='text-davinci-001', temperature=0.7, result_deepl=interacting_deepl()):
    print('interacting_model_gpt')
    prompt = openai.Completion.create(
        engine=engine,
        prompt=result_deepl,  # dane podawane do API OPENAI
        temperature=0.7,
        # The temperature controls how much randomness is in the output
        # https://algowriting.medium.com/gpt-3-temperature-setting-101-41200ff0d0be
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        user='w dokumentacji - Provide user identifier',
        stop="", # TODO powiedziec uzytkownikowi ze po nacisnieciu klawisza zapewne enter tworzy nowy blok wprowadzania
        # TODO sprawdzic jakie sa zmiany gdy user identifier jest, a jak go nie ma - mozna ustawic jakas sztywna temperature, albo kazac ulozyc historie lub vos bardziej logicznego np opisac cos/logicznego
        presence_penalty=0.3
    )
    print(type(prompt))
    return prompt

# todo TO TERAZ ZROBIC
"""
@app.route('/clean')
def gpt_prompt_cleaning(prompt=interacting_model_gpt):
    print(' - gpt_prompt_cleaning')
    temp_prompt = prompt
    data = json.loads(temp_prompt)S
    return data
"""

@app.route("/index")
def index():
    print(' - index')
    # return gpt_prompt_cleaning()
    return interacting_model_gpt()
    #return render_template('index.html', content=res)

# TODO zobacz to na temat tego answers

# TODO rozpisac kazda mozliwosc przyjmowania i wlasciwosci promptu
# TODO wywietlanie odpowiedzi tylko a nie calego zwrotu
# TODO no i jakis prompt trzeba zrobic ogarniety do tego zeby marketing ogarnial
# TODO dodac advenced - z openai