let doors = document.querySelectorAll(".door");
let doorSales = document.querySelectorAll(".door__sales");
let doorWrapper = document.querySelector(".door__wrapper");
let spinResultWrapper = document.querySelector(".spin-result-wrapper");
let orderBlock = document.querySelector("#order");
let door1 = document.getElementById("door__1");
let door2 = document.getElementById("door__2");
let door3 = document.getElementById("door__3");
let doorSale1 = document.getElementById("door__sales1");
let doorSale2 = document.getElementById("door__sales2");
let doorSale3 = document.getElementById("door__sales3");

let discount = "100%"; //
doors.forEach(function (door) {
  door.addEventListener("click", openDoor);
});

var closePopup = document.querySelector(".close-popup");
$(".pop-up-button").click(function (a) {
  $(".spin-result-wrapper").fadeOut();
  a.preventDefault();

  $(".spin-result-wrapper").fadeOut();
  var b = $("#goToForm").offset().top;
  $("body,html").animate({ scrollTop: b }, 400);
});
$(".close-popup, .pop-up-button").click(function (a) {
  $(".spin-result-wrapper").fadeOut();
  a.preventDefault();

  $(".spin-result-wrapper").fadeOut();
});

function openDoor(e) {
  e.currentTarget.classList.add("open");

  setTimeout(function () {
    spinResultWrapper.style.display = "block";
    setTimeout(function () {
      orderBlock.style.display = "block";
      doorWrapper.style.display = "none";
      document.querySelector(".door__head").style.display = "none";
      start_timer && start_timer();
    }, 3500);
  }, 1500);

  doorSales.forEach(function (sale) {
    if (door1.classList.contains("open")) {
      doorSale1.innerHTML = discount;
      // doorSale1.style.left = "12px";

      doorSale2.innerHTML = discount === "50%" ? "25%" : "50%";
      // doorSale2.style.left = "30px";

      doorSale3.innerHTML = discount === "50%" ? "10%" : "25%";
      // doorSale3.style.left = "32px";
    } else if (door2.classList.contains("open")) {
      doorSale2.innerHTML = discount;
      // doorSale2.style.left = "12px";

      doorSale1.innerHTML = discount === "50%" ? "10%" : "25%";
      // doorSale1.style.left = "32px";

      doorSale3.innerHTML = discount === "50%" ? "25%" : "50%";
      // doorSale3.style.left = "30px";
    } else if (door3.classList.contains("open")) {
      doorSale1.innerHTML = discount === "50%" ? "25%" : "50%";
      // doorSale1.style.left = "30px";

      doorSale3.innerHTML = discount;
      // doorSale3.style.left = "12px";

      doorSale2.innerHTML = discount === "50%" ? "10%" : "25%";
      // doorSale2.style.left = "32px";
    }
  });

  for (let i = 0; i < doors.length; i++) {
    if (!doors[i].classList.contains("open")) {
      setTimeout(function () {
        doors[i].classList.add("open");
      }, 2500);
    }
  }

  for (let j = 0; j < doors.length; j++) {
    doors[j].removeEventListener("click", openDoor);
  }
}

const PopUpCss = document.createElement("style");
PopUpCss.innerHTML = `
.pop-up-window {
  position: absolute;
  max-width: 400px;
  width: 85%;
  margin: 0px auto;
  background: #ffffff none repeat scroll 0% 0%;
  text-align: center;
  padding: 10px;
  padding-top: 70px;
  padding-bottom: 20px;
  border-radius: 10px;
  animation: 0.7s ease 0s normal none 1 running pop-up-appear;
  right: auto;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.close-popup {
  position: absolute;
  width: 30px;
  height: 30px;
  background-size: 100%;
  top: -40px;
  border-radius: 50%;
  -webkit-box-shadow: 0 0 10px #fff;
  box-shadow: 0 0 10px #fff;
  right: -40px;
  cursor: pointer;
}
@keyframes pop-up-appear {
  0% {
    transform: translate(-50%, -2000px);
  }
  30% {
    transform: translate(-50%, 100px);
  }
  100% {
    transform: translate(-50%, -50%);
  }
}
@media (max-width: 520px){
  .close-popup {
    right: 0 !important;
  }
}
 `;
document.head.appendChild(PopUpCss);

var time = 600;
var intr;

function start_timer() {
  intr = setInterval(tick, 1000);
}

function tick() {
  time = time - 1;
  var mins = Math.floor(time / 60);
  var secs = time - mins * 60;
  if (mins == 0 && secs == 0) {
    clearInterval(intr);
  }
  secs = secs >= 10 ? secs : "0" + secs;
  mins = mins >= 10 ? mins : "0" + mins;
  $("#min").html(mins);
  $("#sec").html(secs);
}
