# deploy
cloning repository:

```
cd ~/Documents
git clone https://github.com/MyagkikhKonstantin/pdf-email-parser
```

setting parameters:
 * put into `pdf-email-parser/email_parser/` *.json file from email
 * set login and password into `pdf-email-parser/email_parser/settings.py`

 
installing library for pdf parsing

`sudo brew install pdfminer`


installing python requirements

`pip install -r requirements`

# test
run test
`
python -m unittest discover
`

# run
`/usr/local/bin/email_parser`
