document.addEventListener("DOMContentLoaded", () => {
    /*
     * Theme
     */

    const html = document.documentElement;
    const themeButtons = document.querySelectorAll("[data-theme-toggle]");
    const themeIcons = document.querySelectorAll("[data-theme-icon]");

    const getCurrentTheme = () => {
        return html.getAttribute("data-theme") || "light";
    };

    const updateThemeIcons = (theme) => {
        themeIcons.forEach((icon) => {
            icon.className = theme === "dark"
                ? "bi bi-sun"
                : "bi bi-moon-stars";
        });

        themeButtons.forEach((button) => {
            const isDark = theme === "dark";

            button.setAttribute(
                "aria-label",
                isDark ? "Switch to light mode" : "Switch to dark mode"
            );

            button.setAttribute(
                "aria-pressed",
                String(isDark)
            );
        });
    };

    const setTheme = (theme) => {
        html.setAttribute("data-theme", theme);
        localStorage.setItem("fastcars-theme", theme);
        updateThemeIcons(theme);
    };

    updateThemeIcons(getCurrentTheme());

    themeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            setTheme(
                getCurrentTheme() === "dark"
                    ? "light"
                    : "dark"
            );
        });
    });


    /*
     * Booking availability
     */

    const bookingForm = document.getElementById("bookingForm");

    if (!bookingForm) {
        return;
    }

    const pickupInput = document.getElementById("pickup_date");
    const returnInput = document.getElementById("return_date");
    const checkButton = document.getElementById("checkAvailabilityButton");
    const submitButton = document.getElementById("submitBookingButton");
    const summary = document.getElementById("bookingSummary");
    const result = document.getElementById("availabilityResult");
    const loginNotice = document.getElementById("loginNotice");

    const summaryDays = document.getElementById("summaryDays");
    const summaryRate = document.getElementById("summaryRate");
    const summaryTotal = document.getElementById("summaryTotal");

    const getToday = () => {
        const date = new Date();
        const offset = date.getTimezoneOffset();

        date.setMinutes(date.getMinutes() - offset);

        return date.toISOString().split("T")[0];
    };

    pickupInput.min = getToday();
    returnInput.min = getToday();

    pickupInput.addEventListener("change", () => {
        returnInput.min = pickupInput.value || getToday();

        summary.classList.add("d-none");
        result.className = "fc-booking-result d-none";

        if (submitButton) {
            submitButton.classList.add("d-none");
        }

        if (loginNotice) {
            loginNotice.classList.add("d-none");
        }
    });

    returnInput.addEventListener("change", () => {
        summary.classList.add("d-none");
        result.className = "fc-booking-result d-none";

        if (submitButton) {
            submitButton.classList.add("d-none");
        }

        if (loginNotice) {
            loginNotice.classList.add("d-none");
        }
    });

    const clearErrors = () => {
        document
            .querySelectorAll(".fc-form-error")
            .forEach((element) => {
                element.textContent = "";
            });

        pickupInput.classList.remove("is-invalid");
        returnInput.classList.remove("is-invalid");
    };

    const showErrors = (errors) => {
        Object.entries(errors).forEach(([field, messages]) => {
            const errorElement = document.querySelector(
                `[data-error="${field}"]`
            );

            const input = document.getElementById(field);

            if (errorElement) {
                errorElement.textContent = messages[0];
            }

            if (input) {
                input.classList.add("is-invalid");
            }
        });
    };

    const formatCurrency = (amount) => {
        return Number(amount).toLocaleString("en-NG", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        });
    };

    checkButton.addEventListener("click", async () => {
        clearErrors();

        const pickupDate = pickupInput.value;
        const returnDate = returnInput.value;

        if (!pickupDate || !returnDate) {
            showErrors({
                pickup_date: pickupDate
                    ? []
                    : ["Pick-up date is required."],
                return_date: returnDate
                    ? []
                    : ["Return date is required."],
            });

            return;
        }

        const availabilityUrl =
            bookingForm.dataset.availabilityUrl;

        const params = new URLSearchParams({
            pickup_date: pickupDate,
            return_date: returnDate,
        });

        checkButton.disabled = true;
        checkButton.innerHTML = `
            Checking availability
            <span class="spinner-border spinner-border-sm ms-2"
                  aria-hidden="true"></span>
        `;

        result.className = "fc-booking-result d-none";
        summary.classList.add("d-none");

        try {
            const response = await fetch(
                `${availabilityUrl}?${params.toString()}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                }
            );

            const data = await response.json();

            if (!response.ok) {
                result.className = "fc-booking-result unavailable";
                result.innerHTML = `
                    <i class="bi bi-exclamation-circle"></i>
                    <span>
                        ${data.message || "Please check your selected dates."}
                    </span>
                `;

                showErrors(data.errors || {});
                return;
            }

            if (!data.available) {
                result.className = "fc-booking-result unavailable";
                result.innerHTML = `
                    <i class="bi bi-x-circle"></i>
                    <span>
                        This vehicle is not available for those dates.
                    </span>
                `;

                return;
            }

            result.className = "fc-booking-result available";
            result.innerHTML = `
                <i class="bi bi-check-circle"></i>
                <span>${data.message}</span>
            `;

            summaryDays.textContent = data.rental_days;
            summaryRate.textContent = formatCurrency(data.daily_rate);
            summaryTotal.textContent = formatCurrency(data.total_amount);

            summary.classList.remove("d-none");

            if (submitButton) {
                submitButton.classList.remove("d-none");
            } else if (loginNotice) {
                loginNotice.classList.remove("d-none");
            }

        } catch (error) {
            result.className = "fc-booking-result unavailable";
            result.innerHTML = `
                <i class="bi bi-exclamation-triangle"></i>
                <span>
                    Something went wrong while checking availability.
                </span>
            `;
        } finally {
            checkButton.disabled = false;
            checkButton.innerHTML = `
                Check Availability
                <i class="bi bi-arrow-right ms-2"></i>
            `;
        }
    });
});