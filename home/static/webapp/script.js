document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("ir-modal");
  const closeBtn = document.querySelector(".close");

  // 「IR登録」ボタンでモーダル表示
  document.getElementById("btn-register-ir").onclick = () => {
    modal.style.display = "block";
  };

  // モーダルの×ボタン
  closeBtn.onclick = () => {
    modal.style.display = "none";
  };

  // モーダル外クリックで閉じる
  window.onclick = (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };

  // IR受信・登録ボタンが押されたとき
  document.getElementById("ir-recv-btn").onclick = () => {
    const name = document.getElementById("ir-name").value;
    fetch("/register_ir/", {
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

  // 送信ボタンたちにイベント付与
  document.querySelectorAll(".send-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id; // data-id="IR1" などがHTMLに必要
      sendSignal(id);
    });
  });

  function sendSignal(id) {
    fetch("/send_ir/", {
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
