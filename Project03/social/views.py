from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from . import models

def messages_view(request):
    """Private Page Only an Authorized User Can View, renders messages page
       Displays all posts and friends, also allows user to make new posts and like posts
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        # user_post = models.Post.objects.filter(owner=user_info)
        try:
            request.session['counter2']
        except:
            request.session['counter2'] = 1
        posts = []
        for i in models.Post.objects.all().order_by("timestamp").reverse():
                posts.append(i)
                if len(posts) >= request.session['counter2']:
                  break



        # TODO Objective 9: query for posts (HINT only return posts needed to be displayed)

        # TODO Objective 10: check if user has like post, attach as a new attribute to each post
        #user_info = models.UserInfo.objects.get(user=request.user)
        #lk = models.Post.objects.add(to_user_id=int(username), from_user_id=request.user.id)
        #lk.save()

        context = { 'user_info' : user_info
                  , 'posts' : posts }
        return render(request,'messages.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def account_view(request):
    """Private Page Only an Authorized User Can View, allows user to update
       their account information (i.e UserInfo fields), including changing
       their password
    Parameters
    ---------
      request: (HttpRequest) should be either a GET or POST
    Returns
    --------
      out: (HttpResponse)
                 GET - if user is authenticated, will render account.djhtml
                 POST - handle form submissions for changing password, or User Info
                        (if handled in this view)
    """

    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            change_employment = request.POST['change_employment']
            change_location = request.POST['change_location']
            change_birthday = request.POST['change_birthday']
            change_interest = request.POST['change_interest']
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('login:login_view')
            if change_employment != "":
                user_info.employment = change_employment
                user_info.save()
            if change_location != "":
                user_info.location = change_location
                user_info.save()
            if change_birthday != "":
                user_info.birthday = change_birthday
                user_info.save()
            if change_interest != "":
                interests = models.Interest.objects.all()
                new = []
                for interest in interests:
                    if interest.label == change_interest:
                        new.append(interest)
                        # other= models.Interest(label=change_interest)
                        # other.save()
                if len(new) == 0:
                    new_interest = models.Interest(label=change_interest)
                    new_interest.save()
                    user_info.interests.add(new_interest)
                    user_info.save()
        form = PasswordChangeForm(request.user)

        # TODO Objective 3: Create Forms and Handle POST to Update UserInfo / Password
        context = {'user': request.user,
                    'change_form': form}
        return render(request,'account.djhtml',context)




def people_view(request):
    """Private Page Only an Authorized User Can View, renders people page
       Displays all users who are not friends of the current user and friend requests
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render people.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        try:
            request.session['counter']
        except:
            request.session['counter'] = 1
        # TODO Objective 4: create a list of all users who aren't friends to the current user (and limit size)
        all_people = []
        for nonuser in models.UserInfo.objects.all():
            if nonuser != user_info and nonuser not in user_info.friends.all():
                all_people.append(nonuser)
            if len(all_people) >= request.session['counter']:
                break
        # TODO Objective 5: create a list of all friend requests to current user
        friend_requests = models.FriendRequest.objects.filter(to_user_id=request.user.id)

        context = { 'user_info' : user_info,
                    'all_people' : all_people,
                    'friend_requests' : friend_requests }

        return render(request,'people.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def like_view(request):
    '''Handles POST Request recieved from clicking Like button in messages.djhtml,
       sent by messages.js, by updating the corrresponding entry in the Post Model
       by adding user to its likes field
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postID,
                                a string of format post-n where n is an id in the
                                Post model

	Returns
	-------
   	  out : (HttpResponse) - queries the Post model for the corresponding postID, and
                             adds the current user to the likes attribute, then returns
                             an empty HttpResponse, 404 if any error occurs
    '''
    postIDReq = request.POST.get('postID')
    if postIDReq is not None:
        # remove 'post-' from postID and convert to int
        # TODO Objective 10: parse post id from postIDReq
        postID = 0

        if request.user.is_authenticated:
            # TODO Objective 10: update Post model entry to add user to likes field

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('like_view called without postID in POST')

def post_submit_view(request):
    '''Handles POST Request recieved from submitting a post in messages.djhtml by adding an entry
       to the Post Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postContent, a string of content

	Returns
	-------
   	  out : (HttpResponse) - after adding a new entry to the POST model, returns an empty HttpResponse,
                             or 404 if any error occurs
    '''
    postContent = request.POST.get('postContent')
    print(postContent)
    user_info = models.UserInfo.objects.get(user=request.user)
    if postContent is not None:
        if request.user.is_authenticated:
            entry = models.Post.objects.create(owner=user_info, content=postContent)
            # TODO Objective 8: Add a new entry to the Post model
            # user_id=int(request.user.id)
            # status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('post_submit_view called without postContent in POST')

def more_post_view(request):
    '''Handles POST Request requesting to increase the amount of Post's displayed in messages.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating hte num_posts sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of posts dispalyed
        num = request.session.get('counter2', 0)
        request.session['counter2'] = num + 1
        return HttpResponse('Current Count2: %s' % (num + 1))
        # TODO Objective 9: update how many posts are displayed/returned by messages_view

        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def more_ppl_view(request):
    '''Handles POST Request requesting to increase the amount of People displayed in people.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating the num ppl sessions variable
    '''
    #user_info = models.UserInfo.objects.get(user=request.user)
    if request.user.is_authenticated:
        num = request.session.get('counter', 0)
        request.session['counter'] = num + 1
        return HttpResponse('Current Count: %s' % (num + 1))

        # TODO Objective 4: increment session variable for keeping track of num ppl displayed

        # return status='success'

    return redirect('login:login_view')

def friend_request_view(request):
    '''Handles POST Request recieved from clicking Friend Request button in people.djhtml,
       sent by people.js, by adding an entry to the FriendRequest Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute frID,
                                a string of format fr-name where name is a valid username

	Returns
	-------
   	  out : (HttpResponse) - adds an etnry to the FriendRequest Model, then returns
                             an empty HttpResponse, 404 if POST data doesn't contain frID
    '''
    user_info=models.UserInfo.objects.get(user=request.user)
    frID = request.POST.get('frID')
    if frID is not None:
        # remove 'fr-' from frID
        username = frID[3:]

        if request.user.is_authenticated:
            # TODO Objective 5: add new entry to FriendRequest
            fr = models.FriendRequest.objects.create(to_user_id=int(username), from_user_id=request.user.id)
            fr.save()
            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('friend_request_view called without frID in POST')

def accept_decline_view(request):
    '''Handles POST Request recieved from accepting or declining a friend request in people.djhtml,
       sent by people.js, deletes corresponding FriendRequest entry and adds to users friends relation
       if accepted
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute decision,
                                a string of format A-name or D-name where name is
                                a valid username (the user who sent the request)

	Returns
	-------
   	  out : (HttpResponse) - deletes entry to FriendRequest table, appends friends in UserInfo Models,
                             then returns an empty HttpResponse, 404 if POST data doesn't contain decision
    '''
    data = request.POST.get('frID')
    print("data: ",data)
    user_info = models.UserInfo.objects.get(user=request.user)
    username=data[2:]
    friend_user_info = models.UserInfo.objects.get(user=models.User.objects.get(id=int(username)))
    if data is not None:
        print("ran")
        # TODO Objective 6: parse decision from data
        if data[:2] == 'A-':
           friend_user_info.friends.add(user_info.user.id)
           friend_user_info.save()
           user_info.friends.add(friend_user_info.user.id)
           user_info.save()
           fr = models.FriendRequest.objects.get(from_user_id=int(username), to_user_id=request.user.id)
           print(fr)
           fr.delete()
        else:
            fr = models.FriendRequest.objects.get(from_user_id=int(username), to_user_id=request.user.id)
            fr.delete()
        if request.user.is_authenticated:

            # TODO Objective 6: delete FriendRequest entry and update friends in both Users
            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')
    return HttpResponseNotFound('accept-decline-view called without decision in POST')
