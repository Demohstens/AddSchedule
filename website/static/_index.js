let left = document.getElementById("#left")
let middle = document.getElementById("#middle")
let right = document.getElementById("#right")
const draggables = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll(".container")

draggables.forEach(draggable => {
    draggable.addEventListener("dragstart", () => {
        draggable.classList.add("dragging")
    })

    draggable.addEventListener("dragend", () => {
        draggable.classList.remove("dragging")
    })
});

containers.forEach(container => {
    container.addEventListener("dragover", e => {
        e.preventDefault()
        const aferElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')
        if (aferElement == null) {
            container.appendChild(draggable)
        } else {
            container.insertBefore(draggable, aferElement)
        }

    })
    
})

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top -box.height / 2
        if (offset < 0 && offset > closest.offset){
            return {offset: offset, element: child}
        }
        else {
            return closest
        }
    }, {offset: Number.NEGATIVE_INFINITY, element: null}).element;
}

function getTotalHeight(container) {
    let totalHeight = 0;
    container.childNodes.forEach(child => {
        if (child.nodeType === 1) { // Check if it's an element node
            totalHeight += child.offsetHeight; // or clientHeight for the visible height excluding padding
        }
    });
    return totalHeight;
}
