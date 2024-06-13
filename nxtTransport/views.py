from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction

from django.shortcuts import render
from .models import User
from .models import TransportRequest , ReqApplication
from .models import Ride
from datetime import datetime
from datetime import date
CITY_CHOICES = ['hyd', 'blr', 'mum', 'bom']
TRAVEL_CHOICES = ['bus', 'car', 'train']
SENSITIVITY_CHOICES = ['HIGHLY_SENSITIVE', 'SENSITIVE', 'NORMAL'
]
ASSET_TYPE_CHOICES = ['LAPTOP', 'TRAVEL_BAG', 'PACKAGE']
STATUSES = ['unapplied', 'pending', 'applied']

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
    return JsonResponse({'error': 'not found'}, status=405)

def handle_server_error(request):
    return render(request, '500.html', status=500)


@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        # Assuming data is sent as form data
        data = json.loads(request.body)
        name = data.get('name')
        username = data.get('username')
        mobilenumber = data.get('mobilenumber')
        email = data.get('email')

        if name is None or name.strip()=="":
            return JsonResponse({'error': 'name cant be empty or null'}, status=400)
        if username is None or username.strip()=="":
            return JsonResponse({'error': 'username cant be empty or null'}, status=400)
        if mobilenumber is None or mobilenumber.strip()=="":
            return JsonResponse({'error': 'mobilenumber cant be empty or null'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'username already exists'}, status=400)
        if User.objects.filter(mobilenumber=mobilenumber).exists():
            return JsonResponse({'error': 'mobilenumber already exists'}, status=400)

        with transaction.atomic():
            try:
                # Create a new user instance
                newUser = User(name=name, username=username, mobilenumber=mobilenumber, email=email)
                newUser.save()

                user_data = {
                    'id': newUser.id,
                    'name': newUser.name,
                    'username': newUser.username,
                    'mobilenumber': newUser.mobilenumber,
                    'email': newUser.email
                }

                response = {
                    'message': 'User details saved successfully',
                    'data': user_data
                }

                return JsonResponse(response, status=201)  # Render a success page after saving
            except Exception as e:
                # Rollback the transaction in case of any error
                transaction.rollback()
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'METHOD NOT ALLOWED'}, status=405)







# @csrf_exempt
# def createUserV2(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_form = UserForm(data)
#
#         if user_form.is_valid():
#             with transaction.atomic():
#                 try:
#                     user = user_form.save()
#                     user_data = {
#                         'id': user.id,
#                         'name': user.name,
#                         'username': user.username,
#                         'mobilenumber': user.mobilenumber,
#                         'email': user.email
#                     }
#                     response_data = {
#                         'message': 'User details saved successfully',
#                         'data': user_data
#                     }
#                     return JsonResponse(response_data, status=201)
#                 except Exception as e:
#                     transaction.rollback()
#                     return JsonResponse({'error': str(e)}, status=500)
#         else:
#             first_error = next(iter(user_form.errors.values()))[0]
#             return JsonResponse({'error': first_error}, status=400)
#     else:
#         return JsonResponse({'error': 'METHOD NOT ALLOWED'}, status=405)


@csrf_exempt
def addTransportRequest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        validateRequesterId = validate_id(data, 'requester_id')
        if(validateRequesterId!=True): return JsonResponse({'error': validateRequesterId}, status=400)
        validateLocation = validate_location(data)
        if(validateLocation!=True): return JsonResponse({'error': validateLocation}, status=400)
        validateDate = validate_date(data)
        if(validateDate!=True): return JsonResponse({'error': validateDate},status=400)
        validateMobileNo = validate_mobile_number(data)
        if(validateMobileNo!=True): return JsonResponse({'error': validateMobileNo},status=400)
        validateQuantity = validate_quantity(data)
        if(validateQuantity!=True): return JsonResponse({'error': validateQuantity},status=400)
        validateAssetType = validate_asset_type(data)
        if(validateAssetType!=True): return JsonResponse({'error': validateAssetType},status=400)
        validateSensitivity = validate_sensitivity(data)
        if(validateSensitivity!=True): return JsonResponse({'error': validateSensitivity},status=400)


        try:
#             newTransportRequest = TransportRequest(from_location=data['from_location'], to_location=data['to_location'], date=data['date'], receiver_mobilenumber=data['receiver_mobilenumber'],
#                                                 quantity=data['quantity'], asset_type=data['asset_type'], sensitivity=data['sensitivity'], requester_id=data['requester_id'])
             requester_id = User.objects.get(id=data['requester_id'])  # Fetch the User instance
             newTransportRequest = TransportRequest(
                            from_location=data['from_location'],
                            to_location=data['to_location'],
                            date=data['date'],
                            receiver_mobilenumber=data['receiver_mobilenumber'],
                            quantity=data['quantity'],
                            asset_type=data['asset_type'],
                            sensitivity=data['sensitivity'],
                            requester_id=requester_id  # Assign the User instance
                        )
             newTransportRequest.save()
             response_data = {
                'message': 'Transport request added successfully',
                'data': {
                    'id': newTransportRequest.id,
                    'from_location': newTransportRequest.from_location,
                    'to_location': newTransportRequest.to_location,
                    'date': newTransportRequest.date,
                    'receiver_mobilenumber': newTransportRequest.receiver_mobilenumber,
                    'quantity': newTransportRequest.quantity,
                    'asset_type': newTransportRequest.asset_type,
                    'sensitivity': newTransportRequest.sensitivity,
                    'requester_id': newTransportRequest.requester_id.id
                }
             }
            #newUser = User(name=name, username=username, mobilenumber=mobilenumber, email=email)
             return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def validate_id(data, param1):
    try:
        id = int(data[param1])
        if(User.objects.filter(id=id).exists()==False): return f'{param1} does not exist'
        return True
    except Exception as e:
        return str(e)

def validate_location(data):
    from_location = data.get('from_location')
    to_location = data.get('to_location')

    # Check if from_location is not null
    if not from_location:
        return 'From location is required.'

    # Check if from_location is among the choices
    if from_location not in CITY_CHOICES:
        return f'Invalid location. Allowed types are: {", ".join(CITY_CHOICES)}.'

    # Check if to_location is not null
    if not to_location:
        return 'To location is required.'

    # Check if to_location is among the choices
    if to_location not in CITY_CHOICES:
        return f'Invalid location. Allowed types are: {", ".join(CITY_CHOICES)}.'

    # Check if from_location is not equal to to_location
    if from_location == to_location:
        return 'From location cannot be the same as to location.'
    # If all checks pass, return True
    return True


def validate_datetime(data):
    datetime_str = data.get('datetime')

    # Check if datetime string is provided
    if not datetime_str:
        return 'Datetime is required.'

    try:
        # Convert datetime string to datetime object
        datetime_obj = datetime.strptime(datetime_str, '%d-%m-%Y %H:%M')
    except ValueError:
        return 'Invalid datetime format. Datetime should be in dd-mm-yyyy HH:MM format.'

    # Check if datetime is in the future
    if datetime_obj < datetime.now():
        return 'Datetime must be in the future.'

    # If all checks pass, return True
    return True

def validate_mobile_number(data):
    mobile_number = data.get('receiver_mobilenumber')

    # Check if mobile_number is not null
    if not mobile_number:
        return 'Mobile number is required.'

    # Check if mobile_number is a 10-digit string
    if not (isinstance(mobile_number, str) and len(mobile_number) == 10 and mobile_number.isdigit()):
        return 'Mobile number must be a 10-digit string.'

    # If all checks pass, return True
    return True


def validate_quantity(data):
    quantity = data.get('quantity')

    # Check if quantity is not null
    if quantity is None:
        return 'Quantity is required.'

    # Check if quantity is an integer
    if not isinstance(quantity, int):
        return 'Quantity must be an integer.'

    # Check if quantity is greater than 0
    if quantity <= 0:
        return 'Quantity must be greater than 0.'

    # If all checks pass, return True
    return True


def validate_asset_type(data):
    asset_type = data.get('asset_type')

    # Check if asset_type is not null
    if not asset_type:
        return 'Asset type is required.'

    # Check if asset_type is among the allowed choices
    if asset_type not in ASSET_TYPE_CHOICES:
        return f'Invalid asset type. Allowed types are: {", ".join(ASSET_TYPE_CHOICES)}.'

    # If all checks pass, return True
    return True

def validate_sensitivity(data):
    sensitivity = data.get('sensitivity')

    # Check if asset_type is not null
    if not sensitivity:
        return 'sensitivity is required.'

    if sensitivity not in SENSITIVITY_CHOICES:
        return f'Invalid sensitivity type. Allowed types are: {", ".join(SENSITIVITY_CHOICES)}.'

    # If all checks pass, return True
    return True

def validate_medium(data):
    medium = data.get('medium')
    if not medium:
            return 'medium is required.'

    if medium not in TRAVEL_CHOICES:
        return f'Invalid medium type. Allowed types are: {", ".join(TRAVEL_CHOICES)}.'

    # If all checks pass, return True
    return True





@csrf_exempt
def addRide(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        validateRiderId = validate_id(data, 'rider_id')
        if(validateRiderId!=True): return JsonResponse({'error': validateRiderId}, status=400)
        validateLocation = validate_location(data)
        if(validateLocation!=True): return JsonResponse({'error': validateLocation}, status=400)
        validateDate = validate_date(data)
        if(validateDate!=True): return JsonResponse({'error': validateDate},status=400)
        validateQuantity = validate_quantity(data)
        if(validateQuantity!=True): return JsonResponse({'error': validateQuantity},status=400)
        validateMedium = validate_medium(data)
        if(validateMedium!=True): return JsonResponse({'error': validateMedium},status=400)
        try:
             rider_id = User.objects.get(id=data['rider_id'])  # Fetch the User instance
             print("safe till here")
             newRide = Ride(
                            from_location=data['from_location'],
                            to_location=data['to_location'],
                            date=data['date'],
                            quantity=data['quantity'],
                            medium = data['medium'],
                            rider_id=rider_id  # Assign the User instance
                        )
             newRide.save()
             response_data = {
                'message': 'Ride added successfully',
                'data': {
                    'id': newRide.id,
                    'from_location': newRide.from_location,
                    'to_location': newRide.to_location,
                    'date': newRide.date,
                    'quantity': newRide.quantity,
                    'medium': newRide.medium,
                    'rider_id': newRide.rider_id.id
                }
             }
            #newUser = User(name=name, username=username, mobilenumber=mobilenumber, email=email)
             return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
def getTransportRequests(request):
    if request.method == 'GET':
        data = request.GET
        validateRequesterid = validate_id(data, 'requester_id')
        if(validateRequesterid!=True): return JsonResponse({'error': validateRequesterid}, status=400)
        validatePageNo= validate_pageno(data)
        if(validatePageNo!=True): return JsonResponse({'error': validatePageNo}, status=400)
        validatePageSize= validate_pageSize(data)
        if(validatePageSize!=True): return JsonResponse({'error': validatePageSize}, status=400)

        validateStatus =validate_status(data)
        if(validateStatus!=True): return JsonResponse({'error': validateStatus}, status=400)
        validateAssetType = validate_asset_type_null_allowed(data)
        if(validateAssetType!=True): return JsonResponse({'error': validateAssetType}, status=400)


        requester_id = request.GET.get('requester_id')
        pageno = int(request.GET.get('pageno'))
        pageSize = int(request.GET.get('pageSize'))
        status = request.GET.get('status')
        asset_type =request.GET.get('asset_type')



        try:
             if status and asset_type:
                  requests = TransportRequest.objects.filter(status=status, asset_type=asset_type, date__gte=date.today()).order_by('date')[pageno*pageSize: (pageno+1)*pageSize]
             elif status:
                  requests = TransportRequest.objects.filter(status=status,date__gte=date.today()).order_by('date')[pageno*pageSize: (pageno+1)*pageSize]
             elif asset_type:
                  requests = TransportRequest.objects.filter(asset_type=asset_type,date__gte=date.today()).order_by('date')[pageno*pageSize: (pageno+1)*pageSize]
             else:
                  requests = TransportRequest.objects.filter(date__gte=date.today()).order_by('date')[pageno*pageSize: (pageno+1)*pageSize]
             serialized_requests = []
             for req in requests:
                 serialized_requests.append({
                     'requester_id': req.requester_id.id,
                     'from_location': req.from_location,
                     'to_location': req.to_location,
                     'date': req.date,
                     'receiver_mobilenumber': req.receiver_mobilenumber,
                     'quantity': req.quantity,
                     'asset_type': req.asset_type,
                     'sensitivity': req.sensitivity,
                     'status': req.status
                 })
             return JsonResponse({'data': serialized_requests}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def validate_pageno(data):
    pageno = data.get('pageno')
            # Check if quantity is not null
    if pageno is None:
        return 'pageno is required.'

    try:
        pageno = int(pageno)
    except Exception as e:
        return str(e)
    # Check if quantity is greater than 0
    if pageno < 0:
        return 'pageno must be a whole number.'

    # If all checks pass, return True
    return True

def validate_pageSize(data):
    pageSize = data.get('pageSize')
                # Check if quantity is not null
    if pageSize is None:
        return 'pageSize is required.'

    # Check if quantity is an integer
    try:
        pageSize = int(pageSize)
    except Exception as e:
        return str(e)
        # Check if quantity is greater than 0
    if pageSize <= 0:
        return 'pageSize must be a positive number.'

    # If all checks pass, return True
    return True


def validate_status(data):
    status = data.get('status')
    if status is None:
        return True
    if (not isinstance(status, str)) or   status not in STATUSES:
        return 'invalid status'
    return True;



def validate_asset_type_null_allowed(data):
    asset_type = data.get('asset_type')

        # Check if asset_type is not null
    if not asset_type:
        return True

    # Check if asset_type is among the allowed choices
    if (not isinstance(asset_type, str)) or asset_type not in ASSET_TYPE_CHOICES:
        return f'Invalid asset type. Allowed types are: {", ".join(ASSET_TYPE_CHOICES)}.'

    # If all checks pass, return True
    return True

def validate_date(data):
    date_str = data.get('date')

    # Check if date is provided
    if not date_str:
        return 'Date is required.'

    try:
        # Convert date string to datetime object
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return 'Invalid date format. Date should be in yyyy-mm-dd format.'
    print(datetime_obj.date())
    print(datetime.now().date())
    # Check if date is in the future
    if datetime_obj.date() < datetime.now().date():
        return 'Date must be in the future.'

    # If all checks pass, return True
    return True

def getMatchingRides(request):
    if request.method == 'GET':
        validatePageNo= validate_pageno(request.GET)
        if(validatePageNo!=True): return JsonResponse({'error': validatePageNo}, status=400)
        validatePageSize= validate_pageSize(request.GET)
        if(validatePageSize!=True): return JsonResponse({'error': validatePageSize}, status=400)
        pageno = int(request.GET.get('pageno'))
        pageSize = int(request.GET.get('pageSize'))
        request_id = request.GET.get('request_id')
        if request_id is None:
            return JsonResponse({'error': 'request_id is required'}, status=400)
        try:
            request_id = int(request_id)
            if(TransportRequest.objects.filter(id=request_id).exists()==True):
                transportRequest = TransportRequest.objects.get(id=request.GET.get('request_id'))
                rides = Ride.objects.filter(from_location=transportRequest.from_location,
                                            to_location=transportRequest.to_location,
                                            date=transportRequest.date,
                                            quantity__gte=transportRequest.quantity
                )[pageno*pageSize: (pageno+1)*pageSize]
                serialized_rides = []
                for ride in rides:
                    serialized_rides.append({
                        'rider_id': ride.rider_id.id,
                        'from_location': ride.from_location,
                        'to_location': ride.to_location,
                        'date': ride.date,
                        'quantity': ride.quantity,
                        'medium': ride.medium
                    })
                return JsonResponse({'data': serialized_rides}, status=200)
            else:
                return  JsonResponse({'error': 'request_id does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=400)

@csrf_exempt
def applyForRide(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        validateRideIdRequestId = validate_ride_id_request_id(data)

        if(validateRideIdRequestId!=True): return JsonResponse({'error': validateRideIdRequestId}, status=400)

        try:
            request_id = int(data.get('request_id'))

            ride_id = int(data.get('ride_id'))
            newApplication = ReqApplication(request_id=TransportRequest.objects.get(id=request_id),
                             ride_id=Ride.objects.get(id=ride_id), datetime=datetime.now(),status='applied')
            newApplication.save()
            TransportRequest.objects.filter(id=request_id).update(status='applied')

            return JsonResponse({'data': str(newApplication)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def validate_ride_id_request_id(data):
    request_id = data.get('request_id')
    print(request_id)
    if request_id is None: return 'request_id is required'

    ride_id = data.get('ride_id')
    print(ride_id)
    if ride_id is None: return 'ride_id is required'

    try:

        request_id = int(request_id)
        ride_id = int(ride_id)

        if ride_id not in matchingRidesOfRequest(request_id): return 'ride is not a match to the request'
    except Exception as e:
        return str(e)
    return True


def matchingRidesOfRequest(request_id):
    transportRequest = TransportRequest.objects.get(id=request_id)
    matching_rides_ids = Ride.objects.filter(
        from_location=transportRequest.from_location,
        to_location=transportRequest.to_location,
        date=transportRequest.date,
        quantity__gte=transportRequest.quantity
    ).values_list('id', flat=True)
    return list(matching_rides_ids)





"""
jango debug toolbar

next api
application(requestId, rideId)
aplly(requestid, rideid)- this shud save a reciord in applications


matchinf rides(requestid)date, quantity, from to must match

"""
