LinkedinProfileParser
===
DESCRIPTION
This simple parser aimed to parse data from linkedin public profiles.
Simple REST API is written using python 2.7.2, bottle 0.10.9 and  "swiss army knife " scrapy 0.14.1.

API SPECIFICATION
===
Parsing url for competences and education
localhost:8080/doparse?address="public profile url"

Output is in json with the format : 

{
"educations" : [{"school": "XXX", "year_last": "YYY", "year_first": "ZZZ"}, ...], 
"tags"       : ["MYSQL Database design","PYTHON",...], 
"experiences": [{"title": "XXX", "company":"YYY", "year_last":"ZZZ", "year_first":"XXX", "description":"YYY"} ...]
"html": "XXX"
}

Sample request
===
localhost:8080/doparse?address=http://fr.linkedin.com/in/vasylvaskul/

Sample output
===
{"educations": [{"school": "Science Po, Coll\u00e8ge des Ing\u00e9nieurs, \u00c9cole des Mines de Paris", "year_last": "2011", "year_first": "2010"}, {"school": "Kyiv National Taras Shevchenko University", "year_last": "2007", "year_first": "2001"}, {"school": "Drohobych Lyceum at Drohobych State 'Ivan Franko' University", "year_last": "2001", "year_first": "1999"}], "tags": []}
In case of parsing problems error is returned: 
ex. {"error": {"message": "HTTP Response 404", "code":X}}

where code X can be one of the following :

1 -  network problem
2 -  page is not found (404 )
3 -  bad format 


CACHING
===
Currently the system is stateless, every new request re-parse the the page.

TODO
===
Parse experiences 
Stock results to db

OPEN ISSUES
===
Use LInked API to parse provider's profile but using access_token of the users ?
Cache or not cache the requests. 

HOWTO RUN
===
python main.py to start server