import os
import json
import opendatasets as od
from fastapi import FastAPI
import kaggle
from datasets import load_dataset
from kaggle.api.kaggle_api_extended import KaggleApi
from config.database import session, engine, base
from models.documentos import Documentos

"""_summary_
    creacion de una instancia de Fastapi
    creacion de nombre
    version
    para ejecutar el servidor utilizar uvicorn main:app
    cuando se requiere actualizacion se utiliza uvicorn main:app --reload
    cuando se realiza cambio de puerto se utiliza --port 5000
    Cuando se utiliza el host para que este disponible en todos los dispositivos de la res --host 0.0.0.0
"""

os.environ['KAGGLE_USERNAME'] = "rojored96"
os.environ['KAGGLE_KEY'] = "495bc36f5a6c1574164038c6774b8137"



app = FastAPI()
"""app.authenticate()
app.dataset_list_files('Cornell-University/arxiv').files
app.dataset_download_files('Cornell-University/arxiv', path=".", unzip=True)"""

app.title = "RESTAPI with python"
app.version = "0.0.1"
download_ulr = 'https://www.kaggle.com/datasets/Cornell-University/arxiv/versions/120'
#data = load_dataset("arxiv_dataset", data_dir='.', split='train')

dataset=od.download(download_ulr)

base.metadata.create_all(bind=engine)

#with open('arxiv-metadata-oai-snapshot.json','r' , encoding='utf-8') as file:
#   data = json.load(file)

data = [json.loads(line) for line in open('arxiv-metadata-oai-snapshot.json', 'r', encoding='utf-8')]   

"""Definicion de la ruta de incio
"""

@app.get('/', tags=['home'])


def message():
    return "hola mundo"

salida=[]
@app.get('/papers', tags=['papers'])
def get_papers():
    for item in data:  
        salida.append(item["id"]) 
        salida.append(item["title"])
        salida.append(item["abstract"])
        salida.append(item["authors"])
        salida.append(item["categories"])
        salida.append(item["update_date"])
        
        print(item) 
    return salida


@app.get('/papers/{id}', tags=['papers'])
def get_id(id: str):
    for item in data:
        if item["id"] == id:
            return (item["id"],item["title"], item["abstract"], item["authors"],item["categories"],item["update_date"])
    return []

divide_authors=[]

@app.get('/authors', tags=['authors'])
def get_autors():
    for item in data:
        authors_separate=item["authors"].split(',')
        divide_authors.append(authors_separate)
    return divide_authors
    
papers_author=[]   
@app.get('/authors/{authors}', tags=['authors'])
def get_autors(authors: str):
    for item in data:
        authors_separate=item["authors"].split(',')
        for items in authors_separate:
            if items == authors:
                papers_author.append(item["title"])
    return papers_author
    


salida_categories=[]   
@app.get('/categories', tags=['categories'])
def get_categories():
    for item in data:
        if item["categories"] not in salida_categories:
            
            salida_categories.append(item["categories"])
            
        else: 
            pass    
    return salida_categories

salida_papers_categories=[]
@app.get('/categories/{categories}', tags=['categories'])
def get_papers_categories(categories: str):
    for item in data:
        if item["categories"] == categories:
            salida_papers_categories.append(item["title"])
    return salida_papers_categories