(function() {
    "use strict";

    // Функция для логирования (если включен режим отладки)
    function debugLog(...args) {
        if (new URLSearchParams(window.location.search).has("debug")) {
            console.debug("[Backbutton Redirect]", ...args);
        }
    }

    // Функция для предзагрузки страницы редиректа
    function preloadRedirectPage(url) {
        return new Promise((resolve, reject) => {
            const iframe = document.createElement("iframe");
            iframe.style.display = "none"; // Скрываем iframe
            iframe.src = url; // Указываем URL для предзагрузки

            // Обработчик успешной загрузки iframe
            iframe.onload = () => {
                debugLog(`Redirect page preloaded: ${url}`);
                resolve(iframe);
            };

            // Обработчик ошибок загрузки iframe
            iframe.onerror = () => {
                debugLog(`Failed to preload redirect page: ${url}`);
                reject(new Error("Failed to preload redirect page"));
            };

            document.body.appendChild(iframe); // Добавляем iframe на страницу
        });
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

        // Дополнительный обработчик для случаев, когда popstate не срабатывает
        window.addEventListener("pageshow", (event) => {
            if (event.persisted) { // Страница загружена из кэша
                debugLog("Page loaded from cache. Redirecting...");
                redirectTo(targetUrl);
            }
        });
    }

    // Инициализация скрипта
    async function initBackbuttonRedirect(options) {
        const { redirectUrl, debug } = options;

        if (debug) {
            debugLog("Debug mode enabled");
        }

        if (!redirectUrl) {
            console.error("Redirect URL is required.");
            return;
        }

        debugLog("Initializing backbutton redirect...");

        try {
            // Предзагрузка страницы редиректа
            await preloadRedirectPage(redirectUrl);

            // Обработка кнопки "Назад"
            handleBackButton(redirectUrl);
        } catch (error) {
            console.error("Backbutton redirect initialization failed:", error);
        }
    }

    // Экспортируем функцию инициализации в глобальную область видимости
    window.initBackbuttonRedirect = initBackbuttonRedirect;
})();