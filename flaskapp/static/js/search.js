$(document).ready(function(){
console.log('start')
$(document).on('click','button[id="srcb"]',function(){
    console.log("Search clicked")
    var srcurl=new URL(window.location.href)
    query=currenturl.searchParams.get('q')
    srcurl.searchParams.append("q",query)
    console.log(query,srcurl)
    $.ajax({
        url:srcurl.toString(),
        type:'GET',
        success:function(data){
            console.log(data)
            $.each(data,function(i,val){
                console.log(val)
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