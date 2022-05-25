$(".resizable_textarea").each(
    function () {
        this.setAttribute("style", "height:" + (this.scrollHeight) + "px;");
    }
).on("input", function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    }
);