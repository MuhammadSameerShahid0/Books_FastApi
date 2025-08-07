from fastapi import FastAPI, APIRouter

app = FastAPI()
Test_Router = APIRouter(tags=["Test"])

class Test:
    def __init__(self, data):
        self.data = data

    def read_root(self):
        return {"message": self.data}


@Test_Router.get("/read_json_hardcode")  # path and (get, post, etc. are operations)
def read_json_hardcode():  # path operation function
    obj = Test("Hello from class")
    return obj.read_root()


@Test_Router.get("/user_details")
def user_details(user_name: str, user_from: str):
    return {'user_details': {"user_name": user_name, "user_from": user_from}}

app.include_router(Test_Router)