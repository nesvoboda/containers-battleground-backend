

<p><br></p>

![enter image description here](https://imgur.com/GmIcmoN.png)


  <p align="center">
An online benchmark for ft_containers (backend)
    <br />
    <a href="https://containers-battleground.netlify.app"><strong>Check it out »</strong></a>
    <br />  </p>

## Current state

The benchmarks are in their early days. Feel free to contribute!

## How to run this server

#### 1. Build the runner docker image
`docker build . --tag bg`

#### 2. Define the environment variables
```
export SUPABASE_DB_HOST={YOUR SUPABASE DB}
export SUPABASE_DB_PASSWORD={YOUR SUPABASE DB PASSWORD}
```
For now supabase provides the backend in form of a Postgres database.
You can infer the schema from the Peewee model definition in run.py

#### 3. Install the dependencies
```
pip install -r requirements.txt
```

#### 4. Run the benchmark runner
```
python run.py
```

The runner script will find all unhandled benchmark requests and handle them.

