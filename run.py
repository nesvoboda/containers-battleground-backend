from engine import test_solution

import os
from peewee import *
from time import sleep

HOST: str = os.environ.get("SUPABASE_DB_HOST")
PASSWORD: str = os.environ.get("SUPABASE_DB_PASSWORD")


db = PostgresqlDatabase('postgres',
        user='postgres', password=PASSWORD, host=HOST, port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Requests(BaseModel):
    id_ = UUIDField(db_column='id', primary_key=True) # uuid
    github_url = CharField() #varchar
    user_id = UUIDField() #uuid
    processed = BooleanField() #bool

class Results(BaseModel):
    id_ = IntegerField(db_column='id', primary_key=True) # uuid
    url = CharField() #varchar
    vector = FloatField() #float
    map_ = FloatField(db_column='map') #float
    stack = FloatField() #float
    request_id = UUIDField() #float


def handle_solution(request):
    res = test_solution(request.github_url)
    res['url'] = request.github_url

    request.processed = True
    request.save()
    
    new_result = Results.create(url=res['url'], vector=res['vector'], map_=res['map'], stack=res['stack'], request_id=request.id_)


def process():
    for res in Requests.select().where(Requests.processed == False):
        print('Handling: ' + res.github_url)
        handle_solution(res)


if __name__ == '__main__':
    while True:
        process()
        sleep(1)