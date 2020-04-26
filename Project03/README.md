# CS 1XA3 Project03 - <tanx25>
## Usage
Install conda enivornment with
"pip install django"
"conda activate django"
...
Run locally with
python manage.py runserver localhost:8000
Run on mac1xa3.ca with
python manage.py runserver localhost:10102
...
Log in with FrankTan, password 
## Objective 01
Description:
- this feature is displayed in signup.djhtml which is rendered by
signup_view by an appropriate form
- it makes a POST Request to /e/tanx25/signup.djhtml via signup_view
Exceptions:
- If the /e/tanx25/something_post is called without arguments is redirects
to login.djhtml
-registration with incorrect password will not jump into the login page.
## Objective 02
Description:
-this feature is displayed in social_base.djhtml,
I add a 'for loop' for the user interest to show all the interests of currently login user
## Objective 03
Description:
-this feature is displayed in account.djhtml which is rendered by
account_view
-this feature asks me to edit the views.py/account_view and /account.djhtml 
to allow uesr to change password and update info.
- I create a form in account_view, it makes a post request to /e/tanx25 
## Objective 04
Description:
this feature is displayed in people.djhtml which is rendered by
people_view
-I create to list in views.py/people.view and 'for loop' in people.djhtml to replicate the current div
## Objective 05
Description:
-this feature is displayed in people.djhtml which is rendered by
friend_request_view
-it adds an new entry to friend request 
## Objective 06
Description:
-this feature is displayed in people.djhtml which is rendered by
accept_decline_view
-the people.js sends a post to accept_decline_view and once the post is handled,the request will be deleted
## Objective 07
Description:
-this feature is displayed in messages.djhtml
-I edit the messages.djhtml to display all of the friends of the current user
## Objective 08
Description:
-this feature is displayed in messages.js which is rendered by post_submit_view
-it submits a AJAX post and sending the contents of post-text to post_submit_view
## Objective 09
Description:
-this feature is displayed in messages.djhtml which is rendered by messages_view and more_post_view
-the messages_view shows the posts by newest and to oldest
-more_post_view shows more post when clicking the more button
## Objective 010
Description:
-this feature is displayed in messages.djhtml which is rendered by messages_view and messages.js
-it submits AJAX post with those id handled by messages_view
-when the post is liked , the liked button will be removed.
## Objective 011
Description:
-this feature is displayed in db.sqlite3
-I create a variety of test users, create many posts and likes and different friend requests



