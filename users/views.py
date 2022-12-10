import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from hw_27.settings import TOTAL_ON_PAGE
from users.serializers import *


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('-username')
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        response = {}
        items_list = [{'id': user.pk,
                       'name': user.first_name,
                       'first_name': user.first_name,
                       'last_name': user.last_name,
                       'role': user.role,
                       'age': user.age,
                       'locations': list(map(str, user.location.all())),
                       'total_ads': user.ads.filter(is_published=False).count()
                       } for user in obj
                      ]
        response['items_list'] = items_list
        response['total'] = self.object_list.count()
        response['num_pages'] = paginator.num_pages
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({'id': user.pk,
                             'name': user.first_name,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'role': user.role,
                             'age': user.age,
                             'locations': list(map(str, user.location.all())),
                             'total_ads': user.ads.filter(is_published=False).count()
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'role',
        'age',
        'location',
    ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'first_name' in data.keys():
            self.object.first_name = data['first_name']
        if 'last_name' in data.keys():
            self.object.last_name = data['last_name']
        if 'role' in data.keys():
            self.object.role = data['role']
        if 'age' in data.keys():
            self.object.age = data['age']
        if 'location' in data.keys():
            for loc_name in data['location']:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": list(map(str, self.object.location.all())),
        }, safe=False)


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=204)

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()

    serializer_class = LocationSerializer