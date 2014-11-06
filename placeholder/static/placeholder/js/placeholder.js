(function ($) {
    $(function () {
        window.__placeholder_multiedit = window.__placeholder_multiedit ? window.__placeholder_multiedit : false;
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

                });
            }

            $("[data-placeholder-field]").each(function () {
                var $this = $(this);
                var json = $this.attr("data-placeholder-field");
                var meta = jQuery.parseJSON(json);

                var $button = $("#placeholder-field-button").clone();
                $button.attr("id", null);
                $button.addClass("placeholder-field-button");

                var offset = $this.offset();
                offset.left += $this.width();
                $button.css(offset);

                $button.appendTo(document.body);

                var get_text = function () {
                    return $this.text().replace(/^\s*/, "").replace(/\s*$/, "");
                }

                var original_text = get_text();

                var change = function () {
                    if (get_text() != original_text)
                        if (confirm("Salvar as alterações neste texto ?"))
                            save()
                        else {
                            $this.text(original_text)
                        }
                }

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
                });

            });

            $("[data-placeholder-image]").each(function () {

                var $this = $(this);
                var json = $this.attr("data-placeholder-image");
                var meta = jQuery.parseJSON(json);

                var $button = $("#placeholder-image-button").clone();
                $button.attr("id", null);
                $button.addClass("placeholder-image-button");

                var offset = $this.offset();
                offset.left += $this.width();
                $button.css(offset);

                $button.show();
                $button.appendTo(document.body);

                $button.click(function () {
                    $("input[type=file]").click();
                    return false;
                });

            });

            $("[data-placeholder-instance]").each(function () {
                var $this = $(this);
                var json = $this.attr("data-placeholder-instance");
                var meta = jQuery.parseJSON(json);
                var $button = $("#placeholder-instance-button").clone();
                $button.attr("id", null);
                $button.addClass("placeholder-instance-button");
                $button.attr({
                    'href': meta.admin_change_url + '?_popup=1&placeholder_admin=' + meta.placeholder_admin
                })
                $button.show();
                var offset = $this.offset();
                offset.left += $this.width();
                $button.css(offset);
                // $button.appendTo(this);
                $button.appendTo(document.body);
                $button.hover(function () {
                    // $this.effect("highlight", 500);
                    $this.addClass("transparent");
                }, function () {
                    $this.removeClass("transparent");
                });
                $button.fancybox({
                    // autoScale: false,
                    autoDimensions: false,
                    title: '',
                    width: '90%',
                    height: '90%',
                    afterClose: function () {
                        var url = location.href + "?__placeholder_expire_page=1";
                        $.get(url, function (source) {
                            var md5hash = $this.attr("data-placeholder-md5hash");
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
                            placeholders_init()
                        }, "html");
                    }
                });
            })

        }

        if (window.PLACEHOLDER_AUTOSTART) {
            placeholders_init();
        }
        else {
            $(document).bind('keyup', 'ctrl+shift+x', function(){
                placeholders_init();
            });
        }

    })
})(jQuery)
