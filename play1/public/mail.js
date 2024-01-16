// Import the functions you need from the SDKs you need
import { getDatabase, ref, push } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";

// Get a reference to the database
const database = getDatabase();

document.getElementById("container").addEventListener("click", (event) => {
    const button = event.target;

    if (button.dataset.action === "move") {
        const direction = button.dataset.direction;
        saveMovement(direction);
    }
});

function saveMovement(direction) {
    // Reference to the 'movements' node in the database
    const movementsRef = ref(database, 'movements');

    // Push a new movement to the 'movements' node
    push(movementsRef, {
        direction: direction,
        timestamp: firebase.database.ServerValue.TIMESTAMP
    });

    console.log("Command Sent:", direction);
}
