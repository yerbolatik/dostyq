from django.http import JsonResponse
import shortuuid

from django.shortcuts import render
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt

from core.models import Post


def index(request):
    posts = Post.objects.filter(
        active=True, visibility="Everyone").order_by("-id")
    context = {
        "posts": posts
    }
    return render(request, 'core/index.html', context)


@csrf_exempt
def create_post(request):

    if request.method == "POST":
        title = request.POST.get("post-caption")
        visibility = request.POST.get("visibility")
        image = request.FILES.get("post-thumbnail")

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(
                title=title,
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            post.save()

            return JsonResponse({"post": {
                "title": post.title,
                "image": post.image.url,
                "full_name": post.user.profile.full_name,
                "profile_image": post.user.profile.image.url,
                "date": timesince(post.date),
                "id": post.id,
            }})

        else:
            return JsonResponse({"error": "Image or title does not exists"})

    return JsonResponse({"data": "sent"})

# def like_post(request):
