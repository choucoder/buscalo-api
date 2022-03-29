from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.feeds.serializers import FeedSerializer
from apps.products.serializers import ListProductSerializer
from .models import Report
from apps.posts.models import Post
from apps.products.models import Product
from apps.feeds.models import Feed
from .serializers import ReportSerializer, CreateReportSerializer
from core.views import PaginateAPIView


class ReportsAPIView(PaginateAPIView):
    min_reports_to_delete = 4

    serializer_classes = {
        'list': ReportSerializer,
        'create': CreateReportSerializer,
        'feed': FeedSerializer,
        'product': ListProductSerializer
    }
    default_serializer_class = ReportSerializer

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)
    

    def post(self, request):
        user = request.user
        data = request.data
        issued_model = data.get('issued_by_model')

        if issued_model == 0:
            feed = get_object_or_404(Feed, pk=data['id'])
            issued_model = feed.post
        else:
            issued_model = get_object_or_404(Product, pk=data['id'])
        
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            if isinstance(issued_model, Post):
                report = Report.objects.filter(post=issued_model, reported_by=user).first()
                if not report:
                    report = serializer.save(
                        post=issued_model,
                        created_by=issued_model.user if issued_model.user else issued_model.shop,
                        reported_by=user
                    )
                    serializer = self.get_serializer_class('feed')(instance=feed)
                else:
                    if not report.type == data['type']:
                        report.type = data['type']
                        report.save()
                        report.refresh_from_db()
                    
                    serializer = self.get_serializer_class('feed')(instance=feed)
                    msg = "Has cambiado el tipo de reporte de este post"
                    return Response(
                        {'data': serializer.data, 'msg': msg, 'deleted': 0},
                        status=status.HTTP_200_OK
                    )

                issued_model_reports = Report.objects.filter(post=issued_model)
                if issued_model_reports.count() >= self.min_reports_to_delete:
                    issued_model.delete()
                    msg = "El post reportado ha sido eliminado"
                    deleted = 1
                else:
                    msg = "El post ha sido reportado"
                    deleted = 0

            else:
                report = Report.objects.filter(product=issued_model, reported_by=user).first()
                if not report:
                    report = serializer.save(
                        product=issued_model,
                        created_by=issued_model.shop.user,
                        reported_by=user
                    )
                    serializer = self.get_serializer_class('product')(instance=issued_model)

                else:
                    if not report.type == data['type']:
                        report.type = data['type']
                        report.save()
                        report.refresh_from_db()
                    
                    serializer = self.get_serializer_class('product')(instance=issued_model)
                    msg = "Has cambiado el tipo de reporte de este producto"
                    return Response(
                        {'data': serializer.data, 'msg': msg, 'deleted': 0},
                        status=status.HTTP_200_OK
                    )

                issued_model_reports = Report.objects.filter(product=issued_model)
                if issued_model_reports.count() >= self.min_reports_to_delete:
                    issued_model.delete()
                    msg = "El producto reportado ha sido eliminado"
                    deleted = 1
                else:
                    msg = "El producto ha sido reportado"
                    deleted = 0

            return Response(
                {'data': serializer.data, 'msg': msg, 'deleted': deleted},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)