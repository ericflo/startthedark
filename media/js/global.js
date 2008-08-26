$(function() {
    $('#event_description_field textarea').keydown(function() {
        var f = $('#event_description_field');
        var ta = $('#event_description_field textarea');
        var f_height = parseInt(f.css('height').replace('px',''), 10);
        var ta_height = parseInt(ta.css('height').replace('px',''), 10);
        if(this.offsetHeight < this.scrollHeight || this.value.indexOf("\n") != -1 || this.scrollLeft > 0 || this.scrollTop > 0) {
            f.css('height', f_height + 60 + 'px');
            ta.css('height', ta_height + 60 + 'px');
        }
    });
    $('#nav > li > span').mouseover(function() {
        var pos = $('#nav > li > span').position();
        $('#nav > li > ul')
            .css('position', 'absolute')
            .css('top', pos['top'] + 30 + 'px')
            .css('left', pos['left'] + 'px')
            .css('display', 'block');
    });
    $('#nav > li > ul').bind("mouseleave", function() {
        $('#nav > li > ul').css('display', 'none');
    });
    $(document).click(function() {
        $('#nav > li > ul').css('display', 'none');
    });
});