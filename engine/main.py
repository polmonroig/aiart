from flask_cors import CORS
import model
import config

app = model.create_app(config)
# CORS(app, resources={r'/*': {'origins': 'https://aiart-2ddfd.firebaseapp.com'}}) DEPLOY APP
CORS(app, resources={r'/*': {'origins': '*'}})

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(debug=True, port=8080)
