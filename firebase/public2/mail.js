const firebaseConfig = {
    apiKey: "AIzaSyDX5OB8owMnhc48mGZRaSM08oXNVJP5q2g",
    authDomain: "contactform-9d40a.firebaseapp.com",
    databaseURL: "https://player2-controller.firebaseio.com/",
    projectId: "contactform-9d40a",
    storageBucket: "contactform-9d40a.appspot.com",
    messagingSenderId: "1036566517724",
    appId: "1:1036566517724:web:bf34350c155bdd9259a119",
    measurementId: "G-Z20B6J3WBB"
  };
  
firebase.initializeApp(firebaseConfig);

const database = firebase.database();
const movementsRef = database.ref("movements");

document.getElementById("container").addEventListener("click", (event) => {
    const button = event.target;
    
    if (button.dataset.action === "move") {
        const direction = button.dataset.direction;
        saveMovement(direction);
    }
});

function saveMovement(direction) {
    const newMovementRef = movementsRef.push();

    newMovementRef.set({
        direction: direction,
        timestamp: firebase.database.ServerValue.TIMESTAMP
    });