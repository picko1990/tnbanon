# TNBAnon
TNBAnon offers you the ability to anonymously send your coins on [TNBC](http://thenewboston.com) network.  
  
Please follow these steps for testing:
* Clone and install requirements `pip install -r requirements.txt`
* Migrate `python manage.py migrate`
* Run the server `python manage.py runserver`
* Enter the signing keys for the app wallets by visiting `http://127.0.0.1:8000/setup/`
* Open a new terminal and run the cron job `python cron.py`

Now you can start testing.
