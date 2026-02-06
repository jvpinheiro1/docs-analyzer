import httpx
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import RepositorioRequest
from database import engine, Base, get_db
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
async def analyzer_repo(request: RepositorioRequest, db: Session = Depends(get_db)): 
        owner, repo = extract_infos_repo(request.github_url)

        if not owner or not repo:
            raise HTTPException(status_code=400, detail="URL inválida!")
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        async with httpx.AsyncClient() as cliente:
             response = await cliente.get(api_url)

        if response.status_code == 404:
             raise HTTPException(status_code=404, detail="Repositório não encontrado.")
        
        data = response.json()

        db_repo = models.Repositorio(
            github_url=str(request.github_url),
            name= data["name"],
            owner= data["owner"]["login"],
            stars= data["stargazers_count"],
            language= data["language"],
            description= data["description"]
        )

        db.add(db_repo)
        db.commit()
        db.refresh(db_repo)

        return db_repo

@app.get("/repos")
def list_repos(db :Session = Depends(get_db)):
     repos = db.query(models.Repositorio).all()
     return repos