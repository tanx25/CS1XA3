/* ********************************************************************************************
   | Handle Submitting Posts - called by $('#post-button').click(submitPost)
   ********************************************************************************************
   */
function submitPost(event) {
//    alert('Post Button Pressed');
//     TODO Objective 8: send contents of post-text via AJAX Post to post_submit_view (reload page upon success)
    let postContent = $("#post-text").html();
//    alert('post:'+postContent);
    let postID = event.target.id;
    let json_data = { 'postContent' : postContent };
    let url_path = post_submit_url;
//    alert("ran");
     $.post(url_path,
           json_data,
           postResponse);
}
function postResponse(data,status) {
    if (status == 'success') {
        // reload page to display new Post
        location.reload();
    }
    else {
        alert('failed to submit posts' + status);
    }
}

/* ********************************************************************************************
   | Handle Liking Posts - called by $('.like-button').click(submitLike)
   ********************************************************************************************
   */
function submitLike(event) {
    alert('Like Button Pressed');
    // TODO Objective 10: send post-n id via AJAX POST to like_view (reload page upon success)

    let frID = event.target.id;
    let json_data = { 'frID' : frID };
    let url_path = like_post_url;

    // AJAX post
    $.post(url_path,
           json_data,
           frResponse);
}
/* ********************************************************************************************
   | Handle Requesting More Posts - called by $('#more-button').click(submitMore)
   ********************************************************************************************
   */
function moreResponse(data,status) {
    if (status == 'success') {
        // reload page to display new Post
        location.reload();
    }
    else {
        alert('failed to request more posts' + status);
    }
}

function submitMore(event) {
    // submit empty data
    let json_data = { };
    // globally defined in messages.djhtml using i{% url 'social:more_post_view' %}
    let url_path = more_post_url;

    // AJAX post
    $.post(url_path,
           json_data,
           moreResponse);
}

/* ********************************************************************************************
   | Document Ready (Only Execute After Document Has Been Loaded)
   ********************************************************************************************
   */
$(document).ready(function() {
    // handle post submission
    $('#post-button').click(submitPost);
    // handle likes
    $('.like-button').click(submitLike);
    // handle more posts
    $('#more-button').click(submitMore);
});
