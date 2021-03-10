# quickrun

quickrun is a module designed to make it easy to run commands and gather info from multiple servers.  

## Dependencies
- python3.8
- jq
- aws cli (v1)

---

## Getting started

#### Setup
```
$ git clone ...
$ cd quickrun
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Running
```
python3 -m run.example --name 'aws-name-search'
```

#### Defining new scripts

All scripts live in the `run` directory and should have a class extending `quickrun.Base`.  
