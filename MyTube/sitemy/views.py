from django.contrib import auth
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from sitemy.models import Profile, Videos, Like_DisLikes
from rest_framework.permissions import IsAuthenticated

class newVideo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        title = request.data['title']
        id = request.data['id']
        name_video = request.data['name_video']
        video = request.data['video']
        Videos.objects.create(title=title, name_video=name_video, videofile=video, userProfile=Profile.objects.get(id=id))
        return Response({'statuts': 'created'})


class newPhoto(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        photo = request.data['photo']
        profile = Profile.objects.get(id=request.data['id'])
        profile.photo = photo
        print(profile)
        print(profile.photo)
        profile.save()
        return Response({'status': 'downloaded'})


class likeDislikeDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = self.request.data
        Like_DisLikes.objects.filter(video=data['video'], userProfile=data['userLike']).delete()
        return Response({'stutus' : 'deleted'})


# @method_decorator(csrf_protect, name='dispatch')
class likeDisLikesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
            data = self.request.data
            print("DATA:  ", data)

            if Like_DisLikes.objects.filter(video=data['video'], userProfile=data['userLike']).exists():
                like = Like_DisLikes.objects.get(video=data['video'], userProfile=data['userLike'])
                like.likes = data['likes']
                like.dislikes = data['dislikes']
                like.save()
                return Response({'recreate': 'ok'})
            else:
                new_like = Like_DisLikes()
                new_like.likes = data['likes']
                new_like.dislikes = data['dislikes']
                new_like.userProfile = Profile.objects.get(pk=data['userLike'])
                new_like.video = Videos.objects.get(pk=data['video'])
                new_like.save()
                return Response({'created': 'ok'})

def getLikesDislikes(pk):
    result = list(Like_DisLikes.objects.filter(video=pk).values_list('likes', 'dislikes'))
    likes = sum([x[0] for x in result])
    dislike = sum([x[1] for x in result])
    spisok = {'likes': likes, 'dislikes': dislike}
    return spisok


class VideosChannelView(APIView):
    def get(self, request, pk):
        # id канала

        results = list(Videos.objects.filter(userProfile=pk, isPublished=True).values())
        for i in results:
            i.update(getLikesDislikes(i['id']))

        print(results)
        return Response(results)



@api_view(['GET'])
def getUsers(request):
    usersProfile = Profile.objects.all();
    channels = list(usersProfile)
    result = []
    for i in channels:
        try:
            result.append({'photo': i.photo.url, 'username': i.user.username, 'id': i.id})
        except:
            result.append({'photo': '', 'username': i.user.username, 'id': i.id})
    return Response(result)

@api_view(['GET'])
def search(request):
    searchData = request.GET.get('search')
    results = list(Videos.objects.filter(Q(name_video__icontains=searchData) | Q(title__icontains=searchData)).values())
    for i in results:
        i.update(getLikesDislikes(i['id']))
    print(results)
    return Response(results)



@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        print(user)
        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                user_profile = Profile.objects.get(user=user)
                return Response({'isAuthenticated': 'success', "username": user.username, "id" : user_profile.id, 'isManager': user_profile.isManager})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})


@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        re_password = data['re_password']

        try:
            if password == re_password:
                if User.objects.filter(username=username).exists():
                    print(User.objects.all())
                    return Response({'error': 'Username already exists'})
                else:
                    if len(password) < 6:
                        return Response({'error': 'Password must be at least 6 characters'})
                    else:
                        user = User.objects.create_user(username=username, password=password)
                        user.save()
                        #
                        # user_profile = Profile.objects.create(user=user)
                        # user_profile.save()


                        return Response({'success': 'User created successfully'})
            else:
                return Response({'error': 'Passwords do not match'})
        except:
            return Response({'error': 'Something went wrong when registering account'})


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)
            user_profile = Profile.objects.get(user=user)
            if user is not None:
                auth.login(request, user)
                return Response({'success': 'User authenticated', 'userProfileId': user_profile.id, "username": user.username, "isManager": user_profile.isManager})
            else:
                return Response({'error': 'Error Authenticating'})
        except:
            return Response({'error': 'Something went wrong when logging in'})


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Loggout Out'})
        except:
            return Response({'error': 'Something went wrong when logging out'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        user = self.request.user
        id = self.request.id

        profile = Profile.objects.get(user=user)
        if profile.isManager != True:
            return Response({"status": "Permission Failed"})
        else:
            try:
                profile_delete = Profile.objects.filter(id=id).delete()
                return Response({"status": "Profile deleted successfully"})
            except:
                return Response({"status": "Something went wrong when trying to delete user"})


class DeletePublishedVideo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
                user = request.user
                profile = Profile.objects.get(user=user)
                id_video = request.data["id_video"]

                if profile.isManager != True:
                    return Response({"status": "Permission Failed"})
                else:
                    try:
                        video = Videos.objects.filter(id=id_video).delete()
                        print(video)
                        return Response({"status": "Video deleted successfully"})
                    except:
                        return Response({"status": "Profile deleted failed"})


class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        id_user = request.data["id_user"]

        if profile.isManager != True:
            return Response({"status": "Permission Failed"})
        else:
            try:
                deleted_user = Profile.objects.filter(id=id_user).delete()
                deleted_user.save()
                print(deleted_user)
                return Response({"status": "Profile deleted successfully"})
            except:
                return Response({"status": "Profile deleted failed"})

    def delete(self, request, format=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        id_user = request.data["id_user"]

        if profile.isManager != True:
            return Response({"status": "Permission Failed"})
        else:
            try:
                deleted_user = Profile.objects.filter(id=id_user).delete()
                deleted_user.save()
                print(deleted_user)
                return Response({"status": "Profile deleted successfully"})
            except:
                return Response({"status": "Profile deleted failed"})

class IsPublishedVideo(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    def delete(self, request, format=None):
            user = self.request.user
            print(user)
            profile = Profile.objects.get(user=user)
            print(profile)
            id_video = self.request.id_video

            if profile.isManager != True:
                return Response({"status": "Permission Failed"})
            else:
                try:
                    video = Videos.objects.filter(id=id_video)
                    print(video)
                    return Response({"status": "Video deleted successfully"})
                except:
                    return Response({"status": "Profile deleted failed"})

    def post(self, request, format=None):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        id_video = self.request.data["id_video"]

        if profile.isManager != True:
            return Response({"status": "Permission Failed"})
        else:
            try:
                video = Videos.objects.get(id=id_video)
                print(video)
                video.isPublished = True
                video.save()
                return Response({"status": "Video published successfully"})
            except:
                return Response({"status": "Video published failed"})


    def get(self, request, format=None):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile.isManager != True:
            return Response({"status": "Permission Failed"})
        else:
            try:
                videos = list(Videos.objects.filter(isPublished=False).values())
                return Response({"videos": videos})
            except:
                return Response({"status": "failed"})

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            print(self.request)
            user_profile = Profile.objects.get(user=user)

            return Response({"username": user.username, "photo": user_profile.photo})
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile'})