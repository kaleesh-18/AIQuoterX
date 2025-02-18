import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Employee
def employee_crud(request):
    search_query = request.GET.get("search", "").strip().lower()
    
    if search_query:
        employees = Employee.objects.filter(name__icontains=search_query).order_by("id")
    else:
        employees = Employee.objects.all().order_by("id")  # Ensure ordering
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action", "")

            if action == "save_all":
                employees_data = data.get("employees", [])
                for emp_data in employees_data:
                    Employee.objects.filter(id=emp_data["id"]).update(name=emp_data["name"])
                return JsonResponse({"success": True})

            elif action == "discard":
                return JsonResponse({"success": True})  # Nothing changes in DB

            elif action == "add":
                name = data.get("name", "").strip()
                if not name:
                    return JsonResponse({"error": "Name cannot be empty"}, status=400)

                new_emp = Employee.objects.create(name=name)
                return JsonResponse({"id": new_emp.id, "name": new_emp.name})

            elif action == "delete":
                emp_id = data.get("id")
                if not emp_id:
                    return JsonResponse({"error": "Employee ID is required"}, status=400)
                
                emp = get_object_or_404(Employee, id=emp_id)
                emp.delete()
                return JsonResponse({"success": True})

            elif action == "delete_selected":
                ids_to_delete = data.get("ids", [])
                if not ids_to_delete:
                    return JsonResponse({"error": "No employees selected"}, status=400)

                deleted_count, _ = Employee.objects.filter(id__in=ids_to_delete).delete()
                return JsonResponse({"success": True, "deleted_count": deleted_count})

            elif action == "reorder":
                ordered_ids = data.get("ordered_ids", [])
                if not ordered_ids:
                    return JsonResponse({"error": "No ordering data provided"}, status=400)

                for index, emp_id in enumerate(ordered_ids):
                    Employee.objects.filter(id=emp_id).update(id=index + 1)
                return JsonResponse({"success": True})

            else:
                return JsonResponse({"error": "Invalid action"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "myapp/employee_crud.html", {"employees": employees})
