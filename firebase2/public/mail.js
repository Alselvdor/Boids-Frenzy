const firebaseConfig = {
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
    const firebaseConfig = {
        apiKey: "AIzaSyDX5OB8owMnhc48mGZRaSM08oXNVJP5q2g",
        authDomain: "contactform-9d40a.firebaseapp.com",
        databaseURL: "https://contactform-9d40a-default-rtdb.firebaseio.com/",
        projectId: "contactform-9d40a",
        storageBucket: "contactform-9d40a.appspot.com",
        messagingSenderId: "1036566517724",
        appId: "1:1036566517724:web:99ba80343107eaa659a119",
        measurementId: "G-EKQBVS445R"
    };
  
  firebase.initializeApp(firebaseConfig);

const database = firebase.database();
const movementsRef = database.ref("actions");

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