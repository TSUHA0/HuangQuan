import $ from "jquery";


let itemMouseover = function (class_name) {
    var focusTooltip = $(class_name);
    focusTooltip.css("display", "block");
};

let itemMouseout = function (class_name) {
    var focusTooltip = $(class_name);
    focusTooltip.css("display", "none");
};

let itemMousemove = function (e, class_name) {
    var self = this;
    var focusTooltip = $(class_name);
    focusTooltip.css("top", e.clientY - 8 + "px");
    focusTooltip.css("left", e.clientX + 10 + "px");
    var headerHtml =
        "<div style='font-size:12px;color: #fec443;font-weight: bold;font-family: MicrosoftYaHei;'>" +
        "我的悬浮框参考：" +
        "</div>";
    var effectHtml =
        "<div style='font-size:12px;margin-top:5px;'>" + "</div>";
    self.toolTopbody = headerHtml + effectHtml;
};

export {itemMouseover, itemMouseout, itemMousemove};