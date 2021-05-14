var form = $('#myForm'),
    checkbox = $('#saveticket'),
    ticketblock = $('#saveticketinputs');

ticketblock.hide();

checkbox.on('click', function() {
    if($(this).is(':checked')) {
      ticketblock.show();
      ticketblock.find('input').attr('required', true);
    } else {
      ticketblock.hide();
      ticketblock.find('input').attr('required', false);
    }
})
