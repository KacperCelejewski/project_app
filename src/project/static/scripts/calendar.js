let Events = [[]];
fetch("/sendEvent") //catch data from event table1
  .then((res) => res.json())
  .then((eventInfos) => {
    Events = eventInfos;
    CreateArrayOfEventProprties(eventInfos);
  })
  .catch((error) => {
    console.error("Error:", error);
  });

const EventStartDateArray = [];
const EventEndDateArray = [];
const EventNameArray = [];

function CreateArrayOfEventProprties(eventInfos) {
  for (let eventInfo of eventInfos) {
    EventStartDateArray.push(eventInfo.startDate);

    EventEndDateArray.push(eventInfo.endDate);

    EventNameArray.push(eventInfo.name);
  }
}

function ChangeCurrentDate() {
  document.addEventListener("DOMContentLoaded", function () {
    const CurrentDate = document.getElementById("date-display");
    let options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    const today = new Date();
    const todayInRightFormat = new Intl.DateTimeFormat("en-EN", options).format(
      today
    );
    CurrentDate.textContent = todayInRightFormat;
  });
}
function displayNextThreeDays(startDate) {
  const daysOfWeek = [0, 1, 2, 3, 4, 5, 6];

  const calendarDays = document.getElementsByClassName("col-data"); // Zakładając, że elementy kalendarza mają klasę 'day'

  const startDayIndex = daysOfWeek.indexOf(startDate);

  if (startDayIndex !== -1) {
    for (let i = 0; i < calendarDays.length; i++) {
      const dayIndex = (startDayIndex + i) % 7; // Ustalamy indeks dla każdego dnia, biorąc pod uwagę cykl 7 dni

      // Ustawiamy odpowiednią nazwę dnia tygodnia w elemencie kalendarza
      calendarDays[i].textContent = daysOfWeek[dayIndex];
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {});

ChangeCurrentDate();
let filteredArray = [];
//dayModifier === 1 ||-1
function nextDay(dayModifier) {
  const cell = document.querySelectorAll(".cell");
  cell.forEach((cell) => {
    cell.remove();
  });
  const dateDisplay = document.getElementById("date-display");

  const currentDateText = dateDisplay.textContent;

  const currentDate = new Date(currentDateText);

  currentDate.setDate(currentDate.getDate() + dayModifier);
  let options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  renderer(currentDate)
  const nextDate = new Intl.DateTimeFormat("en-EN", options).format(
    currentDate
  );

  
  dateDisplay.textContent = nextDate;
  
  displayNextThreeDays(5);
}
function renderer (currentDate){
  if (!(currentDate instanceof Date)) {
    console.error("Błąd: 'currentDate' nie jest obiektem typu Date.");
    return;
  }

  const filteredArray = Events.filter((Event) => {
    const eventStartDate = new Date(Event.startDate); 
    return eventStartDate.toDateString() === currentDate.toDateString();
  });

  filteredArray.forEach((Event) => {
    const calendar = document.querySelector(".calendar");
    const EventDiv = document.createElement("div");
   
    EventDiv.textContent = Event.name;
    EventDiv.className = "cell";
    let eventStartDate = new Date(Event.startDate);
    const startHour = eventStartDate.getHours();

    const gridRow = startHour ; // Time Zone Diffrenece (+3)


    EventDiv.classList.add(`row-${gridRow}`);
    const rowr = document.querySelectorAll(`.row-${gridRow}`)
    const len = rowr.length+1
    
    EventDiv.style.gridColumn = `${len}`;

    EventDiv.style.gridRow = `${gridRow}`;
    EventDiv.style.border = "2px solid white";
    EventDiv.style.width = "95%";
    EventDiv.style.color = "black";
    EventDiv.style.backgroundColor = "#ff84e885";
    EventDiv.style.margin = "5px 0px";
   
    calendar.appendChild(EventDiv);
  });
  }
// function filterToChoosenDate(){
// const filteredArray = Events.filter((Event) => {
//   let eventStartDate = new Date(Event.startDate); // Konwertujemy startDate wydarzenia na obiekt typu Date
//   eventStartDate = eventStartDate.setDate(eventStartDate.getDate+1)
//   return eventStartDate.toDateString() === currentDate.toDateString();
// });

//   filteredArray.forEach((Event) => {
//   const calendar = document.querySelector(".calendar");
//   const EventDiv = document.createElement("div");
//   EventDiv.textContent = Event.name;

//   let eventStartDate = new Date(Event.startDate);
//   const startHour = eventStartDate.getHours();
//   console.log(eventStartDate);
//   const gridRow = startHour - 1; // +2, aby uwzględnić nagłówki

//   EventDiv.classList.add(`row-${gridRow}`);
//   EventDiv.style.gridColumn = "2";
//   EventDiv.style.gridRow = `${gridRow}`;
//   calendar.appendChild(EventDiv);
// });

// dateDisplay.textContent = nextDate;
// displayNextThreeDays(5);
// }(

document.addEventListener('DOMContentLoaded', function() {
const today = new Date()
renderer(today)})



function hideEventForm(){
  const form = document.querySelector("form");
  form.style.display="block";
  
}
function closeForms() {
 
  const form = document.querySelector("form");
  form.style.display = "none";
}
// const button = document.getElementById("closeBtn");
// button.addEventListener("click", function(event) {
//   event.preventDefault();
//   const form = document.querySelector("form");
//   form.style.display="none";
// });