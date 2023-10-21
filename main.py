from platform import processor
from fastapi import FastAPI
from models import Student, Professor, Department, Faculty
import json
import uvicorn

HOST = "127.0.0.1"
PORT = 8000

app = FastAPI()

@app.on_event("startup")
async def start_func():
    global data
    with open('data.json','r') as f:
        data = json.load(f)

@app.get('/lists')
async def list():
    return data

# Get Request
@app.get('/professors/{prof_id}')
async def get_professor(prof_id):
    profs = data["professors"]
    for prof in profs:
        print(prof)
        if prof['id']==int(prof_id):
            prof_copy = prof.copy()
            prof_copy["links"]={"self":{"href":f"{HOST}:{PORT}/professors/{prof_id}"}}
            return {"data": prof_copy,"status_code":200, "message":"Data parsed Successfully"}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.get('/faculties/{fac_id}')
async def get_faculties(fac_id):
    try:
        facs = data["faculties"]
        for fac in facs:
            print(fac)
            if fac['id']==int(fac_id):
                fac_copy = fac.copy()
                fac_copy['links']={"self":{"href":f"{HOST}:{PORT}/faculties/{fac_id}"}}
                return {"data": fac_copy,"status_code":200, "message":"Data parsed Successfully"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.get('/professors/{prof_id}/students/{std_id}')
async def get_student(prof_id,std_id):
    try:
        profs = data["professors"]
        for prof in profs:
            stds = prof["students"]
            for std in stds:
                if std['id']==int(std_id) and prof['id']==int(prof_id):
                    std_copy = std.copy()
                    std_copy['links']={"self":{"href":f"{HOST}:{PORT}/professors/{prof_id}/students/{std_id}"}}
                    return {"data": std_copy,"status_code":200, "message":"Data parsed Successfully"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.get('/faculties/{fac_id}/departments/{dep_id}',status_code=200)
async def get_student(fac_id,dep_id):
    try:
        facs = data["faculties"]
        for fac in facs:
            deps = fac["depts"]
            for dep in deps:
                if dep['id']==int(dep_id) and fac['id']==int(fac_id):
                    dep_copy = dep.copy()
                    dep_copy['links']={"self":{"href":f"{HOST}:{PORT}/faculties/{fac_id}/departments/{dep_id}"}}
                    return {"data": dep_copy,"status_code":200, "message":"Data parsed Successfully"} 
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

#Post Request

@app.post("/professors",status_code=201)
def add_professor(professor: Professor):
    try:
        data['professors'].append(professor.dict())
        return {"status_code":201, 
                "message":"New Professor Added Successfully"}
    except:
        return {"error":"Invalid Data Format", 
                "status_code": 422, 
                "messages":"Please correct your data format and url."}

@app.post("/professors/{prof_id}/students/",status_code=201)
def add_book(student: Student,prof_id):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            print(prof)
            if prof['id']==int(prof_id):
                data['professors'][i]["students"].append(student.dict())
                break
        return {"status_code":201, "message":f"New Student of Professor {prof_id} Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url"}
    
@app.post("/faculties",status_code=201)
def add_book(faculty: Faculty):
    try:
        data['faculties'].append(faculty.dict())
        return {"status_code":201, "message":"New Faculty Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url."}

@app.post("/faculties/{fac_id}/departments/",status_code=201)
def add_book(department: Department,fac_id):
    try:
        facs = data["faculties"]
        for i,fac in enumerate(facs):
            if fac['id']==int(fac_id):
                data['faculties'][i]["departments"].append(department.dict())
                return {"status_code":201, "message":f"New Department of Faculty {fac_id} Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url"}
    
# Put Request
@app.put('/professors/{prof_id}/update')
async def update_professor(prof_id,new_prof: Professor):
    profs = data["professors"]
    for i,prof in enumerate(profs):
        print(prof)
        if prof['id']==int(prof_id):
            new_prof.id = int(prof_id)
            data["professors"][i] = new_prof
            return {"message": f"Professor {prof_id} updated successfully"}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.put('/faculties/{fac_id}/update')
async def update_faculties(fac_id, new_fac:Faculty):
    try:
        facs = data["faculties"]
        for i,fac in enumerate(facs):
            print(fac)
            if fac['id']==int(fac_id):
                new_fac.id = int(fac_id)
                data['faculties'][i]=new_fac
                return {"message": f"Professor {fac_id} updated successfully", "status_code":200}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.put('/professors/{prof_id}/students/{std_id}/update')
async def update_student(prof_id,std_id,new_student: Student):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            stds = prof["students"]
            for j, std in enumerate(stds):
                if std['id']==int(std_id) and prof['id']==int(prof_id):
                    new_student.id = int(std_id)
                    data['professors'][i]['students'][j]=new_student
                    return {"message": f"Student {std_id} of Professor {prof_id} updated successfully", "status_code":200}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.put('/faculties/{fac_id}/departments/{dep_id}/update')
async def update_department(fac_id,dep_id,new_department: Department):
    try:
        faculties = data["faculties"]
        for i,fac in enumerate(faculties):
            deps = fac["depts"]
            for j, dep in enumerate(deps):
                if dep['id']==int(dep_id) and fac['id']==int(fac_id):
                    new_department.id = int(dep_id)
                    data['faculties'][i]['depts'][j]=new_department
                    return {"message": f"Department {dep_id} of Faculty {fac_id} updated successfully", "status_code":200}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL or data."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

# Delete Opereation

@app.delete('/professors/{prof_id}/delete')
async def delete_professor(prof_id):
    profs = data["professors"]
    for i,prof in enumerate(profs):
        print(prof)
        if prof['id']==int(prof_id):
            del data["professors"][i] 
            return {"message": f"Professor {prof_id} deleted successfully","status_code":204}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.delete('/faculties/{fac_id}/delete')
async def delete_faculties(fac_id):
    try:
        facs = data["faculties"]
        for i,fac in enumerate(facs):
            print(fac)
            if fac['id']==int(fac_id):
                del data['faculties'][i]
                return {"message": f"Faculty {fac_id} deleted successfully", "status_code":204}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.delete('/professors/{prof_id}/students/{std_id}/delete')
async def delete_student(prof_id,std_id):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            stds = prof["students"]
            for j, std in enumerate(stds):
                if std['id']==int(std_id) and prof['id']==int(prof_id):
                    del data['professors'][i]['students'][j]
                    return {"message": f"Student {std_id} of Professor {prof_id} deleted successfully", "status_code":204}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

@app.delete('/faculties/{fac_id}/departments/{dep_id}/delete')
async def update_department(fac_id,dep_id,new_department: Department):
    try:
        faculties = data["faculties"]
        for i,fac in enumerate(faculties):
            deps = fac["depts"]
            for j, dep in enumerate(deps):
                if dep['id']==int(dep_id) and fac['id']==int(fac_id):
                    new_department.id = int(dep_id)
                    data['faculties'][i]['depts'][j]=new_department
                    return {"message": f"Department {dep_id} of Faculty {fac_id} updated successfully", "status_code":200}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL or data."}
    return {"error":"", "status_code": 404, "messages":"Not Found"}

if __name__ == '__main__':
    uvicorn.run("main:app",reload=True, port=PORT, host=HOST)