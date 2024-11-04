import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import UserRegistration
from .geminiapi import chat_with_gemini, get_response
from .models import Biomarker, CustomUser, History


class HomePage(TemplateView):
    template_name = "home.html"


class SignUp(CreateView):
    success_url = reverse_lazy("login")
    form_class = UserRegistration
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(self, request, *args, **kwargs)


class Login(LoginView):
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True
    template_name = "login.html"


class Logout(LogoutView):
    next_page = "home"
    http_method_names = ["get", "post"]


class Health(TemplateView):
    template_name = "health.html"


@login_required
@csrf_exempt
def bot(request):
    history, created = History.objects.get_or_create(user=request.user)
    messages = []
    if not created:
        messages = [
            msg["parts"][0]
            for msg in history.messages[2:]
            if not msg["parts"][0].startswith("Biomarker Update on ")
        ]
    if request.method == "POST":
        data = json.load(request)
        query = data.get("data")
        response = chat_with_gemini(query, history.messages)
        user_msg = {"role": "user", "parts": [query]}
        ai_msg = {"role": "model", "parts": [response]}
        history.messages.append(user_msg)
        history.messages.append(ai_msg)
        history.save()
        return JsonResponse({"status": "success", "response": response})
    return render(request, template_name="bot.html", context={"messages": messages})


@csrf_exempt
def api_call(request):
    data = json.load(request)
    symptoms = data.get("data")
    symptoms = ", ".join(symptoms)
    response = get_response(symptoms)
    if len(response) < 1:
        return JsonResponse(
            {
                "status": "invalid",
                "data": "Please provide valid input so we can help you.",
            }
        )

    card = """
    <div class="disease-card bg-white rounded-xl p-6 mb-4">

        <h3 class="text-xl font-semibold text-pink-600 mb-4">{name}</h3>
        <p class="text-gray-600 mb-6">
            {description}
        </p>

        <div class="space-y-6">
            <details>
                <summary class="font-medium text-gray-700">Preventive Steps</summary>
                <ul class="list-none" style="columns: 2;">
                    {preventions}
                </ul>
            </details>

            <details>
                <summary class="font-medium text-gray-700">Long Term Complications</summary>
                <ul class="list-none" style="columns: 2;">
                    {complications}
                </ul>
            </details>

            <details>
                <summary class="font-medium text-gray-700">Next steps when diagnosed</summary>
                <ul class="list-none" style="columns: 2;">
                   {next_steps}
                </ul>
            </details>
        </div>
    </div>
    
    """
    elements = []

    for disease in response:
        preventions = "".join(
            ["<li> ➡️ {0} </li>".format(x) for x in disease["preventive_steps"]]
        )
        complications = "".join(
            ["<li> ➡️ {0} </li>".format(x) for x in disease["long_term_complications"]]
        )
        next_steps = "".join(
            ["<li> ➡️ {0} </li>".format(x) for x in disease["next_steps"]]
        )

        elements.append(
            card.format(
                name=disease["name"],
                description=disease["description"],
                preventions=preventions,
                complications=complications,
                next_steps=next_steps,
            )
        )

    html_str = "".join(elements)
    return JsonResponse({"status": "success", "data": html_str})


@login_required
@csrf_exempt
def overall(request):
    history, created = History.objects.get_or_create(user=request.user)
    if request.method == "POST":
        data = json.load(request)
        marker = Biomarker(
            marker=data["marker"], value=data["value"], user=request.user
        )
        marker.save()
        time = marker.time.strftime("%d %B %Y, Hour:%H, Minute:%M")
        bio_update_message = {
            "role": "user",
            "parts": [
                f"Biomarker Update on : {time}, {marker.marker} {marker.value}",
            ],
        }

        history.messages.append(bio_update_message)
        history.save()
        return JsonResponse({"status": "success"})
    markers = Biomarker.objects.filter(user=request.user).order_by("time")
    return render(request, template_name="overall.html", context={"markers": markers})
