
    $('.change').css('backgroundColor','green')

$(document).ready(function(){
$('#additems').css({
    'border':'1px solid black',
    'backgroundColor':'#9c9ebb'
})
$('.colors').css({
    'border':'1px solid black',
    'backgroundColor':'#ea8b5c'
    overflow-y:scroll
})

$('#add').click(function(){
 var list = $('#list').val();
 if (list==""){
    alert('Enter a valid list dummy');
    return false;
 }
$('.list-group').append('<li>' + list + '</li>')
$('#list').val('')
})
})
