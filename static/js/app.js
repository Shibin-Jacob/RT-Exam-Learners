let time = 30;

function formatTime(t) {
    let sec = t < 10 ? "0" + t : t;
    return "00:" + sec;
}

const timerEl = document.getElementById("timer");
const form = document.getElementById("quizForm");

if (timerEl && form) {

    timerEl.innerText = formatTime(time);

    let countdown = setInterval(() => {
        time--;

        timerEl.innerText = formatTime(time);

        if (time <= 10) {
            timerEl.style.color = "#dc2626";
            document.querySelector(".timer-box").style.borderColor = "#dc2626";
        }

        if (time <= 0) {
            clearInterval(countdown);
            form.submit();
        }

    }, 1000);
}


// ==========================
// OPTION SELECTION UX
// ==========================
document.querySelectorAll(".option").forEach(opt => {
    opt.addEventListener("click", () => {
        document.querySelectorAll(".option").forEach(o => {
            o.classList.remove("selected");
        });

        opt.classList.add("selected");
    });
});


// ==========================
// KEYBOARD SHORTCUTS
// ==========================
document.addEventListener("keydown", (e) => {
    if (e.key >= "1" && e.key <= "3") {
        let inputs = document.querySelectorAll("input[name='answer']");
        inputs[e.key - 1].checked = true;

        inputs[e.key - 1].closest(".option").click();
    }

    if (e.key === "Enter") {
        if (form) form.submit();
    }
});