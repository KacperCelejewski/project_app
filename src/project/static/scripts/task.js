
function showDetails(id){
    let detailId = `det${id}`
    const detail = document.getElementById(`${detailId}`)
    detail.classList.remove("isHidden")
    detail.classList.add("isActivated")

}

function hideDetails(id){
    let detailId = `det${id}`
    const detail = document.getElementById(`${detailId}`)
    detail.classList.add("isHidden")
    detail.classList.remove("isActivated")
}
function dropdown(id){
   const menu =  document.getElementById(`menu${id}`);
   menu.classList.toggle("show")
    window.onclick = function(event){
        if (!event.target.matches(`#dropDots${id}`) ){
            const dropdowns = document.getElementsByClassName("dropdown-content");
            let i;
            for (i = 0; i < dropdowns.length; i++) {
              const openDropdown = dropdowns[i];
              if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
              }



    }}
}}
function changeStatus(option, id) {
    const current_status = document.getElementById(`status${id}`);
    let newStatus = current_status;
    
    if (option === "completed") {
        newStatus = 'Completed';
    } else if (option === "delete") {
        newStatus = 'Cancelled';
    } else if (option === "edit") {
        
        const editWindow = document.getElementById(`projectEditWindow${id}`);
        editWindow.classList.remove("hidden");
        editWindow.classList.add("visible");
        localStorage.setItem(`projectEditWindowVisible${id}`, 'true');
        return
        }
     else if (option === "addMember") {

        const addMemberWindow = document.getElementById(`AddMemberWindow${id}`);
        addMemberWindow.classList.remove("hidden");
        addMemberWindow.classList.add("visible");
        localStorage.setItem(`addMemberWindowVisible${id}`, 'true');
        return
     }
fetch(`/change_status/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ newStatus: newStatus }),
    })
    
    .then(response => response.json())
    .then(data => {
        console.log('Status changed:', data);
        
    })
    .catch(error => {
        console.error('Error:ten', error);
    });


}
function sortTable() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.querySelector("table");
    switching = true;
    
    while (switching) {
      switching = false;
      rows = table.rows;
      
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[0];
        y = rows[i + 1].getElementsByTagName("TD")[0];
        

        
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
      
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
}
// Funkcja stayAfterLoad(id) będzie wywoływana, gdy strona jest załadowana
function stayAfterLoad(id, localStorageKey,windowToDisplay ){
    // Sprawdź, czy okno edycji projektu powinno być widoczne
    const isVisible = localStorage.getItem(`${localStorageKey}${id}`);
    
    if (isVisible === 'true') {
        const editWindow = document.getElementById(`${windowToDisplay}${id}`);
        editWindow.classList.add("visible");
        editWindow.classList.remove("hidden");
    }
}

// Funkcja closeEdit(id) będzie wywoływana, gdy chcesz zamknąć okno edycji
function closeEdit(id,windowToClose) {
    const window = document.getElementById(`${windowToClose}`);
    window.classList.add("hidden");
}

// Poniższy fragment kodu przypisuje funkcje do elementów HTML po załadowaniu strony
document.addEventListener("DOMContentLoaded", function () {
    const editLinks = document.querySelectorAll("[id^='edit'], #addMember");
    editLinks.forEach((link) => {

        // Dodaj nasłuchiwanie na kliknięcie przycisku Edit
        link.addEventListener("click", function(event) {
            event.preventDefault(); // Zapobiegnij domyślnej akcji linku
            // Wywołaj funkcję changeStatus z odpowiednimi parametrami
            // stayAfterLoad(id); // Wywołaj funkcję stayAfterLoad dla tego okna
        });
    });
});

function filterBy(button){
    
    
    const filterId = button.getAttribute("id");
    
        button.classList.toggle("hightlighted")
        const rest = document.querySelectorAll(".filters")
        rest.forEach((btn) => {
            if ( btn.getAttribute("id")!=filterId){
                btn.classList.remove("hightlighted")
            }
        })
        console.log(filterId)
        if( button.classList.contains("hightlighted")) {
        const status =  document.querySelectorAll(".status")
        for (let t of status)
        {  let row = t.closest("tr")
        if (row){
            row.classList.remove("hidden")
        }
        else{
            console.log("chuj")
        }
        }
      
        if (filterId === "Completed") {
            for (let x of status) {
                if (x.textContent !== "Completed") {
                    let row = x.closest("tr");
                    if (row) {
                        row.classList.add("hidden");
                    }
                }
            }
        }
    
        else if (filterId === "In Progress") {
            for (let x of status) {
                if (x.textContent !== "In Progress") {
                    let row = x.closest("tr");
                    if (row) {
                        row.classList.add("hidden");
                    }
                }
            }
        }
        else if (filterId === "Cancelled") {
            
            for (let x of status) {
                
                if (x.textContent !== "Cancelled") {
                    
                    let row = x.closest("tr")
                    if (row) {
                        row.classList.add("hidden");
                    }
                 
                }
            }
        }
        else if (filterId === "Edited") {
            for (let x of status) {
                if (x.textContent !== "Edited") {
                    let row = x.closest("tr");
                    if (row) {
                        row.classList.add("hidden");
                    }
                }
            }
        }
    
}
else{
    
    const status =  document.querySelectorAll(".status")
    for (let t of status)
    {  let row = t.closest("tr")
    if (row){
        row.classList.remove("hidden")
    }
}

}}

