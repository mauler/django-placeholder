(function ($) {

    function reposition_button($button) {
        var $placeholder = $button.data("data-placeholder");
        var offset = $placeholder.offset();
        offset.left += $placeholder.width() - $button.width();
        $button.css(offset);
    }

    function reposition_all_button() {
        $(".placeholder-button").each(function () {
            reposition_button($(this));
        });
    }

    function get_placeholder_button($placeholder, selector) {
        var $button = $("#" + selector).clone();
        $button.attr("id", null);
        $button.addClass(selector);
        $button.addClass("placeholder-button");
        $button.data("data-placeholder", $placeholder);
        reposition_button($button);
        return $button;
    }

    $(function () {

        window.__placeholder_multiedit = window.__placeholder_multiedit ? window.__placeholder_multiedit : false;

        $(window).scroll(function () {
            reposition_all_button();
        });

        function refresh (md5hash) {
            var url = location.href + "?__placeholder_expire_page=1";
            $.get(url, function (source) {
                var sel = "[data-placeholder-md5hash=" + md5hash +"]";
                var d = document.implementation.createHTMLDocument();
                d.write(source);
                var $current = $(sel);
                var $updated = $(sel, d);
                $current.each(function (index, element) {
                    var $element = $updated.eq(index);
                    $(element).replaceWith($element);
                    $('html, body').animate({
                        scrollTop: $element.offset().top + 'px'
                    }, 'fast');
                    $element.effect("highlight", 1000);
                });
                $(".placeholder-button").remove();
                imagesLoaded($updated, function(instance) {
                    placeholders_init()
                });
            }, "html");
        }


        window.placeholders_init = function () {

            var multiedit_data = {};

            var $multiedit_button = $("#placeholder-multiedit-button");

            if (__placeholder_multiedit) {

                function prepare(arr, key) {
                    arr[key] = arr[key] ? arr[key]: {};
                    return arr[key];
                }

                $multiedit_button.click(function () {

                    var url = '/placeholder/multiedit/save/';
                    var params = {data: JSON.stringify(multiedit_data)};
                    $.post(url, params, function () {
                        $multiedit_button.hide();
                    })
                    return false;
                });
            }

            $("[data-placeholder-field]").each(function () {
                var $this = $(this);
                var json = $this.attr("data-placeholder-field");
                var meta = jQuery.parseJSON(json);

                var $button = get_placeholder_button(
                    $this, "placeholder-field-button");

                $button.appendTo(document.body);

                var get_text = function () {
                    return $this.text().replace(/^\s*/, "").replace(/\s*$/, "");
                }

                var original_text = get_text();

                $this.bind("keyup blur", function ()  {
                    if (__placeholder_multiedit) {
                        var text = get_text();
                        if (text != original_text) {

                            var data = multiedit_data;
                            var data = prepare(data, meta.app_label);
                            var data = prepare(data, meta.model_name);
                            var data = prepare(data, meta.model_pk);
                            data[meta.model_field] = text;

                            $multiedit_button.show();
                        }
                    }
                    else {
                        if (get_text() != original_text) {
                            $button.show();
                            reposition_all_button();
                        }
                        else {
                            $button.hide();
                        };
                    }
                });

                $this.attr("contenteditable", true);

                $button.click(function () {
                    meta['value'] = get_text();
                    $.post(meta.save_url, meta, function () {
                        original_text = meta['value'];
                        $button.hide();
                    })
                    return false;
                });

            });

            $("[data-placeholder-image]").each(function () {

                var $this = $(this);
                var $ph = $this;
                var json = $this.attr("data-placeholder-image");
                var meta = jQuery.parseJSON(json);

                var $button = get_placeholder_button(
                    $this, "placeholder-image-button");

                $button.show();
                $button.appendTo(document.body);

                $button.click(function () {
                    var $form = $("#__placeholder_form");
                    $form.children("input[type=text]").remove();

                    var $file = $('<input type="file" name="' + meta.model_field + '"/>');
                    $file.appendTo($form);
                    $file.unbind("change").change(function () {
                        if (this.value != "") {
                            window.__this = this;

                            var $input = $(this);
                            var input = this;
                            var form = $form.get(0);
                            var data = new FormData(form);

                            $.each(meta, function (key, value) {
                                data.append(key, value);
                            });

                            $.ajax({
                                url: $form.attr('action'),
                                type: $form.attr('method'),
                                data: data,
                                dataType: "json",
                                cache: false,
                                processData: false,
                                contentType: false,
                                success: function(data) {

                                    if (data == true) {
                                        refresh($ph.attr("data-placeholder-md5hash"));
                                    }
                                    else if (data == false) {

                                    }
                                    else {
                                        alert("else");
                                    }
                                }
                            });

                        }
                    });
                    $file.click();
                    return false;
                });

            });

            $("[data-placeholder-instance]").each(function () {
                var $this = $(this);
                var json = $this.attr("data-placeholder-instance");
                var meta = jQuery.parseJSON(json);

                var $button = get_placeholder_button(
                    $this, "placeholder-instance-button");

                var url = meta.admin_change_url + '?_popup=1' +
                    '&placeholder_admin=' + meta.placeholder_admin +
                    '&placeholder_admin_fields=' + meta.placeholder_admin_fields;
                $button.attr({
                    'href': url
                })
                $button.show();
                $button.appendTo(document.body);
                $button.hover(function () {
                    $this.effect("highlight", 500);
                }, function () {
                });
                $button.fancybox({
                    // autoScale: false,
                    autoDimensions: false,
                    title: '',
                    width: '90%',
                    height: '90%',
                    afterClose: function () {
                        refresh($this.attr("data-placeholder-md5hash"));
                    }
                });
            })

        }

        if (window.PLACEHOLDER_AUTOSTART) {
            setTimeout(function () {
                placeholders_init();
            }, 0);
        }
        else {
            $(document).bind('keyup', 'ctrl+shift+x', function(){
                placeholders_init();
            });
        }

    })
})(jQuery)
