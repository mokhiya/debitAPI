from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import DebitModel
from .serializers import LoanSerializer, RegisterSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"token": "dummy-token-for-now"}, status=status.HTTP_200_OK)
    return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_loan(request):
    request.data['user'] = request.user.id
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Loan added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_loans(request):
    loans = DebitModel.objects.filter(user=request.user, loan_type="BORROWED")
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loans_owed(request):
    loans = DebitModel.objects.filter(user=request.user, loan_type="LENT")
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_loan(request, pk):
    loan = get_object_or_404(DebitModel, pk=pk, user=request.user)
    loan.is_closed = True
    loan.save()
    return Response({"message": "Loan closed successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_get_users(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.query_params.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serializer = UserSerializer(page_obj, many=True)
    return Response({
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "results": serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_search_users(request):
    query = request.query_params.get('q', '')
    users = User.objects.filter(username__icontains=query)
    paginator = Paginator(users, 10)
    page_number = request.query_params.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serializer = UserSerializer(page_obj, many=True)
    return Response({
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "results": serializer.data
    })
