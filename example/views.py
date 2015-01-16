# coding: utf-8

import json

from flow import BaseElement, Flow

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse

from example.models import Post, Like


class PostElement(BaseElement):
    element_class = Post
    template_name = 'example/flow_post_item.html'

    def objects(self):
        return Post.objects.all()


class LikeElement(BaseElement):
    element_class = Like
    template_name = 'example/flow_like_item.html'

    def objects(self):
        return Like.objects.all()


def index(request):
    flow = Flow()
    return render_to_response('example/index.html', {'flow': flow})


@login_required
def like(request, content_type_id, object_id):
    try:
        # It's allowed to like an object more than once for testing purposes.
        like_object = Like.objects.create(
            user=request.user,
            content_type_id=content_type_id,
            object_id=object_id
        )
        like_object.save()

        response = {
            'OK': 'Object was successfully liked'
        }

    except ValueError:
        response = {
            'Error': 'Wrong data'
        }

    return HttpResponse(json.dumps(response), content_type='application/json')
