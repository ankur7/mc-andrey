from flask import Flask
from build_markov_model import get_rhyme
application = app = Flask('wsgi')

@app.route('/')
def reroute():
  return '<h3>Please enter the number of lines to generate, like <br><pre>https://mcandrey.ngrok.com/10</pre></h3>'
@app.route('/<lines>')
def serve_rhyme(lines):
  if int(lines) > 30:
    return "<h3>Damn playa, that's a lot of rhymes."
  if int(lines) < 1:
    return "<h3>How's a rapper gonna make a rap with %s lines?" % int(lines)
  if int(lines) % 2 == 1:
    return '<h3>Enter an even number of lines. We need to make rhymes son.</h3>'
  rhyme = get_rhyme(lines)
  rhyme += '<br><b>* drops the mic *</b><br>'
  rhyme += '<title>MC Andrey (Markov)</title>'
  rhyme += '<br><i>freestyle rapping is basically applied markov chains - <a href="http://xkcd.com/210/">XKCD 210</a></i>'
  return rhyme

if __name__ == '__main__':
  app.run(debug=True)