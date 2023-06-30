$(document).ready(function(){
    $('#btn').click(function(){
            $('#btn').toggleClass('btn btn-primary');
           var liked = $(this).hasClass('btn btn-primary');
           if(liked){
                $(this).text('liked');
           }else{
                $(this).text('like');
           }
    })
}); 