from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Blogsocial index page")

def post(request, post_id):
    return HttpResponse("You're looking at post %s." % post_id)