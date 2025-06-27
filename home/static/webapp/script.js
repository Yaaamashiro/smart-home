document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("ir-modal");
  const closeBtn = document.querySelector(".close");

  document.getElementById("btn-register-ir").onclick = () => {
    modal.style.display = "block";
  };

  closeBtn.onclick = () => {
    modal.style.display = "none";
  };

  window.onclick = (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };

  document.getElementById("ir-recv-btn").onclick = () => {
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
        alert(data.status === "ok" ? "登録成功！" : `失敗：${data.message}`);
        if (data.status === "ok") {
          modal.style.display = "none";
          location.reload();
        }
      });
  };

  document.querySelectorAll(".send-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;
      sendSignal(id);
    });
  });

  function sendSignal(id) {
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
        alert(
          data.status === "ok" ? "送信成功！" : `送信失敗：${data.message}`
        );
      });
  }

  function getCsrfToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }
});
