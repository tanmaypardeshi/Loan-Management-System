from rest_framework.views import APIView
from rest_framework.response import Response


class BaseView(APIView):
    def get(self, request):
        return Response({'message': 'Base View'})
