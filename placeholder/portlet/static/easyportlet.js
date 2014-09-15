(function ($) {

    function get_qs_param(name) {
        return decodeURI(
            (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
        );
    }

    $(function () {
        $("#id_template_name").change(function () {
            var ct_id = get_qs_param("ct_id")
            var url = location.origin + location.pathname + "?ct_id=" + ct_id + "&template_name=" + this.value;
            location.href = url;
        });
    });

})(django.jQuery);
