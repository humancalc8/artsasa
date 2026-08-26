(function () {
    "use strict";

    /* NAV scroll state */
    const nav = document.getElementById("nav");
    function onScroll() {
        if (window.scrollY > 40) nav.classList.add("is-scrolled");
        else nav.classList.remove("is-scrolled");
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    /* Mobile burger -> simple show/hide of nav-links as overlay list */
    const burger = document.getElementById("burger");
    burger.addEventListener("click", function () {
        const links = document.querySelector(".nav-links");
        const open = links.style.display === "flex";
        links.style.cssText = open
            ? ""
            : "display:flex;position:fixed;top:0;left:0;right:0;bottom:0;flex-direction:column;align-items:center;justify-content:center;gap:34px;background:#1c1611;z-index:200;";
        if (!open) {
            links.querySelectorAll("a").forEach(function (a) {
                a.style.color = "#f6efe2";
                a.style.fontSize = "14px";
            });
        }
    });

})();