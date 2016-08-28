from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.
@requires_csrf_token
def add_to_cart(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        # post = Post(text=post_text, author=request.user)
        # post.save()

        response_data['result'] = 'Add to cart successful!'
        # response_data['postpk'] = post.pk
        # response_data['text'] = post.text
        # response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        # response_data['author'] = post.author.username

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})

def show_cart(request, template_name='cart/cart.html'):
    cart_item_count = cart.cart_item_count(request)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
