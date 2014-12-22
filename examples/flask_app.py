from flask import Flask, request, redirect, session
from flask.json import jsonify

import pokitdok


#Get your client id and client secret at https://platform.pokitdok.com
client_id = "<your client id>"
client_secret = "<your client secret>"

#Set up your Redirect URI in App Settings on https://platform.pokitdok.com
app_redirect_uri = 'https://yourapplication.com/redirect_uri'

app = Flask(__name__)
#A made up secret to enable sessions - use a different (and better) secret for real applications
app.secret_key ='12345678900AbILiQzXiYnqYi'


def new_token_handler(token):
    print('new token received: {0}'.format(token))
    # persist token information for later use


@app.route("/login")
def login():

    pd = pokitdok.api.connect(client_id, client_secret, redirect_uri=app_redirect_uri,
                              scope=['user_schedule'], auto_refresh=True, token_refresh_callback=new_token_handler)

    authorization_url, state = pd.authorization_url()

    #Retain the `state` value for later use as it is used to prevent CSRF
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route("/redirect_uri")
def redirect_uri():
    code = request.args.get('code')
    redirect_state_value = request.args.get('state')
    if redirect_state_value != session.get('oauth2_state'):
        return jsonify({'error': 'invalid state value'})

    pd = pokitdok.api.connect(client_id, client_secret, redirect_uri=app_redirect_uri,
                              scope=['user_schedule'], auto_refresh=True, token_refresh_callback=new_token_handler,
                              code=code)

    #Start making API calls
    #pd.book_appointment(...)
    return jsonify({})


if __name__ == "__main__":
    app.run(debug=True)