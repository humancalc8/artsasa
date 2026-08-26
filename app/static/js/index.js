(function () {
    "use strict";

    /* Work filter */
    const filters = document.querySelectorAll(".filter");
    const cards = document.querySelectorAll(".work-card");

    filters.forEach(function (filter) {
        filter.addEventListener("click", function () {
            const category = filter.dataset.filter;

            filters.forEach(function (f) { f.classList.remove("active"); });
            filter.classList.add("active");

            cards.forEach(function (card) {
                const matches = category === "all" || card.dataset.category === category;
                if (matches) {
                    card.style.display = "";
                    requestAnimationFrame(function () {
                        card.style.opacity = "1";
                        card.style.transform = "scale(1)";
                    });
                } else {
                    card.style.opacity = "0";
                    card.style.transform = "scale(.96)";
                    setTimeout(function () {
                        if (card.dataset.category !== category && category !== "all") {
                            card.style.display = "none";
                        }
                    }, 350);
                }
            });
        });
    });

    /* Scroll reveal */
    const revealElements = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const delay = Number(el.dataset.delay || 0);
                setTimeout(function () { el.classList.add("is-visible"); }, delay * 90);
                observer.unobserve(el);
            });
        }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

        revealElements.forEach(function (el) { observer.observe(el); });
    } else {
        revealElements.forEach(function (el) { el.classList.add("is-visible"); });
    }

})();