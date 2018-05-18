setInterval(function() {
    $("#content").load(location.href+" #content>*","");
}, 60000);