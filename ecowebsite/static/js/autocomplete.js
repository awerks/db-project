$(function () {
    console.log("Autocomplete script loaded");
    $("input").on("focus", function () {
        const table = $(this).closest("fieldset").attr("id");
        const field = $(this).attr("id");

        const formData = {
            table: table,
            field: field
        };

        $.ajax({
            url: "/autocomplete",
            type: "GET",
            data: formData,
            dataType: "json",
            success: function (data) {
                $("#" + field).autocomplete({
                    source: function (request, response) {
                        var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
                        response($.grep(data, function (item) {
                            return matcher.test(item);
                        }));    
                    },
                    minLength: 1
                });
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Failed to load autocomplete data: ", textStatus, errorThrown);
                console.error("Response details: ", jqXHR.responseText);
            }
        });
    });
});