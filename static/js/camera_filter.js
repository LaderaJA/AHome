document.addEventListener("DOMContentLoaded", function () {
    const cameraFeed = document.getElementById("camera-feed");
    const overlayImg = document.getElementById("overlay-img");
    const designItems = document.querySelectorAll('.design-item'); 
    const captureBtn = document.getElementById("capture-btn");
    const captureCanvas = document.getElementById("capture-canvas");
    let offsetX = 0;
    let offsetY = 0;
    let scale = 1;

    // Start the camera
    async function startCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
            cameraFeed.srcObject = stream;
        } catch (err) {
            console.error("Error accessing camera:", err);
        }
    }

    // Enable gestures
    function enableGestures() {
        const hammer = new Hammer(overlayImg);
        const panSensitivity = 0.1;  
    
        hammer.add(new Hammer.Pan({ direction: Hammer.DIRECTION_ALL, threshold: 0 }));
        hammer.on("pan", (e) => {
            offsetX += e.deltaX * panSensitivity;
            offsetY += e.deltaY * panSensitivity;
    
            overlayImg.style.left = `${Math.max(0, Math.min(cameraFeed.clientWidth - overlayImg.clientWidth, offsetX))}px`;
            overlayImg.style.top = `${Math.max(0, Math.min(cameraFeed.clientHeight - overlayImg.clientHeight, offsetY))}px`;
        });
    
        hammer.add(new Hammer.Pinch());
        hammer.on("pinch", (e) => {
            scale = Math.min(Math.max(0.5, e.scale), 3); 
            overlayImg.style.transform = `scale(${scale})`;
        });
    
        overlayImg.addEventListener('panend', (e) => {
            offsetX = parseFloat(overlayImg.style.left);
            offsetY = parseFloat(overlayImg.style.top);
        });
    }
    

    // Function to capture image from video feed and overlay
    function captureImage() {
        captureCanvas.width = cameraFeed.videoWidth;
        captureCanvas.height = cameraFeed.videoHeight;

        const ctx = captureCanvas.getContext("2d");
        ctx.drawImage(cameraFeed, 0, 0, captureCanvas.width, captureCanvas.height);

        if (overlayImg.style.display !== "none") {
            ctx.drawImage(
                overlayImg,
                parseFloat(overlayImg.style.left),
                parseFloat(overlayImg.style.top),
                overlayImg.width * scale,
                overlayImg.height * scale
            ); 
        }

        const imageData = captureCanvas.toDataURL("image/png");

        sendImageToServer(imageData);
    }


    function sendImageToServer(imageData) {
        fetch("/save-captured-image/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: "image=" + encodeURIComponent(imageData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert("Image saved successfully!");
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error sending image:", error));
    }

    function getCSRFToken() {
        let csrfToken = null;
        document.cookie.split(";").forEach((cookie) => {
            let [name, value] = cookie.trim().split("=");
            if (name === "csrftoken") {
                csrfToken = value;
            }
        });
        return csrfToken;
    }

    designItems.forEach(item => {
        item.addEventListener('click', () => {
            const designSrc = item.getAttribute('data-src');
            overlayImg.src = designSrc;
            overlayImg.style.display = 'block';
            overlayImg.style.position = 'absolute';
            overlayImg.style.left = '0px'; 
            overlayImg.style.top = '0px';  
            overlayImg.style.transform = 'scale(1)'; 
            offsetX = 0;
            offsetY = 0;
            scale = 1;
            enableGestures(); 
        });
    });

 
    captureBtn.addEventListener("click", captureImage);


    startCamera();
});
