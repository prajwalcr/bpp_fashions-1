$(document).ready(function(){
$('select[id="category2"]').hide();
$.ajax({
  url:'/categories',
  type:'GET',
  datatype:'JSON',
  success:function(data){
    for(var key in data){
      var opt='<option value="'+key+'">'+key+'</option>';
      $(opt).appendTo('#category1')
    }
    $('select[id="category1"]').change(function(){
      $('#category2 options:not(:first)').remove();
      var ca1=document.getElementById("category1").value
      $.each(data[ca1],function(key,val){
        var opt2='<option value="'+val+'">'+val+'</option>';
        $(opt2).appendTo('#category2')
      })
      $('select[id="category2"]').show();
    });
    }
  })
$('button[id="fac"]').click(function(){
  cat1=document.getElementById('category1').value
  cat2=document.getElementById('category2').value
  console.log(cat1,cat2)
  var url=new URL("http://127.0.0.1:5000/")
  if (cat1!=null && cat2!=""){
    url.searchParams.append("cat1",cat1.toString())
    url.searchParams.append("cat2",cat2.toString())
  }
  else if(cat1!=null && cat2==""){
    url.searchParams.append("cat1",cat1.toString())
  }
  window.location.href=url
  console.log(url)
    })

  
});


  