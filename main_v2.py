from platform import processor
from fastapi import FastAPI, Depends
from models import Student, Professor, Department, Faculty
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated
import json
import uvicorn

HOST = "0.0.0.0"
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
    try:
        profs = dict(data)["professors"]
        print(profs)
        for prof in profs:
            print(prof)
            if prof['id']==int(prof_id):
                prof_copy = prof.copy()
                prof_out = {}
                for k,v in prof_copy.items():
                    if type(v) == type([]):
                        continue
                    prof_out[k]=v
                prof_out["links"]=[{"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}","action":"GET"},
                                    {"rel":"students","href":f"{HOST}:{PORT}/professors/{prof_id}/students/`student_id`","action":"GET"},
                                    {"rel":"self","href":f"{HOST}:{PORT}/professors/`professor_id`/","action":"POST"},
                                    {"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}/update","action":"PUT"},
                                    {"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}/delete","action":"DELETE"}]
                return prof_out
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

@app.get('/faculties/{fac_id}')
async def get_faculties(fac_id):
    try:
        facs = data["faculties"]
        for fac in facs:
            print(fac)
            if fac['id']==int(fac_id):
                fac_copy = fac.copy()
                fac_out = {}
                for k,v in fac_copy.items():
                    if type(v) == type([]):
                        continue
                    fac_out[k]=v
                fac_out["links"]=[{"rel":"self","href":f"{HOST}:{PORT}/faculties/","action":"GET"},
                                    {"rel":"departments","href":f"{HOST}:{PORT}/faculties/{fac_id}/departements/`department_id`","action":"GET"},
                                    {"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/departements/","action":"POST"},
                                    {"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/update","action":"PUT"},
                                    {"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/delete","action":"DELETE"}]
                return fac_out
        return {"error":"Not Found", "status_code": 404}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

@app.get('/professors/{prof_id}/students/{std_id}')
async def get_student(prof_id,std_id):
    try:
        profs = data["professors"]
        for prof in profs:
            stds = prof["students"]
            for std in stds:
                if std['id']==int(std_id) and prof['id']==int(prof_id):
                    std_copy = std.copy()
                    std_out = {}
                    for k,v in std_copy.items():
                        if type(v) == type([]):
                            continue
                        std_out[k]=v
                    std_out["links"]=[{"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}/students/{std_id}","action":"GET"},
                                        {"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}/students/`student_id`","action":"POST"},
                                        {"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}/update","action":"PUT"},
                                        {"rel":"self","href":f"{HOST}:{PORT}/professors/{prof_id}/delete","action":"DELETE"}]
                    return std_out
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

@app.get('/faculties/{fac_id}/departments/{dep_id}',status_code=200)
async def get_student(fac_id,dep_id):
    try:
        facs = data["faculties"]
        for fac in facs:
            deps = fac["depts"]
            for dep in deps:
                if dep['id']==int(dep_id) and fac['id']==int(fac_id):
                    dep_copy = dep.copy()
                    dep_out = {}
                    for k,v in dep_copy.items():
                        if type(v) == type([]):
                            continue
                        dep_out[k]=v
                    dep_out["links"]=[{"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/departments/{dep_id}","action":"GET"},
                                        {"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/departments/`department_id`","action":"POST"},
                                        {"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/departments/{dep_id}/update","action":"PUT"},
                                        {"rel":"self","href":f"{HOST}:{PORT}/faculties/{fac_id}/departments/{dep_id}/delete","action":"DELETE"}]
                    return dep_out
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

#Post Request

@app.post("/professors",status_code=201)
def add_professor(professor: Professor):
    try:
        data['professors'].append(professor.dict())
        return {"status_code":201, "message":"New Professor Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url."}

@app.post("/professors/{prof_id}/students/",status_code=201)
def add_student(student: Student,prof_id):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            print(prof)
            if prof['id']==int(prof_id):
                keys= data['professors'][i].keys()
                if "students" not in keys:
                    data['professors'][i]["students"] = []    
                data['professors'][i]["students"].append(student.dict())
                break
        return {"status_code":201, "message":f"New Student of Professor {prof_id} Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url"}
    
@app.post("/faculties",status_code=201)
def add_faculty(faculty: Faculty):
    try:
        data['faculties'].append(faculty.dict())
        return {"status_code":201, "message":"New Faculty Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url."}

@app.post("/faculties/{fac_id}/departments/",status_code=201)
def add_department(department: Department,fac_id):
    try:
        facs = data["faculties"]
        for i,fac in enumerate(facs):
            if fac['id']==int(fac_id):
                keys= data['faculties'][i].keys()
                if "depts" not in keys:
                    data['faculties'][i]["depts"] = []
                data['faculties'][i]["depts"].append(department.dict())
                return {"status_code":201, "message":f"New Department of Faculty {fac_id} Added Successfully"}
    except:
        return {"error":"Invalid Data Format", "status_code": 422, "messages":"Please correct your data format and url"}
    
# Put Request
@app.put('/professors/{prof_id}/update')
async def update_professor(prof_id,new_prof: Professor):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            print(prof)
            if prof['id']==int(prof_id):
                new_prof.id = int(prof_id)
                data["professors"][i] = new_prof.dict()
                return {"message": f"Professor {prof_id} updated successfully"}
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

@app.put('/faculties/{fac_id}/update')
async def update_faculties(fac_id, new_fac:Faculty):
    try:
        facs = data["faculties"]
        for i,fac in enumerate(facs):
            # print(fac)
            if fac['id']==int(fac_id):
                new_fac.id = int(fac_id)
                data['faculties'][i]=new_fac.dict()
                return {"message": f"Faculty {fac_id} updated successfully", "status_code":200}
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}

@app.put('/professors/{prof_id}/students/{std_id}/update')
async def update_student(prof_id,std_id,new_student: Student):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            stds = prof["students"]
            for j, std in enumerate(stds):
                if std['id']==int(std_id) and prof['id']==int(prof_id):
                    new_student.id = int(std_id)
                    data['professors'][i]['students'][j]=new_student.dict()
                    return {"message": f"Student {std_id} of Professor {prof_id} updated successfully", "status_code":200}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}

@app.put('/faculties/{fac_id}/departments/{dep_id}/update')
async def update_department(fac_id,dep_id,new_department: Department):
    try:
        faculties = data["faculties"]
        for i,fac in enumerate(faculties):
            deps = fac["depts"]
            for j, dep in enumerate(deps):
                if dep['id']==int(dep_id) and fac['id']==int(fac_id):
                    new_department.id = int(dep_id)
                    data['faculties'][i]['depts'][j]=new_department.dict()
                    return {"message": f"Department {dep_id} of Faculty {fac_id} updated successfully", "status_code":200}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL or data."}

# Delete Opereation

@app.delete('/professors/{prof_id}/delete')
async def delete_professor(prof_id):
    try:
        profs = data["professors"]
        for i,prof in enumerate(profs):
            print(prof)
            if prof['id']==int(prof_id):
                del data["professors"][i] 
                return {"message": f"Professor {prof_id} deleted successfully","status_code":204}
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL or data."}
        
@app.delete('/faculties/{fac_id}/delete')
async def delete_faculties(fac_id):
    try:
        facs = data["faculties"]
        for i,fac in enumerate(facs):
            print(fac)
            if fac['id']==int(fac_id):
                del data['faculties'][i]
                return {"message": f"Faculty {fac_id} deleted successfully", "status_code":204}
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

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
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL."}
    

@app.delete('/faculties/{fac_id}/departments/{dep_id}/delete')
async def update_department(credentials: cred_class, fac_id,dep_id):
    try:
        faculties = data["faculties"]
        for i,fac in enumerate(faculties):
            deps = fac["depts"]
            for j, dep in enumerate(deps):
                if dep['id']==int(dep_id) and fac['id']==int(fac_id):
                    del data['faculties'][i]['depts'][j]
                    return {"message": f"Department {dep_id} of Faculty {fac_id} updated successfully", "status_code":200}
        return {"error":"", "status_code": 404, "messages":"Not Found"}
    except Exception as e:
        return {"error":"Invalid Url", "status_code": 422, "messages":"Please correct the URL or data."}
    
if __name__ == '__main__':
    uvicorn.run("main_basic_auth:app",reload=True, port=PORT, host=HOST)