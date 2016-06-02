$(document).ready(function() {
    /**
     * Dynamicaly adds button to each input element
     * Required by filter section to allow form to be submitted
     */
    $("#filter_form").find('input').each(function(){
        var input_field = $(this);

        var btn = input_field.after('<button class="btn">Go</button>');
    });

});
