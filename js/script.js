document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // MOBILE MENU
    // =========================

    const menuToggle = document.querySelector(".menu-toggle");
    const mainNav = document.querySelector(".main-nav");

    if (menuToggle && mainNav) {

        menuToggle.addEventListener("click", function () {

            mainNav.classList.toggle("active");

            const isOpen = mainNav.classList.contains("active");

            menuToggle.setAttribute("aria-expanded", isOpen);
            menuToggle.textContent = isOpen ? "✕" : "☰";

        });


        // Close menu after clicking a navigation link
        const navLinks = document.querySelectorAll(".main-nav a");

        navLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                mainNav.classList.remove("active");

                menuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                menuToggle.textContent = "☰";

            });

        });

    }


    // =========================
    // PACKAGE SELECTION
    // =========================

    const packageButtons =
        document.querySelectorAll(".package-request");

    const serviceSelect =
        document.getElementById("serviceSelect");

    const contactSection =
        document.getElementById("contact");


    packageButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            event.preventDefault();

            const selectedPackage =
                this.getAttribute("data-package");

            console.log(
                "Selected package:",
                selectedPackage
            );


            if (serviceSelect) {

                serviceSelect.value =
                    selectedPackage;

                serviceSelect.dispatchEvent(
                    new Event("change")
                );

            }


            if (contactSection) {

                contactSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    // =========================
    // QUOTE FORM
    // =========================

    const quoteForm =
        document.getElementById("quoteForm");


    if (quoteForm) {

        quoteForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const name =
                    quoteForm.elements["name"].value;

                const email =
                    quoteForm.elements["email"].value;

                const phone =
                    quoteForm.elements["phone"].value;

                const service =
                    quoteForm.elements["service"].value;

                const message =
                    quoteForm.elements["message"].value;


                const whatsappMessage =
`Hello EdVance Tech,

I would like to request a quote.

Name: ${name}
Email: ${email}
Phone: ${phone}
Service: ${service}

Project Details:
${message}`;


                const whatsappURL =
                    "https://wa.me/27733141222?text=" +
                    encodeURIComponent(
                        whatsappMessage
                    );


                window.location.href =
                    whatsappURL;

            }
        );

    }

});