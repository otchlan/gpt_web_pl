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
        content = request.form['content']

        if not content:
            flash('Contetnt is required', 'info')
        else:
            pass
            #todo wysłanie zapytania do GPT
            # return redirect(url_for('index'), Response=int_glob)
    return render_template('dane_do_back.html')


# temp_ppt = " mam na imie Technologia"
temp_ppt = "Możesz podać mi listę dostępnych zdecentralizowanych giełd proszę?"

"""  !!!DO DOKUMENTACJI!!! wazne nie dziala jako source_lang EN-US trzeba dawac samo EN, ale jako target language EN_US dziala"""
# def interacting_deepl(text=temp_ppt, source_lang='EN', target_lang='PL'):
# @app.route('/dis')
def interacting_deepl(text=temp_ppt, source_lang='PL', target_lang='EN-US'):
    print(' - integrating_deepl')
    translator = deepl.Translator(DEEPL_API_KEY)
    # print('source -- ', source_lang)
    # print('target -- ', target_lang)
    result_deepl = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    # return result_deepl.text
    return result_deepl


# @app.route('/clean')
# def interacting_model_gpt(engine='text-davinci-001', temperature=0.7, result_deepl=interacting_deepl):
def interacting_model_gpt(engine='text-davinci-001', temperature=0.7, result_deepl=temp_ppt):
    print(' - interacting_model_gpt')
    prompt = openai.Completion.create(
        engine=engine,
        prompt=result_deepl,  # dane podawane do API OPENAI
        temperature=0.3,
        # The temperature controls how much randomness is in the output
        # https://algowriting.medium.com/gpt-3-temperature-setting-101-41200ff0d0be
        max_tokens=20,
        top_p=1,
        frequency_penalty=0,
        # user='w dokumentacji - Provide user identifier',
        # stop="", # TODO powiedziec uzytkownikowi ze po nacisnieciu klawisza zapewne enter tworzy nowy blok wprowadzania
        # TODO sprawdzic jakie sa zmiany gdy user identifier jest, a jak go nie ma - mozna ustawic jakas sztywna temperature, albo kazac ulozyc historie lub vos bardziej logicznego np opisac cos/logicznego
        presence_penalty=0.3
    )

    prompt = gpt_prompt_cleaning(prompt)
    return render_template('index.html', content=prompt)


# @app.route('/clean')
def gpt_prompt_cleaning(prompt=interacting_model_gpt):
    prompt = repr(prompt)
    prompt = prompt.split('JSON:')
    prompt = str(prompt[1])
    prompt = prompt[1:]
    prompt = prompt[:-1] + '}'
    prompt = prompt.replace('null', 'None')
    prompt = eval(prompt)
    prompt = json.loads(json.dumps(prompt))
    prompt = prompt['choices']
    prompt = str(prompt)
    prompt = prompt.split("'text': '")
    prompt = prompt[1]
    prompt = prompt.replace("'}]", '')
    prompt = prompt[4:]
    return prompt

""" Test dzialania Exceptions """
def test_error():
    try:
        t = 4 + "g"
    except Exception as e:
        print("testowy error ", e)
    #return render_template(render_template('test_exception.html'))
    finally:
        print('blad obslugi')

@app.route("/index")
def index():
    print(' - index')
    result = 'Tu jest jakiś tekst po polsku. Jaka jest belgijska tradycyjna potrawa?'
    result = str(interacting_deepl(result))
    result = interacting_model_gpt(result_deepl=result)
    result = interacting_deepl(result, 'EN', 'PL')
    # result = 'ee'
    return render_template('index.html', content=result)
    # return render_template('index.html', content=result)

# TODO zobacz to na temat tego answers

# TODO rozpisac kazda mozliwosc przyjmowania i wlasciwosci promptu
# TODO wywietlanie odpowiedzi tylko a nie calego zwrotu
# TODO no i jakis prompt trzeba zrobic ogarniety do tego zeby marketing ogarnial
# TODO dodac advenced - z openai

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)