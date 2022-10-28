from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import Test
from .serializers import TestSerializer, TestCreateSerializer


class TestApiView(RetrieveAPIView, CreateAPIView, UpdateAPIView):
    serializer_class = TestSerializer
    lookup_field = 'code'
    allowed_methods = ['GET', 'POST', 'HEAD', 'OPTIONS']

    def get_queryset(self):
        return Test.objects.all()

    def post(self, request, *args, **kwargs):
        test_qs = Test.objects.filter(code=request.data['code'])
        # Shouldn't use POST to update an object, there are PUT and PATCH for that.
        # (I'm assuming it's for update, no specification was given)
        # Also, "code" variable is present in both body and URL, which calls for additional validation.
        if test_qs.first():
            return self.update(request, *args, **kwargs)
        else:
            return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Should be validated at serializer level (lines 20:25).
        # In tests, HTTP status code should be asserted; Error text is for humans and may be changed,
        # while status codes do not change unless application specification changes.
        if 'upper' and 'lower' not in request.data:
            return Response('Lower and upper cannot both be null', status=status.HTTP_400_BAD_REQUEST)
        if request.data['upper'] and request.data['upper'] < (request.data['lower'] or 0):
            return Response("Lower value can't exceed upper value", status=status.HTTP_400_BAD_REQUEST)

        serializer = TestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Should use status code 201 instead of 200, since this method is supposed to directly creates an object.
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.get_success_headers(serializer.data))

    # These ensure the error code is 405 instead of default 404
    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")
