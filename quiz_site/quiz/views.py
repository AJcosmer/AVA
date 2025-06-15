from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.http import require_POST
import random
import json
from django.http import JsonResponse


# Vista de Registro
@csrf_exempt
@csrf_exempt
@require_POST
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email", "")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not username or not password:
            return JsonResponse({"error": "Usuario y contraseña requeridos."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "El usuario ya existe."}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=first_name, last_name=last_name)

        return JsonResponse({"message": "Registro exitoso."})

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Vista principal con login y registro
@csrf_exempt
def index(request):
    if request.method == 'POST' and 'register' in request.POST:
        return register(request)

    return render(request, 'quiz/index.html')


# API para obtener preguntas matemáticas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questions(request):
    difficulty = request.GET.get('difficulty', 'easy')
    num_questions = int(request.GET.get('num', 5))
    questions = []

    operators = {
        "easy": ['+', '-'],
        "medium": ['+', '-', '*'],
        "hard": ['+', '-', '*', '/']
    }

    for _ in range(num_questions):
        op = random.choice(operators[difficulty])

        if difficulty == 'easy':
            a, b = random.randint(1, 10), random.randint(1, 10)
        elif difficulty == 'medium':
            a, b = random.randint(10, 30), random.randint(1, 10)
        else:
            a, b = random.randint(20, 100), random.randint(1, 20)
            if op == '/':
                a = a * b

        question_text = f"{a} {op} {b}"
        correct_answer = eval(question_text)
        if op == '/':
            correct_answer = round(correct_answer, 2)

        options = {correct_answer}
        while len(options) < 4:
            delta = random.randint(1, 10)
            wrong = correct_answer + random.choice([-delta, delta])
            wrong = round(wrong, 2) if op == '/' else wrong
            options.add(wrong)

        questions.append({
            "question": question_text,
            "options": [str(x) for x in random.sample(list(options), 4)],
            "answer": str(correct_answer)
        })

    return Response(questions)


# API de información del usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "id": user.id,
    })
