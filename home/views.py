from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
# what are the contents of JsonResponse
# what are the contents of request

def say_hello(request):
    response = {}  # Fix the variable name here
    data = {'name': 'manoj', 'age': 10}
    status_code = 200
    message = 'hello boy'
    response['data'] = data
    response['status'] = status_code
    response['message'] = message
    headers = {}
    headers['token'] = 'hbvacsdhgcvhdgsc'
    return JsonResponse(response, status=status_code, headers=headers)

def say_hello_with_name(request):
    name = request.GET.get('name','')
    data = f'hello {name}' if name else 'please provide name'
    status_code = 200
    message = 'nothing'
    response = {}
    response['data'] = data
    response['status'] = status_code
    response['message'] = message
    headers = {}
    headers['token'] = 'hbvacsdhgcvhdgsc'
    return JsonResponse(response, status=status_code, headers=headers)

def say_hello_with_nameV2(request):
    name = request.GET.get('name', '')
    if name:
        data = f'hello {name}'
    else:
        data = None

    status_code = 200
    message = 'nothing'

    if data is None:
        status_code = 400
        message = 'please provide name'

    response = {
        'data': data,
        'status': status_code,
        'message': message,
        'data2': data
    }

    headers = {
        'token': 'hbvacsdhgcvhdgsc'
    }

    return JsonResponse(response, status=status_code, headers=headers)


@csrf_exempt
def save_user_details(request):
    print("hello")
    print(request)
    if request.method == 'POST':
        data = json.loads(request.body)  # Assuming data is sent as form data
        name = data.get('name', '')
        mobile_no = data.get('mobileNo', '')
        # Create a new user instance
        if User.objects.filter(username=name).exists():
                    return JsonResponse({'error': 'Username already exists'}, status=400)
        new_user = User.objects.create(username=name)
        new_user.set_password(mobile_no)  # Assuming mobile_no is the password

        # Save the user to the database
        new_user.save()

        return JsonResponse({'message': 'User details saved successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# HOW TO HANDLE METHOD OR URL NOT FOUND ?
def handle_not_found(request, exception):
    return render(request, '404.html', status=404)

def handle_server_error(request):
    return render(request, '500.html', status=500)
"""
jango debug toolbar


"""
