def profile_id(request):
    if request.user.is_authenticated:
        username = request.user.username
        if "_" in username:
            return {"profile_id": username.split("_")[-1]}
    return {}
