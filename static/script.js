document.addEventListener("DOMContentLoaded", async () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    async function setupCamera() {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    }

    async function sendFrame() {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const canvasData = canvas.toDataURL("image/jpeg");

        const response = await fetch("http://localhost:5000/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: canvasData })
        });

        const result = await response.json();
        console.log(result);
    }

    await setupCamera();
    setInterval(sendFrame, 500);
});
