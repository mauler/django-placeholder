(function ($) {
    $(function () {
        var placeholders_init = function () {

            $("[data-placeholder-instance]").each(function () {
                var $this = $(this);
                var json = $this.attr("data-placeholder-instance");
                var meta = jQuery.parseJSON(json);
                var $button = $("#placeholder-button").clone()
                $button.attr("id", null);
                $button.attr({
                    'href': meta.admin_change_url + '?_popup=1&placeholder_admin=' + meta.placeholder_admin
                })
                $button.show();
                var offset = $this.offset();
                offset.left += $this.width();
                $button.css(offset);
                $button.appendTo(document.body);
                $button.fancybox({
                    title: '',
                    afterClose: function () {
                        var url = location.href + "?__placeholder_expire_page=1";
                        $.get(url, function (source) {
                            var md5hash = $this.attr("data-placeholder-md5hash");
                            var sel = "[data-placeholder-md5hash=" + md5hash +"]";
                            var $current = $(sel);
                            var $updated = $(source).find(sel);
                            $current.replaceWith($updated);
                        });
                    }
                });
            })

        }

        $(document).bind('keyup', 'ctrl+shift+x', function(){
            placeholders_init();
        });

    })
})(jQuery)
