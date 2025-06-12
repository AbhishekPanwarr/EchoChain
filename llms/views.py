from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404 
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import User, Conversation, Message
from .apis import calling
load_dotenv()


# Create your views here.
def index(request):
    return HttpResponse("This is the llm-django-backend")


@csrf_exempt
@require_POST
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return JsonResponse({'error': 'All fields are required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=400)
        user = User.objects.create(username=username, email=email, password=password)
        return JsonResponse({'message': 'User registered successfully.', 'user_id': user.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            try:
                user = User.objects.get(username=username, password=password)
                request.session["user_id"] = user.id
                return JsonResponse({"message": "Login successfull", "user_id": user.id})
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def llm_call(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            conv_id = data.get("conversation_id")
            user_promt = data.get("prompt")
            if not conv_id or not user_promt:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            try:
                responses = calling(conv_id, user_promt)
                
                return JsonResponse({"message": "successfull call", "llm_respones": responses})
            except :
                return JsonResponse({'error': 'LLM calling error'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt        
def message_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            conv_id = data.get("conversation_id")
            llm_model = data.get("model")
            role = "user" if data.get("role") == "user" else "assistant"
            content = data.get("content")
            if not role or not content or not conv_id or not llm_model:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            try:
                conv = Conversation.objects.get(id=conv_id)
                response = Message(conversation=conv, llm_model=llm_model, sender=role, content=content)
                response.save()
                
                return JsonResponse({"message": "message uploaded succesfully"})
            except :
                return JsonResponse({'error': 'message uploading error'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

def get_message(request, message_id):
    if request.method == "GET":
        try:
            msg = Message.objects.get(id=message_id)
            data = {
                "id": msg.id,
                "conversation_id": msg.conversation.id,
                "llm_model": msg.llm_model,
                "role": msg.sender,
                "content": msg.content,
                "timestamp": msg.timestamp,
            }
            return JsonResponse(data)
        except Message.DoesNotExist:
            return JsonResponse({"error": "Message not found"}, status=404)