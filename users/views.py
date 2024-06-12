import json
import random
from datetime import datetime, timedelta

import jwt
import requests
from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.forms import CreateUserRequestForm
from users.models import User, Document, UserCreateRequest, Type, University, UniversityImage, Partner, Suggestion
from users.serializers import UserSerializer, DocumentSerializer, PartnerSerializer, SuggestionSerializer


class PartnerListView(APIView):
    def post(self, request):
        partners = Partner.objects.all()
        print(partners)
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data)


class SubmitPartnerView(APIView):
    def post(self, request):
        print(request.data)
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        print(serializer.errors)
        return Response(serializer.errors, status=400)


class SubmitSuggestionView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        data = request.data
        data['user'] = User.objects.filter(id=payload['id']).first().id
        serializer = SuggestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        print(serializer.errors)
        return Response(serializer.errors, status=400)


class SuggestionListView(APIView):
    def post(self, request):
        suggestions = Suggestion.objects.all()
        serializer = SuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)


class CheckUserView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        email = request.data['email']

        if len(User.objects.filter(phone_number=phone_number)) + len(User.objects.filter(email=email)) == 0:
            return Response({}, status=200)
        return Response({}, status=400)


class UploadDocumentView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        title = request.data.get('title')
        document_id = request.data.get('id')
        print(document_id)
        if document_id != 'undefined':
            document = Document.objects.filter(pk=document_id).first()
            if document:
                document.file = file
                document.status = 'pending'
                document.save()
                print('DOCUMENT HAS BEEN CHANGED')
                return Response({'message': 'Document updated successfully'}, status=200)
            else:
                token = request.data.get('jwt')
                payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
                user = User.objects.filter(id=payload['id']).first()
                if not user:
                    return Response({'error': 'User not found'}, status=404)
                document_type = Type.objects.filter(title=title).first()
                if not document_type:
                    return Response({'error': 'Document type not found'}, status=404)
                document = Document.objects.create(title=document_type, file=file, status='pending')
                user.user_documents.add(document)
                return Response({'message': 'Document updated successfully'}, status=200)
        else:
            token = request.data.get('jwt')
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
            user = User.objects.filter(id=payload['id']).first()
            if not user:
                return Response({'error': 'User not found'}, status=404)
            document_type = Type.objects.filter(title=title).first()
            if not document_type:
                return Response({'error': 'Document type not found'}, status=404)
            document = Document.objects.create(title=document_type, file=file, status='pending')
            user.user_documents.add(document)
            return Response({'message': 'Document updated successfully'}, status=200)


class ApplicationView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        chance = 0
        stats = True
        for document in user.user_documents.all():
            print(document.title.score)
            if document.status == 'approved':
                chance += document.title.score
            else:
                stats = False

        if not user.apply_approved:
            return Response({'chance': -1}, status=200)
        print(user.university)
        return Response({
            'status': stats and len(user.user_documents.all()) > 0,
            'chance': chance,
            'start': user.created_date,
            'university': user.university.name,
            'days_left': user.university.end_date - datetime.now().date(),
            'user': user.first_name + ' ' + user.last_name,
        },
        status=200)


class ApplicationByIdView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        chance = 0
        stats = True
        for document in user.user_documents.all():
            print(document.title.score)
            if document.status == 'approved':
                chance += document.title.score
            else:
                stats = False

        if not user.apply_approved:
            return Response({'chance': -1}, status=200)
        print(user.university)
        return Response({
            'status': stats and len(user.user_documents.all()) > 0,
            'chance': chance,
            'start': user.created_date,
            'university': user.university.name,
            'days_left': user.university.end_date - datetime.now().date(),
            'user': user.first_name + ' ' + user.last_name,
        },
        status=200)


class ApplicationByIdView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        chance = 0
        stats = True
        for document in user.user_documents.all():
            print(document.title.score)
            if document.status == 'approved':
                chance += document.title.score
            else:
                stats = False

        if not user.apply_approved:
            return Response({'chance': -1}, status=200)
        print(user.university)
        return Response({
            'status': stats and len(user.user_documents.all()) > 0,
            'chance': chance,
            'start': user.created_date,
            'university': user.university.name,
            'days_left': user.university.end_date - datetime.now().date(),
            'user': user.first_name + ' ' + user.last_name,
        },
        status=200)


class ApplicationAdminView(APIView):
    def post(self, request):
        users = User.objects.filter(apply_approved=True)
        applications = []
        for user in users:
            chance = 0
            stats = True
            for document in user.user_documents.all():
                print(document.title.score)
                if document.status == 'approved':
                    chance += document.title.score
                else:
                    stats = False
            if not user.apply_approved:
                return Response({'chance': -1}, status=200)
            print(user.university)
            applications.append({
                'user': user.toJson(),
                'status': stats and len(user.user_documents.all()) > 0,
                'chance': chance,
                'start': user.created_date,
                'university': user.university.name,
                'days_left': user.university.end_date - datetime.now().date(),
                # 'user': user.first_name + ' ' + user.last_name,
            },)
        print(applications)
        return Response(applications, status=200)


class EditDocumentStatusView(APIView):
    def post(self, request, id):
        document = Document.objects.get(pk=id)
        print(document)
        status = request.data.get('status')
        reject_reason = request.data.get('reject_reason')
        if status == 'Approved':
            document.status = 'approved'
        if status == 'Rejected':
            document.status = 'rejected'
            document.decline_reason = reject_reason
        if status == 'Pending':
            document.status = 'pending'

        document.save()
        print(request.data)
        return Response({}, status=200)


class ApproveApplicationView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        print(user)
        user.apply_approved = True
        user.created_date = datetime.now()
        user.university = University.objects.filter(slug=request.data.get('university')).first()
        user.save()
        return Response({}, status=200)


def update_user(request, field):
    data = json.loads(request.body)
    token = data.get('jwt')
    payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    if field == 'first_name':
        name = data.get('first_name')
        user.first_name = name
        user.save()
        return JsonResponse({'status': 'success', 'message': f'{field} updated successfully.'}, status=200)
    if field == 'last_name':
        last_name = data.get('last_name')
        user.last_name = last_name
        user.save()
        return JsonResponse({'status': 'success', 'message': f'{field} updated successfully.'}, status=200)
    elif field == 'birth_date':
        birth_date = data.get('birth_date')
        user.birth_date = birth_date
        user.save()
        return JsonResponse({'status': 'success', 'message': f'{field} updated successfully.'}, status=200)
    elif field == 'iin':
        iin = data.get('iin')
        user.iin = iin
        user.save()
        return JsonResponse({'status': 'success', 'message': f'{field} updated successfully.'}, status=200)

    elif field == 'email':
        email = data.get('email')
        user.email = email
        user.save()
        return JsonResponse({'status': 'success', 'message': f'{field} updated successfully.'}, status=200)
    elif field == 'password':
        password = data.get('password')
        user.password = password
        user.save()
        return JsonResponse({'status': 'success', 'message': f'{field} updated successfully.'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid field.'}, status=400)


class RegisterRequestView(APIView):
    def post(self, request):
        form = CreateUserRequestForm(data=request.data)
        if form.is_valid():
            # try:
            userCreateRequest = form.save()
            # except:
            #     print(e)
            #     return Response({'message': 'Пользователь с такой почтой или номером уже существует!'})
            sms_code = str(random.randint(100000, 999999))
            userCreateRequest.sms_code = sms_code
            userCreateRequest.save()
            print(sms_code)
            response = requests.post("https://api.mobizon.kz/service/message/sendsmsmessage?recipient=" + userCreateRequest.phone_number + "&text=Код для входа на сайт www.dormbooking.kz : " + sms_code + "&apiKey=kz0502f56621750a9ca3ac636e8301e235c2b647839531f2994222514c786fb6ff2178")
            print(response.json())
            return Response({'message': 'SMS code sent. Please verify to complete registration.', 'sms_code': sms_code},
                            status=200)

        return Response(form.errors, status=400)


class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        if len(UserCreateRequest.objects.filter(sms_code=request.data['sms_code'])) == 0:
            return Response({'message': 'Wrong sms code'}, status=400)

        userCreateRequest = UserCreateRequest.objects.filter(sms_code=request.data['sms_code']).first()

        user = User(
            first_name=userCreateRequest.first_name,
            last_name=userCreateRequest.last_name,
            email=userCreateRequest.email,
            phone_number=userCreateRequest.phone_number,
            username=userCreateRequest.username,
            password=userCreateRequest.password,
            iin=userCreateRequest.iin,
            birth_date=userCreateRequest.birth_date
        )
        user.save()

        token = jwt.encode(
            {'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24), 'iat': datetime.utcnow()}, 'sercet',
            algorithm='HS256').encode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'token': token}

        return response


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(email, password)
        user = User.objects.filter(email=email, password=password).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        token = jwt.encode(
            {'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24), 'iat': datetime.utcnow()}, 'sercet',
            algorithm='HS256').encode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'token': token}

        return response


class UserView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        if not token:
            raise AuthenticationFailed("Failed to authorize")
        try:
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authorization is expired")

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed("User not found")

        # Add isAdmin field to the user data
        user_data = UserSerializer(user).data
        user_data['isAdmin'] = user.is_superuser

        return Response(user_data)


class UserDocuments(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed("Failed to authorize")
        try:
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authorization is expired")
        user = User.objects.filter(id=payload['id']).first()
        data = []
        for i in user.user_documents.all():
            item = {
                'id': i.pk,
                'decline': i.decline_reason,
                'title': i.title.title,
                'score': i.title.score,
                'status': i.status,
                'file' : i.file.name
            }
            data.append(item)
        print(data)
        return Response(data)


class UserDocumentsById(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        data = []
        for i in user.user_documents.all():
            item = {
                'id': i.pk,
                'decline': i.decline_reason,
                'title': i.title.title,
                'score': i.title.score,
                'status': i.status,
                'file' : i.file.name
            }
            data.append(item)
        print(data)
        return Response(data)


class UniversitiesView(APIView):
    def get(self, request, search):
        queryset = University.objects.all()
        data = []
        for i in queryset:
            item = {
                'id': i.pk,
                'name': i.name,
                'slug': i.slug,
                'distance': i.distance,
                'description': i.description,
                'address': i.address,
                'places': i.available_places - len(User.objects.filter(university=i, apply_approved=True)),
                'price': i.price,
                'days_left': i.end_date - datetime.now().date(),
                'image': i.image.url
            }
            data.append(item)
        if search != 'undefined':
            queryset = queryset.filter(name__icontains=search)  # Example filter on 'name' field

            # Update data with filtered queryset
            data = [{
                'id': obj.pk,
                'name': obj.name,
                'slug': obj.slug,
                'distance': obj.distance,
                'description': obj.description,
                'address': obj.address,
                'places': obj.available_places - len(User.objects.filter(university=obj, apply_approved=True)),
                'price': obj.price,
                'days_left': obj.end_date - datetime.now().date(),
                'image': obj.image.url
            } for obj in queryset]
        print(data)
        return Response(data)


class UniversityBySlugView(APIView):
    def get(self, request, slug):
        university = University.objects.filter(slug=slug).first()
        images = [image.images.url for image in UniversityImage.objects.filter(post=university)]
        return Response({
            'images': images,
            'id': university.pk,
            'name': university.name,
            'slug': university.slug,
            'distance': university.distance,
            'description': university.description,
            'address': university.address,
            'places': university.available_places - len(User.objects.filter(university=university, apply_approved=True)),
            'price': university.price,
            'start': university.start_date,
            'end': university.end_date,
            'days_left': university.end_date - datetime.now().date(),
            'image': university.image.url
        })
