(function ($) {
    $(function () {
        var placeholders_init = function () {

            $("[data-placeholder-instance]").each(function () {
                var $this = $(this);
                var json = $this.attr("data-placeholder-instance");
                var meta = jQuery.parseJSON(json);
                var $button = $("#placeholder-button").clone();
                $button.attr("id", null);
                $button.addClass("placeholder-button");
                $button.attr({
                    'href': meta.admin_change_url + '?_popup=1&placeholder_admin=' + meta.placeholder_admin
                })
                $button.show();
                var offset = $this.offset();
                offset.left += $this.width();
                $button.css(offset);
                // $button.appendTo(this);
                $button.appendTo(document.body);
                window._$b = $button;
                window._$t = $this;
                $button.hover(function () {
                    $this.effect("highlight", 500);
                    $this.addClass("transparent");
                }, function () {
                    $this.removeClass("transparent");
                });
                $button.fancybox({
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
                                $element.effect("pulsate", 500);
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

    })
})(jQuery)
