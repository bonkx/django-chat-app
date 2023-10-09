from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dash.helpers.crypt import do_decrypt, do_encrypt


@login_required
def index(request):
    q = request.POST.get("q", "")
    encrypted_string = None
    decrypted_string = None

    if request.method == "POST":
        if q:
            encrypted_string = do_encrypt(q)
            decrypted_string = do_decrypt(encrypted_string)

    context = {
        "q": q,
        "encrypted_string": encrypted_string,
        "decrypted_string": decrypted_string,
    }
    return render(request, "web/encryption.html", context)
