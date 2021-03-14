$(document).ready(function () {

});

function makeDELETErequest(id) {
    $.ajax({
        url: '/item/' + id,
        type: 'DELETE',
        success: function (result) {
            window.location.replace("/")
        }
    });
}
