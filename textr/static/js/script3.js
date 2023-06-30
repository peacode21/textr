$(document).ready(function(){

$('#add').click(function(){
 var list = $('.list').val();
 if (list==""){
    alert('do not submit an empty comment again else you will be blocked');
    return false;
 }
$('.comment').append(list);
$('.list').val('')
})
})
