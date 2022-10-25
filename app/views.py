from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Cap, Price, Stock, Order
from .serializers import CapListSerializer, SizeSerializer, CapDetailSerializer, LinkSerializer, OrderCreateSerializer, OrderSerializer
from .pagination import CustomPagination


class CatalogListView(ListAPIView):
    queryset = Cap.objects.all().order_by('-id')
    serializer_class = CapListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'brand__name', ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(self.request.GET)
        сheapest = self.request.GET.get('сheapest')
        dearest = self.request.GET.get('dearest')
        print(сheapest, dearest)

        if сheapest is not None:
            queryset = queryset.all().order_by('-prices')
            print(queryset.values())
        elif dearest:
            queryset = queryset.all().order_by('prices')
        return queryset


class CapDetailView(RetrieveAPIView):
    queryset = Cap.objects.all()
    serializer_class = CapDetailSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', 'brand__name', ]

    # print(Cap.objects.filter(stocks=1))


    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #
    #     data = {}
    #
    #     # cap = data['cap'] = ['size']
    #
    # # for date_food in response.data:
    #     cap = response.data['cap']
    #     cap['size'] = response.data['size']
    #
    #         # if cap not in data:
    #         #     data[cap] = {"caps": [], 'size': date_food['size']}
    #         #
    #         # foods = data[cap]['caps']
    #         # foods.append(date_food['caps'])
    #
    #     return Response(cap)


    # def get(self, request):
    #     size = Stock.objects.all()
    #
    #     serializer = CapDetailView(size)
    #
    #     return Response(serializer.data)


class HomePageView(ListAPIView):
    queryset = Cap.objects.filter(name='Supreme')
    serializer_class = CapListSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', 'brand__name', ]


class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        elif self.request.method == "GET":
            return OrderSerializer

