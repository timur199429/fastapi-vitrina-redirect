(function() {
    "use strict";

    // Функция для логирования (если включен режим отладки)
    function debugLog(...args) {
        if (new URLSearchParams(window.location.search).has("debug")) {
            console.debug("[Backbutton Redirect]", ...args);
        }
    }

    // Функция для перенаправления на указанный URL
    function redirectTo(url) {
        debugLog(`Redirecting to: ${url}`);
        window.location.href = url;
    }

    // Функция для обработки нажатия кнопки "Назад"
    function handleBackButton(targetUrl) {
        // Добавляем состояние в историю браузера
        window.history.pushState({ redirected: true }, "", window.location.href);

        // Обработчик события popstate (срабатывает при нажатии кнопки "Назад")
        window.onpopstate = function(event) {
            if (event.state && event.state.redirected) {
                debugLog("Back button pressed. Redirecting...");
                redirectTo(targetUrl);
            }
        };
    }

    // Инициализация скрипта
    function initBackbuttonRedirect(options) {
        const { redirectUrl, debug } = options;

        if (debug) {
            debugLog("Debug mode enabled");
        }

        if (!redirectUrl) {
            console.error("Redirect URL is required.");
            return;
        }

        debugLog("Initializing backbutton redirect...");
        handleBackButton(redirectUrl);
    }

    // Экспортируем функцию инициализации в глобальную область видимости
    window.initBackbuttonRedirect = initBackbuttonRedirect;
})();