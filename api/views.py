from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from pets.models import Pet, Basket, RequestForGuardianship
from pets.serializers import (PetSerializer, BasketSerializer,
                              RequestForGuardianshipSerializer)
from users.serializers import UserRegistrationSerializer, UserSerializer
from pets.services.changing_the_basket import create_or_update_the_basket
from pets.tasks import send_email_about_request_for_guardianship_task
from users.tasks import send_email_verification


class PetModelViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser, )
        return  super(PetModelViewSet, self).get_permissions()

class BascketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        queryset = super(BascketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            pet_id = request.data['pet_id']
            pet = Pet.objects.filter(id=pet_id)
            if not pet.exists():
                return Response({'product_id': 'Данный объект не существует'},
                                status=status.HTTP_400_BAD_REQUEST)
            obj, new = create_or_update_the_basket(pet_id, self.request.user)
            status_code = status.HTTP_201_CREATED if new else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'pet_id': 'Данное поле является обязательным'},
                            status=status.HTTP_400_BAD_REQUEST)


class RequestForGuardianshipAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RequestForGuardianshipSerializer

    def get(self, request, format=None):
        snippet = RequestForGuardianship.objects.all()
        serializer = RequestForGuardianshipSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RequestForGuardianshipSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            feedback_id = feedback.id
            send_email_about_request_for_guardianship_task.delay(feedback_id)
            return Response({'status': 'sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_id = user.id
        send_email_verification.delay(user_id)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })