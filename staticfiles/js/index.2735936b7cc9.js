$(document).ready(function () {
    var current_fs, next_fs, previous_fs;
    var left, opacity, scale;
    var animating;
    $(".steps").validate({
        errorClass: 'invalid',
        errorElement: 'span',
        errorPlacement: function (error, element) {
            error.insertAfter(element.next('span').children());
        },
        highlight: function (element) {
            $(element).next('span').show();
        },
        unhighlight: function (element) {
            $(element).next('span').hide();
        }
    });

    // Survey submission Event
    $("#survey-form").submit(function (e) {
        e.preventDefault(e);
        var data = $(this).serializeArray();

        // Disable action button
        var submit_btn = $('#submit');
        var prev_btn = submit_btn.prev('input[name="previous"]');
        submit_btn.prop("disabled", true);
        prev_btn.prop("disabled", true);
        submit_btn.fadeTo(100, 0.4);
        prev_btn.fadeTo(100, 0.4);
        $('.lds-ripple').show();
        postSurvey(data, $(this));
    });

    // Start Again Event
    $(".again").click(function () {
        window.location.href = '/';
    });

    // Next Event
    $(".next").click(function () {
        $(".steps").validate({
            errorClass: 'invalid',
            errorElement: 'span',
            errorPlacement: function (error, element) {
                error.insertAfter(element.next('span').children());
            },
            highlight: function (element) {
                $(element).next('span').show();
            },
            unhighlight: function (element) {
                $(element).next('span').hide();
            }
        });
        if ((!$('.steps').valid())) {
            return true;
        }
        if (animating) return false;
        animating = true;
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();
        if ($(this).val() != 'Submit') {
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
            next_fs.show();
            current_fs.animate({
                opacity: 0
            }, {
                step: function (now, mx) {
                    scale = 1 - (1 - now) * 0.2;
                    left = (now * 50) + "%";
                    opacity = 1 - now;
                    current_fs.css({
                        'transform': 'scale(' + scale + ')'
                    });
                    next_fs.css({
                        'left': left,
                        'opacity': opacity
                    });
                },
                duration: 800,
                complete: function () {
                    current_fs.hide();
                    animating = false;
                },
                easing: 'easeInOutExpo'
            });
        }
    });

    // Previous Event
    $(".previous").click(function () {
        if (animating) return false;
        animating = true;
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
        previous_fs.show();
        current_fs.animate({
            opacity: 0
        }, {
            step: function (now, mx) {
                scale = 0.8 + (1 - now) * 0.2;
                left = ((1 - now) * 50) + "%";
                opacity = 1 - now;
                current_fs.css({
                    'left': left
                });
                previous_fs.css({
                    'transform': 'scale(' + scale + ')',
                    'opacity': opacity
                });
            },
            duration: 800,
            complete: function () {
                current_fs.hide();
                animating = false;
            },
            easing: 'easeInOutExpo'
        });
    });

    var barColor = function (score) {
        if (score >= 80) {
            return 'bg-success';
        }
        else if (score < 80 && score >= 50) {
            return 'bg-warning';
        }
        else {
            return 'bg-danger';
        }
    }

    var postSurvey = function (data, current_html) {
        $.ajax({
            url: $(location).attr('pathname'),
            type: "post",
            data: data,
            success: function (response) {
                // Moving to Ending Popup
                current_fs = $('#submit').parent();
                next_fs = $('#submit').parent().next();
                next_fs.show();
                current_fs.animate({
                    opacity: 0
                }, {
                    step: function (now, mx) {
                        scale = 1 - (1 - now) * 0.2;
                        left = (now * 50) + "%";
                        opacity = 1 - now;
                        current_fs.css({
                            'transform': 'scale(' + scale + ')'
                        });
                        next_fs.css({
                            'left': left,
                            'opacity': opacity
                        });
                    },
                    duration: 800,
                    complete: function () {
                        current_fs.hide();
                        animating = false;
                    },
                    easing: 'easeInOutExpo'
                });

                var _type = response.type;
                var response_elm = $('.response');
                if (_type == 'client') {
                    var client_html = "";
                    $.each(response.data, function (index, obj) {
                        var br_clr = barColor(obj.score);
                        var _score = parseFloat(obj.score);
                        client_html += '<div style="margin-top:10px;"><span>Agency: ' + obj.name + '</span><div class="progress">\n' +
                            '                <div class="progress-bar-animated progress-bar-striped ' + br_clr + '" role="progressbar" style="width: ' + _score + '%; font-weight: bold;text-align: center;color:white;" aria-valuenow="' + _score + '" aria-valuemin="0" aria-valuemax="100">' + _score + '%</div>\n' +
                            '            </div></div>';
                    });
                    if (client_html) {
                        response_elm.html(client_html);
                    }
                    else{
                        response_elm.html('<h3 class="fs-subtitle" style="text-align: center">No Agencies Data Found!</h3>')
                    }
                }
                else if (_type = 'agency') {
                    response_elm.html('<h3 class="fs-subtitle" style="text-align: center">Survey Submitted Successfully!</h3>')
                }

            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(textStatus, errorThrown);
            }


        });
    }


});