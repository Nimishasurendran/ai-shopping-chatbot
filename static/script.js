async function send() {
  const input = document.getElementById("msg");
  const chat = document.getElementById("chat");

  if (!input.value.trim()) return;

  chat.innerHTML += `<p class="user-message"><b>You:</b> ${input.value}</p>`;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input.value })
  });

  const data = await res.json();
  chat.innerHTML += `<p class="bot-message"><b>Bot:</b> ${data.reply}</p>`;

  chat.scrollTop = chat.scrollHeight;

  input.value = "";
}


