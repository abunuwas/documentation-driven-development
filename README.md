# Simple example of documentation-driven development

1. Install the dependencies:

    `$ pipenv install`

    `$ npm install dredd`

2. Activate the environment:

    `$ pipenv shell`

3. Run the app:

    `$ FLASK_APP=app:app flask run`

    Visit the auto-generated documentation at 127.0.0.1:5000/docs

4. Run the Dredd tests:

    `$ ./node_modules/.bin/dredd oas.yaml http://127.0.0.1:5000  --hookfiles=./hooks.py --language=python --server "flask run"`
