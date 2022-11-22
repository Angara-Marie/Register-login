from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import User,Detail, Identification
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, DetailSerializer
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser,FileUploadParser

User = get_user_model()
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)        

# Create your views here.
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def Register_Users(request):
#     try:
#         data = []
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.is_active = True
#             user.save()
#             token = Token.objects.get_or_create(user=user)[0].key
#             data["message"] = "user registered successfully"
#             data["email"] = user.email
#             data["token"] = token

#         else:
#             data = serializer.errors


#         return Response(data)
#     except IntegrityError as e:
#         user=User.objects.get(email='')
#         user.delete()
#         raise ValidationError({"400": f'{str(e)}'})

#     except KeyError as e:
#         print(e)
#         raise ValidationError({"400": f'Field {str(e)} missing'})


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):

#         data = {}
#         reqBody = json.loads(request.body)
#         email = reqBody['email']
#         print(email)
#         password = reqBody['password']
#         try:

#             Customer = User.objects.get(email=email)
#         except BaseException as e:
#             raise ValidationError({"400": f'{str(e)}'})

#         token = Token.objects.get_or_create(user=Customer)[0].key
#         print(token)
#         if not check_password(password, user.password):
#             raise ValidationError({"message": "Incorrect Login credentials"})

#         if Customer:
#             if Customer.is_active:
#                 print(request.user)
#                 login(request, Customer)
#                 data["message"] = "user logged in"
#                 data["email"] = Customer.email

#                 Res = {"data": data, "token": token}

#                 return Response(Res)

#             else:
#                 raise ValidationError({"400": f'Customer not active'})

#         else:
#             raise ValidationError({"400": f'Customer doesnt exist'})


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def User_logout(request):

#     request.user.auth_token.delete()

#     logout(request)

#     return Response('User Logged out successfully')   


# class IdentificationView(viewsets.ModelViewSet):
#     queryset=Identification.objects.all()
#     serializer_class = IdentificationSerializer
#     parser_classes = (MultiPartParser, FormParser, JSONParser)


#     def create(self, request, format=None):
#         data = request.data
#         if isinstance(data, list):  # <- is the main logic
#             serializer = IdentificationSerializer(data=request.data, many=True)
#         else:
#             serializer = IdentificationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailView(viewsets.ModelViewSet):
    queryset = Detail.objects.all() 
    serializer_class =   DetailSerializer  
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser) 
    def create(self, request):
            serializer = DetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            validated_data= serializer.validated_data
            income = validated_data.get("income")
            rent_amount = validated_data.get("rent_amount")
            electricity_bill= validated_data.get("electricity_bill")
            water_bill = validated_data.get("water_bill")

            fixed_obligations = rent_amount + electricity_bill + water_bill
            loan_amount =validated_data.get("loan_amount")
            disposable_income_for_loan = income - fixed_obligations

            probability = (disposable_income_for_loan / income) * 100
            customer = validated_data.get("customer")
            if probability > 50 and loan_amount <= disposable_income_for_loan:
                return Response (f"Congratulations {customer.first_name}, you are eligible for Ksh {loan_amount}.")
            return Response (f"We are sorry {customer.first_name}, you are not eligible for Ksh {loan_amount}, you can apply for Ksh {disposable_income_for_loan}.")                      