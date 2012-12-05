(function($){
    "use strict";
    $(function(){
        $('#browserid').tooltip();
    });
})(jQuery);


$(document).ready(function(){
    $('.in-background').click(function(){
        var href = $(this).attr('href');

        $.get(href, function(data){
            window.location.reload()
        });
        return false;
    });
	var priorities = {
		'Highest': 5,
		'High': 4,
		'Normal': 3,
		'Low': 2,
		'Lowest': 1,
		'---': 0
	};
	$('.stupidtable').each(function(index){
		$(this).stupidtable({
			'priority': function(a,b){
				return priorities[a] - priorities[b];
			}
		});
	});

});
