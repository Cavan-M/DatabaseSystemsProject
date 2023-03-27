$("#search").click(()=>{
    let querystring = $("#query").val();
    window.location.replace("/manageorders?q=" + querystring + "");
});