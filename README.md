# CSB-Project-1


This is is a course project for cyber security base project 1: 
https://cybersecuritybase.mooc.fi/module-3.1

The idea is to demonstrate at least 5 flaws from the OWASP listing 2021:
https://owasp.org/www-project-top-ten/

***Installing instructions / how to test the app locally***
```
Prerequisites: Python 3.10.12 and PostgreSQL.
```

```
PostgreSQL download instructions to different systems:

linux: https://github.com/hy-tsoha/local-pg
mac: https://postgresapp.com/
other: https://www.postgresql.org/download/
```

**1. Clone this repository to your computer and navigate to the root folder.**

```
git clone https://github.com/mikaelri/CSB-Project-1.git
```

**2. Update .env file's (DATABASE_URL) username to the one you have in terminal** (this is one of the flaws that .env is in the repository)
```
DATABASE_URL=postgresql:///<username>
```
*If the application won't work, you can try also the below*
```
DATABASE_URL=postgresql+psycopg2://<username>
```

**3. Next activate the virtual environment and install the requirements in terminal:**
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r ./requirements.txt
```

**4. Create the database (option 1) in psql to your main user with command:**
```
psql < schema.sql
```

*If you get error connectio to server on socket you can activate the script with the command below and then re run the previous command:*
```
start-pg.sh
```

**if you need to create alternative user database (option 2) it can be done like this:**

*activate postgreSQL:*

```
psql
```

*create the database:*

```
CREATE DATABASE <database-name>;
```

*exit postgreSQL:*

```
\q
```
*run the schema.sql to your created database:*

```
psql -d <database-name> < schema.sql
```

**5. Start the application with command:**

```
flask run
```