(function($){
    "use strict";

    var loadedStamp = Date.now();
    var initialWait = 30000;  // 30 sec

    var bugsUpdatedRecently = function(){
        var bug_ids = $('.bug-list tbody tr').map(function(i, el){return $(el).data('bugid');}).get();
        if(bug_ids.length){
            bug_ids = bug_ids.join(',');
            $.ajax({
                url: '/bugs_updated/',
                type: 'POST',
                data: {'bug_ids': bug_ids},
                statusCode: {
                    204: checkUpdatesAgain,
                    200: function(){
                        $('#alert_messages').append([
                            '<div class="alert alert-info hide">',
                            '<a class="close" data-dismiss="alert">&times;</a>',
                            '<strong>Bugs on this page have been updated.</strong> Refresh to see.',
                            '</div>'
                        ].join('')).find('.alert').slideDown();
                    }
                }
            });
        }
    };

    var waitMultiplier = function(){
        // increase wait every 5 min
        return Math.ceil((Date.now() - loadedStamp)/300000);
    };

    var checkUpdatesAgain = function(){
        window.setTimeout(bugsUpdatedRecently, initialWait * waitMultiplier());
    };

    $(checkUpdatesAgain);

    // blocker popovers
    var $blocked_labels = $('.blocked-bug');
    var hide_all = function(){
        $blocked_labels.popover('hide');
    };
    $blocked_labels.popover({
        title: 'Blocked By',
        content: function(){
            return $(this).find('.blocker-links').html();
        },
        trigger: 'manual',
        animation: false
    });
    $blocked_labels.on('click', function(e){
        hide_all();
        $(this).popover('toggle');
        $('a.ttip').tooltip();
        return false;
    });
    $('body').on('click', hide_all);

})(jQuery);
