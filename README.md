# Quick Run

Quickly create python modules to run commands across servers.  

## Dependencies
- python3.8
- jq
- aws cli (v1)

---

## Get started

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
python3 -m run.example
```

#### Adding new modules
The intended usage here is to create new modules in `run/` which inherit from `quickrun.Base`.  

See `docs/` for more.  
