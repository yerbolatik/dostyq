from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from core.models import Post, FriendRequest
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from userauths.models import Profile, User


def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already registered!")
        return redirect("core:feed")

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name")
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        user = authenticate(email=email, password=password)
        login(request, user)

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        messages.success(
            request, f"Hi! {full_name}! Your account was created successfully.")
        return redirect("core:feed")

    context = {
        "form": form
    }
    return render(request, "userauths/sign-up.html", context)


def LoginView(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged In!")
                return redirect("core:feed")
            else:
                messages.error(request, "Username or password does not match")
                return redirect("userauths:sign-up")
        except:
            messages.error(request, "Username does not exist")
            return redirect("userauths:sign-up")

    return HttpResponseRedirect("/")


def LogoutView(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect("userauths:sign-up")


@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user).order_by("-id")

    context = {
        "profile": profile,
        "posts": posts,
    }
    return render(request, "userauths/my-profile.html", context)


@login_required
def profile_update(request):
    print("Handling profile update request...")

    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            messages.success(request, "Profile Updated Successfully.")
            return redirect('userauths:profile-update')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)

        print("POST request received.")

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'userauths/profile-update.html', context)


@login_required
def delete_user(request):
    if request.method == 'POST':
        confirm_delete = request.POST.get('confirm_delete')
        if confirm_delete == 'True':
            # Удалить профиль пользователя
            user = request.user
            user.delete()
            messages.success(request, 'Your profile has been deleted.')
            # Измените URL на тот, который вы хотите использовать после удаления профиля
            return redirect('userauths:sign-up')
        else:
            # Вернуться на страницу обновления профиля, если пользователь нажал "Нет"
            return redirect('userauths:profile-update')
    else:
        # Если запрос не POST, перенаправить на страницу обновления профиля
        return render(request, 'userauths/delete-user.html')


@login_required
def friend_profile(request, username):
    profile = Profile.objects.get(user__username=username)
    if request.user.profile == profile:
        return redirect("userauths:my-profile")

    posts = Post.objects.filter(active=True, user=profile.user).order_by("-id")

    bool = False
    bool_friend = False

    sender = request.user
    receiver = profile.user

    try:
        friend_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver)
        if friend_request:
            bool = True
        else:
            bool = False
    except:
        bool = False

    context = {
        "profile": profile,
        "posts": posts,
        "bool": bool,
        "bool_friend": bool_friend,
    }
    return render(request, "userauths/friend-profile.html", context)
