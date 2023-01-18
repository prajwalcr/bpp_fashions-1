$(document).ready(function(){
$('select[id="category2"]').hide();
$('select[id="category1"]').change(function(){
    $('select[id="category2"]').show();
});
$("button").click(function(){
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