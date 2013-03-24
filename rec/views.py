from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rec.models import *
from rec.forms import *
import render
import uuid

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    data = json.dumps({'success': True})
                else:
                    data = json.dumps({'success': False, 'errors': {'general': 'Disabled account.'}})
            else:
                data = json.dumps({'success': False, 'errors': {'general': 'Incorrect login or password.'}})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def logout_view(request):
    logout(request)
    data = json.dumps({'success': True})
    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
            user.save()
            profile = Profile(user=user, name=request.POST['name'])
            profile.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            data = json.dumps({'success': True})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def mix_view(request, id=1):
    if request.method == 'GET':
        mix = get_object_or_404(Mix, pk=id)
        tracks = []
        for track in mix.tracks.all():
            track_data = {
                'id': track.pk,
                'author': track.author.username,
                'author_name': track.author.profile.name,
                'sound_id': track.sound.pk,
                'sound_author': track.sound.author.username,
                'sound_author_name': track.sound.author.profile.name,
                'file_path': track.sound.file.url,
                'tempo': track.sound.tempo,
                'title': track.sound.title,
                'offset': track.offset,
                'volume': track.volume,
            }
            tracks.append(track_data)
        if mix.author.profile.image:
            image_path = mix.author.profile.image['small'].url
        else:
            image_path = None
        data = json.dumps({
            'id': mix.pk,
            'author': mix.author.username,
            'author_name': mix.author.profile.name,
            'author_image_path': image_path,
            'tempo': mix.tempo,
            'title': mix.title,
            'remix_count': mix.remixes.count(),
            'play_count': mix.play_count,
            'favorite_count': mix.favorites.count(),
            'comment_count': mix.comments.count(),
            'tracks': tracks,
        })
        return HttpResponse(data, mimetype='application/json')

    elif request.method == 'POST':
        form = MixForm(request.POST)
        if form.is_valid():
            mix = Mix(author=request.user, parent=None, tempo=90, title=request.POST['title'], play_count=0)
            mix.save()
            data = json.dumps({'success': True, 'id': mix.pk})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def remix_view(request, id=1):
    if request.method == 'GET':
        parent = get_object_or_404(Mix, pk=id)
        remixes = []
        for remix in parent.remixes.all():
            if remix.author.profile.image:
                image_path = remix.author.profile.image['small'].url
            else:
                image_path = None
            remix_data = {
                'id': remix.pk,
                'author': remix.author.username,
                'author_name': remix.author.profile.name,
                'author_image_path': image_path,
                'tempo': remix.tempo,
                'title': remix.title,
                'play_count': remix.play_count,
                'favorite_count': remix.favorites.count(),
                'comment_count': remix.comments.count(),
                'remix_count': remix.remixes.count(),
            }
            remixes.append(remix_data)
        if parent.author.profile.image:
            image_path = parent.author.profile.image['small'].url
        else:
            image_path = None
        data = json.dumps({
            'id': parent.pk,
            'author': parent.author.username,
            'author_name': parent.author.profile.name,
            'author_image_path': image_path,
            'title': parent.title,
            'play_count': parent.play_count,
            'favorite_count': parent.favorites.count(),
            'comment_count': parent.comments.count(),
            'remix_count': parent.remixes.count(),
            'remixes': remixes
        })
        return HttpResponse(data, mimetype='application/json')

    elif request.method == 'POST':
        form = RemixForm(request.POST)
        if form.is_valid():
            parent = get_object_or_404(Mix, pk=request.POST['parent_id'])
            mix = Mix(author=request.user, parent=parent, tempo=parent.tempo, title=request.POST['title'], play_count=0)
            mix.save()
            for track in parent.tracks.all():
                new_track = Track(mix=mix, author=request.user, sound=track.sound, offset=track.offset, volume=track.volume)
                new_track.save()
                mix.tracks.add(new_track)
            data = json.dumps({'success': True, 'id': mix.pk})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def mix_social_view(request, id=1):
    if request.method == 'GET':
        mix = get_object_or_404(Mix, pk=id)
        mix.play_count += 1
        mix.save()
        data = json.dumps({
            'id': mix.pk,
            'author': mix.author.username,
            'author_name': mix.author.profile.name,
            'is_yours': mix.author.pk == request.user.pk,
            'title': mix.title,
            'play_count': mix.play_count,
            'favorite_count': mix.favorites.count(),
            'comment_count': mix.comments.count(),
            'remix_count': mix.remixes.count(),
            'favorite': request.user.favorite_mixes.all().filter(pk=mix.pk).exists(),
        })
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def track_view(request, id=1):
    if request.method == 'GET':
        track = get_object_or_404(Track, pk=id)
        data = json.dumps({
            'id': track.pk,
            'author': track.author.username,
            'author_name': track.author.profile.name,
            'sound_author': track.sound.author.username,
            'sound_author_name': track.sound.author.profile.name,
            'file_path': track.sound.file.name,
            'tempo': track.sound.tempo,
            'length': track.sound.length,
            'title': track.sound.title,
            'offset': track.offset,
            'volume': track.volume,
        })
        return HttpResponse(data, mimetype='application/json')

    elif request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            mix = get_object_or_404(Mix, pk=request.POST['mix_id'])
            sound = get_object_or_404(Mix, pk=request.POST['sound_id'])
            track = Track(mix=mix, author=request.user, sound=sound, offset=request.POST['offset'], volume=request.POST['volume'])
            track.save()
            data = json.dumps({'success': True, 'id': track.pk})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def upload_track_view(request):
    if request.method == 'POST':
        form = UploadTrackForm(request.POST, request.FILES)
        if form.is_valid():
            mix = get_object_or_404(Mix, pk=request.POST['mix_id'])
            sound = TrackSound(author=request.user, file=request.FILES['sound'], tempo=mix.tempo, title=request.POST['title'])
            sound.save()
            track = Track(mix=mix, author=request.user, sound=sound, offset=request.POST['offset'], volume=request.POST['volume'])
            track.save()
            data = json.dumps({'success': True, 'track_id': track.pk, 'sound_id': sound.pk})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def render_mix_view(request):
    if request.method == 'POST':
        

@csrf_exempt
@login_required
def mix_comment_view(request, id=1):
    if request.method == 'GET':
        mix = get_object_or_404(Mix, pk=id)
        comments = []
        for comment in mix.comments.all().order_by('-created_at'):
            if comment.author.profile.image:
                image_path = mix.author.profile.image['small'].url
            else:
                image_path = None
            comment_data = {
                'id': comment.pk,
                'author': comment.author.username,
                'author_name': comment.author.profile.name,
                'author_image_path': image_path,
                'content': comment.content,
            }
            comments.append(comment_data)
        if mix.author.profile.image:
            image_path = mix.author.profile.image['small'].url
        else:
            image_path = None
        data = json.dumps({
            'id': mix.pk,
            'author': mix.author.username,
            'author_name': mix.author.profile.name,
            'author_image_path': image_path,
            'title': mix.title,
            'play_count': mix.play_count,
            'favorite_count': mix.favorites.count(),
            'comment_count': mix.comments.count(),
            'remix_count': mix.remixes.count(),
            'favorite': request.user.favorite_mixes.all().filter(pk=mix.pk).exists(),
            'comments': comments,
        })
        return HttpResponse(data, mimetype='application/json')

    elif request.method == 'POST':
        form = MixCommentForm(request.POST)
        if form.is_valid():
            mix = get_object_or_404(Mix, pk=request.POST['mix_id'])
            comment = MixComment(mix=mix, author=request.user, content=request.POST['content'])
            comment.save()
            data = json.dumps({'success': True, 'id': comment.pk, 'author': comment.author.username, 'author_name': comment.author.profile.name, 'content': comment.content})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def favorite_mix_view(request, id=1):
    if request.method == 'GET':
        mixes = []
        for mix in request.user.favorite_mixes.all():
            if mix.author.profile.image:
                image_path = mix.author.profile.image['small'].url
            else:
                image_path = None
            mix_data = {
                'id': mix.pk,
                'author': mix.author.username,
                'author_name': mix.author.profile.name,
                'author_image_path': image_path,
                'tempo': mix.tempo,
                'title': mix.title,
                'play_count': mix.play_count,
                'favorite_count': mix.favorites.count(),
                'comment_count': mix.comments.count()
            }
            mixes.append(mix_data)
        data = json.dumps({'mixes': mixes})
        return HttpResponse(data, mimetype='application/json')

    if request.method == 'POST':
        form = FavoriteMixForm(request.POST)
        if form.is_valid():
            mix = get_object_or_404(Mix, pk=id)
            if request.POST['removing'] == 'true':
                request.user.favorite_mixes.remove(mix)
                favorite = False
            else:
                request.user.favorite_mixes.add(mix)
                favorite = True
            data = json.dumps({'success': True, 'favorite': favorite})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def user_view(request, username):
    if username == 'you':
        user = request.user
    else:
        user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        mixes = []
        for mix in user.mixes.order_by('-created_at'):
            if mix.file:
                file_path = mix.file.url
            else:
                file_path = None
            mix_data = {
                'id': mix.pk,
                'author': mix.author.username,
                'author_name': mix.author.profile.name,
                'file_path': file_path,
                'tempo': mix.tempo,
                'title': mix.title,
                'play_count': mix.play_count,
                'favorite_count': mix.favorites.count(),
                'comment_count': mix.comments.count(),
                'remix_count': mix.remixes.count()
            }
            mixes.append(mix_data)
        if user.profile.image:
            image_path = user.profile.image['small'].url
        else:
            image_path = None
        data = json.dumps({
            'username': user.username,
            'name': user.profile.name,
            'description': user.profile.description,
            'image_path': image_path,
            'is_you': user.pk == request.user.pk,
            'you_follow': user.followers.all().filter(pk=request.user.profile.pk).exists(),
            'follower_count': user.followers.count(),
            'mixes': mixes
        })
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def profile_image_view(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.image = request.FILES['image']
            profile.save()
            data = json.dumps({'success': True, 'image_path': profile.image['small'].url})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')


@csrf_exempt
@login_required
def follow_view(request, username='you'):
    if username == 'you':
        user = request.user
    else:
        user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        following = request.user.profile.following.all().values_list('pk', flat=True)
        set = Mix.objects.filter(author__in=list(following)).order_by('-created_at')
        mixes = []
        for mix in set:
            if mix.author.profile.image:
                image_path = mix.author.profile.image['small'].url
            else:
                image_path = None
            mix_data = {
                'id': mix.pk,
                'author': mix.author.username,
                'author_name': mix.author.profile.name,
                'author_image_path': image_path,
                'tempo': mix.tempo,
                'title': mix.title,
                'play_count': mix.play_count,
                'favorite_count': mix.favorites.count(),
                'comment_count': mix.comments.count()
            }
            mixes.append(mix_data)
        data = json.dumps({'mixes': mixes})
        return HttpResponse(data, mimetype='application/json')

    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            if request.POST['unfollowing'] == 'true':
                user.followers.remove(request.user.profile)
                you_follow = False
            else:
                user.followers.add(request.user.profile)
                you_follow = True
            data = json.dumps({
                'success': True,
                'you_follow': you_follow,
                'follower_count': user.followers.count(),
            })
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data, mimetype='application/json')

@csrf_exempt
@login_required
def global_view(request):
    if request.method == 'GET':
        mixes = []
        for mix in Mix.objects.all().order_by('-created_at'):
            if mix.author.profile.image:
                image_path = mix.author.profile.image['small'].url
            else:
                image_path = None
            mix_data = {
                'id': mix.pk,
                'author': mix.author.username,
                'author_name': mix.author.profile.name,
                'author_image_path': image_path,
                'tempo': mix.tempo,
                'title': mix.title,
                'play_count': mix.play_count,
                'favorite_count': mix.favorites.count(),
                'comment_count': mix.comments.count()
            }
            mixes.append(mix_data)
        data = json.dumps({'mixes': mixes})
        return HttpResponse(data, mimetype='application/json')