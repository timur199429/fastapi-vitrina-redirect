(function() {
    "use strict";

    function isDebugMode() {
        return new URLSearchParams(window.location.search).has("debug");
    }

    function debugLog(...args) {
        if (isDebugMode()) {
            console.debug(`[${window.name || "root"}]`, ...args);
        }
    }

    const queryParamMappings = [
        { landing: "stream_uuid", backlink: "stream_uuid" },
        { landing: "googleIdTh", backlink: "lna-surfer-uuid" },
        { landing: "googleIdTh", backlink: "surfer_uuid" },
        { landing: "thank_you_page", backlink: "thank_you_page" },
        { landing: "lf_utm_source", backlink: "utm_source" },
        { landing: "lf_utm_medium", backlink: "utm_medium" },
        { landing: "lf_utm_campaign", backlink: "utm_campaign" },
        { landing: "lf_utm_content", backlink: "utm_content" },
        { landing: "lf_utm_term", backlink: "utm_term" },
        { landing: "lf_subid1", backlink: "subid1" },
        { landing: "lf_subid2", backlink: "subid2" },
        { landing: "lf_subid3", backlink: "subid3" },
        { landing: "lf_subid4", backlink: "subid4" },
        { landing: "lf_subid5", backlink: "subid5" },
        { landing: "kit", backlink: "kit" },
        { landing: "debug", backlink: "debug" },
        { landing: "tup", backlink: "tup" }
    ];

    const prefix = "eqp_";

    function mapQueryParams(targetUrl) {
        const targetUrlObj = new URL(targetUrl);
        const currentUrlParams = new URLSearchParams(window.location.search);

        if (currentUrlParams.has("googleIdTh")) {
            debugLog("set no-trek");
            targetUrlObj.searchParams.set("no-trek", "1");
        } else {
            debugLog("set trek");
            targetUrlObj.searchParams.set("trek", "1");
        }

        queryParamMappings.forEach(mapping => {
            const value = currentUrlParams.get(mapping.landing);
            if (value) {
                targetUrlObj.searchParams.set(mapping.backlink, value);
            }
        });

        currentUrlParams.forEach((value, key) => {
            if (key.startsWith(prefix)) {
                targetUrlObj.searchParams.set(key, value);
            }
        });

        return targetUrlObj.toString();
    }

    function setFromBacklinkFlag() {
        const url = new URL(window.location.href);
        url.searchParams.set("from_backlink", "1");
        return url.toString();
    }

    function updateHistory() {
        window.history.replaceState(window.history.state, "", setFromBacklinkFlag());
    }

    const frameId = "newsFrame";

    function isFrameExists() {
        return !!window.top.frames[frameId];
    }

    const frameManager = {
        frame: document.createElement("iframe"),
        recreateFrame() {
            this.frame.remove();
            this.frame = document.createElement("iframe");
            this.frame.src = "";
        },
        hideRootPageContent() {
            debugLog("Hide root page content");
            document.body.style.overflow = "hidden";
            document.querySelectorAll(`body > *:not(#${frameId})`).forEach(element => {
                element.setAttribute("style", "display:none;");
            });
        },
        initBacklinkFrame() {
            this.recreateFrame();
            debugLog(`Init frame named '${frameId}'`);
            this.frame.id = frameId;
            this.frame.name = frameId;
            this.frame.style.width = "100%";
            this.frame.style.height = "100vh";
            this.frame.style.position = "fixed";
            this.frame.style.top = "0";
            this.frame.style.left = "0";
            this.frame.style.border = "none";
            this.frame.style.zIndex = "-1";
            this.frame.style.display = "block";
            this.frame.style.opacity = "0";
            this.frame.style.backgroundColor = "#fff";
            this.frame.src = "";
            document.body.append(this.frame);
            this.frame.onload = () => frameManager.setVisibility("show");
        },
        setVisibility(visibility) {
            const opacity = visibility === "hide" ? "0" : "1";
            const zIndex = visibility === "hide" ? "-1" : "999997";
            this.frame.style.opacity = opacity;
            this.frame.style.zIndex = zIndex;
        },
        setFrameUrl(url) {
            this.frame.src = url;
        }
    };

    const operations = {
        UPDATE_BACKLINK_OPTIONS: 0
    };

    function serialize(data) {
        return JSON.stringify(data);
    }

    function deserialize(data) {
        try {
            const parsed = JSON.parse(data);
            if (typeof parsed !== "object" || !Object.keys(parsed).includes("operation") || !Object.keys(operations).includes(parsed.operation.toString())) {
                throw new Error;
            }
            return parsed;
        } catch {
            return null;
        }
    }

    function sendMessage(data) {
        window.parent.postMessage(serialize(data), "*");
    }

    function listenForMessages(callback, target) {
        function handler(event) {
            const data = deserialize(event.data);
            if (data) {
                callback(data);
            }
        }
        target.addEventListener("message", handler);
        return () => target.removeEventListener("message", handler);
    }

    function updateBacklinkOptions(options) {
        if (options.sendInitMessages) {
            sendMessage({ operation: operations.UPDATE_BACKLINK_OPTIONS, payload: options });
        }
    }

    const historyStateName = "NOVOSTI24";
    const historyItemsCount = 1;

    const historyManager = {
        _timeout: null,
        forward() {
            if (this._timeout) {
                clearTimeout(this._timeout);
            }
            this._timeout = setTimeout(() => window.history.forward());
        }
    };

    function addToHistory() {
        try {
            debugLog(`Add to history ${historyItemsCount.toString()} items`);
            const state = { eventStateName: historyStateName, origin: window.location.href };
            for (let i = 0; i < historyItemsCount; ++i) {
                window.history.pushState(state, "", state.origin);
            }
        } catch (error) {
            console.warn(error);
        }
    }

    const backlinkOptions = {
        url: location.href
    };

    function configureBacklink(options) {
        if (options.url !== undefined) {
            backlinkOptions.url = options.url;
        }
        if (options.mapQueryParams !== undefined) {
            backlinkOptions.mapQueryParams = options.mapQueryParams;
        }
        if (options.registerBacklink !== undefined) {
            backlinkOptions.registerBacklink = options.registerBacklink;
        }
    }

    function handlePopstate() {
        window.onpopstate = handleFirstPopstate;
        addToHistory();
    }

    function handleFirstPopstate(event) {
        event.preventDefault();
        debugLog("On first popstate");
        window.onpopstate = handleSubsequentPopstate;
        frameManager.hideRootPageContent();
        handleSubsequentPopstate(event);
    }

    function handleSubsequentPopstate(event) {
        event.preventDefault();
        debugLog("Stub popstate handler");
        if (backlinkOptions.registerBacklink) {
            updateHistory();
        }
        window.onpopstate = handleSubsequentPopstate;
    }

    function getMappedUrl(url) {
        if (!backlinkOptions.mapQueryParams) {
            return url;
        }
        const mappedUrl = mapQueryParams(url);
        debugLog(`Mapped url = ${mappedUrl}`);
        return mappedUrl;
    }

    function handleBacklink(event) {
        event.preventDefault();
        window.onpopstate = handleSubsequentPopstate;
        const url = getMappedUrl(backlinkOptions.url || window.location.href);
        debugLog(`History length is ${window.history.length.toString()}`);
        debugLog(`Back to ${url}`);
        frameManager.initBacklinkFrame();
        frameManager.setFrameUrl(url);
        historyManager.forward();
    }

    function initializeBacklink(options) {
        configureBacklink(options);
        window.onpopstate = handleFirstPopstate;
        listenForMessages(({ operation, payload }) => {
            switch (operation) {
                case operations.UPDATE_BACKLINK_OPTIONS:
                    configureBacklink(payload);
                    break;
            }
        }, window);
    }

    function triggerBacklink(trigger) {
        const triggerHandler = () => {
            debugLog(`Trigger = ${trigger}`);
            handlePopstate();
        };
        switch (trigger) {
            case "timeout":
                setTimeout(triggerHandler, 1500);
                break;
            case "init":
                triggerHandler();
                break;
            default:
                window.addEventListener(trigger, triggerHandler, { once: true });
        }
    }

    function initBacklink(url, mapQueryParams = true, registerBacklink = false) {
        const isFrameExist = isFrameExists();
        if (!isFrameExist) {
            initializeBacklink({ url, mapQueryParams, registerBacklink });
            debugLog("Init master backlink");
            ["init", "timeout", "click", "touchstart", "scroll"].forEach(triggerBacklink);
        }
        updateBacklinkOptions({ url, sendInitMessages: isFrameExist, registerBacklink, mapQueryParams });
        debugLog("Init slave backlink");
    }

    window.initBacklink = initBacklink;
})();