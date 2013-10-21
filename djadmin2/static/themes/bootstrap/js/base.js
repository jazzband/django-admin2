$(document).ready(function() {

    /**
     * Dynamically adds button to each input element
     * Required by filter section to allow form to be submitted
     */
    $("#filter_form").find('input').each(function(){
        var input_field = $(this);

        var btn = input_field.after('<button class="btn">Go</button>');
    });
    /**
     * If the there's a select in the filters; filter when it's changed
     */
    $('#filter_form select').on('change', function(e){
        $(this).closest('form').submit();
    });

});
