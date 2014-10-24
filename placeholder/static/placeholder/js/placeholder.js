(function ($) {
    $(function () {
        var placeholders_init = function () {

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
                    if (get_text() != original_text) {
                        $button.show();
                    }
                    else {
                        $button.hide();
                    };
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

        $(document).bind('keyup', 'ctrl+shift+x', function(){
            placeholders_init();
        });

        placeholders_init();

    })
})(jQuery)
