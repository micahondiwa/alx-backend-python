from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseNotAllowed

# Keep existing imports and views above this

@login_required
def delete_user(request):
    """
    View to allow the logged-in user to delete their own account.
    Triggers cleanup via post_delete signal.
    """
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect("home")  # Adjust to your actual homepage or login redirect
    return HttpResponseNotAllowed(["POST"])
