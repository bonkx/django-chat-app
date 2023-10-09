from django.shortcuts import redirect, render


def home(request):
    context = {}
    # return render(request, "web/home.html", context)
    return redirect("chat")

