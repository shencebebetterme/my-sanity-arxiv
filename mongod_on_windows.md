following [the official doc](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/#run-mongodb-from-cmd)

1. create database dir to store the tmp file (only need to be run once)
       md D:\myarxiv\data\db

2. start mongodb database
      start "C:\Program Files\MongoDB\Server\4.2\bin\mongod.exe" --dbpath="D:\myarxiv\data\db"

3. connect to mongodb
        "C:\Program Files\MongoDB\Server\4.2\bin\mongo.exe"

4. run the service
        start "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" serve.py