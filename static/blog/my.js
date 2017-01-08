$(document).ready(function(){
    $(".content-markdown").each(function(){
        var content=$(this).text();
        var markedContent = marked(content);
        $(this).html(markedContent);
        });
    $(".post-detail-item img").each(function(){
        $(this).addClass("img-responsive");
        });

    var titleInput = $("#id_title");

    function setTitle(value){
        $("#preview-title").text(value);
    }

    setTitle(titleInput.val());

    titleInput.keyup(function(){
        var newTitle = $(this).val();
        setTitle(newTitle);
    });


    var contentInput = $("#id_text");

    function setContent(value){
        var markedContent = marked(value);
        $("#preview-content").html(markedContent);
        $("#preview-content img").each(function(){
            $(this).addClass("img-responsive");
        });
    }

    setContent(contentInput.val());

    contentInput.keyup(function(){
        var newContent = $(this).val();
        setContent(newContent);
    });


})