$(function() {
    var add_notification = function(message) {
        if($('.messages').length > 0) {
            $('.messages').append('<li><span>' + message + '</span></li>');
        }
        else {
            $('#content').before('<ul class="messages grid_12"><li><span>' + message + '</span></li></ul>');
        }
    };
    $('#event_description_field textarea').keydown(function(event) {
        if(event.keyCode == 13) {
            $('#event_form').submit();
            return false;
        }
        else {
            var f = $('#event_description_field');
            var ta = $('#event_description_field textarea');
            var f_height = parseInt(f.css('height').replace('px',''), 10);
            var ta_height = parseInt(ta.css('height').replace('px',''), 10);
            if(this.offsetHeight < this.scrollHeight || this.value.indexOf("\n") != -1 || this.scrollLeft > 0 || this.scrollTop > 0) {
                f.css('height', f_height + 60 + 'px');
                ta.css('height', ta_height + 60 + 'px');
            }
        }
    });
    $('#nav > li a, #footer li a').mouseover(function() {
        $(this).fadeTo('fast', 1.0);
    }).mouseout(function() {
        $(this).fadeTo('fast', 0.6);
    });
    $('#nav > li > span.subnav_everyone').mouseover(function() {
        var pos = $('#nav > li > span').position();
        $('#nav > li > ul.subnav_everyone')
            .css('position', 'absolute')
            .css('top', pos['top'] + 35 + 'px')
            .css('left', pos['left'] - 22 + 'px')
            .css('z-index', '999')
            .fadeIn('fast');
    });
    $('#nav > li > span.subnav_friends').mouseover(function() {
        var pos = $('#nav > li > span').position();
        $('#nav > li > ul.subnav_friends')
            .css('position', 'absolute')
            .css('top', pos['top'] + 35 + 'px')
            .css('left', pos['left'] + 90 + 'px')
            .css('z-index', '999')
            .fadeIn('fast');
    });
    $('#nav > li > ul').bind("mouseleave", function() {
        $('#nav > li > ul').fadeOut('fast');
    });
    $(document).click(function() {
        $('#nav > li > ul').fadeOut('fast');
    });
    $('ul.messages li').livequery(function() {
        $(this).append('<a class="clear_button" href="#">Clear</a>');
    });
    $('a.clear_button').livequery(function() {
        $(this).click(function() {
            $(this).parent().fadeOut("fast");
            return false;
        });
    });
    /* TODO: Uncomment this if you want to be annoyed.
    $('div.person').livequery(function() {
        $(this).mouseover(function() {
            $(this).animate({'marginRight': '16px', 'marginBottom': '0px'}, "fast")
            .find('img')
            .animate({'width': '65px', 'height': '65px', 'marginTop': '-3px', 'marginLeft': '-3px'}, "fast")
            .parent().find('.username')
            .animate({'fontSize': '12px', 'width': '65px', 'marginTop': '51px', 'marginLeft': '-3px'}, "fast")
            .fadeTo('fast', 1.0);
        }).mouseout(function() {
            $(this).animate({'marginRight': '20px', 'marginBottom': '10px'}, "fast")
            .find('img')
            .animate({'width': '58px', 'height': '58px', 'marginTop': '0px', 'marginLeft': '0px'}, "fast")
            .parent().find('.username')
            .animate({'fontSize': '11px', 'width': '58px', 'marginTop': '47px', 'marginLeft': '0px'}, "fast")
            .fadeTo('fast', 0.7);
        });
    });
    */
    $('#event_form').ajaxForm({
        clearForm: true,
        beforeSubmit: function(formData, jqForm, options) {
            var field_length = $('#id_description').fieldValue()[0].length;
            if(field_length > 340) {
                add_notification('Content too long.  Please shorten by ' + 
                    (field_length - 340) + ' character' + 
                    ((field_length - 340) == 1 ? '' : 's') + '.');
                return false;
            }
            return true;
        },
        success: function(response_text, status_text) {
            $('#event_description_field').css('height', '60px');
            $('#event_description_field textarea').css('height', '56px');
            $('#my_event').fadeOut("fast", function() {
                $('#my_event').html(response_text);
                $('#my_event').fadeIn("fast");
            });
        }
    });
    $('.toggle_attendance_form').each(function (i) {
        var form = $($('.toggle_attendance_form').get(i));
        form.ajaxForm({
            dataType: 'json',
            success: function(data) {
                if(data.created == true) {
                    form.children('.attendance').replaceWith('<input class="attendance unattend" type="submit" value="✓" />');
                }
                else {
                    form.children('.attendance').replaceWith('<input class="attendance attend" type="submit" value="+" />');
                }
                form.parent().siblings('.person_count').children('a').html('<span class="number">' + data.count + '</span> <span class="label">' + (data.count == 1 ? 'Person' : 'People') + '</span>');
            }
        });
    });
    $('.attend').val('+').livequery(function() {
        $(this).val('+');
    });
    $('.unattend').val('✓').livequery(function() {
        $(this).val('✓');
    });
});
