/*global $tooltip:true */
$(function(){
    "use strict";
    window.$tooltip = $('<div id="tooltip"></div>').appendTo("body");
    $('td.ttip').tooltip();
});
