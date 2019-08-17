/*
    Author: Shankar K (Oct 2017)
    Description:
        First simple web application to manage day-to-day task lists
*/


$(document).on("ready", function(){
    /* 
        Fill up responses:
        1. Front end: create button and send post 
        2. Backend : Write mongodb schema and create post API
    */
    function readBody(xhr) {
        var data;
        if (!xhr.responseType || xhr.responseType === "text") {
            data = xhr.responseText;
        } else if (xhr.responseType === "document") {
            data = xhr.responseXML;
        } else {
            data = xhr.response;
        }
        return data;
    }
    
    function displayLiItemStr(str, id) {
        var liItem = '<li class="list-group-item" data-id="' + id + '"><input type="checkbox" class="mycheck"> <div class="tasktext">'+ str  + ' </div></span><span class="glyphicon glyphicon-remove taskgly "></span></li>';
        return liItem;
    }
    
    /*  
        JSON-GENERATOR:
            createDate: '{{date(new Date(2017, 1, 1), new Date(), "YYYY-MM-dd hh:mm:ss")}}',
            taskDesc: '{{lorem(integer(15,25), "words")}}' (OR)  task:'{{lorem(1,"sentences")}}'
    */
    function setupInitialView() {
        var req = new XMLHttpRequest();
        req.open("GET", "/tasks", true);
        req.onload = function () {
            if (req.status == 200) {
                data = JSON.parse(readBody(req));
                for (var i=0;i < data.length; i++) {
                    var liItem = displayLiItemStr(data[i].task, data[i]._id);
                    $(".cTaskList").append(liItem);
                }
            }
        };
        req.send();
        $(".imgmore").css("display", 'none');
    }

    $(".creategly").click(function() {
        var str = $("input").val();
        if (!str || str.length == 0) {
            return;
        }
        
        var req = {
            url: '/tasks',
            type: 'POST',
            success: onSuccess,
            error: onError,
            data: JSON.stringify({ task: str }),
            contentType: 'application/json; charset=utf-8'
        };
        $.ajax(req);
        
        function onSuccess(data) {
            var liItem = displayLiItemStr(data.task, data._id);
            $(".cTaskList li:first").before(liItem);
        }
        function onError(r, err) {
            alert("Request: "+JSON.stringify(err));
        }
    })

    $(".taskmore").click(function() {
        start_think();
        function onSuccess(data) {
            for (var i=0;i < data.length; i++) {
                var liItem = displayLiItemStr(data[i].task, data[i]._id);
                $(".cTaskList").append(liItem);
            }
            stop_think();
        }
        function onError(r, err) {
            alert("Request: "+JSON.stringify(err));
            stop_think();
        }
        var req = {
            url: '/tasks',
            type: 'GET',
            success: onSuccess,
            error: onError

        };
        $.ajax(req);
    });
    
    $(".cTaskList").on("click", ".taskgly", function() {
        var item = $(this).closest("li");
        var id =  item[0].getAttribute("data-id");
        console.log("Pressed taskgly - delete the task " + item.index() + " id " + id )
            
        var req = {
            url: '/tasks/' + id ,
            type: 'DELETE',
            success: onSuccess,
            error: onError,
        };
        $.ajax(req);
        
        function onSuccess(data) {
            item.remove();
        }
        function onError(r, err) {
            alert(JSON.stringify(err));
        }
    });
    
    $(".mycollapse").click(function() {
        $(".cTaskList").empty();
        setupInitialView();
    });

    function start_think() {
        $(".taskmore").css("display", 'none');
        $(".imgmore").css("display", 'block');
    }
    
    function stop_think() {
        $(".imgmore").css("display", 'none');
        $(".taskmore").css("display", 'block');
    }

    /* Setup Initial view */
    setupInitialView()
})
