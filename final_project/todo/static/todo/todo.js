document.addEventListener('DOMContentLoaded', function () {
    //add click event to create new todo if user is logged in:
    if (document.getElementById('newTodo') !== null) {
        document.getElementById('newTodo').addEventListener('click', createTodo)
    }

    //determine if we are currently in the home page, if we are then load the active list function:
    if (`${window.location.origin}/` == window.location.href) {
        window.setInterval(activeTasks, 1000);
    }
});
//change the format of moment
moment.updateLocale('en', {
    relativeTime : {
        future: "in %s",
        past:   "%s ago",
        s  : '%d seconds',
        ss : '%d seconds',
        m:  "a minute",
        mm: "%d minutes",
        h:  "an hour",
        hh: "%d hours",
        d:  "a day",
        dd: "%d days",
        w:  "a week",
        ww: "%d weeks",
        M:  "a month",
        MM: "%d months",
        y:  "a year",
        yy: "%d years"
    }
});

function createTodo(event) {
    event.preventDefault()
    //console log the date time format for now
    var date_time = $("#time-picker").val();
    //manipulate date_time to use with moment:
    var split_date_time = date_time.split("-", 3);
    var year = parseInt(split_date_time[0]);
    var month = parseInt(split_date_time[1]);
    var date = parseInt(split_date_time[2].split("T", 1));
    var hour = parseInt(date_time.split("T")[1].split(":")[0]);
    var minute = parseInt(date_time.split("T")[1].split(":")[1]);
    //content of todo
    var content = $('#compose-body').val();

    var time_moment = moment()
    var time_set = moment({ year: year, month: month - 1, date: date, hour: hour, minute: minute })
    var time_difference_minute = time_set.diff(time_moment, 'minute')
    var time_difference_seconds = time_set.diff(time_moment, 'seconds')

    //console log debug
    console.log(`content: ${content}; datetime: ${split_date_time}`);
    console.log(`year: ${year}; month: ${month}; date: ${date}; hour: ${hour}, minute: ${minute}`);
    console.log(`time now: ${time_moment}`);
    console.log(`time set: ${time_set}`);
    console.log(`remaining time: ${time_difference_minute} minutes ${time_difference_seconds} seconds`);
    console.log(`add url: ${window.location.href}/add`);


    // send the post request to 'create/add'
    fetch(`${window.location.href}/add`, {
        method: 'POST',
        body: JSON.stringify({
            date_time: time_set,
            content: content,
            year: year,
            month: month,
            date: date,
            hour: hour,
            minute: minute
        })
    })
        .then(response => response.json())
        .then(result => {
            //Print result
            console.log(result);
            $(`#warning-view`).html(`
        <div class="alert alert-success" role="alert">
            Successfully created post
        </div>
        `)
            //if everything is ok then just redirect back to home page.
            //to be implemented when everything is done.
            // window.location.href="/";
        })
}


function activeTasks() {
    //make a get request to /active to get all the active list
    fetch(`${window.location.origin}/active`)
        .then(response => response.json())
        .then(result => {
            // console.log(result)
            //call tasksDisplay function and pass in result
            tasksDisplay(result)
        })
}

function tasksDisplay(result) {
    // console.log(result)
    $(`#tasks-view`).empty()
    //get the current time using moment:
    var time_moment = moment()
    //get the time set from the database:
    for (var i = 0; i < result.length; i++) {
        //set the time 
        var time_set = moment({ year: result[i].year, month: result[i].month - 1, date: result[i].date, hour: result[i].hour, minute: result[i].minute })
        //get time difference in seconds to use to determine color of the card
        var time_difference_seconds = time_set.diff(time_moment, 'seconds')
        //get the time remaining
        var time_remaining = time_set.countdown()
        // console.log(`${result[i].content}; ${time_remaining}`)

        //if the difference in minute is > 0 then it is still active and then print it to front page. Also determine if it is within 10 minutes of dead line
        if (time_difference_seconds > 0 && time_difference_seconds < 600){
            $(`#tasks-view`).append(`
            <div class="card text-white bg-danger">
                <div class="card-body">
                    <h5 class="card-title">${result[i].content}</h5>
                    <p class="card-text">${time_remaining}</p>
                    <button type="button" class="btn btn-primary" onclick="completeTask(${result[i].id})">Complete</button>
                </div>
            </div>
            `)
        }else if (time_difference_seconds > 600 ){
            $(`#tasks-view`).append(`
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5 class="card-title">${result[i].content}</h5>
                    <p class="card-text">${time_remaining}</p>
                    <button type="button" class="btn btn-primary" onclick="completeTask(${result[i].id})">Complete</button>
                </div>
            </div>
            `)
        }
    }
}

function completeTask(id){
    fetch(`${window.location.origin}/complete/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          completed: true
        })
    })
    .then(response => response.text())
    .then(result => console.log('updated'))
}


