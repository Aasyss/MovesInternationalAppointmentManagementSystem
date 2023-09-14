$(function() {
    // Create sliders for each day of the week
    $('.availability-slider').slider({
        range: true,
        min: 0,
        max: 24, // 24 hours in a day
        values: [9, 17], // Initial values (9 am to 5 pm)
        slide: function(event, ui) {
            // Update hidden input fields or other form fields with start and end times
            // ...
        }
    });
});
