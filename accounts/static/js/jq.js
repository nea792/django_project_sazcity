$(document).ready(function()
{
   /* $( ".dropdown" ).hover(
        function() {
          $(this).children('div').show(100);
        }, function() {
            $(this).children('div').hide(100);
        }
    );*/
    setInterval(function(){ 
        $( ".parent_banner img" ).fadeToggle(1500);
    }, 100);
})
