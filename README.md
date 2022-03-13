# gpt_web_pl

Prosta strona ktora:
  - pobiera polski TEKST
  - wysyla TEKST do API deepl 
  - otrzymuje TLUMACZENIE(EN_US)
  - przesyla TLUMACZENIE go do API openai
  - otrzymana ODPOWIEDZ z openai wysyla do API deepl(PL)
  - wyswietla to na stronie internetowej



Rozruch aplikacji

_$ export FLASK_ENV=development_

_$ flask run_
