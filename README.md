# CSB-Project-1

This is is a course project for cyber security base project 1: https://cybersecuritybase.mooc.fi/module-3.1

The idea is to demonstrate at least 5 flaws from the OWASP listing 2021: https://owasp.org/www-project-top-ten/

***Installing instructions / how to test the app locally***
```
Prerequisites: Python 3.10.12 and PostgreSQL.
```
**Clone this repository to your computer and navigate to the root folder.**

```
git clone https://github.com/mikaelri/CSB-Project-1.git
```

**Create .env file to the root folder and add these:**
```
DATABASE_URL=<database-local-address> (I have: postgresql:///user)
```
```
SECRET_KEY=<your_secret_key>
```

**Next activate the virtual environment and install the requirements in terminal:**
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r ./requirements.txt
```

**Create the database in psql with command:**
```
psql < schema.sql
```

**Start the application with command:**

```
flask run
```