$(function() {
	var element = $("#model-list");
	var selectAllCheckbox = element.find('.model-select-all');
	var selectCheckbox = element.find('.model-select');
	var selectedCount = element.find('.selected-count');

	var updateSelectedCount = function() {
		if (selectedCount.length) {
		    var count = 0;
		    for (var ix = 0; ix < selectCheckbox.length; ix++) {
			    if ($(selectCheckbox[ix]).prop('checked')) {
				    count++;
			    }
		    }
		    selectAllCheckbox.prop('checked', count == selectCheckbox.length);
		    selectedCount.text(count);
		}
	};

	selectAllCheckbox.click(function(e) {
		selectCheckbox.prop('checked', this.checked);
		updateSelectedCount();
	});

	selectCheckbox.click(function(e) {
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
