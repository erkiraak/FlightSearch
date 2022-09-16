# FlightSearch

Welcome to our cheap flights search engine. It can be used to search for flights 
and subscribe to the searches using a maximum price criteria. The subscribed
searches will be run once a day and if some cheap flights are found, email 
alerts are sent to the subscribers.
Flight search is done using [Tequla API by kiwi.com](https://tequila.kiwi.com/)
## Built With

Flightsearch is written in python 3.10 using Django 4.1.1 framework.  
Styling is done using Bootstrap and functionality added by JQuery.
Default database is MySQL. 

* [![Python][Python.com]][Python-url]
* [![Django][Django.com]][Django-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![MySQL][MySQL.com]][MySQL-url]



## Getting Started

### Dependencies

Required libraries are described in requirements.txt. Timed jobs are performed 
by chron, that means only unix machines are supported for that functionality.
If Gmail is used for sending emails, an app password must be created 
([https://devanswers.co/create-application-specific-password-gmail/](https://devanswers.co/create-application-specific-password-gmail/))

### Installation

1. Clone the repository 
   ```git clone https://github.com/erkiraak/FlightSearch.git```

2. Create virtual environment for python 3.10:
   ```python3.10 -m venv venv```
3. Activate virtual environment :
   ```source venv/bin/activate```
4. Install required packages:
   ```pip install -r requirements.txt```
5. Create '.env' file at the root directory with the following variables:
    ```
    DEBUG=
    SECRET_KEY=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_IP=
    GMAIL_ADDRESS=
    GMAIL_APP_PASSWORD=
    GMAIL_PASSWORD=
    KIWI_TEQUILA_API_KEY=
    EASYPNR_API_KEY=
    RAPIDAPI_API_KEY=
    ```
6. Initialise database and run migrations

### Executing program

1. Launch Django server ```pip install -r requirements.txt```
2. Navigate to `http://127.0.0.1:8000` or `http://localhost:8000`


## Help

Commands for setting up cronjobs:
```
python3 manage.py crontab add  # add all jobs to crontab
python3 manage.py crontab show  # view all jobs in crontab
python3 manage.py crontab remove  # remove all jobs from crontab
```

## Authors

- Erki Rääk
- Kalvi Kahi

Project Link: [https://github.com/erkiraak/FlightSearch](https://github.com/erkiraak/FlightSearch)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details




[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Django.com]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://getbootstrap.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[MySQL.com]: https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com/