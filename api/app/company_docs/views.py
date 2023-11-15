import os
from django.http import JsonResponse, HttpResponse
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response

from app.main_users.permissions import IsFounder
from .models import Company_Doc
from .serializers import ReferalLinkSerializer, CompanyDocSerializer
from app.main_users.emails import send_become_founder



class ReferalLinkView(generics.CreateAPIView):
    serializer_class = ReferalLinkSerializer

    def post(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyDocViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company_Doc.objects.filter(is_private=False)
    serializer_class = CompanyDocSerializer
    lookup_field = 'slug'


class PrivateCompanyDocs(generics.GenericAPIView):
    queryset = Company_Doc.objects.filter(is_private=True)
    serializer_class = CompanyDocSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        doc = self.queryset.filter(slug=kwargs["slug"]).first()
        file_path =f"/ClickWork/backend/static/media/{doc.file}"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as pdf_doc:
                response = HttpResponse(pdf_doc)
                response['Content-Type'] = 'application/pdf'
                response['Content-Disposition'] = f'attachment; filename={kwargs["slug"]}'
                return response
        return JsonResponse(data={"message": "File doesn't exists"})

    
class FounderAgreementView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        user.founder = True
        user.save()
        send_become_founder.delay(user_id=user.id, email_to=user.email)
        return Response({'Status': True, 'message': 'Ok'}, status=status.HTTP_200_OK)
        

class FounderRevokeView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsFounder)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        user.founder = False
        user.save()
        # send email that foundership was revoked
        return Response({'Status': True, 'message': 'Ok'}, status=status.HTTP_200_OK)
        
