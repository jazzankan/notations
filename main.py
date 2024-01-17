from typing import Union
from fastapi import FastAPI, Request, HTTPException, Depends, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import models
from database import engine, ValidLoc, SessionLocal, ValidationError
from sqlalchemy import update
from sqlalchemy.orm import Session

edit_png = "/img/edit.png"
app = FastAPI()
templates = Jinja2Templates(directory="templates")
favicon_path = '/img/favicon.ico'
models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name='img')


@app.get("/img/edit.png")
async def main():
    return FileResponse(edit_png)


@app.get('/img/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def name(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "name": "codingwithroby"})


@app.get("/locations", response_model=List[ValidLoc], status_code=status.HTTP_200_OK)
async def read_locations(request: Request, db: db_dependency):
    locations = db.query(models.Locations).all()
    return templates.TemplateResponse("locations.html", {"request": request, "locations": locations})


@app.get("/createlocation", status_code=status.HTTP_200_OK)
async def create_location(request: Request, db: db_dependency):
    return templates.TemplateResponse("createlocation.html", {"request": request})


@app.get("/modifylocation/{location_id}", response_model=ValidLoc, status_code=status.HTTP_200_OK)
async def change_location(request: Request, location_id: int, db: db_dependency):
    location = db.query(models.Locations).filter(models.Locations.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail='Posten finns inte')
    return templates.TemplateResponse("modifylocation.html",
                                      {"request": request, "location": location})


@app.get("/locations/{location_id}", response_model=ValidLoc, status_code=status.HTTP_200_OK)
async def delete_location(location_id: int, db: db_dependency):
    location = db.query(models.Locations).filter(models.Locations.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail='Posten finns inte')
    db.delete(location)
    db.commit()
    response = RedirectResponse("/locations", status_code=303)
    return response


@app.delete("/locations/{location_id}", response_model=ValidLoc, status_code=status.HTTP_200_OK)
async def read_location(location_id: int, db: db_dependency):
    location = db.query(models.Locations).filter(models.Locations.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail='Posten finns inte')
    return location


@app.post("/add_location", status_code=status.HTTP_201_CREATED)
async def create_location(request: Request,db: db_dependency, title: Annotated[str, Form()], url: Annotated[str, Form()],
                          prio: Annotated[int, Form()], comment: Annotated[str | None, Form()] = None):
    location = models.Locations(title=title, url=url, comment=comment, prio=prio)
    exceptions = ""
    try:
        ValidLoc(title=title, url=url, comment=comment, prio=prio)
        db.add(location)
        db.commit()
    except ValidationError as ex:
        exceptions = ex
        print(ex)
    return templates.TemplateResponse("locations.html",
                                      {"request": request, "exceptions": exceptions})
    # response = RedirectResponse("/locations",status_code=303)
    # return response


@app.post("/location/modify/{location_id}", response_model=ValidLoc, status_code=status.HTTP_200_OK)
async def modify_location(db: db_dependency, location_id: int, title: Annotated[str, Form()],
                          url: Annotated[str, Form()], prio: Annotated[int, Form()],
                          comment: Annotated[str | None, Form()] = None, delete: Annotated[str | None, Form()] = None):
    location = db.query(models.Locations).filter(models.Locations.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail='Posten finns inte')
    if delete == 'delete':
        db.delete(location)
    modified_location = update(models.Locations).where(models.Locations.id == location_id).values(title=title, url=url,
                                                                                                  comment=comment,
                                                                                                  prio=prio)
    db.execute(modified_location)
    db.commit()
    response = RedirectResponse("/locations", status_code=303)
    return response
