from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import exceptions

from rest_framework.view import APIView as AV
from rest_framework.generics import RetrieveUpdateAPIView
from .models import User, Users_likes, Posts
from .serializer import PostSerializer, RegistrationSerializer, LoginSerializer, UserSerializer, PostlikeSerializer
from .renderers import UserJSONRenderer



class SignUp(AV):
    # Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    def post(self, request):
        user = request.data.get('user', {})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginUser(AV):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # метод GET
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # метод PATCH: в теле отправлять все с изменениями
        serializer_data = request.data.get('user', {})

        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class PostCreation(AV):
    permission_classes = (IsAuthenticated,)
    def post (self, request):
        new_post = request.data.get('new_post')
        new_post['author_id'] = self.request.user.id

        serializer = PostSerializer (data=new_post)

        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()
        return Response(
                        {'success': f"Post '{post_saved.theme}' created successfully"},
                        status=status.HTTP_201_CREATED
                        )



class PostLike(AV):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        new_like = request.data.get('new_like')
        posts_id = new_like['posts_id']
        posts_author_id = Posts.objects.get(pk=posts_id).author_id
        if self.request.user.id == posts_author_id:
            return Response({'errors': "Author can't like hisown posts"},
                            status=status.HTTP_403_FORBIDDEN)
        new_like['user_id'] = self.request.user.id
        if Users_likes.objects.filter(posts_id__exact=posts_id,
                                      user__exact=self.request.user):
            return Response({'errors': "You've already like it"})
        serializer = PostlikeSerializer (data=new_like)

        if serializer.is_valid(raise_exception=True):
            try:
                _ = serializer.save()
            except Exception:
                msg = "Can't save data"
                raise exceptions.ValidationError(detail=msg)

            return Response(
              {'success': 'like was registrated'},
              status=status.HTTP_201_CREATED
        )



