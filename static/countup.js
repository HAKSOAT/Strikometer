let startDate = new Date("Nov 5, 2018 00:00:00").getTime();

function counter() {

    let currentTime = new Date().getTime();

    let timeDifference = currentTime - startDate;

    let months = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 30));
    let days = Math.floor(timeDifference % (1000 * 60 * 60 * 24 * 30) / (1000 * 60 * 60 * 24));
    let hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

    console.log(document.getElementsByClassName("counter"));

    document.querySelector(".counter").textContent = months + "M " + days + "d " + hours + "h "
  + minutes + "m " + seconds + "s ";
};

setInterval(counter, 1000)

