from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Employee Management API",
    description="A practical FastAPI project demonstrating HTTP methods",
    version="1.0.0"
)


# Used for POST (employee_id comes in the body)
class Employee(BaseModel):
    employee_id: int
    name: str
    department: str
    salary: float = Field(gt=0)
    email: EmailStr


# Used for PUT (employee_id comes from the URL, so it's not in the body)
class EmployeeReplace(BaseModel):
    name: str
    department: str
    salary: float = Field(gt=0)
    email: EmailStr


# Used for PATCH (every field optional)
class EmployeeUpdate(BaseModel):
    name: str | None = None
    department: str | None = None
    salary: float | None = Field(default=None, gt=0)
    email: EmailStr | None = None


employees = {}


@app.get("/")
def home():
    return {"message": "Welcome to Employee Management API"}


@app.get("/employees")
def get_employees():
    return {"employees": employees}


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees[employee_id]


@app.post("/employees", status_code=201)
def create_employee(employee: Employee):
    if employee.employee_id in employees:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    employees[employee.employee_id] = employee.model_dump()
    return {
        "message": "Employee created successfully",
        "employee": employees[employee.employee_id]
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeReplace):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees[employee_id] = {"employee_id": employee_id, **employee.model_dump()}
    return {
        "message": "Employee completely updated",
        "employee": employees[employee_id]
    }


@app.patch("/employees/{employee_id}")
def partial_update_employee(employee_id: int, employee: EmployeeUpdate):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    update_data = employee.model_dump(exclude_unset=True)
    employees[employee_id].update(update_data)
    return {
        "message": "Employee partially updated",
        "employee": employees[employee_id]
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    deleted_employee = employees.pop(employee_id)
    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee
    }