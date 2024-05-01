// Sample data (replace with your actual data)
const scheduleItems = [
    { start: "1:00", end: "5:00", title: "Task 5" },
    // Add more tasks as needed
];

// Function to create task elements
function createTaskElement(task) {
    const taskElement = document.createElement('div');
    taskElement.classList.add('task');
    taskElement.classList.add("2023-12-12")
    taskElement.textContent = task.title;
    return taskElement;
}

// Function to render tasks on the schedule
function renderTasks() {
    const tasksContainers = document.querySelectorAll(".schedule");
    tasksContainers.forEach(tasksContainer => {
        tasks.forEach(task => {
            const taskElement = createTaskElement(task);
            tasksContainer.appendChild(taskElement);
            wrap_a(taskElement);
        });
    });
}
function wrap_a(element) {
    const dateFormatRegex = /^\d{4}-\d{2}-\d{2}$/;
    element.classList.forEach((className) => {
        if (dateFormatRegex.test(className)) {
            var wrapper = document.createElement("a");
            wrapper.href = className;
            element.parentNode.insertBefore(wrapper, element);
            wrapper.appendChild(element);
        }
    });
}


renderTasks();
window.onload = () => {
    renderTasks()
}
