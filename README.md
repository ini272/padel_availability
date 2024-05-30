# padel_availability

## How to install
- install virtualenv `pip3 install virtualenv --bypass-system-packages`
- create envrionment `python3 -m venv env`
- activate envrionment `source env/bin/activate`
    - you should now see a "(env)" in your command line
    - for later deactivating the environment run `deactivate`
- install dependencies `pip3 install -r requirements.txt --break-system-packages`

## Installing new dependencies
- be sure that envrionment is activated (`source env/bin/activate`)
- install dependency `pip3 install ...`
- save dependency to requirements.txt by running `pip3 freeze > requirements.txt`
- and commit it
