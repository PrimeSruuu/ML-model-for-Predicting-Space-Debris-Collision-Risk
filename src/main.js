// Replace 'YOUR_CESIUM_ION_TOKEN' with your real token
Cesium.Ion.defaultAccessToken = 'YOUR_CESIUM_ION_TOKEN';

// Initialize Cesium Viewer
const viewer = new Cesium.Viewer('cesiumContainer', {
    animation: false,  // Remove timeline
    timeline: false,   // Remove Cesium's default timeline
    fullscreenButton: false, 
    sceneModePicker: false, 
    baseLayerPicker: false,
    homeButton: false, 
    geocoder: false, 
    navigationHelpButton: false,
    infoBox: false, 
    selectionIndicator: false
});

// Optional: Set space-like background
viewer.scene.globe.baseColor = Cesium.Color.BLACK;

// Remove Cesium logo watermark
viewer.cesiumWidget.creditContainer.style.display = "none";

// Zoom to Earth
viewer.camera.setView({
    destination: Cesium.Cartesian3.fromDegrees(0, 0, 20000000) // Adjust zoom level
});
