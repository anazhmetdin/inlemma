$(".resizable_textarea").each(
    function () {
        this.setAttribute("style", "height:" + (this.scrollHeight) + "px;");
    }
).on("input", function () {
        this.style.height = "80px";
        // this.style.height = (this.scrollHeight) + "px";
        if (this.scrollHeight >= 80) { this.style.height = 5 + "px"; this.style.height = (this.scrollHeight + 10) + "px"; }
    }
);