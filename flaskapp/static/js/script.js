$(document).ready(function(){
jQuery.ajaxSetup({async:false});
/*$.ajax({
  url:'/api/products/categories/children/1',
  type:'GET',
  datatype:'JSON',
  success:function(data){
    var html ='<div class="dropdown">'
    html+='<button class="btn btn-info dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" data-mdb-toggle="dropdown" aria-expanded="false">Categories</button>';
    html+='<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">';
    for (var i=0;i<data.length;i++){
      html += '<li><a class="dropdown-item" id="'+data[i]['id']+'"onclick="category('+data[i]['id']+')">'+data[i]['name']+'</a>';
      $.get('/api/products/categories/children/'+data[i]['id'],function(subdata){
        console.log(subdata.length)
        if (subdata.length==0){
          console.log('hi')
        }
        else{
        html += '<ul class="dropdown-menu dropdown-submenu">'
        console.log(html)
        for (var j=0;j<subdata.length;j++){
          html+='<li><a class="dropdown-item" id="'+subdata[j]['id']+'"onclick="category('+subdata[j]['id']+')">'+subdata[j]['name']+'</a></li>';
        }
        html+='</ul>'
      }
        })
      html+='</li>'
      }
    html+='</ul>'
    html+='</div>'
    $('#facets').append(html)
  }

})*/
$.ajax({
  url:'/api/products/categories/children/1',
  type:'GET',
  datatype:'JSON',
  success:function(data){
    var html ='<div class="dropdown">'
    html+='<button class="btn btn-info dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" data-mdb-toggle="dropdown" aria-expanded="false">Categories</button>';
    html+='<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">';
    for (var i=0;i<data.length;i++){
      html += '<li><a class="dropdown-item" id="'+data[i]['id']+'"onclick="category('+data[i]['id']+')">'+data[i]['name']+'</a>';
      html += subcat(data[i]['id'])
      html += '</li>'
    }
    html += '</ul>'
    $('#facets').append(html)
  }
})
    var curl=new URL(window.location.href)
    sort=curl.searchParams.get('sort')
    $('select[id="sort"]').val(sort).change();

  function category(val){
    ceurl=new URL("http://127.0.0.1:5000/")
    ceurl.searchParams.append('id',val)
    console.log(ceurl)
    window.location.href=ceurl
  }
  function subcat(subcatid){
    var html =''
    $.get('/api/products/categories/children/'+subcatid,function(subdata){
      if (subdata.length==0){
        console.log(html1)
      }
      else{
        html += '<ul class="dropdown-menu dropdown-submenu">'
        for (var j=0;j<subdata.length;j++){
          html += '<li><a class="dropdown-item" id="'+subdata[j]['id']+'"onclick="category('+subdata[j]['id']+')">'+subdata[j]['name']+'</a>';
          html +=subcat(subdata[j]['id'])
          html += '</li>'
      }
      html += '</ul>'
    
      }
      })
      return html

  }

})

  