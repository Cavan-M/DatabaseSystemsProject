$("#search").click(()=>{
    let querystring = $("#query").val();
    window.location.replace("/managekeys?q=" + querystring + "");
});