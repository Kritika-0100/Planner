$(document).ready(function () {
    // Add task
    $('#add-task').click(function () {
        var taskText = $('#new-task').val();
        if (taskText) {
            var newTask = $('<li>').addClass('list-group-item').text(taskText);
            newTask.append($('<button>').addClass('btn btn-danger btn-sm float-right delete-task').text('Delete'));
            $('#task-list').append(newTask);
            $('#new-task').val('');
        }
    });

    // Delete task
    $(document).on('click', '.delete-task', function () {
        $(this).closest('li').remove();
    });

    // Make the list sortable
    $('#task-list').sortable();
});
