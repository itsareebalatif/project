from fastapi import FastAPI
import database
import models
from routes import auth, groups, expenses, balances, export

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Tally API")

app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(balances.router)
app.include_router(export.router)