import httpx
from fastapi import FastAPI, HTTPException
from schemas import RepositorioRequest
from database import engine, Base
import models 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def extract_infos_repo(url: str):
    clean_url = str(url).replace(".git", "").rstrip("/")
    parts = clean_url.split("/")
    if len(parts) < 2:
        return None, None
    return parts[-2], parts[-1]

@app.post("/analyze")
async def analyzer_repo(request: RepositorioRequest): 
        owner, repo = extract_infos_repo(request.github_url)

        if not owner or not repo:
            raise HTTPException(status_code=400, detail="URL inválida!")
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        async with httpx.AsyncClient() as cliente:
             response = await cliente.get(api_url)

        if response.status_code == 404:
             raise HTTPException(status_code=404, detail="Repositório não encontrado.")
        
        data = response.json()

        return {
            #  "data": data
             "name": data["name"],
             "owner": data["owner"]["login"],
             "stars": data["stargazers_count"],
             "language": data["language"],
             "description": data["description"]
        }


# @app.get("/items/{item_id}")
# async def read_items(item_id: int):
#     return simulation_db[item_id]

# @app.post("/items/new")
# def create_item(item: Item):
#     simulation_db.append(item)
#     return item

# @app.get("/items/")
# def list_items():
#     return simulation_db