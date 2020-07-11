// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function like()
{
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();
 
    $.ajax({
        url : action + "/",
        type : 'POST',
        data : { 'obj' : pk },
 
        success : function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });
 
    return false;
}
 
function dislike()
{
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();
 
    $.ajax({
        url : action + "/",
        type : 'POST',
        data : { 'obj' : pk },
 
        success : function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
        }
    });
 
    return false;
}

function maketop()
{

    var maketop = $(this);
    var type = maketop.data('type');
    var pk = maketop.data('id');
    var action = maketop.data('action');
 
    $.ajax({
        url : action + "/",
        type : 'POST',
        data : { 'obj' : pk },
 
        success : function (json) {
            maketop.find("[data-count='top']").text(json.top);
        }
    });
 
    return false;
}
 
// Подключение обработчиков
$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
    $('[data-action="top"]').click(maketop);
});