function getUrlParams() {
  return window.location.search
    .replace("?", "")
    .split("&")
    .reduce(function (p, e) {
      var a = e.split("=");
      p[decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
      return p;
    }, {});
}
const urlParams = getUrlParams();

function buttonSend(formId, _offer) {
  window.addEventListener("pageshow", () => {
    document.querySelector(`${formId} [type="submit"]`).style.display = "";
    document
      .querySelector(`${formId} [type="submit"]`)
      .removeAttribute("disabled", "");
    document.querySelector(`${formId} .ring-loading`).style.display = "none";
  });
  const languagePage = document
    .getElementsByTagName("html")[0]
    .getAttribute("lang")
    ? document
        .getElementsByTagName("html")[0]
        .getAttribute("lang")
        .toLowerCase()
    : "";

  let confirm = _offer
    ? _offer === "infolder"
      ? "confirm/success.php"
      : `/systems/confirm/special/${_offer.toLowerCase()}/${languagePage}/confirm/success.php`
    : `/systems/confirm/ordinary/${languagePage}/confirm/success.php`;

  let forma = document.querySelector(formId);
  localStorage.setItem(
    "hiddenValue",
    JSON.stringify(
      [...forma.querySelectorAll("input[type=hidden]")].reduce((aggr, inp) => {
        aggr[inp.name] = inp.value;
        return aggr;
      }, {})
    )
  );

  let backLink = window.location.origin + window.location.pathname;

  let baseUrl = window.location.host + window.location.pathname;
  forma
    .querySelector('[type="submit"]')
    .addEventListener("click", function (event) {
      if (
        forma.querySelector('[name="name"]').value.length > 1 &&
        forma.querySelector('[name="phone"]').value.length > 7
      ) {
        document.querySelector(`${formId} [type="submit"]`).style.display =
          "none";
        document.querySelector(`${formId} [type="submit"]`).setAttribute('disabled', '');
        document.querySelector(`${formId} .ring-loading`).style.display =
          "block";

        let formData = {
          name: forma.querySelector("input[name=name]").value,
          phone: forma.querySelector("input[name=phone]").value,
          country: urlParams["country"] ?? "",
          utm_source: forma.querySelector("input[name=utm_source]").value,
          utm_term: forma.querySelector("input[name=utm_term]").value,
          subid: forma.querySelector("input[name=subid]").value,
          subid1: forma.querySelector("input[name=subid1]").value,
          subid4: '{"url_landing":"' + baseUrl + '"}',
          subid3: forma.querySelector("input[name=subid3]").value,
          t_id: forma.querySelector("input[name=t_id]").value,
          hash: urlParams["hash"] ?? "",
          user_ip: urlParams["user_ip"] ?? "",
          comment: forma.querySelector("input[name=comment]")?.value ?? "",
          subid5: forma.querySelector("input[name=name]").value,
          subid6: forma.querySelector("input[name=phone]").value,
        };
        fetch(
          `/systems/19f0984d75307b0a07a12e277cabd3a5/order.php`,
          {
            method: "POST",
            body: JSON.stringify(formData),
            headers: {
              "Content-Type":
                "application/x-www-form-urlencoded; charset=UTF-8",
            },
          }
        )
          .then((response) => response.json())
          .then((data) => {
            let response = Object.values(data);
            if (
              response[0] === "success" &&
              window.location.href.includes(`thank_you_page`)
            ) {
              async function getThankpageUrl() {
                let targetLink = "";
                const loc = window.location.search;
                const params = loc.slice(1).split("&");

                const paramsObject = params.reduce((res, item) => {
                  const [key, value] = item.split("=");
                  return {
                    ...res,
                    [key]: value,
                  };
                }, {});

                let pageId = paramsObject.thank_you_page;
                if (pageId) {
                  let arr = [+pageId];
                  if (!isNaN(arr)) {
                    console.log("not local");
                    try {
                      let res = await fetch(
                        `https://${window.showcaseUrl}/v1/.api/v1/thank-you-page/${pageId}`
                      );
                      res = await res.json();

                      if (res.data && res.data.url) targetLink = res.data.url;
                      console.log(res.data.url);
                    } catch (e) {
                      console.log(e);
                    }
                  } else {
                    console.log("local");
                    window.location.assign(
                      confirm +
                        window.location.search +
                        `&name=${formData.name}&phone=${formData.phone}&backLink=${backLink}`
                    );
                  }
                } else if (pageId === "") {
                  window.location.assign(
                    confirm +
                      window.location.search +
                      `&name=${formData.name}&phone=${formData.phone}&backLink=${backLink}`
                  );
                }

                return targetLink;
              }

              getThankpageUrl().then((res) => {
                let targetThankYouLink = res;
                let isUserThankYouPage = targetThankYouLink.length > 0;

                const loc = window.location.search;

                let formName, formPhone;
                let nameSubmit, phoneSubmit;

                formName = document.querySelectorAll('[name="name"]');
                formPhone = document.querySelectorAll('[name="phone"]');
                formName.forEach((name) => {
                  if (name.value.length >= 2) {
                    nameSubmit = name.value;
                  }
                });
                formPhone.forEach((phone) => {
                  if (phone.value.length >= 8) {
                    phoneSubmit = phone.value;
                  }
                });

                if (isUserThankYouPage) {
                  let endsWithSlash =
                    targetThankYouLink[targetThankYouLink.length - 1] === "/";
                  // targetThankYouLink += endsWithSlash ? '?' : '/?'
                  targetThankYouLink += `${loc}&name=${nameSubmit}&phone=${phoneSubmit}`;

                  console.log(targetThankYouLink);
                  if (window.location.href.includes("tup=1")) {
                    window.open(
                      confirm +
                        window.location.search +
                        `&name=${formData.name}&phone=${formData.phone}&backLink=${backLink}`,
                      "_blank"
                    );
                    window.location.assign(targetThankYouLink);
                  } else {
                    window.location.assign(targetThankYouLink);
                  }
                }
              });
            } else if (response[0] !== "success") {
              window.location.assign(
                `/systems/confirm/ordinary/error/error.php`+ window.location.search + `&backLink=${backLink}`
              );
            } else {
              let formName, formPhone;
              let nameSubmit, phoneSubmit;
              formName = document.querySelectorAll('[name="name"]');
              formPhone = document.querySelectorAll('[name="phone"]');
              formName.forEach((name) => {
                if (name.value.length >= 2) {
                  nameSubmit = name.value;
                }
              });
              formPhone.forEach((phone) => {
                if (phone.value.length >= 8) {
                  phoneSubmit = phone.value;
                }
              });

              window.location.assign(
                confirm +
                  window.location.search +
                  `&name=${formData.name}&phone=${formData.phone}&backLink=${backLink}`
              );
            }
          });
        event.preventDefault();
      }
    });
}

document.querySelectorAll('[name="name"]').forEach((name) => {
  name.addEventListener("textInput", (evt) => {
    let char = evt.data;
    let keyCode = char.charCodeAt(0);
    if (
      (keyCode === 32 && evt.target.selectionStart === 0) ||
      (evt.target.selectionStart === 0 && evt.code === "Space")
    ) {
      evt.preventDefault();
      return false;
    }
  });
});
document.querySelectorAll('[name="phone"]').forEach((phone) => {
  phone.addEventListener("input", function () {
    if (this.value.match(/[^0-9+]/g)) {
      this.value = this.value.replace(/[^0-9+]/g, "");
    }
  });
});
