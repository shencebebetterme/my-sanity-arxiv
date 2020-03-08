change `policy.xml`  if converting thumb fails

<policy domain="coder" rights="read|write" pattern="PDf"> 



install mongod on WSL following https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/blob/master/readmes/installs/MongoDB.md

also https://gist.github.com/Mikeysax/cc86c30903727c556bcce960f7e4d59b  but need to install the community edition as in the official guide.



open one WSL terminal, type

```bash
sudo mongod --dbpath ~/data/db
```



open a new WSL terminal, cd to `myarxiv/codes`  directory, type

```bash
cd /mnt/d/myarxiv/codes
sudo mongo
```

to start a mongod service



open a third WLS terminal, cd to `myarxiv/codes`  and type

```bash
python3 serve.py
```



open a windows browser and go to `localhost:5000` to visit web server

