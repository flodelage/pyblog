from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect

from blog.models import Post, Comment
from blog import model_helpers
from blog import navigation
from blog.forms import CreateCommentForm



def post_list(request, category_name=model_helpers.post_category_all.slug()):
    category, posts = model_helpers.get_category_and_posts(category_name)
    categories = model_helpers.get_categories()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'category': category,
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, post_id, message=''):
    post = get_object_or_404(Post, pk=post_id)
    posts_same_category = Post.objects.filter(published=True, category=post.category)\
        .exclude(pk=post_id)
    comments = post.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')

    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse('post-detail-message', args=[post.pk, "You're comment has been posted!"]) + '#comments' )
    else:
        comment_form = CreateCommentForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'post': post,
        'posts_same_category': posts_same_category,
        'comments': comments,
        'comment_form': comment_form,
        'message': message,
    }

    return render(request, 'blog/post_detail.html', context)
