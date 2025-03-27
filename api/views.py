from django.shortcuts import render

#Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact

class HelloWorld(APIView):



    def get(self, request):
        return Response({"message": "Hello, Group3!"}, status=status.HTTP_200_OK)

class Students(APIView):
    def get(self, request):
        students = {
            1: {
                "NAME": "John",
                "AGE": 20,
                "GRADE": "A",
                "COURSE": "Computer Science"
            },
            2: {
                "NAME": "Alice",
                "AGE": 22,
                "GRADE": "B",
                "COURSE": "Engineering"
            },
            3: {
                "NAME": "Bob",
                "AGE": 21,
                "GRADE": "A",
                "COURSE": "Mathematics"
            },
            4: {
                "NAME": "Eve",
                "AGE": 23,
                "GRADE": "C",
                "COURSE": "Physics"
            },
            5: {
                "NAME": "Charlie",
                "AGE": 19,
                "GRADE": "B",
                "COURSE": "Biology"
            }
        }
        return Response(students, status=status.HTTP_200_OK)
class ContactListView(APIView):
    #class helper
    def create_contact(self, data):
        """Helper function to create a Contact object from data."""
        return Contact(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', '')
        )
    
    def post(self, request, *args, **kwargs):
        data = request.data  # Can be a single dict or a list of dicts
        
        if isinstance(data, dict):  # Single entry
            contact = self.create_contact(data)
            contact.save()
            return Response({"message": "Contact added successfully!", "id": contact.id}, status=status.HTTP_201_CREATED)

        elif isinstance(data, list):  # Bulk upload
            contacts = [self.create_contact(item) for item in data]
            Contact.objects.bulk_create(contacts)  # Efficient bulk insert
            return Response({"message": f"{len(contacts)} contacts added successfully!"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)