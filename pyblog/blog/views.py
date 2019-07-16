from django.shortcuts import render

from blog.models import Post
from blog import model_helpers


def post_list(request, category_name=model_helpers.post_category_all.slug()):
    category, posts = model_helpers.get_category_and_posts(category_name)

    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, 'blog/post_list.html', context)
