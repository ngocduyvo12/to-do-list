document.addEventListener('DOMContentLoaded', function () {
    //add click event to create new todo if user is logged in:
    if (document.getElementById('newTodo') !== null) {
        document.getElementById('newTodo').addEventListener('click', createTodo)
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

    //this can be used to determine if currently in homepage
    var random = true;
    if (window.location.origin = window.location.href){
        random = false
    }
    console.log(random)

    // send the post request to 'create/add'
    // fetch(`${window.location.href}/add`, {
    //     method: 'POST',
    //     body: JSON.stringify({
    //         content: content,
    //         year: year,
    //         month: month,
    //         date: date,
    //         hour: hour,
    //         minute: minute
    //     })
    // })
    // .then(response => response.json())
    // .then(result => {
    //     //Print result
    //     console.log(result);
    //     $(`#warning-view`).html(`
    //     <div class="alert alert-success" role="alert">
    //         Successfully created post
    //     </div>
    //     `)
    //     //if everything is ok then just redirect back to home page.
    //     // window.location.href="/";
    // })
}