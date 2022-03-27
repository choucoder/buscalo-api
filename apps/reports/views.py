from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Report
from apps.posts.models import Post
from apps.products.models import Product
from .serializers import ReportSerializer, CreateReportSerializer
from core.views import PaginateAPIView


class ReportsAPIView(PaginateAPIView):
    serializer_classes = {
        'list': ReportSerializer,
        'create': CreateReportSerializer,
    }
    default_serializer_class = ReportSerializer

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)
    

    def post(self, request):
        user = request.user
        data = request.data
        issued_model = data.get('issued_by_model')

        if issued_model == 'Post':
            issued_model = get_object_or_404(Post, pk=data['id'])
        else:
            issued_model = get_object_or_404(Product, pk=data['id'])
        
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            if isinstance(issued_model, Post):
                report = Report.objects.filter(post=issued_model, reported_by=user).first()
                if not report:
                    report = serializer.save(
                        post=issued_model,
                        created_by=issued_model.user,
                        reported_by=user
                    )
                else:
                    if not report.type == data['type']:
                        report.type = data['type']
                        report.save()
                        report.refresh_from_db()
                    
                    serializer = self.get_serializer_class('list')(instance=report)
                    return Response(
                        {'data': serializer.data},
                        status=status.HTTP_200_OK
                    )
                    
            else:
                report = Report.objects.filter(product=issued_model, reported_by=user).first()
                if not report:
                    report = serializer.save(
                        product=issued_model,
                        created_by=issued_model.shop.user,
                        reported_by=user
                    )
                else:
                    if not report.type == data['type']:
                        report.type = data['type']
                        report.save()
                        report.refresh_from_db()
                    
                    serializer = self.get_serializer_class('list')(instance=report)
                    return Response(
                        {'data': serializer.data},
                        status=status.HTTP_200_OK
                    )

            serializer = self.get_serializer_class('list')(instance=report)
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)