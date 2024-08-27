// Wait until the HTML document is fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Select the canvas element with the class 'coveringCanvas'
    const canvas = document.querySelector('.coveringCanvas');
    // Get the 2D drawing context from the canvas
    const ctx = canvas.getContext('2d');
    // Select the image element with the class 'coveredImage'
    const img = document.querySelector('.coveredImage');

    // Set the canvas dimensions to match the image dimensions
    canvas.width = img.clientWidth; // Match the canvas width to the image width
    canvas.height = img.clientHeight; // Match the canvas height to the image height

    // Initialize variables to track drawing state and coordinates
    let isDrawing = false; // Flag to indicate if drawing is currently happening
    let startX = 0; // Starting X coordinate of the drawn box
    let startY = 0; // Starting Y coordinate of the drawn box
    let x1 = 0, y1 = 0, x2 = 0, y2 = 0; // Coordinates for the top-left (x1, y1) and bottom-right (x2, y2) corners of the box

    // Function to handle the start of drawing
    function startDrawing(e) {
        isDrawing = true; // Set drawing flag to true
        startX = e.offsetX; // Set startX to the X coordinate where the mouse is clicked
        startY = e.offsetY; // Set startY to the Y coordinate where the mouse is clicked
        x1 = startX; // Set the top-left X coordinate
        y1 = startY; // Set the top-left Y coordinate
    }

    // Function to handle the drawing (when the mouse is moved while clicked)
    function draw(e) {
        if (!isDrawing) return; // If not drawing, exit the function

        // Clear the entire canvas before redrawing
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Redraw the image on the canvas to avoid drawing over previous boxes
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        // Calculate the width and height of the box being drawn
        const width = e.offsetX - startX; // Width is the current X minus the starting X
        const height = e.offsetY - startY; // Height is the current Y minus the starting Y

        // Set the bottom-right coordinates of the box
        x2 = e.offsetX; // Set x2 to the current X coordinate
        y2 = e.offsetY; // Set y2 to the current Y coordinate

        // Draw the rectangle (box) on the canvas
        ctx.strokeStyle = 'red'; // Set the color of the box's border to red
        ctx.lineWidth = 1; // Set the thickness of the box's border to 2 pixels
        ctx.strokeRect(startX, startY, width, height); // Draw the box using the starting coordinates and calculated width/height

        // Update the displayed coordinates in HTML with six decimal places
        document.getElementById('x1').textContent = x1.toFixed(6); // Update the displayed top-left X coordinate
        document.getElementById('y1').textContent = y1.toFixed(6); // Update the displayed top-left Y coordinate
        document.getElementById('x2').textContent = x2.toFixed(6); // Update the displayed bottom-right X coordinate
        document.getElementById('y2').textContent = y2.toFixed(6); // Update the displayed bottom-right Y coordinate

        // Calculate the width and height of the box as a normalized value between 0 and 1
        const imgWidth = canvas.width; // Get the width of the image (and canvas)
        const imgHeight = canvas.height; // Get the height of the image (and canvas)

        const normWidth = Math.abs(width) / imgWidth; // Normalize the box's width relative to the image width
        const normHeight = Math.abs(height) / imgHeight; // Normalize the box's height relative to the image height

        // Calculate the center coordinates of the box, normalized to the range [0, 1]                  THIS IS CORRECT HERE, I GET CENTER OF BOX X,Y
        const centerX = ((x1 + x2) / 2) / imgWidth; // Calculate and normalize the center X coordinate
        const centerY = ((y1 + y2) / 2) / imgHeight; // Calculate and normalize the center Y coordinate

        // Display the YOLOv8 format (centerX, centerY, normWidth, normHeight) with six decimal places in HTML
        document.getElementById('centerX').textContent = centerX.toFixed(6); // Update the displayed center X coordinate
        document.getElementById('centerY').textContent = centerY.toFixed(6); // Update the displayed center Y coordinate
        document.getElementById('normWidth').textContent = normWidth.toFixed(6); // Update the displayed normalized width
        document.getElementById('normHeight').textContent = normHeight.toFixed(6); // Update the displayed normalized height

        // Log the YOLOv8 format values in the console for debugging or verification purposes
        console.log(`YOLOv8 Format: ${centerX.toFixed(6)} ${centerY.toFixed(6)} ${normWidth.toFixed(6)} ${normHeight.toFixed(6)}`); //UPDATING TO BE 1/2 h and w

        // New code to send the halfHeight to the server
        const halfHeight = normHeight / 2;

        fetch('/save-annotations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                centerX: centerX,
                centerY: centerY,
                normWidth: normWidth,
                normHeight: halfHeight
            })
        }).then(response => response.json())
        .then(data => {
            console.log('Data sent successfully:', data);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    // Function to handle the end of drawing (when the mouse is released or moved out of the canvas)
    function stopDrawing() {
        isDrawing = false; // Set the drawing flag to false, ending the drawing process
    }

    // Add event listeners to the canvas for mouse actions
    canvas.addEventListener('mousedown', startDrawing); // Start drawing when the mouse is pressed down
    canvas.addEventListener('mousemove', draw); // Draw as the mouse moves (if the drawing flag is true)
    canvas.addEventListener('mouseup', stopDrawing); // Stop drawing when the mouse button is released
    canvas.addEventListener('mouseout', stopDrawing); // Stop drawing if the mouse leaves the canvas
});
