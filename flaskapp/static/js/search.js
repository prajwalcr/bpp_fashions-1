$(document).ready(function(){
$('button[id="srcb').click(function(){
    searchquery=document.getElementById('srcq').val
    var srcurl=new URL("http://127.0.0.1:5000/search")
    srcurl.searchParams.append('q',searchquery)
    $.ajax({
        url:srcurl,
        type:'GET',
        success:function(data){
            $.each(data,function(i,val){
                console.log(val.id)
                var html='<div class="col md-4 d-flex">';
                html+='<div class="card" id="'+val.id+'">';
                html+='<img class="card-img-top" src="'+val.imageURL+'" alt="...">';
                html+='<div class="card-body">';
                html+='<h4 class="card-title">'+val.title+'       '+val.price+'$</h4>';
                html+='<p class="card-text">'+val.productDescription+'</p>';
                html+='<a href="{{url_for("info",id="val.id")}}" class="btn btn-primary stretched-link">View Product</a>'.replace('val.id',val.id);
                html+='</div>';
                html+='</div>';
                html+='</div>';
                $('#forma').append(html)
        })
        }
    })
})
})