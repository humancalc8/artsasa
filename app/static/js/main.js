document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       MOBILE NAVIGATION
    ========================= */

    const mobileMenuButton = document.getElementById("mobileMenuButton");
    const mainNavigation = document.getElementById("mainNavigation");

    if (mobileMenuButton && mainNavigation) {

        mobileMenuButton.addEventListener("click", () => {

            mainNavigation.classList.toggle("open");

            const icon = mobileMenuButton.querySelector("i");

            if (mainNavigation.classList.contains("open")) {
                icon.classList.remove("fa-bars");
                icon.classList.add("fa-xmark");
                document.body.style.overflow = "hidden";
            } else {
                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
                document.body.style.overflow = "";
            }

        });


        /* Close menu when navigation link is clicked */

        const navLinks = mainNavigation.querySelectorAll(".nav-link");

        navLinks.forEach(link => {

            link.addEventListener("click", () => {

                mainNavigation.classList.remove("open");

                const icon = mobileMenuButton.querySelector("i");

                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");

                document.body.style.overflow = "";

            });

        });

    }


    /* =========================
       SEARCH OVERLAY
    ========================= */

    const searchButton = document.getElementById("searchButton");
    const searchOverlay = document.getElementById("searchOverlay");
    const closeSearch = document.getElementById("closeSearch");
    const searchInput = document.getElementById("searchInput");

    if (searchButton && searchOverlay) {

        searchButton.addEventListener("click", () => {

            searchOverlay.classList.add("open");

            document.body.style.overflow = "hidden";

            setTimeout(() => {

                if (searchInput) {
                    searchInput.focus();
                }

            }, 300);

        });

    }


    if (closeSearch && searchOverlay) {

        closeSearch.addEventListener("click", () => {

            searchOverlay.classList.remove("open");

            document.body.style.overflow = "";

        });

    }


    /* Close search with Escape */

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {

            if (
                searchOverlay &&
                searchOverlay.classList.contains("open")
            ) {

                searchOverlay.classList.remove("open");
                document.body.style.overflow = "";

            }

            if (
                mainNavigation &&
                mainNavigation.classList.contains("open")
            ) {

                mainNavigation.classList.remove("open");

                if (mobileMenuButton) {

                    const icon =
                        mobileMenuButton.querySelector("i");

                    icon.classList.remove("fa-xmark");
                    icon.classList.add("fa-bars");

                }

                document.body.style.overflow = "";

            }

        }

    });


    /* =========================
       SEARCH INPUT
    ========================= */

    if (searchInput) {

        searchInput.addEventListener("keydown", (event) => {

            if (event.key === "Enter") {

                const searchTerm =
                    searchInput.value.trim();

                if (searchTerm !== "") {

                    console.log(
                        "Searching for:",
                        searchTerm
                    );

                    /*
                     * Later you can connect this
                     * to your Django search view.
                     */

                }

            }

        });

    }


    /* =========================
       HEADER SCROLL EFFECT
    ========================= */

    const siteHeader =
        document.getElementById("siteHeader");

    if (siteHeader) {

        const handleHeaderScroll = () => {

            if (window.scrollY > 50) {

                siteHeader.classList.add("scrolled");

            } else {

                siteHeader.classList.remove("scrolled");

            }

        };

        window.addEventListener(
            "scroll",
            handleHeaderScroll,
            { passive: true }
        );

        handleHeaderScroll();

    }


    /* =========================
       ACTIVE NAVIGATION
    ========================= */

    const sections =
        document.querySelectorAll("section[id]");

    const navigationLinks =
        document.querySelectorAll(".nav-link");

    const updateActiveNavigation = () => {

        let currentSection = "home";

        sections.forEach(section => {

            const sectionTop =
                section.offsetTop - 150;

            if (window.scrollY >= sectionTop) {
                currentSection = section.id;
            }

        });

        navigationLinks.forEach(link => {

            link.classList.remove("active");

            const target =
                link.getAttribute("href");

            if (target === #${currentSection}) {

                link.classList.add("active");

            }

        });

    };

    if (sections.length && navigationLinks.length) {

        window.addEventListener(
            "scroll",
            updateActiveNavigation,
            { passive: true }
        );

        updateActiveNavigation();

    }


    /* =========================
       SCROLL REVEAL
    ========================= */

    const revealElements =
        document.querySelectorAll(".reveal");

    if (revealElements.length) {

        const revealObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (entry.isIntersecting) {

                            entry.target.classList.add(
                                "visible"
                            );

                            observer.unobserve(
                                entry.target
                            );

                        }

                    });

                },
                {
                    threshold: 0.12,
                    rootMargin: "0px 0px -40px 0px"
                }
            );

        revealElements.forEach(element => {

            revealObserver.observe(element);

        });

    }


    /* =========================
       WISHLIST BUTTONS
    ========================= */

    const wishlistButtons =
        document.querySelectorAll(".wishlist-button");

    wishlistButtons.forEach(button => {

        button.addEventListener("click", () => {

            button.classList.toggle("active");

            const icon =
                button.querySelector("i");

            if (!icon) return;

            if (button.classList.contains("active")) {

                icon.classList.remove(
                    "fa-regular"
                );

                icon.classList.add(
                    "fa-solid"
                );

            } else {

                icon.classList.remove(
                    "fa-solid"
                );

                icon.classList.add(
                    "fa-regular"
                );

            }

        });

    });


    /* =========================
       CART BUTTON
    ========================= */

    const cartButton =
        document.querySelector(".cart-button");

    const cartCount =
        document.querySelector(".cart-count");

    let cartItems = 0;

    if (cartButton) {

        cartButton.addEventListener("click", () => {

            /*
             * Temporary frontend behaviour.
             * You can later connect this
             * to Django cart functionality.
             */

            console.log(
                "Cart clicked. Items:",
                cartItems
            );

        });

    }


    /* =========================
       NEWSLETTER FORM
    ========================= */

    const newsletterForm =
        document.querySelector(".newsletter-form");

    if (newsletterForm) {

        newsletterForm.addEventListener(
            "submit",
            (event) => {

                event.preventDefault();

                const emailInput =
                    newsletterForm.querySelector(
                        "input[type='email']"
                    );

                if (!emailInput) return;

                const email =
                    emailInput.value.trim();

                if (!email) return;

                /*
                 * Temporary frontend confirmation.
                 * Later connect this to Django.
                 */

                const button =
                    newsletterForm.querySelector("button");

                if (button) {

                    const originalText =
                        button.textContent;

                    button.textContent =
                        "Subscribed ✓";

                    emailInput.value = "";

                    setTimeout(() => {

                        button.textContent =
                            originalText;

                    }, 3000);

                }

            }
        );

    }


    /* =========================
       SMOOTH ANCHOR SCROLL
    ========================= */

    document
        .querySelectorAll('a[href^="#"]')
        .forEach(link => {

            link.addEventListener("click", (event) => {

                const targetId =
                    link.getAttribute("href");

                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    return;
                }

                const target =
                    document.querySelector(targetId);

                if (!target) return;

                event.preventDefault();

                const headerHeight =
                    siteHeader
                        ? siteHeader.offsetHeight
                        : 0;

                const targetPosition =
                    target.getBoundingClientRect().top +
                    window.scrollY -
                    headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: "smooth"
                });

            });

        });


    /* =========================
       IMAGE FALLBACK
    ========================= */

    const images =
        document.querySelectorAll("img");

    images.forEach(image => {

        image.addEventListener("error", () => {

            /*
             * Prevent broken images from
             * destroying the layout.
             */

            image.style.display = "none";

            const parent = image.parentElement;

            if (parent) {
                parent.classList.add("image-missing");
            }

        });

    });


    /* =========================
       HERO INDICATORS
    ========================= */

    const indicators =
        document.querySelectorAll(
            ".hero-slider-indicator .indicator"
        );

    indicators.forEach((indicator, index) => {

        indicator.addEventListener("click", () => {

            indicators.forEach(item => {
                item.classList.remove("active");
            });

            indicator.classList.add("active");

            /*
             * This is ready for a future
             * Django/database-powered hero
             * slider.
             */

            console.log(
                "Hero slide:",
                index + 1
            );

        });

    });


    /* =========================
       CURRENT YEAR
    ========================= */

    const footerYear =
        document.querySelector(
            ".footer-bottom span"
        );

    if (footerYear) {

        footerYear.textContent =
            © ${new Date().getFullYear()} ARTSASA. All rights reserved.;

    }

});