# coding: utf-8

import json

from flow import FlowElement, Flow

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.http import HttpResponse

from example.models import Post, Like


class PostElement(FlowElement):
    element_class = Post
    template_name = 'example/flow_post_item.html'

    sorting_key = 'created_at'

    def get_objects(self):
        return Post.objects.all()


class LikeElement(FlowElement):
    element_class = Like
    template_name = 'example/flow_like_item.html'

    sorting_key = 'created_at'

    def get_objects(self):
        return Like.objects.select_related('user').all()


def index(request):
    flow = Flow(reverse=True)

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
