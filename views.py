from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(username=email)  # Assuming email is stored as username
            if user.check_password(password):  # Validate password
                return JsonResponse({"success": True, "message": "Login successful!"}, status=200)
            else:
                return JsonResponse({"success": False, "message": "Invalid password!"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found!"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request method!"}, status=400)
