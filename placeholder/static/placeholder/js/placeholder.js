var PLACEHOLDER_NODE_DATA_PREFIX = "django:placeholder:"

function list_node_comments(node, comments, recursive) {
    if (comments == null)
        var comments = []
    if (recursive == null)
        var recursive = true
    if (node != null) {
        if (document.ELEMENT_NODE == node.nodeType) {
            for (var i = 0; i < node.childNodes.length; i++) {
                var child = node.childNodes[i]
                if (document.COMMENT_NODE == child.nodeType) {
                    comments.push(child)
                }
                else if ((recursive) && (document.ELEMENT_NODE == child.nodeType)) {
                    list_node_comments(child, comments, recursive)
                }
            }
        }
        return comments
    }
}

function is_placeholder(node) {
    return ((node.nodeType == document.COMMENT_NODE) && (node.data.search(PLACEHOLDER_NODE_DATA_PREFIX) == 0))
}

function list_placeholder(element, recursive) {
    return jQuery.grep(list_node_comments(element, [], recursive), function (node, index) {
        return is_placeholder(node)
    })
}

(function ($) {
    $(function () {
        var placeholders_init = function () {
            $.each(list_placeholder(document.body), function () {
                var len = PLACEHOLDER_NODE_DATA_PREFIX.length
                var ph_node = this
                var meta = jQuery.parseJSON(this.data.slice(len))
                var $this = $(this.parentNode)
                $this.attr("contenteditable", true)
                var get_text = function () {
                    return $this.text().replace(/^\s*/, "").replace(/\s*$/, "");
                }
                var original_text = get_text()
                var save = function () {
                    // trim the string
                    meta['value'] = get_text();
                    $.post("/placeholder/save/", meta, function () {
                        alert("Texto alterado com sucesso.")
                        original_text = meta['value']
                    })
                }
                var change = function () {
                    if (get_text() != original_text)
                        if (confirm("Salvar as alterações neste texto ?"))
                            save()
                        else {
                            $this.text(original_text)
                        }
                }
                $this.bind("blur", function ()  {
                    change()
                })
            })
        }

        $.getScript("/static/placeholder/js/jquery.hotkeys.js", function () {
            $(document).bind('keyup', 'ctrl+shift+e', function(){
                if (confirm("Carregar edição de conteúdo ?"))
                {
                    var credentials = prompt("Usuário/Senha");
                    placeholders_init();
                }
            });
        })

    })
})(jQuery)
