from fastapi import FastAPI
from App.Databse.session import create_db_tables
from contextlib import asynccontextmanager
from App.api.master_router import master_router
from scalar_fastapi import get_scalar_api_reference

@asynccontextmanager
async def lifespan_handler(app : FastAPI):
    await create_db_tables()
    yield
    


#lifespan a context manager use it instead of when_start/when_end
app = FastAPI(lifespan=lifespan_handler)

app.include_router(master_router)


@app.get("/scalar",include_in_schema=False)
def get_scalar_doc():
    return get_scalar_api_reference(
        openapi_url =app.openapi_url,
        title = "Sad api"
    )












# @app.get("/shipment/{field}")
# def get_shipment_field(field : str , id : int) -> dict:
#     return {
#         "field" : db[id][field]
#     }

# @app.put("/shipment")
# def shipment_update(id : int,content :str,weight: float , status:str) -> dict[str,Any]:
#     db[id]= {
#         "content": content,
#         "weight" : weight,
#         "status" : status
#     }
#     return db[id]