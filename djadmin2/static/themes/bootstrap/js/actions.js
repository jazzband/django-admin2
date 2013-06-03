$(function() {
	var element = $("#model-list");
	var selectAllCheckbox = element.find('.model-select-all');
	var selectCheckboxen = element.find('.model-select');
	var selectedCount = element.find('#selected-count');

	var updateSelectedCount = function() {
		var count = 0;
		for (var ix = 0; ix < selectCheckboxen.length; ix++) {
			if ($(selectCheckboxen[ix]).prop('checked')) {
				count++;
			}
		}
		selectAllCheckbox.prop('checked', count == selectCheckboxen.length);
		selectedCount.text(count);
	};

	selectAllCheckbox.click(function(e) {
		selectCheckboxen.prop('checked', this.checked);
		updateSelectedCount();
	});

	selectCheckboxen.click(function(e) {
		updateSelectedCount();
	});

    
    var actionDropdownLink = element.find('.dropdown-menu a');
    actionDropdownLink.click(function (e) {
        e.preventDefault();
        var form = $(this).closest('form');
        form.find('input[name="' + $(this).data('name') + '"]').val(
            $(this).data('value'));
        form.submit();
    });

});
