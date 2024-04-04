$(document).ready(function() {
    $('#post-form').submit(function(e) {
      e.preventDefault();
  
      let post_caption = $("#post-caption").val();
      let post_visibility = $("#visibility").val();
  
      let fileInput = $('#post-thumbnail')[0];
      let file = fileInput.files[0];
      let fileName = file.name; // Extract the filename

      console.log(post_caption);
      console.log(post_visibility);
      console.log(fileName);
      console.log(file);
  
      let formData = new FormData();
      formData.append('post-caption', post_caption);
      formData.append('visibility', post_visibility);
      formData.append('post-thumbnail', file, fileName);
  
      $.ajax({
        url: '/create-post/',
        type: 'POST',
        dataType: 'json',
        data: formData,
        processData: false,
        contentType: false,


        success: function(res) {
            console.log(res);

                let _html = '<div class="card lg:mx-0 uk-animation-slide-bottom-small mt-3 mb-3">\
                        <div class="flex justify-between items-center lg:p-4 p-2.5">\
                            <div class="flex flex-1 items-center space-x-4">\
                                <a href="#">\
                                    <img src="' + res.post.profile_image + '" class="bg-gray-200 border border-white rounded-full w-10 h-10" />\
                                </a>\
                                <div class="flex-1 font-semibold capitalize">\
                                    <a href="#" class="text-black dark:text-gray-100"> ' + res.post.full_name + ' </a>\
                                    <div class="text-gray-700 flex items-center space-x-2"><span><small>' + res.post.date + ' ago </span><ion-icon name="time-outline"></ion-icon></small>\
                                </div>\
                            </div>\
                        </div>\
                        <div>\
                            <a href="#"> <i class="icon-feather-more-horizontal text-2xl hover:bg-gray-200 rounded-full p-2 transition -mr-1 dark:hover:bg-gray-700"></i> </a>\
                            <div\
                                class="bg-white w-56 shadow-md mx-auto p-2 mt-12 rounded-md text-gray-500 hidden text-base border border-gray-100 dark:bg-gray-900 dark:text-gray-100 dark:border-gray-700"\
                                uk-drop="mode: click;pos: bottom-right;animation: uk-animation-slide-bottom-small"\
                            >\
                                <ul class="space-y-1">\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-share-alt mr-1"></i> Share </a>\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-edit-alt mr-1"></i> Edit Post </a>\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-comment-slash mr-1"></i> Disable comments </a>\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-favorite mr-1"></i> Add favorites </a>\
                                    </li>\
                                    <li>\
                                        <hr class="-mx-2 my-2 dark:border-gray-800" />\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 text-red-500 hover:bg-red-100 hover:text-red-500 rounded-md dark:hover:bg-red-600"> <i class="uil-trash-alt mr-1"></i> Delete </a>\
                                    </li>\
                                </ul>\
                            </div>\
                        </div>\
                    </div>\
                    <div class="p-5 pt-0 border-b dark:border-gray-700">\
                    ' + res.post.title + '\
                    </div>\
                    <div uk-lightbox>\
                        <a href="' + res.post.image + '">\
                            <img src="' + res.post.image + '" alt="" class="max-h-96 w-full object-cover" />\
                        </a>\
                    </div>\
                    <div class="p-4 space-y-3">\
                        <div class="flex space-x-4 lg:font-bold">\
                            <a style="cursor: pointer;" class="flex items-center space-x-2">\
                                <div class="p-2 rounded-full like-btn' + res.post.id + ' {% if request.user in post.likes.all %} text-gray-500 {% else %} text-black {% endif %}" id="like-btn" data-like-btn="' + res.post.id + '">\
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                                        <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />\
                                    </svg>\
                                </div>\
                                <div> Like</div>\
                            </a>\
                            <a href="#" class="flex items-center space-x-2">\
                                <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                                        <path fill-rule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clip-rule="evenodd" />\
                                    </svg>\
                                </div>\
                                <div> <span id="comment-count' + res.post.id + '">0</span> Comment</div>\
                            </a>\
                            <a href="#" class="flex items-center space-x-2 flex-1 justify-end">\
                                <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />\
                                    </svg>\
                                </div>\
                                <div> Share</div>\
                            </a>\
                        </div>\
                        <div class="flex items-center space-x-3 pt-2">\
                                <div class="dark:text-gray-100">\
                                    <strong><span id="like-count' + res.post.id + '">0</span></strong> Like\
                                </div>\
                        </div>\
                        <div class="border-t py-4 space-y-4 dark:border-gray-600" id="comment-div' + res.post.id + '"></div>\
                        <div class="bg-gray-100 rounded-full relative dark:bg-gray-800 border-t">\
                            <input placeholder="Add your Comment.." id="comment-input' + res.post.id + '" data-comment-input="' + res.post.id + '" class="bg-transparent max-h-10 shadow-none px-5 comment-input' + res.post.id + '">\
                            <div class="-m-0.5 absolute bottom-0 flex items-center right-3 text-xl">\
                                <a style="cursor: pointer;" id="comment-btn" class="comment-btn' + res.post.id + '" data-comment-btn="' + res.post.id + '">\
                                    <ion-icon name="send-outline" class="hover:bg-gray-200 p-1.5 rounded-full"></ion-icon>\
                                </a>\
                            </div>\
                        </div>\
                    </div>\
                </div>\
                '

                $("#create-post-modal").removeClass("uk-flex uk-open")
                $(".post-div").prepend(_html)
            }
        })
    })


    //Like post
    $(document).ready(function(){
        $(document).on("click", "#like-btn", function(){
            let btn_val = $(this).attr("data-like-btn")
            console.log(btn_val);

            $.ajax({
                url:"/like-post/",
                dataType: "json",
                data:{
                    "id": btn_val
                },
                success: function(response){
                    if(response.data.bool === true){
                        $("#like-count"+btn_val).text(response.data.likes)
                        $(".like-btn"+btn_val).addClass("text-blue-500")
                        $(".like-btn"+btn_val).removeClass("text-black")
                    } else {
                        $("#like-count"+btn_val).text(response.data.likes)
                        $(".like-btn"+btn_val).addClass("text-black")
                        $(".like-btn"+btn_val).removeClass("text-blue-500")
                    }
                }
            })
        })
    })


    // Comment on Post
    $(document).on("click", "#comment-btn", function(){
        let id = $(this).attr("data-comment-btn")
        let comment = $("#comment-input"+id).val()
        console.log(id);
        console.log(comment);

        $.ajax({
            url:"/comment-post/",
            dataType:"json",
            data:{
                "id": id,
                "comment": comment,
            },
            success: function(response){
                console.log(response);
                let newCommentId = response.data.comment_id;
                let newComment = '<div class="flex card shadow p-2">\
                    <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                        <img src="'+ response.data.profile_image +'" alt="" class="absolute h-full rounded-full w-full">\
                    </div>\
                    <div>\
                        <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12  dark:bg-gray-800 dark:text-gray-100 flex items-center">\
                            <p class="leading-6 flex-grow">'+ response.data.comment +'</p>\
                            <button class="ml-auto text-xs" id="delete-comment" data-delete-comment="'+ response.data.comment_id +'">\
                                <i class="fas fa-trash text-red-500"></i>\
                            </button>\
                            <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                        </div>\
                        <div class="text-sm flex items-center space-x-3 mt-2 ml-5">\
                                <a id="like-comment-btn" data-like-comment="'+ response.data.comment_id +'" class="like-comment'+ response.data.comment_id +'" style="color:black; cursor: pointer;"><i class="fa-regular fa-heart"></i></a> <small><span id="comment-likes-count'+ response.data.comment_id +'">0</span></small>\
                                    <details >\
                                    <summary>\
                                    <div class="">Reply</div>\
                                    </summary>\
                                    <details-menu role="menu" class="origin-topf-right relative right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">\
                                    <div class="pyf-1" role="none">\
                                        <div method="POST" class="p-1 d-flex">\
                                            <input type="text"  class="with-border" name="" placeholder="Write Reply" id="reply-input'+ response.data.comment_id +'">\
                                            <button id="reply-comment-btn" data-reply-comment="'+ response.data.comment_id +'" type="submit" class="block w-fulfl text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 reply-comment-btn'+ response.data.comment_id +'" role="menuitem">\
                                                <ion-icon name="send"></ion-icon>\
                                            </button>\
                                        </div>\
                                    </div>\
                                    </details-menu>\
                                </details>\
                            <span><small> '+ response.data.date +' ago</small></span>\
                        </div>\
                        <div class="reply-div'+ response.data.comment_id +'"></div>\
                    </div>\
                </div>\
                '
                $("#comment-div"+id).prepend(newComment)
                $("#comment-input"+id).val("")
                $("#comment-count"+id).text(response.data.comment_count)

                $("#comment-"+newCommentId).find("#delete-comment").on("click", function(){
                deleteComment(newCommentId);
            });
            }
        })
    })

    
    // Like Comment
    $(document).on("click", "#like-comment-btn", function(){
        let id = $(this).attr("data-like-comment")
            console.log("Comment ID:",id);


        let iconElement = $(this).find("i");

        $.ajax({
            url:"/like-comment/",
            dataType:"json",
            data:{
                "id": id,
            },
            success: function(response){
                console.log(response);

                if(response.data.bool === true){
                    $("#comment-likes-count"+id).html(response.data.likes);
                    iconElement.removeClass("far").addClass("fas").css("color", "red"); // Изменяем классы иконки на fas
                } else {
                    $("#comment-likes-count"+id).text(response.data.likes);
                    iconElement.removeClass("fas").addClass("far").css("color", "black"); // Изменяем классы иконки на far
                }

            }

        })
    })

    // Reply Comment
    $(document).on("click", "#reply-comment-btn", function(){

        let id = $(this).attr("data-reply-comment")
        let reply = $("#reply-input"+id).val()
        console.log("Reply ID:",id);
        console.log("Reply:",reply);

        $.ajax({
            url: "/reply-comment/",
            dataType:"json",
            data:{
                "id":id,
                "reply":reply
            },
            success: function(response){
                let newReplyId = response.data.comment_id;
                let newReply = '<div class="flex mr-12 mb-2 mt-2" style="margin-right: 20px;">\
                <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                    <img src="'+ response.data.profile_image +'" style="width: 40px; height: 40px;" alt="" class="absolute h-full rounded-full w-full">\
                </div>\
                <div>\
                    <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100 flex items-center">\
                        <p class="leading-6 flex-grow">'+ response.data.reply +'</p>\
                        <button class="ml-12 text-xs" id="delete-reply" data-delete-reply="'+ response.data.reply_id +'">\
                                <i class="fas fa-trash text-red-500"></i>\
                            </button>\
                    </div>\
                </div>\
            </div>\
            '
            $(".reply-div"+id).prepend(newReply)
            $("#reply-input"+id).val("")

            $("#reply-"+newReplyId).find("#delete-reply").on("click", function(){
                deleteReply(newReplyId);
            });
            }
        })

    })


    // Delete Comment
    $(document).on("click", "#delete-comment", function(){

        let id = $(this).attr("data-delete-comment")
        console.log("Delete Comment ID:",id);

        $.ajax({
            url: "/delete-comment/",
            dataType:"json",
            data:{
                "id":id,
            },
            success: function(response){
                console.log("Comment ",id, "deleted");
            $("#comment-div"+id).addClass("d-none")
            }

        })
    })
    
    
    // Delete Reply
    $(document).on("click", "#delete-reply", function(){

        let id = $(this).attr("data-delete-reply")
        console.log("Delete Reply ID:",id);

        $.ajax({
            url: "/delete-reply/",
            dataType:"json",
            data:{
                "id":id,
            },
            success: function(response){
                console.log("Reply ",id, "deleted");
            $("#reply-div"+id).addClass("d-none")
            }

        })
    })


    // Add Friend
    $(document).on("click", "#add-friend", function(){

        let id = $(this).attr("data-friend-id")
        console.log("Added ID:" + id + " as a Friend");

        $.ajax({
            url: "/add-friend/",
            dataType: "json",
            data: {
                "id":id,
            },
            success: function(response){
                console.log(response);
                if(response.bool === true){
                    $("#friend-text").html('<i class="fas fa-user-minus"></i> Cancel Request')
                    $(".add-friend"+id).addClass("bg-red-600")
                    $(".add-friend"+id).removeClass("bg-blue-600")
                }
                
                if(response.bool === false){
                    $("#friend-text").html('<i class="fas fa-user-plus"></i> Add Friend')
                    $(".add-friend"+id).addClass("bg-blue-600")
                    $(".add-friend"+id).removeClass("bg-red-600")
                }
            }
        })

    })


    // Unfriend
    $(document).on("click", "#unfriend", function(){

        let id = $(this).attr("data-unfriend")
        console.log("Removed ID:" + id + " as a Friend");

        $.ajax({
            url: "/unfriend/",
            dataType: "json",
            data: {
                "id":id,
            },
            success: function(response){
                console.log(response);
                if(response.bool === true){
                    $("#unfriend-text").html('<i class="fas fa-check-circle"></i> Friend Removed')
                    $(".unfriend"+id).addClass("bg-green-600")
                    $(".unfriend"+id).removeClass("bg-red-600")
                }
            }
        })

    })


    // Accept Friend Request
    $(document).on("click", "#accept-friend-request", function(){
        let id = $(this).attr("data-request-id")
        console.log("New Friend ID:", id);

        $.ajax({
            url:"/accept-friend-request/",
            dataType: "json",
            data: {
                "id":id
            },
            
            success: function(response){
                console.log(response);
                $(".reject-friend-request-hide"+id).hide()
                $(".accept-friend-request"+id).html('<i class="fas fa-check-circle"></i> Accepted')
            }
        })
    })
    
    
    // Reject Friend Request
    $(document).on("click", "#reject-friend-request", function(){
        let id = $(this).attr("data-request-id")
        console.log("Reject Friend ID:", id);

        $.ajax({
            url:"/reject-friend-request/",
            dataType: "json",
            data: {
                "id":id
            },
            
            success: function(response){
                console.log(response);
                $(".accept-friend-request-hide"+id).hide()
                $(".reject-friend-request"+id).html('<i class="fas fa-check-circle"></i> Rejected')
            }
        })
    })


    // Block User
    $(document).on("click", "#block-user-btn", function(){
        let id = $(this).attr("data-block-user")
        console.log("Blocked User ID:", id);

        $.ajax({
            url:"/block-user/",
            dataType: "json",
            beforeSend: function(){
                $("#block-user-btn").html("<i class='fas fa-spinner fa-spin'></i>")
            },
            data: {
                "id": id
            },

            success: function(response){
                console.log(response);
                $(".block-text"+id).html("<i class='fas fa-check-circle'></i> User Blocked Successfully.")

            }
        })
    })


    // Is_read
    $(document).on("click", "#notification-link", function(){
        let id = $(this).attr("data-notification-id")
        console.log("Notification ID:", id);

        $.ajax({
            url:"/update-notification/",
            dataType: "json",
            data: {
                "id": id
            },
            success: function(response){
                console.log(response);
            }
        })      
    })

    // Is read all
    $("#mark-as-read-all").click(function () {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/mark-as-read-all/", // Замените на ваш URL-адрес для обработки запроса
            type: "POST",
            dataType: "json",
            headers: { "X-CSRFToken": csrftoken },
            success: function (response) {
                console.log(response); // Обработайте ответ, если необходимо
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // Обработайте ошибку, если необходимо
            }
        });
    });

    
    // Group Post
    $('#group-post-form').submit(function(e) {
        e.preventDefault();
    
        let post_caption = $("#group-post-caption").val();
        let post_visibility = $("#group-post-visibility").val();
        let group_id = $("#group_id").val()
    
        let fileInput = $('#group-post-thumbnail')[0];
        let file = fileInput.files[0];
        let fileName = file.name; // Extract the filename

        console.log(post_caption);
        console.log(post_visibility);
        console.log(fileName);
        console.log(file);
        console.log(group_id);
    
        let formData = new FormData();
        formData.append('group-post-caption', post_caption);
        formData.append('group-post-visibility', post_visibility);
        formData.append('group-post-thumbnail', file, fileName);
        formData.append('group_id', group_id);
    
        $.ajax({
        url: '/create-group-post/',
        type: 'POST',
        dataType: 'json',
        data: formData,
        processData: false,
        contentType: false,


        success: function(res) {
            console.log(res);

                let _html = '<div class="card lg:mx-0 uk-animation-slide-bottom-small mt-3 mb-3">\
                        <div class="flex justify-between items-center lg:p-4 p-2.5">\
                            <div class="flex flex-1 items-center space-x-4">\
                                <a href="#">\
                                    <img src="' + res.post.profile_image + '" class="bg-gray-200 border border-white rounded-full w-10 h-10" />\
                                </a>\
                                <div class="flex-1 font-semibold capitalize">\
                                    <a href="#" class="text-black dark:text-gray-100"> ' + res.post.full_name + ' </a>\
                                    <div class="text-gray-700 flex items-center space-x-2"><span><small>' + res.post.date + ' ago </span><ion-icon name="time-outline"></ion-icon></small>\
                                </div>\
                            </div>\
                        </div>\
                        <div>\
                            <a href="#"> <i class="icon-feather-more-horizontal text-2xl hover:bg-gray-200 rounded-full p-2 transition -mr-1 dark:hover:bg-gray-700"></i> </a>\
                            <div\
                                class="bg-white w-56 shadow-md mx-auto p-2 mt-12 rounded-md text-gray-500 hidden text-base border border-gray-100 dark:bg-gray-900 dark:text-gray-100 dark:border-gray-700"\
                                uk-drop="mode: click;pos: bottom-right;animation: uk-animation-slide-bottom-small"\
                            >\
                                <ul class="space-y-1">\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-share-alt mr-1"></i> Share </a>\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-edit-alt mr-1"></i> Edit Post </a>\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-comment-slash mr-1"></i> Disable comments </a>\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800"> <i class="uil-favorite mr-1"></i> Add favorites </a>\
                                    </li>\
                                    <li>\
                                        <hr class="-mx-2 my-2 dark:border-gray-800" />\
                                    </li>\
                                    <li>\
                                        <a href="#" class="flex items-center px-3 py-2 text-red-500 hover:bg-red-100 hover:text-red-500 rounded-md dark:hover:bg-red-600"> <i class="uil-trash-alt mr-1"></i> Delete </a>\
                                    </li>\
                                </ul>\
                            </div>\
                        </div>\
                    </div>\
                    <div class="p-5 pt-0 border-b dark:border-gray-700">\
                    ' + res.post.title + '\
                    </div>\
                    <div uk-lightbox>\
                        <a href="' + res.post.image + '">\
                            <img src="' + res.post.image + '" alt="" class="max-h-96 w-full object-cover" />\
                        </a>\
                    </div>\
                    <div class="p-4 space-y-3">\
                        <div class="flex space-x-4 lg:font-bold">\
                            <a style="cursor: pointer;" class="flex items-center space-x-2">\
                                <div class="p-2 rounded-full like-btn' + res.post.id + ' {% if request.user in post.likes.all %} text-gray-500 {% else %} text-black {% endif %}" id="like-btn" data-like-btn="' + res.post.id + '">\
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                                        <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />\
                                    </svg>\
                                </div>\
                                <div> Like</div>\
                            </a>\
                            <a href="#" class="flex items-center space-x-2">\
                                <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                                        <path fill-rule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clip-rule="evenodd" />\
                                    </svg>\
                                </div>\
                                <div> <span id="comment-count' + res.post.id + '">0</span> Comment</div>\
                            </a>\
                            <a href="#" class="flex items-center space-x-2 flex-1 justify-end">\
                                <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />\
                                    </svg>\
                                </div>\
                                <div> Share</div>\
                            </a>\
                        </div>\
                        <div class="flex items-center space-x-3 pt-2">\
                                <div class="dark:text-gray-100">\
                                    <strong><span id="like-count' + res.post.id + '">0</span></strong> Like\
                                </div>\
                        </div>\
                        <div class="border-t py-4 space-y-4 dark:border-gray-600" id="comment-div' + res.post.id + '"></div>\
                        <div class="bg-gray-100 rounded-full relative dark:bg-gray-800 border-t">\
                            <input placeholder="Add your Comment.." id="comment-input' + res.post.id + '" data-comment-input="' + res.post.id + '" class="bg-transparent max-h-10 shadow-none px-5 comment-input' + res.post.id + '">\
                            <div class="-m-0.5 absolute bottom-0 flex items-center right-3 text-xl">\
                                <a style="cursor: pointer;" id="comment-btn" class="comment-btn' + res.post.id + '" data-comment-btn="' + res.post.id + '">\
                                    <ion-icon name="send-outline" class="hover:bg-gray-200 p-1.5 rounded-full"></ion-icon>\
                                </a>\
                            </div>\
                        </div>\
                    </div>\
                </div>\
                '

                $("#create-post-modal").removeClass("uk-flex uk-open")
                $(".post-div").prepend(_html)
            }
        })
    })



})