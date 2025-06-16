from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from firebase_admin import db

# Constantes reutilizables
DOCUMENT_NOT_FOUND_MSG = "Documento no encontrado"

class LandingAPI(APIView):
    name = 'Landing API'
    collection_name = 'coleccion'
     
    def get(self, request):
        ref = db.reference(f'{self.collection_name}')
        data = ref.get()
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        ref = db.reference(f'{self.collection_name}')
        current_time = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format})
        new_resource = ref.push(request.data)
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)


class LandingAPIDetail(APIView):
    name = 'Landing Detail API'
    collection_name = 'coleccion'

    def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        data = ref.get()

        if data:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": DOCUMENT_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        data = ref.get()

        if data:
            ref.update(request.data)
            return Response({"message": "Documento actualizado correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": DOCUMENT_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        data = ref.get()

        if data:
            ref.delete()
            return Response({"message": "Documento eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": DOCUMENT_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
z