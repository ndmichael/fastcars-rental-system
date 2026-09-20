document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const themeButtons = document.querySelectorAll("[data-theme-toggle]");
    const themeIcons = document.querySelectorAll("[data-theme-icon]");

    const getCurrentTheme = () => html.getAttribute("data-theme") || "light";

    const updateThemeIcons = (theme) => {
        themeIcons.forEach((icon) => {
            icon.className =
                theme === "dark"
                    ? "bi bi-sun"
                    : "bi bi-moon-stars";
        });

        themeButtons.forEach((button) => {
            const isDark = theme === "dark";

            button.setAttribute(
                "aria-label",
                isDark ? "Switch to light mode" : "Switch to dark mode"
            );

            button.setAttribute("aria-pressed", String(isDark));
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
            const nextTheme =
                getCurrentTheme() === "dark"
                    ? "light"
                    : "dark";

            setTheme(nextTheme);
        });
    });
});