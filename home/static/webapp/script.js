document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("ir-modal");

  document.getElementById("btn-ir-register").onclick = () => {
    modal.style.display = "block";
  };

  window.onclick = (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };

  document.getElementById("btn-ir-receive-register").onclick = () => {
    const name = document.getElementById("ir-name").value;
    fetch("/post_register_ir/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCsrfToken(),
      },
      body: `name=${encodeURIComponent(name)}`,
    })
      .then((res) => res.json())
      .then((data) => {
        alert(
          data.status === "ok"
            ? "Successful register!"
            : `ERROR：${data.message}`
        );
        if (data.status === "ok") {
          modal.style.display = "none";
          location.reload();
        }
      });
  };

  document.querySelectorAll(".btn-ir-send").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;
      fetch("/post_send_ir/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({ id: id }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status !== "ok") {
            alert(`ERROR：${data.message}`);
          }
        });
    });
  });

  function getCsrfToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }
});
