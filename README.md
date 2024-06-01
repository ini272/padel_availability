# padel_availability

## How to install
- ensure python3.9 is installed `python3 --version`
- install virtualenv `pip3 install virtualenv`
- create environment directly for python3.9 `python3.9 -m venv env`
- activate envrionment `source env/bin/activate`
    - you should now see a "(env)" in your command line
    - for later deactivating the environment run `deactivate`
- install dependencies `pip3 install -r requirements.txt`

## Installing new dependencies
- be sure that envrionment is activated (`source env/bin/activate`)
- install dependency `pip3 install ...`
- save dependency to requirements.txt by running `pip3 freeze > requirements.txt`
- and commit it

## Deploy serverless function
- run `npm install` to install serverless dependency
- run `npm run deploy` to deploy
- you probably have to authenticate via serverless and aws
