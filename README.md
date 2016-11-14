# installation
cloning repository
`cd ~/Documents`
`git clone https://github.com/MyagkikhKonstantin/pdf-email-parser`

setting parameters
`cd pdf-email-parser/email_parser/`

put there *.json file from email
set login and password in settings.py
 
installing library for pdf parsing
`sudo brew install pdfminer`

installing python requirements
`pip install -r requirements`

run test
`python -m unittest discover`

# run script
`/usr/local/bin/email_parser`
