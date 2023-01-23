$(document).ready(function(){
$('select[id="category2"]').hide();
$.ajax({
  url:'/categories',
  type:'GET',
  datatype:'JSON',
  success:function(data){
    for(var key in data){
      var opt="<option value="+key+">"+key+"</option>";
      $(opt).appendTo('#category1')
    }
    $('select[id="category1"]').change(function(){
      $('#category2').empty();
      var ca1=document.getElementById("category1").value
      $.each(data[ca1],function(key,val){
        var opt2="<option value="+val+">"+val+"</option>";
        $(opt2).appendTo('#category2')
      })
      $('select[id="category2"]').show();
    });
    }
  })
$('button[id="fac"]').click(function(){
  $.ajax({
    url:'/',
    type:'GET',
    data:{
      'cat1':document.getElementById("category1").value,
      'cat2':document.getElementById("category2").value
    },
    success: function(response){ 
        $('#main').text(response)
    console.log('button click')
    }

  })
});


  
  });