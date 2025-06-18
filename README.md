You can use this lab to follow along with the [SQL injection video](https://www.youtube.com/watch?v=jufQk2Phfq4&t=82s).

Start PostgreSQL locally. 
```bash
sudo systemctl start postgresql
```
Create DB. The hardcoded credentials are postgres:postgres. Change if your local PotgreSQL uses different credentials.
```
psql -U postgres -h 127.0.0.1 -f db_setup.sql
```
Start the application.
```bash
python3 app.py
```
